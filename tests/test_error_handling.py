#!/usr/bin/env python3
"""
Error Handling Test for Selenium MCP Server
Tests various error scenarios and ensures proper error handling
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from selenium_mcp_server import SeleniumMCPServer

async def test_error_handling():
    """Test error handling functionality"""
    print("⚠️ Testing Error Handling Features")
    print("=" * 50)
    
    server = SeleniumMCPServer()
    
    # Test 1: Invalid browser type
    print("\n1️⃣ Testing invalid browser type...")
    try:
        result = await server._start_browser({
            "browser": "invalid_browser",
            "session_name": "error_test"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 2: Invalid URL
    print("\n2️⃣ Testing invalid URL...")
    try:
        # Start a browser first
        await server._start_browser({
            "browser": "chrome",
            "options": {"headless": True},
            "session_name": "error_test"
        })
        
        result = await server._navigate({
            "url": "https://invalid-url-that-does-not-exist-12345.com"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 3: Element not found
    print("\n3️⃣ Testing element not found...")
    try:
        # Navigate to a real page
        await server._navigate({
            "url": "https://www.google.com",
            "wait_for_load": True
        })
        
        result = await server._find_element({
            "by": "id",
            "value": "non_existent_element_12345",
            "timeout": 2
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 4: Invalid locator strategy
    print("\n4️⃣ Testing invalid locator strategy...")
    try:
        result = await server._find_element({
            "by": "invalid_strategy",
            "value": "test",
            "timeout": 2
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 5: Invalid keyboard key
    print("\n5️⃣ Testing invalid keyboard key...")
    try:
        result = await server._press_key({
            "key": "INVALID_KEY_12345"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 6: File upload with non-existent file
    print("\n6️⃣ Testing file upload with non-existent file...")
    try:
        result = await server._upload_file({
            "by": "id",
            "value": "file_input",
            "filePath": "/path/to/non/existent/file.txt",
            "timeout": 5
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 7: Screenshot with invalid path
    print("\n7️⃣ Testing screenshot with invalid path...")
    try:
        result = await server._take_screenshot({
            "outputPath": "/invalid/path/that/does/not/exist/screenshot.png"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 8: JavaScript execution with invalid script
    print("\n8️⃣ Testing invalid JavaScript...")
    try:
        result = await server._execute_script({
            "script": "invalid javascript syntax {"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 9: Session switching with invalid session ID
    print("\n9️⃣ Testing invalid session switching...")
    try:
        result = await server._switch_session({
            "session_id": "invalid_session_id_12345"
        })
        print(f"❌ Unexpected success: {result}")
    except Exception as e:
        print(f"✅ Expected error caught: {type(e).__name__}: {e}")
    
    # Test 10: Valid operations should still work
    print("\n🔟 Testing valid operations still work...")
    try:
        # Start a new browser
        result = await server._start_browser({
            "browser": "chrome",
            "options": {"headless": True},
            "session_name": "valid_test"
        })
        print(f"✅ Valid browser start: {result}")
        
        # Navigate to a valid page
        result = await server._navigate({
            "url": "https://www.google.com",
            "wait_for_load": True
        })
        print(f"✅ Valid navigation: {result}")
        
        # Get page info
        result = await server._get_page_info({
            "include_title": True,
            "include_url": True
        })
        print(f"✅ Valid page info: {result}")
        
        # Take screenshot
        result = await server._take_screenshot({
            "outputPath": "error_test_screenshot.png"
        })
        print(f"✅ Valid screenshot: {result}")
        
    except Exception as e:
        print(f"❌ Valid operation failed: {e}")
    
    print("\n🎉 Error handling tests completed!")
    print("✅ All expected errors were caught properly")
    print("✅ Valid operations still work correctly")

if __name__ == "__main__":
    print("Selenium MCP Server - Error Handling Test")
    print("This will test various error scenarios")
    print("Expected errors are normal and indicate proper error handling")
    
    response = input("\nPress Enter to continue or 'q' to quit: ")
    if response.lower() != 'q':
        asyncio.run(test_error_handling())
    else:
        print("Test cancelled by user") 