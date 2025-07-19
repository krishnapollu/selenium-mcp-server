# Manual Testing Guide for Selenium MCP Server

This guide shows you how to manually test your Selenium MCP server using different approaches.

## 🚀 Quick Test Methods

### Method 1: Using the Built-in Test Suite

The easiest way to test is using the existing test file:

```bash
python test_selenium_mcp.py
```

This runs a comprehensive test suite that validates:
- Tool schema validation
- Browser session management
- Element interactions
- Screenshot functionality
- Error handling

### Method 2: Interactive Python Testing

Create a simple interactive test script:

```python
# interactive_test.py
import asyncio
import json
from selenium_mcp_server import SeleniumMCPServer

async def test_basic_functionality():
    server = SeleniumMCPServer()
    
    # Test 1: Start browser
    result = await server._start_browser({
        "browser": "chrome",
        "options": {"headless": False},
        "session_name": "test_session"
    })
    print("Browser started:", result)
    
    # Test 2: Navigate to a page
    result = await server._navigate({
        "url": "https://www.google.com",
        "wait_for_load": True
    })
    print("Navigation result:", result)
    
    # Test 3: Find and interact with search box
    result = await server._send_keys({
        "by": "name",
        "value": "q",
        "text": "Selenium MCP test",
        "clear_first": True
    })
    print("Text input result:", result)
    
    # Test 4: Take screenshot
    result = await server._take_screenshot({
        "outputPath": "test_screenshot.png"
    })
    print("Screenshot result:", result)

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
```

### Method 3: MCP Protocol Testing

Test the actual MCP protocol by simulating client calls:

```python
# mcp_protocol_test.py
import asyncio
import json
from selenium_mcp_server import SeleniumMCPServer

async def test_mcp_protocol():
    server = SeleniumMCPServer()
    
    # Simulate MCP tool call
    tool_call = {
        "name": "start_browser",
        "arguments": {
            "browser": "chrome",
            "options": {"headless": False},
            "session_name": "mcp_test"
        }
    }
    
    # Get tool schema
    tools = server.get_tools()
    print("Available tools:", [tool["name"] for tool in tools])
    
    # Test tool call
    result = await server._handle_tool_call(tool_call)
    print("MCP tool call result:", result)

if __name__ == "__main__":
    asyncio.run(test_mcp_protocol())
```

## 🔧 Step-by-Step Manual Testing

### Step 1: Start the Server

```bash
python selenium_mcp_server.py
```

The server should start and show:
```
Selenium MCP Server starting...
Server initialized with tools: ['start_browser', 'navigate', ...]
```

### Step 2: Test Individual Tools

#### Test Browser Management

```python
# test_browser_management.py
import asyncio
from selenium_mcp_server import SeleniumMCPServer

async def test_browser_management():
    server = SeleniumMCPServer()
    
    print("=== Testing Browser Management ===")
    
    # 1. Start browser
    print("1. Starting Chrome browser...")
    result = await server._start_browser({
        "browser": "chrome",
        "options": {"headless": False},
        "session_name": "manual_test"
    })
    print(f"Result: {result}")
    
    # 2. List sessions
    print("\n2. Listing sessions...")
    result = await server._list_sessions({})
    print(f"Active sessions: {result}")
    
    # 3. Start another browser
    print("\n3. Starting Firefox browser...")
    result = await server._start_browser({
        "browser": "firefox",
        "options": {"headless": True},
        "session_name": "firefox_test"
    })
    print(f"Result: {result}")
    
    # 4. List sessions again
    print("\n4. Listing sessions again...")
    result = await server._list_sessions({})
    print(f"Active sessions: {result}")

if __name__ == "__main__":
    asyncio.run(test_browser_management())
```

#### Test Navigation and Page Interaction

```python
# test_navigation.py
import asyncio
from selenium_mcp_server import SeleniumMCPServer

async def test_navigation():
    server = SeleniumMCPServer()
    
    print("=== Testing Navigation and Page Interaction ===")
    
    # 1. Start browser
    await server._start_browser({
        "browser": "chrome",
        "options": {"headless": False},
        "session_name": "nav_test"
    })
    
    # 2. Navigate to Google
    print("1. Navigating to Google...")
    result = await server._navigate({
        "url": "https://www.google.com",
        "wait_for_load": True
    })
    print(f"Navigation result: {result}")
    
    # 3. Get page info
    print("\n2. Getting page info...")
    result = await server._get_page_info({
        "include_title": True,
        "include_url": True
    })
    print(f"Page info: {result}")
    
    # 4. Find search box
    print("\n3. Finding search box...")
    result = await server._find_element({
        "by": "name",
        "value": "q",
        "timeout": 10
    })
    print(f"Element found: {result}")
    
    # 5. Type in search box
    print("\n4. Typing in search box...")
    result = await server._send_keys({
        "by": "name",
        "value": "q",
        "text": "Selenium MCP testing",
        "clear_first": True
    })
    print(f"Text input result: {result}")
    
    # 6. Take screenshot
    print("\n5. Taking screenshot...")
    result = await server._take_screenshot({
        "outputPath": "google_test.png"
    })
    print(f"Screenshot result: {result}")

if __name__ == "__main__":
    asyncio.run(test_navigation())
```

#### Test Advanced Features

```python
# test_advanced_features.py
import asyncio
from selenium_mcp_server import SeleniumMCPServer

async def test_advanced_features():
    server = SeleniumMCPServer()
    
    print("=== Testing Advanced Features ===")
    
    # 1. Start browser
    await server._start_browser({
        "browser": "chrome",
        "options": {"headless": False},
        "session_name": "advanced_test"
    })
    
    # 2. Navigate to a test page
    await server._navigate({
        "url": "https://httpbin.org/forms/post",
        "wait_for_load": True
    })
    
    # 3. Test JavaScript execution
    print("1. Testing JavaScript execution...")
    result = await server._execute_script({
        "script": "return document.title;"
    })
    print(f"Page title: {result}")
    
    # 4. Test element waiting
    print("\n2. Testing element waiting...")
    result = await server._wait_for_element({
        "by": "tag",
        "value": "form",
        "timeout": 10,
        "wait_for_visible": True
    })
    print(f"Form element found: {result}")
    
    # 5. Test hover (if element exists)
    print("\n3. Testing hover...")
    try:
        result = await server._hover({
            "by": "tag",
            "value": "form",
            "timeout": 5
        })
        print(f"Hover result: {result}")
    except Exception as e:
        print(f"Hover test failed (expected): {e}")
    
    # 6. Test keyboard input
    print("\n4. Testing keyboard input...")
    result = await server._press_key({
        "key": "Tab"
    })
    print(f"Tab key result: {result}")

if __name__ == "__main__":
    asyncio.run(test_advanced_features())
```

## 🧪 Error Testing

### Test Error Handling

```python
# test_error_handling.py
import asyncio
from selenium_mcp_server import SeleniumMCPServer

async def test_error_handling():
    server = SeleniumMCPServer()
    
    print("=== Testing Error Handling ===")
    
    # 1. Test invalid browser
    print("1. Testing invalid browser...")
    try:
        result = await server._start_browser({
            "browser": "invalid_browser",
            "session_name": "error_test"
        })
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error: {e}")
    
    # 2. Test element not found
    print("\n2. Testing element not found...")
    await server._start_browser({
        "browser": "chrome",
        "options": {"headless": True},
        "session_name": "error_test"
    })
    
    await server._navigate({
        "url": "https://www.google.com"
    })
    
    try:
        result = await server._find_element({
            "by": "id",
            "value": "non_existent_element",
            "timeout": 2
        })
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error: {e}")
    
    # 3. Test invalid URL
    print("\n3. Testing invalid URL...")
    try:
        result = await server._navigate({
            "url": "https://invalid-url-that-does-not-exist.com"
        })
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_error_handling())
```

## 🔍 Debug Mode Testing

### Enable Debug Logging

```python
# debug_test.py
import logging
import asyncio
from selenium_mcp_server import SeleniumMCPServer

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def debug_test():
    server = SeleniumMCPServer()
    
    print("=== Debug Mode Testing ===")
    
    # This will show detailed logs
    result = await server._start_browser({
        "browser": "chrome",
        "options": {"headless": True},
        "session_name": "debug_test"
    })
    print(f"Debug result: {result}")

if __name__ == "__main__":
    asyncio.run(debug_test())
```

## 📋 Testing Checklist

### Basic Functionality
- [ ] Server starts without errors
- [ ] Browser launches (Chrome and Firefox)
- [ ] Navigation works
- [ ] Element finding works
- [ ] Text input works
- [ ] Screenshots work

### Advanced Features
- [ ] Multiple sessions work
- [ ] Session switching works
- [ ] JavaScript execution works
- [ ] File upload works
- [ ] Error handling works properly

### Edge Cases
- [ ] Invalid URLs handled gracefully
- [ ] Non-existent elements handled properly
- [ ] Timeout errors work correctly
- [ ] Browser crashes handled

## 🚨 Common Issues and Solutions

### Issue: Browser won't start
**Solution**: Check if Chrome/Firefox is installed and webdriver-manager can access the internet

### Issue: Elements not found
**Solution**: Increase timeout, check locator strategy, ensure page is loaded

### Issue: Permission errors
**Solution**: Run with appropriate permissions, check file paths

### Issue: Import errors
**Solution**: Install dependencies with `pip install -r requirements.txt`

## 🎯 Quick Test Commands

Run these commands in sequence for a quick test:

```bash
# 1. Test basic functionality
python test_selenium_mcp.py

# 2. Test browser management
python test_browser_management.py

# 3. Test navigation
python test_navigation.py

# 4. Test advanced features
python test_advanced_features.py

# 5. Test error handling
python test_error_handling.py
```

## 📊 Performance Testing

```python
# performance_test.py
import asyncio
import time
from selenium_mcp_server import SeleniumMCPServer

async def performance_test():
    server = SeleniumMCPServer()
    
    print("=== Performance Testing ===")
    
    # Test browser startup time
    start_time = time.time()
    await server._start_browser({
        "browser": "chrome",
        "options": {"headless": True},
        "session_name": "perf_test"
    })
    startup_time = time.time() - start_time
    print(f"Browser startup time: {startup_time:.2f} seconds")
    
    # Test navigation time
    start_time = time.time()
    await server._navigate({
        "url": "https://www.google.com"
    })
    nav_time = time.time() - start_time
    print(f"Navigation time: {nav_time:.2f} seconds")
    
    # Test screenshot time
    start_time = time.time()
    await server._take_screenshot({
        "outputPath": "perf_test.png"
    })
    screenshot_time = time.time() - start_time
    print(f"Screenshot time: {screenshot_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(performance_test())
```

This comprehensive testing guide will help you thoroughly test your Selenium MCP server and ensure it's working correctly! 🎉 