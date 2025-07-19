#!/usr/bin/env python3
"""
Setup script for the Selenium MCP Server

This script helps install dependencies and configure the MCP server.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_browsers():
    """Check if browsers are available."""
    print("\n🌐 Checking browser availability...")
    
    browsers = {
        "chrome": {
            "windows": ["chrome.exe", "google-chrome.exe"],
            "darwin": ["google-chrome", "chromium"],
            "linux": ["google-chrome", "chromium", "chromium-browser"]
        },
        "firefox": {
            "windows": ["firefox.exe"],
            "darwin": ["firefox"],
            "linux": ["firefox"]
        }
    }
    
    system = platform.system().lower()
    if system == "windows":
        system = "windows"
    elif system == "darwin":
        system = "darwin"
    else:
        system = "linux"
    
    available_browsers = []
    
    for browser, paths in browsers.items():
        for path in paths.get(system, []):
            try:
                if system == "windows":
                    result = subprocess.run(["where", path], capture_output=True, text=True)
                else:
                    result = subprocess.run(["which", path], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {browser.capitalize()} found: {path}")
                    available_browsers.append(browser)
                    break
            except Exception:
                continue
        else:
            print(f"⚠️  {browser.capitalize()} not found")
    
    return available_browsers

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ["screenshots", "logs", "downloads"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}/")

def test_installation():
    """Test the installation by running a simple test."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test importing required modules
        import selenium
        import mcp
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        
        print("✅ All modules imported successfully!")
        
        # Test driver manager
        print("📥 Testing driver managers...")
        try:
            chrome_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver: {chrome_path}")
        except Exception as e:
            print(f"⚠️  ChromeDriver download failed: {e}")
        
        try:
            firefox_path = GeckoDriverManager().install()
            print(f"✅ GeckoDriver: {firefox_path}")
        except Exception as e:
            print(f"⚠️  GeckoDriver download failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_config_files():
    """Create configuration files for different MCP clients."""
    print("\n⚙️  Creating configuration files...")
    
    # Claude Desktop configuration
    claude_config = {
        "mcpServers": {
            "selenium": {
                "command": "python",
                "args": [str(Path.cwd() / "selenium_mcp_server.py")],
                "env": {
                    "PYTHONPATH": str(Path.cwd()),
                    "PYTHONUNBUFFERED": "1"
                }
            }
        }
    }
    
    with open("claude_desktop_config.json", "w") as f:
        import json
        json.dump(claude_config, f, indent=2)
    
    print("✅ Created claude_desktop_config.json")
    
    # Create a simple shell script for easy server startup
    if platform.system() != "windows":
        with open("start_server.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("python selenium_mcp_server.py\n")
        
        os.chmod("start_server.sh", 0o755)
        print("✅ Created start_server.sh")
    else:
        with open("start_server.bat", "w") as f:
            f.write("@echo off\n")
            f.write("python selenium_mcp_server.py\n")
            f.write("pause\n")
        print("✅ Created start_server.bat")

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the MCP server:")
    if platform.system() != "windows":
        print("   ./start_server.sh")
    else:
        print("   start_server.bat")
    print("   or manually: python selenium_mcp_server.py")
    
    print("\n2. Configure your MCP client:")
    print("   - Copy claude_desktop_config.json to your Claude Desktop config")
    print("   - Or use the mcp_config.json for other clients")
    
    print("\n3. Test the server:")
    print("   python test_selenium_mcp.py")
    
    print("\n4. Run examples:")
    print("   python example_usage.py")
    
    print("\n📚 Documentation:")
    print("   - README.md - Complete documentation")
    print("   - Available tools and usage examples")
    
    print("\n🔧 Troubleshooting:")
    print("   - Check browser installation if drivers fail to download")
    print("   - Ensure Python 3.8+ is installed")
    print("   - Check internet connection for driver downloads")

def main():
    """Main setup function."""
    print("🚀 Selenium MCP Server Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check browsers
    available_browsers = check_browsers()
    if not available_browsers:
        print("⚠️  No browsers found. You may need to install Chrome or Firefox.")
    
    # Create directories
    create_directories()
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed!")
        sys.exit(1)
    
    # Create config files
    create_config_files()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 