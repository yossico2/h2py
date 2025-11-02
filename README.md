# h2py

A tool to convert C header files to Python using clang2py.

## Installation

### Quick Installation (Recommended)

Run the automated installation script:
```bash
./install.sh
```

This script will automatically:
- Install all required system dependencies (libclang-dev, libclang1, clang, llvm-dev)
- Create the necessary symbolic links
- Set up a Python virtual environment
- Install ctypeslib2 (which contains clang2py)
- Test the installation

### Manual Installation

#### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)
- libclang development libraries

#### Setup Instructions

#### Setup Instructions

1. **Install system dependencies**:
   ```bash
   sudo apt update && sudo apt install libclang-dev libclang1 clang llvm-dev
   
   # Create symbolic link for libclang
   sudo ln -sf /usr/lib/x86_64-linux-gnu/libclang-18.so /usr/lib/x86_64-linux-gnu/libclang.so
   ```

2. **Create and activate a virtual environment** (if not already done):
   ```bash
   python -m venv py312
   source py312/bin/activate  # On Linux/Mac
   # or
   py312\Scripts\activate     # On Windows
   ```

3. **Install ctypeslib2** (which contains clang2py):
   ```bash
   pip install ctypeslib2
   ```

### Usage

This project converts C header files from the `hfiles/` directory to Python files in the `pyfiles/` directory using clang2py.

**Directory Structure:**
```
h2py/
├── hfiles/          # C header files (.h)
├── pyfiles/         # Generated Python files
├── h2py.py          # Main conversion script
└── README.md
```

**Convert header files to Python:**
```bash
# Convert a single header file
clang2py hfiles/types.h -o pyfiles/types.py

# Convert all header files
for file in hfiles/*.h; do
    basename=$(basename "$file" .h)
    clang2py "$file" -o "pyfiles/${basename}.py"
done
```
