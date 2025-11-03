import os
import re
from pathlib import Path
from typing import Dict, Set, List


def parse_includes(filepath: str) -> Set[str]:
    """
    Parse a header file and extract all #include directives.

    Args:
        filepath: Path to the header file

    Returns:
        Set of included header filenames
    """
    includes = set()
    include_pattern = re.compile(r'#include\s*[<"]([^>"]+)[>"]')

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = include_pattern.search(line)
                if match:
                    included_file = match.group(1)
                    # Extract just the filename if it's a path
                    includes.add(os.path.basename(included_file))
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")

    return includes


def build_dependency_tree(hfiles_dir: str = "hfiles") -> Dict[str, Set[str]]:
    """
    Build a dependency tree for all .h files in the specified directory.

    Args:
        hfiles_dir: Directory containing header files (default: "hfiles")

    Returns:
        Dictionary mapping each header file to the set of headers it includes
    """
    hfiles_path = Path(hfiles_dir)

    if not hfiles_path.exists():
        raise FileNotFoundError(f"Directory '{hfiles_dir}' not found")

    # Find all .h files
    h_files = list(hfiles_path.glob("*.h"))

    if not h_files:
        print(f"Warning: No .h files found in '{hfiles_dir}'")
        return {}

    # Build a set of available header filenames for filtering
    available_headers = {f.name for f in h_files}

    # Build dependency tree
    dependency_tree = {}

    for h_file in h_files:
        includes = parse_includes(str(h_file))
        # Filter to only include headers that exist in our directory
        local_includes = includes & available_headers
        dependency_tree[h_file.name] = local_includes

    return dependency_tree


def print_dependency_tree(dependency_tree: Dict[str, Set[str]], indent: int = 0):
    """
    Print the dependency tree in a human-readable format.

    Args:
        dependency_tree: Dictionary mapping files to their dependencies
        indent: Current indentation level (for recursive calls)
    """
    for filename, dependencies in sorted(dependency_tree.items()):
        print("  " * indent + f"📄 {filename}")
        if dependencies:
            for dep in sorted(dependencies):
                print("  " * (indent + 1) + f"└─ includes: {dep}")
        else:
            print("  " * (indent + 1) + "(no local dependencies)")


def get_all_dependencies(
    filename: str, dependency_tree: Dict[str, Set[str]], visited: Set[str] = None
) -> Set[str]:
    """
    Recursively get all dependencies for a given file (transitive closure).

    Args:
        filename: The header file to analyze
        dependency_tree: The complete dependency tree
        visited: Set of already visited files (to avoid cycles)

    Returns:
        Set of all files that this file depends on (directly or indirectly)
    """
    if visited is None:
        visited = set()

    if filename in visited or filename not in dependency_tree:
        return set()

    visited.add(filename)
    all_deps = set(dependency_tree[filename])

    for dep in dependency_tree[filename]:
        all_deps.update(get_all_dependencies(dep, dependency_tree, visited.copy()))

    return all_deps


def detect_circular_dependencies(
    dependency_tree: Dict[str, Set[str]],
) -> List[List[str]]:
    """
    Detect circular dependencies in the dependency tree.

    Args:
        dependency_tree: Dictionary mapping files to their dependencies

    Returns:
        List of cycles found (each cycle is a list of filenames)
    """

    def find_cycle(node: str, path: List[str], visited: Set[str]) -> List[str]:
        if node in path:
            # Found a cycle
            cycle_start = path.index(node)
            return path[cycle_start:] + [node]

        if node in visited:
            return []

        visited.add(node)
        path.append(node)

        for dep in dependency_tree.get(node, set()):
            cycle = find_cycle(dep, path[:], visited)
            if cycle:
                return cycle

        return []

    cycles = []
    visited = set()

    for filename in dependency_tree:
        if filename not in visited:
            cycle = find_cycle(filename, [], visited)
            if cycle and cycle not in cycles:
                cycles.append(cycle)

    return cycles


def topological_sort(dependency_tree: Dict[str, Set[str]]) -> List[str]:
    """
    Sort files in dependency order using topological sort (Kahn's algorithm).
    Files with no dependencies come first, then files that depend on them, etc.

    Args:
        dependency_tree: Dictionary mapping files to their dependencies

    Returns:
        List of filenames in topological order

    Note:
        If circular dependencies exist, they will be placed at the end
    """
    # Create a copy of the dependency tree to work with
    deps = {k: set(v) for k, v in dependency_tree.items()}

    # Track in-degree (number of dependencies) for each file
    in_degree = {filename: len(dependencies) for filename, dependencies in deps.items()}

    # Start with files that have no dependencies
    queue = [filename for filename, degree in in_degree.items() if degree == 0]
    result = []

    while queue:
        # Sort to ensure consistent ordering
        queue.sort()
        current = queue.pop(0)
        result.append(current)

        # Find all files that depend on the current file
        for filename, dependencies in deps.items():
            if current in dependencies:
                dependencies.remove(current)
                in_degree[filename] -= 1

                # If all dependencies are satisfied, add to queue
                if in_degree[filename] == 0:
                    queue.append(filename)

    # If there are files with circular dependencies, add them at the end
    remaining = set(dependency_tree.keys()) - set(result)
    if remaining:
        result.extend(sorted(remaining))

    return result


def print_topologically_sorted(dependency_tree: Dict[str, Set[str]]):
    """
    Print files in topological order (dependency order).

    Args:
        dependency_tree: Dictionary mapping files to their dependencies
    """
    sorted_files = topological_sort(dependency_tree)

    print("Files in dependency order (process in this order):")
    print("=" * 60)

    for i, filename in enumerate(sorted_files, 1):
        dependencies = dependency_tree[filename]
        print(f"\n{i}. 📄 {filename}")

        if dependencies:
            print("   Dependencies:")
            for dep in sorted(dependencies):
                print(f"      └─ {dep}")
        else:
            print("   (no local dependencies)")

    return sorted_files


if __name__ == "__main__":
    # Example usage
    print("Building dependency tree for header files...")
    print("=" * 60)

    try:
        dep_tree = build_dependency_tree("hfiles")

        print(f"\nFound {len(dep_tree)} header files\n")

        # Print files in dependency order
        print("\n" + "=" * 60)
        print_topologically_sorted(dep_tree)

        # Print full dependency tree
        print("\n" + "=" * 60)
        print("Full dependency tree:\n")
        print_dependency_tree(dep_tree)

        # Check for circular dependencies
        print("\n" + "=" * 60)
        print("Checking for circular dependencies...")
        cycles = detect_circular_dependencies(dep_tree)

        if cycles:
            print(f"\n⚠️  Found {len(cycles)} circular dependency cycle(s):")
            for i, cycle in enumerate(cycles, 1):
                print(f"\n  Cycle {i}: {' → '.join(cycle)}")
        else:
            print("\n✓ No circular dependencies detected")

        # Show transitive dependencies for each file
        print("\n" + "=" * 60)
        print("Transitive dependencies (all dependencies):\n")
        for filename in sorted(dep_tree.keys()):
            all_deps = get_all_dependencies(filename, dep_tree)
            print(f"📄 {filename}")
            if all_deps:
                for dep in sorted(all_deps):
                    print(f"    └─ {dep}")
            else:
                print(f"    (no dependencies)")
            print()

    except FileNotFoundError as e:
        print(f"Error: {e}")
