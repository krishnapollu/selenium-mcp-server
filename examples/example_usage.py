#!/usr/bin/env python3
"""
Example usage of the Selenium MCP Server

This script demonstrates how to use the Selenium MCP server for real browser automation.
It shows a practical example of automating a web form submission.
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

# This is a simplified example - in a real MCP client, you would use the MCP protocol
# to communicate with the server via JSON-RPC messages

class SeleniumMCPExample:
    """Example class showing how to use the Selenium MCP server."""
    
    def __init__(self):
        self.server_process = None
        
    async def start_server(self):
        """Start the MCP server process."""
        try:
            # In a real implementation, you would start the MCP server
            # and communicate with it via JSON-RPC
            print("Starting Selenium MCP server...")
            # self.server_process = subprocess.Popen(
            #     [sys.executable, "selenium_mcp_server.py"],
            #     stdin=subprocess.PIPE,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE
            # )
            print("Server started successfully!")
            return True
        except Exception as e:
            print(f"Failed to start server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the MCP server process."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("Server stopped.")
    
    def simulate_mcp_call(self, tool_name: str, arguments: dict) -> dict:
        """Simulate an MCP tool call (for demonstration purposes)."""
        print(f"\n🔧 Calling: {tool_name}")
        print(f"📝 Arguments: {json.dumps(arguments, indent=2)}")
        
        # Simulate the response based on the tool
        if tool_name == "mcp_selenium_start_browser":
            return {
                "content": [{"type": "text", "text": "✅ Browser started successfully"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_navigate":
            return {
                "content": [{"type": "text", "text": f"✅ Navigated to {arguments.get('url')}"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_send_keys":
            return {
                "content": [{"type": "text", "text": f"✅ Typed '{arguments.get('text')}' into {arguments.get('by')}={arguments.get('value')}"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_click_element":
            return {
                "content": [{"type": "text", "text": f"✅ Clicked {arguments.get('by')}={arguments.get('value')}"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_get_element_text":
            return {
                "content": [{"type": "text", "text": f"✅ Retrieved text from {arguments.get('by')}={arguments.get('value')}: 'Sample text content'"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_take_screenshot":
            return {
                "content": [{"type": "text", "text": f"✅ Screenshot saved to {arguments.get('outputPath', 'screenshot.png')}"}],
                "isError": False
            }
        elif tool_name == "mcp_selenium_close_session":
            return {
                "content": [{"type": "text", "text": "✅ Browser session closed"}],
                "isError": False
            }
        else:
            return {
                "content": [{"type": "text", "text": f"❌ Unknown tool: {tool_name}"}],
                "isError": True
            }

async def example_google_search():
    """Example: Automate a Google search."""
    print("🌐 Example: Google Search Automation")
    print("=" * 50)
    
    example = SeleniumMCPExample()
    
    try:
        # Start the MCP server
        await example.start_server()
        
        # Step 1: Start browser
        result = example.simulate_mcp_call("mcp_selenium_start_browser", {
            "browser": "chrome",
            "options": {
                "headless": False,
                "arguments": ["--no-sandbox", "--disable-dev-shm-usage"]
            }
        })
        print(f"Result: {result['content'][0]['text']}")
        
        # Step 2: Navigate to Google
        result = example.simulate_mcp_call("mcp_selenium_navigate", {
            "url": "https://www.google.com"
        })
        print(f"Result: {result['content'][0]['text']}")
        
        # Step 3: Find and fill search box
        result = example.simulate_mcp_call("mcp_selenium_send_keys", {
            "by": "name",
            "value": "q",
            "text": "Selenium automation testing",
            "timeout": 10000
        })
        print(f"Result: {result['content'][0]['text']}")
        
        # Step 4: Click search button
        result = example.simulate_mcp_call("mcp_selenium_click_element", {
            "by": "css",
            "value": "input[type='submit']",
            "timeout": 10000
        })
        print(f"Result: {result['content'][0]['text']}")
        
        # Step 5: Wait a moment and take screenshot
        print("⏳ Waiting for page to load...")
        await asyncio.sleep(2)
        
        result = example.simulate_mcp_call("mcp_selenium_take_screenshot", {
            "outputPath": "google_search_results.png"
        })
        print(f"Result: {result['content'][0]['text']}")
        
        # Step 6: Close browser
        result = example.simulate_mcp_call("mcp_selenium_close_session", {
            "random_string": "close"
        })
        print(f"Result: {result['content'][0]['text']}")
        
        print("\n✅ Google search automation completed!")
        
    except Exception as e:
        print(f"❌ Error during automation: {e}")
    finally:
        await example.stop_server()

async def example_form_filling():
    """Example: Fill out a web form."""
    print("\n📝 Example: Web Form Filling")
    print("=" * 50)
    
    example = SeleniumMCPExample()
    
    try:
        await example.start_server()
        
        # Start browser
        example.simulate_mcp_call("mcp_selenium_start_browser", {
            "browser": "chrome",
            "options": {"headless": True}
        })
        
        # Navigate to a form page (example)
        example.simulate_mcp_call("mcp_selenium_navigate", {
            "url": "https://example.com/contact"
        })
        
        # Fill out form fields
        form_data = [
            {"by": "id", "value": "name", "text": "John Doe"},
            {"by": "id", "value": "email", "text": "john.doe@example.com"},
            {"by": "id", "value": "message", "text": "This is a test message from Selenium MCP server."}
        ]
        
        for field in form_data:
            example.simulate_mcp_call("mcp_selenium_send_keys", {
                "by": field["by"],
                "value": field["value"],
                "text": field["text"],
                "timeout": 5000
            })
        
        # Submit form
        example.simulate_mcp_call("mcp_selenium_click_element", {
            "by": "css",
            "value": "button[type='submit']",
            "timeout": 5000
        })
        
        # Take screenshot of submitted form
        example.simulate_mcp_call("mcp_selenium_take_screenshot", {
            "outputPath": "form_submission.png"
        })
        
        # Close browser
        example.simulate_mcp_call("mcp_selenium_close_session", {
            "random_string": "close"
        })
        
        print("✅ Form filling automation completed!")
        
    except Exception as e:
        print(f"❌ Error during form filling: {e}")
    finally:
        await example.stop_server()

async def example_element_interaction():
    """Example: Various element interactions."""
    print("\n🎯 Example: Element Interactions")
    print("=" * 50)
    
    example = SeleniumMCPExample()
    
    try:
        await example.start_server()
        
        # Start browser
        example.simulate_mcp_call("mcp_selenium_start_browser", {
            "browser": "firefox",
            "options": {"headless": False}
        })
        
        # Navigate to a test page
        example.simulate_mcp_call("mcp_selenium_navigate", {
            "url": "https://example.com"
        })
        
        # Demonstrate different locator strategies
        locators = [
            {"by": "id", "value": "main-content", "description": "Find by ID"},
            {"by": "css", "value": "h1", "description": "Find by CSS selector"},
            {"by": "xpath", "value": "//a[@href]", "description": "Find by XPath"},
            {"by": "name", "value": "search", "description": "Find by name"},
            {"by": "tag", "value": "button", "description": "Find by tag name"},
            {"by": "class", "value": "btn-primary", "description": "Find by class"}
        ]
        
        for locator in locators:
            print(f"Testing {locator['description']}: {locator['by']}={locator['value']}")
            
            # Try to find the element
            result = example.simulate_mcp_call("mcp_selenium_find_element", {
                "by": locator["by"],
                "value": locator["value"],
                "timeout": 3000
            })
            
            # Try to get text from the element
            if not result["isError"]:
                example.simulate_mcp_call("mcp_selenium_get_element_text", {
                    "by": locator["by"],
                    "value": locator["value"],
                    "timeout": 3000
                })
        
        # Demonstrate advanced interactions
        print("\nDemonstrating advanced interactions:")
        
        # Hover over an element
        example.simulate_mcp_call("mcp_selenium_hover", {
            "by": "css",
            "value": ".menu-item",
            "timeout": 5000
        })
        
        # Double click
        example.simulate_mcp_call("mcp_selenium_double_click", {
            "by": "css",
            "value": ".selectable-text",
            "timeout": 5000
        })
        
        # Right click
        example.simulate_mcp_call("mcp_selenium_right_click", {
            "by": "css",
            "value": ".context-menu-trigger",
            "timeout": 5000
        })
        
        # Press keyboard keys
        example.simulate_mcp_call("mcp_selenium_press_key", {
            "key": "Escape"
        })
        
        # Close browser
        example.simulate_mcp_call("mcp_selenium_close_session", {
            "random_string": "close"
        })
        
        print("✅ Element interaction examples completed!")
        
    except Exception as e:
        print(f"❌ Error during element interactions: {e}")
    finally:
        await example.stop_server()

def main():
    """Run all examples."""
    print("🚀 Selenium MCP Server Examples")
    print("=" * 60)
    print("This script demonstrates various use cases for the Selenium MCP server.")
    print("Note: These are simulated examples. In a real scenario, you would")
    print("communicate with the MCP server via JSON-RPC protocol.\n")
    
    # Run examples
    asyncio.run(example_google_search())
    asyncio.run(example_form_filling())
    asyncio.run(example_element_interaction())
    
    print("\n🎉 All examples completed!")
    print("\nTo use the real MCP server:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python selenium_mcp_server.py")
    print("3. Configure your MCP client with the provided mcp_config.json")
    print("4. Use the tools in your AI assistant!")

if __name__ == "__main__":
    main() 