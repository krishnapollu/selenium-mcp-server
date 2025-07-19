#!/usr/bin/env python3
"""
Main entry point for Selenium MCP Server
Run this script to start the MCP server
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from selenium_mcp_server import SeleniumMCPServer

def main():
    """Main entry point"""
    print("🚀 Starting Selenium MCP Server...")
    print("=" * 50)
    
    # Create and run the server
    server = SeleniumMCPServer()
    
    # This would typically start the MCP server
    # For now, just show that it's initialized
    print("✅ Selenium MCP Server initialized successfully!")
    print("📋 Available tools:", [tool["name"] for tool in server.get_tools()])
    print("\n💡 To run tests, use: python tests/run_tests.py")
    print("💡 To see examples, check: examples/example_usage.py")

if __name__ == "__main__":
    main() 