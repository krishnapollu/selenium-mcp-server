#!/usr/bin/env python3
"""
Cleanup script for Selenium MCP Server
Removes temporary files, cache directories, and other unnecessary files
"""

import os
import shutil
import glob

def cleanup_python_cache():
    """Remove Python cache directories"""
    print("🧹 Cleaning Python cache files...")
    
    cache_patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd"
    ]
    
    for pattern in cache_patterns:
        for path in glob.glob(pattern, recursive=True):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✅ Removed directory: {path}")
                else:
                    os.remove(path)
                    print(f"✅ Removed file: {path}")
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")

def cleanup_test_files():
    """Remove test-generated files"""
    print("\n🧹 Cleaning test-generated files...")
    
    test_files = [
        "*.png",  # Screenshots
        "*.jpg",
        "*.jpeg",
        "test_*.png",
        "interactive_test_screenshot.png",
        "google_test.png",
        "chrome_test.png",
        "firefox_test.png",
        "error_test_screenshot.png",
        "perf_test.png"
    ]
    
    for pattern in test_files:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
                print(f"✅ Removed test file: {path}")
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")

def cleanup_temp_directories():
    """Remove temporary directories"""
    print("\n🧹 Cleaning temporary directories...")
    
    temp_dirs = [
        "temp",
        "tmp",
        "logs",
        "downloads",
        "screenshots"
    ]
    
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Removed directory: {dir_name}")
            except Exception as e:
                print(f"⚠️ Could not remove {dir_name}: {e}")

def cleanup_browser_drivers():
    """Remove browser driver files"""
    print("\n🧹 Cleaning browser driver files...")
    
    driver_patterns = [
        "chromedriver*",
        "geckodriver*",
        "msedgedriver*",
        "operadriver*"
    ]
    
    for pattern in driver_patterns:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
                print(f"✅ Removed driver: {path}")
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")

def cleanup_build_files():
    """Remove build and distribution files"""
    print("\n🧹 Cleaning build files...")
    
    build_dirs = [
        "build",
        "dist",
        "*.egg-info"
    ]
    
    for pattern in build_dirs:
        for path in glob.glob(pattern):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"✅ Removed build directory: {path}")
                else:
                    os.remove(path)
                    print(f"✅ Removed build file: {path}")
            except Exception as e:
                print(f"⚠️ Could not remove {path}: {e}")

def show_project_size():
    """Show the size of the project"""
    print("\n📊 Project Size Information")
    print("=" * 50)
    
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and cache
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            if not file.startswith('.'):
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    file_count += 1
                except:
                    pass
    
    print(f"📁 Total files: {file_count}")
    print(f"📦 Total size: {total_size / 1024:.1f} KB")

def main():
    """Main cleanup function"""
    print("🧹 Selenium MCP Server - Cleanup Script")
    print("=" * 50)
    
    # Run cleanup operations
    cleanup_python_cache()
    cleanup_test_files()
    cleanup_temp_directories()
    cleanup_browser_drivers()
    cleanup_build_files()
    
    # Show project information
    show_project_size()
    
    print("\n🎉 Cleanup completed!")
    print("💡 The project is now clean and ready for development.")

if __name__ == "__main__":
    main() 