import os
import ast

# Example usage:
# remove_helper_classes_from_files('/home/yossico/dev/h2py/pyfiles')


def remove_clang2py_helper_classes_from_files(directory):
    class IfRemover(ast.NodeTransformer):
        def visit_If(self, node):
            # Remove if/else blocks that only define c_long_double_t
            assigns = [
                n
                for n in node.body + getattr(node, "orelse", [])
                if isinstance(n, ast.Assign)
            ]
            all_targets = [
                t.id for a in assigns for t in a.targets if isinstance(t, ast.Name)
            ]
            if all_targets and set(all_targets) == {"c_long_double_t"}:
                return None
            return node

    class TryRemover(ast.NodeTransformer):
        def visit_Try(self, node):
            # Remove try/except blocks that assign from _libraries[...] (any usage)
            assigns = [n for n in node.body if isinstance(n, ast.Assign)]
            for assign in assigns:
                if isinstance(assign.value, ast.Attribute) and isinstance(
                    assign.value.value, ast.Subscript
                ):
                    sub = assign.value.value
                    if isinstance(sub.value, ast.Name) and sub.value.id == "_libraries":
                        return None
                # Also handle direct assignment from _libraries[...] (e.g. config_load = _libraries[...].config_load)
                if (
                    isinstance(assign.value, ast.Subscript)
                    and isinstance(assign.value.value, ast.Name)
                    and assign.value.value.id == "_libraries"
                ):
                    return None
            return node

    classes_to_remove = {"AsDictMixin", "Structure", "Union", "FunctionFactoryStub"}
    functions_to_remove = {"string_cast", "char_pointer_cast"}
    assignments_to_remove = {"_libraries", "c_int128", "c_uint128", "void"}

    def is_targeted_assign(node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                # Remove _libraries = ...
                if isinstance(target, ast.Name) and target.id in assignments_to_remove:
                    return True
                # Remove _libraries[...] = ...
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "_libraries"
                ):
                    return True
        return False

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()

            try:
                tree = ast.parse(source)
            except SyntaxError:
                print(f"✗ Syntax error in {filename}, skipping.")
                continue

            new_body = []
            removed = False
            for node in tree.body:
                # Remove specified classes
                if isinstance(node, ast.ClassDef) and node.name in classes_to_remove:
                    removed = True
                    continue
                # Remove specified functions
                if (
                    isinstance(node, ast.FunctionDef)
                    and node.name in functions_to_remove
                ):
                    removed = True
                    continue
                # Remove specified assignments and _libraries[...] subscripts
                if is_targeted_assign(node):
                    removed = True
                    continue
                new_body.append(node)

            tree.body = new_body
            # Remove try/except blocks for buffer_create, buffer_destroy, buffer_append
            tree = TryRemover().visit(tree)
            # Remove if/else blocks that only define c_long_double_t
            tree = IfRemover().visit(tree)
            ast.fix_missing_locations(tree)
            # Always rewrite class base names: Structure -> ctypes.Structure, Union -> ctypes.Union
            updated_bases = False
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for i, base in enumerate(node.bases):
                        if isinstance(base, ast.Name) and base.id == "Structure":
                            node.bases[i] = ast.Attribute(
                                value=ast.Name(id="ctypes", ctx=ast.Load()),
                                attr="Structure",
                                ctx=ast.Load(),
                            )
                            updated_bases = True
                        elif isinstance(base, ast.Name) and base.id == "Union":
                            node.bases[i] = ast.Attribute(
                                value=ast.Name(id="ctypes", ctx=ast.Load()),
                                attr="Union",
                                ctx=ast.Load(),
                            )
                            updated_bases = True
            if removed or updated_bases:
                new_source = ast.unparse(tree)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_source)
                print(f"✓ Cleaned {filename}.")
