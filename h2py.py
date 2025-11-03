#!/usr/bin/env python3
"""
H2PY - C Header to Python Converter
Converts C header files to Python using clang2py
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from clang2py_cleanup import remove_clang2py_helper_classes_from_files


def convert_header_to_python(header_path, output_path):
    """
    Convert a single C header file to Python using clang2py

    Args:
        header_path (str): Path to the C header file
        output_path (str): Path for the output Python file

    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        cmd = ["clang2py", header_path, "-o", output_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Converted {header_path} -> {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to convert {header_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ clang2py not found. Please install it with: pip install ctypeslib2")
        return False


def convert_all_headers(input_dir, output_dir):
    """
    Convert all .h files in input directory to Python files in output directory

    Args:
        input_dir (str): Directory containing C header files
        output_dir (str): Directory for output Python files

    Returns:
        tuple: (successful_conversions, failed_conversions)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)

    # Find all .h files
    header_files = list(input_path.glob("*.h"))

    if not header_files:
        print(f"No .h files found in {input_dir}")
        return 0, 0

    successful = 0
    failed = 0

    print(f"Found {len(header_files)} header files to convert...")
    print("-" * 50)

    for header_file in header_files:
        # Generate output filename
        python_filename = header_file.stem + ".py"
        python_file = output_path / python_filename

        if convert_header_to_python(str(header_file), str(python_file)):
            successful += 1
        else:
            failed += 1

    print("-" * 50)
    print(f"Conversion complete: {successful} successful, {failed} failed")

    return successful, failed


def main():
    parser = argparse.ArgumentParser(
        description="Convert C header files to Python using clang2py"
    )
    parser.add_argument(
        "-i",
        "--input",
        default="hfiles",
        help="Input directory containing .h files (default: hfiles)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="pyfiles",
        help="Output directory for .py files (default: pyfiles)",
    )
    parser.add_argument(
        "-f", "--file", help="Convert a single file (provide full path)"
    )
    parser.add_argument("--output-file", help="Output file path when using -f option")

    args = parser.parse_args()

    # Single file conversion
    if args.file:
        if not args.output_file:
            # Generate output filename
            input_path = Path(args.file)
            output_file = Path(args.output) / (input_path.stem + ".py")
        else:
            output_file = Path(args.output_file)

        if convert_header_to_python(args.file, str(output_file)):
            print("Single file conversion completed successfully")
            return 0
        else:
            print("Single file conversion failed")
            return 1

    # Batch conversion
    else:
        if not os.path.exists(args.input):
            print(f"Error: Input directory '{args.input}' does not exist")
            return 1

        successful, failed = convert_all_headers(args.input, args.output)

        print()
        print(f"Removing clang2py helper classes from generated python files...")
        print("-" * 50)
        remove_clang2py_helper_classes_from_files(args.output)

        if failed > 0:
            return 1

        return 0


if __name__ == "__main__":
    sys.exit(main())
