import os
import re

# Example usage:
# remove_helper_classes_from_files('/home/yossico/dev/h2py/pyfiles')


def remove_clang2py_helper_classes_from_files(directory):
    """
    Removes AsDictMixin, Structure, Union, and FunctionFactoryStub class definitions
    (with their bodies) from all .py files in the specified directory.
    """
    # Classes to remove (add more if needed)
    classes = ["AsDictMixin", "Structure", "Union", "FunctionFactoryStub"]
    # Regex to match class definitions and their bodies (handles indentation)
    class_regex = re.compile(
        r"(?ms)^class\s+({})(\(.*?\))?:\n(?:^[ \t]+.*\n?)*".format("|".join(classes))
    )

    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            new_content = class_regex.sub("", content)
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"✓ Removed helper classes from {filename}")
