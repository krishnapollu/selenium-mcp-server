#!/usr/bin/env python3
"""
Entry point for running the Selenium MCP Server as a module.
Usage: python -m selenium_mcp_server
"""

import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run the main function from selenium_mcp_server
from selenium_mcp_server import main

if __name__ == "__main__":
    asyncio.run(main()) 