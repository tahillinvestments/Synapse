"""
AST-based Zero-LLM Programmatic Code Parser.
Extracts functions, classes, calls, imports, routes, and builds lightweight surrogate signatures.
"""

import ast
from typing import List, Tuple, Dict, Any, Optional
from synapse_graph.models import SymbolNode, MemoryEdge, LobeType, EdgeType


class CodebaseParser:
    """Parses code files into structured SymbolNodes and MemoryEdges without LLM calls."""

    def __init__(self):
        self.nodes: Dict[str, SymbolNode] = {}
        self.edges: List[MemoryEdge] = []

    def parse_python_source(self, file_path: str, source_code: str, commit_sha: str = "HEAD") -> Tuple[List[SymbolNode], List[MemoryEdge]]:
        """Parses a Python file and returns discovered nodes and edges."""
        file_nodes: List[SymbolNode] = []
        file_edges: List[MemoryEdge] = []

        try:
            tree = ast.parse(source_code, filename=file_path)
        except SyntaxError:
            # Fallback or skip if invalid syntax
            return file_nodes, file_edges

        module_name = file_path.replace("/", ".").replace(".py", "").strip(".")
        module_id = f"mod:{module_name}"

        # Estimate full tokens (~4 chars per token)
        full_file_tokens = max(1, len(source_code) // 4)

        # Module node
        mod_node = SymbolNode(
            id=module_id,
            name=module_name.split(".")[-1],
            symbol_type="module",
            file_path=file_path,
            lobe=LobeType.PARIETAL if "schema" in file_path or "model" in file_path or "type" in file_path else LobeType.FRONTAL,
            line_start=1,
            line_end=len(source_code.splitlines()) or 1,
            signature=f"module {module_name}",
            docstring=ast.get_docstring(tree),
            surrogate=f"module {module_name} ({len(source_code.splitlines())} lines)",
            full_tokens=full_file_tokens,
            surrogate_tokens=10,
            commit_sha=commit_sha,
            tags=["module", module_name.split(".")[-1]]
        )
        file_nodes.append(mod_node)

        # Visitor to collect symbols and calls
        class Visitor(ast.NodeVisitor):
            def __init__(self, parser_ref):
                self.parser = parser_ref
                self.current_scope = [module_id]
                self.calls_in_scope: Dict[str, List[str]] = {}

            def visit_Import(self, node: ast.Import):
                for alias in node.names:
                    target_id = f"mod:{alias.name}"
                    file_edges.append(MemoryEdge(
                        source_id=module_id,
                        target_id=target_id,
                        edge_type=EdgeType.IMPORTS,
                        commit_sha=commit_sha
                    ))
                self.generic_visit(node)

            def visit_ImportFrom(self, node: ast.ImportFrom):
                if node.module:
                    mod_target = f"mod:{node.module}"
                    file_edges.append(MemoryEdge(
                        source_id=module_id,
                        target_id=mod_target,
                        edge_type=EdgeType.IMPORTS,
                        commit_sha=commit_sha
                    ))
                    for alias in node.names:
                        sym_target = f"{node.module}:{alias.name}"
                        file_edges.append(MemoryEdge(
                            source_id=module_id,
                            target_id=sym_target,
                            edge_type=EdgeType.IMPORTS,
                            commit_sha=commit_sha
                        ))
                self.generic_visit(node)

            def visit_ClassDef(self, node: ast.ClassDef):
                class_id = f"{module_name}:{node.name}"
                is_schema = any(base.id in ["BaseModel", "Schema", "TypedDict", "Dataclass"] 
                                for base in node.bases if isinstance(base, ast.Name)) or "model" in file_path.lower()
                
                lobe = LobeType.PARIETAL if is_schema else LobeType.FRONTAL

                # Build signature
                bases_str = ", ".join(ast.unparse(b) for b in node.bases)
                sig = f"class {node.name}({bases_str}):" if bases_str else f"class {node.name}:"
                doc = ast.get_docstring(node)
                
                # Estimate token size of class body vs surrogate
                class_code = ast.get_source_segment(source_code, node) or sig
                full_tok = max(1, len(class_code) // 4)
                surr = f"{sig}\n    \"\"\"{doc[:80] + '...' if doc and len(doc) > 80 else (doc or '')}\"\"\""
                surr_tok = max(1, len(surr) // 4)

                c_node = SymbolNode(
                    id=class_id,
                    name=node.name,
                    symbol_type="class",
                    file_path=file_path,
                    lobe=lobe,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    signature=sig,
                    docstring=doc,
                    surrogate=surr,
                    full_tokens=full_tok,
                    surrogate_tokens=surr_tok,
                    commit_sha=commit_sha,
                    tags=["class", "schema" if is_schema else "logic"]
                )
                file_nodes.append(c_node)
                file_edges.append(MemoryEdge(source_id=module_id, target_id=class_id, edge_type=EdgeType.EXPOSES, commit_sha=commit_sha))

                # Inheritance edges
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        file_edges.append(MemoryEdge(
                            source_id=class_id,
                            target_id=f"{module_name}:{base.id}",
                            edge_type=EdgeType.INHERITS,
                            commit_sha=commit_sha
                        ))

                self.current_scope.append(class_id)
                self.generic_visit(node)
                self.current_scope.pop()

            def visit_FunctionDef(self, node: ast.FunctionDef):
                self._handle_func(node, is_async=False)

            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
                self._handle_func(node, is_async=True)

            def _handle_func(self, node, is_async: bool):
                parent_scope = self.current_scope[-1]
                func_id = f"{parent_scope}.{node.name}" if parent_scope != module_id else f"{module_name}:{node.name}"
                is_method = parent_scope != module_id

                # Check if route decorator or API endpoint
                is_route = False
                for dec in node.decorator_list:
                    dec_str = ast.unparse(dec)
                    if any(kw in dec_str.lower() for kw in ["route", "get", "post", "put", "delete", "endpoint", "api"]):
                        is_route = True

                # Lobe classification
                if is_route:
                    lobe = LobeType.OCCIPITAL  # External / API sensory boundary
                elif "cache" in node.name.lower() or "bridge" in node.name.lower() or "connector" in node.name.lower() or "index" in node.name.lower():
                    lobe = LobeType.HIPPOCAMPUS # Associative connector
                else:
                    lobe = LobeType.FRONTAL     # Core computation / logic

                # Build signature
                args_str = ast.unparse(node.args)
                prefix = "async def " if is_async else "def "
                ret_str = f" -> {ast.unparse(node.returns)}" if node.returns else ""
                sig = f"{prefix}{node.name}({args_str}){ret_str}:"
                doc = ast.get_docstring(node)

                func_code = ast.get_source_segment(source_code, node) or sig
                full_tok = max(1, len(func_code) // 4)
                surr = f"{sig}\n    \"\"\"{doc[:80] + '...' if doc and len(doc) > 80 else (doc or '')}\"\"\""
                surr_tok = max(1, len(surr) // 4)

                f_node = SymbolNode(
                    id=func_id,
                    name=node.name,
                    symbol_type="method" if is_method else ("route" if is_route else "function"),
                    file_path=file_path,
                    lobe=lobe,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    signature=sig,
                    docstring=doc,
                    surrogate=surr,
                    full_tokens=full_tok,
                    surrogate_tokens=surr_tok,
                    commit_sha=commit_sha,
                    tags=["async" if is_async else "sync", "route" if is_route else "internal"]
                )
                file_nodes.append(f_node)
                file_edges.append(MemoryEdge(
                    source_id=parent_scope,
                    target_id=func_id,
                    edge_type=EdgeType.EXPOSES,
                    commit_sha=commit_sha
                ))

                self.current_scope.append(func_id)
                self.calls_in_scope[func_id] = []
                self.generic_visit(node)
                self.current_scope.pop()

            def visit_Call(self, node: ast.Call):
                current_caller = self.current_scope[-1]
                callee_name = None
                if isinstance(node.func, ast.Name):
                    callee_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee_name = node.func.attr

                if callee_name and current_caller != module_id:
                    # Potential call edge
                    file_edges.append(MemoryEdge(
                        source_id=current_caller,
                        target_id=f"{module_name}:{callee_name}", # Resolved later in engine
                        edge_type=EdgeType.CALLS,
                        commit_sha=commit_sha
                    ))
                self.generic_visit(node)

        visitor = Visitor(self)
        visitor.visit(tree)
        return file_nodes, file_edges
