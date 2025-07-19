#!/usr/bin/env python3
"""
Browser Management Test for Selenium MCP Server
Tests multiple browser sessions, switching, and management
"""

import asyncio
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from selenium_mcp_server import SeleniumMCPServer

async def test_browser_management():
    """Test browser management functionality"""
    print("🌐 Testing Browser Management Features")
    print("=" * 50)
    
    server = SeleniumMCPServer()
    
    try:
        # Test 1: Start Chrome browser
        print("\n1️⃣ Starting Chrome browser...")
        result = await server._start_browser({
            "browser": "chrome",
            "options": {"headless": False},
            "session_name": "chrome_test"
        })
        print(f"✅ Chrome started: {result}")
        
        # Test 2: List sessions
        print("\n2️⃣ Listing active sessions...")
        result = await server._list_sessions({})
        print(f"✅ Active sessions: {result}")
        
        # Test 3: Start Firefox browser
        print("\n3️⃣ Starting Firefox browser...")
        result = await server._start_browser({
            "browser": "firefox",
            "options": {"headless": True},
            "session_name": "firefox_test"
        })
        print(f"✅ Firefox started: {result}")
        
        # Test 4: List sessions again
        print("\n4️⃣ Listing sessions after Firefox...")
        result = await server._list_sessions({})
        print(f"✅ Active sessions: {result}")
        
        # Test 5: Navigate in Chrome
        print("\n5️⃣ Navigating Chrome to Google...")
        result = await server._navigate({
            "url": "https://www.google.com",
            "wait_for_load": True
        })
        print(f"✅ Chrome navigation: {result}")
        
        # Test 6: Switch to Firefox
        print("\n6️⃣ Switching to Firefox session...")
        sessions = await server._list_sessions({})
        firefox_session = None
        for session in sessions.get('sessions', []):
            if session.get('name') == 'firefox_test':
                firefox_session = session.get('id')
                break
        
        if firefox_session:
            result = await server._switch_session({
                "session_id": firefox_session
            })
            print(f"✅ Switched to Firefox: {result}")
            
            # Test 7: Navigate in Firefox
            print("\n7️⃣ Navigating Firefox to Bing...")
            result = await server._navigate({
                "url": "https://www.bing.com",
                "wait_for_load": True
            })
            print(f"✅ Firefox navigation: {result}")
        else:
            print("⚠️ Firefox session not found")
        
        # Test 8: Switch back to Chrome
        print("\n8️⃣ Switching back to Chrome...")
        sessions = await server._list_sessions({})
        chrome_session = None
        for session in sessions.get('sessions', []):
            if session.get('name') == 'chrome_test':
                chrome_session = session.get('id')
                break
        
        if chrome_session:
            result = await server._switch_session({
                "session_id": chrome_session
            })
            print(f"✅ Switched to Chrome: {result}")
            
            # Test 9: Get page info in Chrome
            print("\n9️⃣ Getting Chrome page info...")
            result = await server._get_page_info({
                "include_title": True,
                "include_url": True
            })
            print(f"✅ Chrome page info: {result}")
        
        # Test 10: Take screenshots from both browsers
        print("\n🔟 Taking screenshots...")
        
        # Chrome screenshot
        await server._switch_session({"session_id": chrome_session})
        result = await server._take_screenshot({
            "outputPath": "chrome_test.png"
        })
        print(f"✅ Chrome screenshot: {result}")
        
        # Firefox screenshot
        await server._switch_session({"session_id": firefox_session})
        result = await server._take_screenshot({
            "outputPath": "firefox_test.png"
        })
        print(f"✅ Firefox screenshot: {result}")
        
        print("\n🎉 Browser management tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up all sessions
        print("\n🧹 Cleaning up all sessions...")
        try:
            sessions = await server._list_sessions({})
            for session in sessions.get('sessions', []):
                session_id = session.get('id')
                if session_id:
                    await server._switch_session({"session_id": session_id})
                    await server._close_session({})
                    print(f"✅ Closed session: {session.get('name', 'unknown')}")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

if __name__ == "__main__":
    print("Selenium MCP Server - Browser Management Test")
    print("This will test multiple browser sessions and switching")
    print("Make sure you have Chrome and Firefox installed")
    
    response = input("\nPress Enter to continue or 'q' to quit: ")
    if response.lower() != 'q':
        asyncio.run(test_browser_management())
    else:
        print("Test cancelled by user") 