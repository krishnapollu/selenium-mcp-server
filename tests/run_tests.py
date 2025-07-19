#!/usr/bin/env python3
"""
Test Runner for Selenium MCP Server
Run different test suites easily
"""

import asyncio
import sys
import os

def print_menu():
    """Print the test menu"""
    print("\n🧪 Selenium MCP Server - Test Runner")
    print("=" * 50)
    print("Choose a test to run:")
    print("1. 🚀 Basic Functionality Test (interactive_test.py)")
    print("2. 🌐 Browser Management Test (test_browser_management.py)")
    print("3. ⚠️ Error Handling Test (test_error_handling.py)")
    print("4. 🧪 Full Test Suite (test_selenium_mcp.py)")
    print("5. 🎯 Run All Tests")
    print("6. 📋 Show Test Files")
    print("7. ❌ Exit")
    print("=" * 50)

def run_test_file(filename):
    """Run a specific test file"""
    if not os.path.exists(filename):
        print(f"❌ Test file {filename} not found!")
        return False
    
    print(f"\n🚀 Running {filename}...")
    print("=" * 50)
    
    try:
        # Import and run the test
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", filename)
        if spec is None:
            print(f"❌ Could not load spec for {filename}")
            return False
        test_module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            print(f"❌ Could not load module {filename}")
            return False
        spec.loader.exec_module(test_module)
        
        # Find the main test function
        if hasattr(test_module, 'test_basic_functionality'):
            asyncio.run(test_module.test_basic_functionality())
        elif hasattr(test_module, 'test_browser_management'):
            asyncio.run(test_module.test_browser_management())
        elif hasattr(test_module, 'test_error_handling'):
            asyncio.run(test_module.test_error_handling())
        elif hasattr(test_module, 'main'):
            asyncio.run(test_module.main())
        else:
            print(f"❌ No test function found in {filename}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error running {filename}: {e}")
        return False

def run_all_tests():
    """Run all test files"""
    test_files = [
        "interactive_test.py",
        "test_browser_management.py", 
        "test_error_handling.py",
        "test_selenium_mcp.py"
    ]
    
    print("\n🎯 Running All Tests")
    print("=" * 50)
    
    results = {}
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Running {test_file}...")
            success = run_test_file(test_file)
            results[test_file] = success
        else:
            print(f"⚠️ {test_file} not found, skipping...")
            results[test_file] = False
    
    # Print summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    for test_file, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_file}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    print(f"\n🎉 {passed}/{total} tests passed!")

def show_test_files():
    """Show available test files"""
    print("\n📋 Available Test Files")
    print("=" * 50)
    
    test_files = [
        ("interactive_test.py", "Basic functionality test with visual browser"),
        ("test_browser_management.py", "Multiple browser sessions and switching"),
        ("test_error_handling.py", "Error scenarios and exception handling"),
        ("test_selenium_mcp.py", "Complete test suite with all features"),
        ("MANUAL_TESTING.md", "Comprehensive testing guide")
    ]
    
    for filename, description in test_files:
        exists = "✅" if os.path.exists(filename) else "❌"
        print(f"{exists} {filename}: {description}")

def main():
    """Main test runner function"""
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                run_test_file("interactive_test.py")
            elif choice == "2":
                run_test_file("test_browser_management.py")
            elif choice == "3":
                run_test_file("test_error_handling.py")
            elif choice == "4":
                run_test_file("test_selenium_mcp.py")
            elif choice == "5":
                run_all_tests()
            elif choice == "6":
                show_test_files()
            elif choice == "7":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Test runner interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        
        if choice in ["1", "2", "3", "4", "5"]:
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 