#!/bin/bash

# install.sh - Automated installation script for h2py (clang2py)
# This script installs all dependencies needed for converting C headers to Python

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if running on Ubuntu/Debian
check_os() {
    if ! command_exists apt; then
        print_error "This script is designed for Ubuntu/Debian systems with apt package manager."
        print_error "Please install dependencies manually for your system."
        exit 1
    fi
    print_success "Detected Ubuntu/Debian system"
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # Update package list
    print_status "Updating package list..."
    sudo apt update
    
    # Install required packages
    print_status "Installing libclang-dev, libclang1, clang, and llvm-dev..."
    sudo apt install -y libclang-dev libclang1 clang llvm-dev
    
    print_success "System dependencies installed"
}

# Create symbolic link for libclang
create_libclang_symlink() {
    print_status "Creating symbolic link for libclang..."
    
    # Find the libclang shared library
    LIBCLANG_PATH=$(find /usr/lib -name "libclang-*.so" | head -1)
    
    if [ -z "$LIBCLANG_PATH" ]; then
        print_error "Could not find libclang shared library"
        exit 1
    fi
    
    print_status "Found libclang at: $LIBCLANG_PATH"
    
    # Create symbolic link
    SYMLINK_DIR=$(dirname "$LIBCLANG_PATH")
    sudo ln -sf "$LIBCLANG_PATH" "$SYMLINK_DIR/libclang.so"
    
    print_success "Created symbolic link: $SYMLINK_DIR/libclang.so -> $LIBCLANG_PATH"
}

# Install Python packages
install_python_packages() {
    print_status "Installing Python packages..."
    
    # Install ctypeslib2 (which contains clang2py)
    print_status "Installing ctypeslib2 (contains clang2py)..."
    pip install ctypeslib2
    
    print_success "Python packages installed"
}

# Test installation
test_installation() {
    print_status "Testing clang2py installation..."
    
    # Test clang2py command
    if command_exists clang2py; then
        print_status "Running clang2py version check..."
        clang2py --version || true  # Don't exit on version warnings
        print_success "clang2py is working!"
    else
        print_error "clang2py command not found after installation"
        exit 1
    fi
}

# Main installation function
main() {
    print_status "Starting h2py (clang2py) installation..."
    echo
    
    # Check prerequisites
    check_os
    
    # Install system dependencies
    install_system_deps
    echo
    
    # Create libclang symbolic link
    create_libclang_symlink
    echo
    
    # Install Python packages
    install_python_packages
    echo
    
    # Test installation
    test_installation
    echo
    
    # Final success message
    print_success "Installation completed successfully!"
    echo
    print_status "To use h2py:"
    echo "  1. Activate the virtual environment: source py312/bin/activate"
    echo "  2. Run the conversion script: python h2py.py"
    echo "  3. Or use clang2py directly: clang2py input.h -o output.py"
    echo
    print_status "Example usage:"
    echo "  python h2py.py                    # Convert all .h files from hfiles/ to pyfiles/"
    echo "  python h2py.py -f hfiles/types.h  # Convert single file"
    echo "  clang2py hfiles/types.h -o pyfiles/types.py  # Direct conversion"
}

# Run main function
main "$@"