#!/usr/bin/env python3
"""
Generic MCP Launcher for Selenium MCP Server
Automatically installs and starts the server for any user.
"""

import subprocess
import sys
import importlib.util
import os
import asyncio

def install_package(package_name):
    """Install package if not already installed."""
    try:
        # Try to import the package
        importlib.import_module(package_name.replace('-', '_'))
        print(f"Package {package_name} is already installed.", file=sys.stderr)
        return True
    except ImportError:
        print(f"Installing {package_name}...", file=sys.stderr)
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                package_name, '--quiet', '--user'
            ], check=True, capture_output=True)
            print(f"Successfully installed {package_name}", file=sys.stderr)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_name}: {e}", file=sys.stderr)
            return False

def main():
    """Main launcher function."""
    package_name = "selenium-mcp-server"
    
    # Install the package if needed
    if not install_package(package_name):
        print("Failed to install selenium-mcp-server", file=sys.stderr)
        sys.exit(1)
    
    # Import and run the server
    try:
        import selenium_mcp_server
        print("Starting Selenium MCP Server...", file=sys.stderr)
        # Run the async main function
        asyncio.run(selenium_mcp_server.main())
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 