#!/usr/bin/env python3
"""
Interactive test script for Selenium MCP Server
Run this to test basic functionality manually
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from selenium_mcp_server import SeleniumMCPServer

async def test_basic_functionality():
    """Test basic MCP server functionality"""
    print("🚀 Starting Selenium MCP Server Basic Test")
    print("=" * 50)
    
    server = SeleniumMCPServer()
    
    try:
        # Test 1: Start browser
        print("\n1️⃣ Starting Chrome browser...")
        result = await server._start_browser({
            "browser": "chrome",
            "options": {"headless": False},
            "session_name": "interactive_test"
        })
        print(f"✅ Browser started: {result}")
        
        # Test 2: Navigate to a page
        print("\n2️⃣ Navigating to Google...")
        result = await server._navigate({
            "url": "https://www.google.com",
            "wait_for_load": True
        })
        print(f"✅ Navigation result: {result}")
        
        # Test 3: Get page info
        print("\n3️⃣ Getting page information...")
        result = await server._get_page_info({
            "include_title": True,
            "include_url": True
        })
        print(f"✅ Page info: {result}")
        
        # Test 4: Find and interact with search box
        print("\n4️⃣ Finding search box...")
        result = await server._find_element({
            "by": "name",
            "value": "q",
            "timeout": 10
        })
        print(f"✅ Element found: {result}")
        
        print("\n5️⃣ Typing in search box...")
        result = await server._send_keys({
            "by": "name",
            "value": "q",
            "text": "Selenium MCP test",
            "clear_first": True
        })
        print(f"✅ Text input result: {result}")
        
        # Test 6: Take screenshot
        print("\n6️⃣ Taking screenshot...")
        result = await server._take_screenshot({
            "outputPath": "interactive_test_screenshot.png"
        })
        print(f"✅ Screenshot result: {result}")
        
        # Test 7: List sessions
        print("\n7️⃣ Listing active sessions...")
        result = await server._list_sessions({})
        print(f"✅ Active sessions: {result}")
        
        print("\n🎉 All basic tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        print("\n🧹 Cleaning up...")
        try:
            await server._close_session({})
            print("✅ Session closed successfully")
        except:
            print("⚠️ Session cleanup failed (this is normal if no session was active)")

if __name__ == "__main__":
    print("Selenium MCP Server - Interactive Test")
    print("This will open a Chrome browser and perform basic tests")
    print("Make sure you have Chrome installed and internet connection")
    
    response = input("\nPress Enter to continue or 'q' to quit: ")
    if response.lower() != 'q':
        asyncio.run(test_basic_functionality())
    else:
        print("Test cancelled by user") 