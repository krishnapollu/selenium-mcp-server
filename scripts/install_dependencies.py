#!/usr/bin/env python3
"""
Dependency installation script for Selenium MCP Server
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing Dependencies")
    print("=" * 50)
    
    # List of dependencies
    dependencies = [
        "mcp>=1.0.0",
        "selenium>=4.15.0", 
        "webdriver-manager>=4.0.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0"
    ]
    
    for dep in dependencies:
        print(f"\n📦 Installing {dep}...")
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {dep}: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    print("\n🎉 All dependencies installed successfully!")
    return True

def verify_installation():
    """Verify that all dependencies are installed"""
    print("\n🔍 Verifying Installation")
    print("=" * 50)
    
    try:
        import mcp
        print("✅ MCP package imported successfully")
    except ImportError:
        print("❌ MCP package not found")
        return False
    
    try:
        import selenium
        print("✅ Selenium package imported successfully")
    except ImportError:
        print("❌ Selenium package not found")
        return False
    
    try:
        import webdriver_manager
        print("✅ WebDriver Manager imported successfully")
    except ImportError:
        print("❌ WebDriver Manager not found")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError:
        print("❌ Pydantic not found")
        return False
    
    print("\n🎉 All dependencies verified!")
    return True

def test_server_import():
    """Test that the server can be imported"""
    print("\n🧪 Testing Server Import")
    print("=" * 50)
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from selenium_mcp_server import SeleniumMCPServer
        print("✅ SeleniumMCPServer imported successfully")
        
        # Test server initialization
        server = SeleniumMCPServer()
        print(f"✅ Server initialized successfully")
        print(f"✅ Tools configured and ready")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 Selenium MCP Server - Dependency Installer")
    print("=" * 60)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed!")
        return
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Dependency verification failed!")
        return
    
    # Test server import
    if not test_server_import():
        print("\n❌ Server import test failed!")
        return
    
    print("\n🎉 Installation Complete!")
    print("=" * 60)
    print("✅ All dependencies installed and verified")
    print("✅ Server can be imported and initialized")
    print("\n💡 Next steps:")
    print("  1. Run tests: python tests/run_tests.py")
    print("  2. Start server: python run_server.py")
    print("  3. Check examples: python examples/example_usage.py")

if __name__ == "__main__":
    main() 