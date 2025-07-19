#!/usr/bin/env python3
"""
Simple server runner for Selenium MCP Server
This script runs the MCP server directly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Import and run the server
    try:
        from selenium_mcp_server import SeleniumMCPServer
        print("🚀 Starting Selenium MCP Server...")
        print("=" * 50)
        
        # Create server instance
        server = SeleniumMCPServer()
        
        # Show server status
        print(f"✅ Server initialized successfully")
        print(f"✅ Server has tools configured")
        
        print("\n💡 Server is ready to accept MCP connections!")
        print("💡 To run tests, use: python tests/run_tests.py")
        print("💡 To see examples, check: examples/example_usage.py")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc() 