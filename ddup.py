#!/usr/bin/env python3
# Deduplicate structure definitions in generated Python files (pyfiles/), processing in dependency order.
import os
import re
from dep_tree import build_dependency_tree, topological_sort

PYFILES_DIR = "pyfiles"


def get_pyfile_for_header(header):
    """Map a header filename to its corresponding Python file name."""
    base = os.path.splitext(header)[0]
    return f"{base}.py"


def find_struct_class_defs(pyfile_path):
    """Find struct/class definitions in a Python file. Returns dict: name -> (start, end) line numbers."""
    struct_defs = {}
    with open(pyfile_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    pattern = re.compile(r"^class (struct_[A-Za-z0-9_]+)\(ctypes.Structure\):")
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            name = m.group(1)
            # Find end of class (next class or EOF)
            start = i
            end = start + 1
            while end < len(lines) and not lines[end].startswith("class "):
                end += 1
            struct_defs[name] = (start, end)
    return struct_defs


def deduplicate_structs():
    # Build dependency tree and get topological order for headers
    dep_tree = build_dependency_tree("hfiles")
    ordered_headers = topological_sort(dep_tree)
    seen_structs = {}  # struct_name -> (pyfile, header)
    removed_structs = {}  # pyfile -> list of (struct_name, defining_pyfile)
    modified_files = set()
    for header in ordered_headers:
        pyfile = get_pyfile_for_header(header)
        pyfile_path = os.path.join(PYFILES_DIR, pyfile)
        if not os.path.exists(pyfile_path):
            continue
        with open(pyfile_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        struct_defs = find_struct_class_defs(pyfile_path)
        to_remove = []
        for struct_name, (start, end) in struct_defs.items():
            if struct_name in seen_structs:
                to_remove.append((start, end))
                # Track where to import from
                defining_pyfile, _ = seen_structs[struct_name]
                removed_structs.setdefault(pyfile, []).append(
                    (struct_name, defining_pyfile)
                )
            else:
                seen_structs[struct_name] = (pyfile, header)
        # Remove duplicates (from bottom up to not mess up indices)
        if to_remove:
            for start, end in sorted(to_remove, reverse=True):
                del lines[start:end]
            with open(pyfile_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"✓ Deduplication fixed in {pyfile_path}.")
            modified_files.add(pyfile_path)

    # Add imports for removed structs
    for pyfile, structs in removed_structs.items():
        pyfile_path = os.path.join(PYFILES_DIR, pyfile)
        if not os.path.exists(pyfile_path):
            continue
        with open(pyfile_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find first non-comment, non-empty, non-import line
        insert_at = 0
        for i, line in enumerate(lines):
            if not (
                line.strip().startswith("import")
                or line.strip().startswith("#")
                or not line.strip()
            ):
                insert_at = i
                break
        import_lines = []
        for struct_name, defining_pyfile in structs:
            module = os.path.splitext(defining_pyfile)[0]
            if module == os.path.splitext(pyfile)[0]:
                continue  # Don't import from self
            import_lines.append(f"from .{module} import {struct_name}\n")
        # Only add imports that aren't already present
        added = False
        for import_line in import_lines:
            if import_line not in lines:
                lines.insert(insert_at, import_line)
                insert_at += 1
                added = True
        if added:
            with open(pyfile_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"✓ Deduplication fixed in {pyfile_path}.")
            modified_files.add(pyfile_path)
    if not modified_files:
        print("No files were modified.")


if __name__ == "__main__":
    deduplicate_structs()
