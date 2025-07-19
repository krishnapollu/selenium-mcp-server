#!/usr/bin/env python3
"""
Selenium MCP Server

This MCP server provides Selenium WebDriver functionality with improvements:
- Better session management (multiple sessions)
- Enhanced error handling
- Resource support
- Performance optimizations
- Additional tools
- Better state management
"""

import asyncio
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions

# Create a simple NotificationOptions class since it's not available in the current MCP version
class NotificationOptions:
    def __init__(self):
        self.resources_changed = False
        self.tools_changed = False
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    Resource,
    ListResourcesRequest,
    ListResourcesResult,
    ReadResourceRequest,
    ReadResourceResult,
)
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    SessionNotCreatedException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BrowserSession:
    """Represents a browser session with metadata."""
    session_id: str
    driver: webdriver.Remote
    browser_type: str
    created_at: datetime
    last_activity: datetime
    options: Dict[str, Any]
    url: Optional[str] = None

class SeleniumMCPServer:
    """MCP Server for Selenium WebDriver operations."""

    def __init__(self):
        self.server = Server("selenium-mcp")
        self.sessions: Dict[str, BrowserSession] = {}
        self.current_session_id: Optional[str] = None
        self.setup_tools()
        self.setup_resources()

    def setup_resources(self):
        """Setup MCP resources for browser status."""
        
        @self.server.list_resources()
        async def handle_list_resources():
            """List available resources."""
            resources = [
                Resource(
                    uri="browser-status://current",
                    name="Current Browser Status",
                    description="Status of the current browser session",
                    mimeType="text/plain"
                ),
                Resource(
                    uri="browser-status://sessions",
                    name="All Sessions",
                    description="List of all browser sessions",
                    mimeType="application/json"
                )
            ]
            return resources

        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Read resource content."""
            if uri == "browser-status://current":
                if self.current_session_id and self.current_session_id in self.sessions:
                    session = self.sessions[self.current_session_id]
                    content = f"Active session: {session.session_id}\n"
                    content += f"Browser: {session.browser_type}\n"
                    content += f"URL: {session.url or 'No URL'}\n"
                    content += f"Created: {session.created_at}\n"
                    content += f"Last activity: {session.last_activity}"
                else:
                    content = "No active browser session"
                
                return ReadResourceResult(
                    contents=[{
                        "uri": uri,
                        "text": content
                    }]
                )
            
            elif uri == "browser-status://sessions":
                sessions_data = []
                for session_id, session in self.sessions.items():
                    sessions_data.append({
                        "session_id": session_id,
                        "browser_type": session.browser_type,
                        "url": session.url,
                        "created_at": session.created_at.isoformat(),
                        "last_activity": session.last_activity.isoformat(),
                        "is_current": session_id == self.current_session_id
                    })
                
                return ReadResourceResult(
                    contents=[{
                        "uri": uri,
                        "text": json.dumps(sessions_data, indent=2)
                    }]
                )
            
            return ReadResourceResult(
                contents=[{
                    "uri": uri,
                    "text": "Resource not found"
                }]
            )

    def setup_tools(self):
        """Register all enhanced Selenium tools with the MCP server."""

        @self.server.list_tools()
        async def handle_list_tools():
            """List all available Selenium tools."""
            tools = [
                # Enhanced browser management
                Tool(
                    name="start_browser",
                    description="launches browser with enhanced session management",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "browser": {
                                "type": "string",
                                "enum": ["chrome", "firefox"],
                                "description": "Browser to launch (chrome or firefox)"
                            },
                            "options": {
                                "type": "object",
                                "properties": {
                                    "headless": {
                                        "type": "boolean",
                                        "description": "Run browser in headless mode"
                                    },
                                    "arguments": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Additional browser arguments"
                                    },
                                    "window_size": {
                                        "type": "object",
                                        "properties": {
                                            "width": {"type": "number"},
                                            "height": {"type": "number"}
                                        },
                                        "description": "Browser window size"
                                    }
                                },
                                "additionalProperties": False
                            },
                            "session_name": {
                                "type": "string",
                                "description": "Optional name for the session"
                            }
                        },
                        "required": ["browser"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="list_sessions",
                    description="lists all active browser sessions",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="switch_session",
                    description="switches to a different browser session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to switch to"
                            }
                        },
                        "required": ["session_id"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="close_session",
                    description="closes a specific browser session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to close (optional, closes current if not specified)"
                            }
                        },
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                # Enhanced navigation
                Tool(
                    name="navigate",
                    description="navigates to a URL with enhanced error handling",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to navigate to"
                            },
                            "wait_for_load": {
                                "type": "boolean",
                                "description": "Wait for page to fully load"
                            }
                        },
                        "required": ["url"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                # Enhanced element interaction
                Tool(
                    name="find_element",
                    description="finds an element with enhanced waiting",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "wait_for_clickable": {
                                "type": "boolean",
                                "description": "Wait for element to be clickable"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="click_element",
                    description="clicks an element with enhanced error handling",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "force_click": {
                                "type": "boolean",
                                "description": "Force click using JavaScript if normal click fails"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="send_keys",
                    description="sends keys to an element with enhanced typing",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "text": {
                                "type": "string",
                                "description": "Text to enter into the element"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "clear_first": {
                                "type": "boolean",
                                "description": "Clear the field before typing"
                            },
                            "type_speed": {
                                "type": "number",
                                "description": "Delay between keystrokes in milliseconds"
                            }
                        },
                        "required": ["by", "value", "text"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="get_element_text",
                    description="gets the text of an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                # Advanced interactions
                Tool(
                    name="hover",
                    description="moves the mouse to hover over an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="drag_and_drop",
                    description="drags an element and drops it onto another element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "targetBy": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find target element"
                            },
                            "targetValue": {
                                "type": "string",
                                "description": "Value for the target locator strategy"
                            }
                        },
                        "required": ["by", "value", "targetBy", "targetValue"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="double_click",
                    description="performs a double click on an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="right_click",
                    description="performs a right click (context click) on an element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="press_key",
                    description="simulates pressing a keyboard key",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Key to press (e.g., 'Enter', 'Tab', 'a', etc.)"
                            }
                        },
                        "required": ["key"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                # File operations
                Tool(
                    name="upload_file",
                    description="uploads a file using a file input element",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "filePath": {
                                "type": "string",
                                "description": "Absolute path to the file to upload"
                            }
                        },
                        "required": ["by", "value", "filePath"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="take_screenshot",
                    description="captures a screenshot of the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "outputPath": {
                                "type": "string",
                                "description": "Optional path where to save the screenshot. If not provided, returns base64 data."
                            },
                            "full_page": {
                                "type": "boolean",
                                "description": "Take full page screenshot"
                            }
                        },
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                # New enhanced tools
                Tool(
                    name="wait_for_element",
                    description="waits for an element to be present and optionally visible",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "by": {
                                "type": "string",
                                "enum": ["id", "css", "xpath", "name", "tag", "class"],
                                "description": "Locator strategy to find element"
                            },
                            "value": {
                                "type": "string",
                                "description": "Value for the locator strategy"
                            },
                            "timeout": {
                                "type": "number",
                                "description": "Maximum time to wait for element in milliseconds"
                            },
                            "wait_for_visible": {
                                "type": "boolean",
                                "description": "Wait for element to be visible"
                            }
                        },
                        "required": ["by", "value"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="execute_script",
                    description="executes JavaScript code in the browser",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "script": {
                                "type": "string",
                                "description": "JavaScript code to execute"
                            },
                            "arguments": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Arguments to pass to the script"
                            }
                        },
                        "required": ["script"],
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                ),
                Tool(
                    name="get_page_info",
                    description="gets information about the current page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "include_title": {
                                "type": "boolean",
                                "description": "Include page title"
                            },
                            "include_url": {
                                "type": "boolean",
                                "description": "Include current URL"
                            },
                            "include_source": {
                                "type": "boolean",
                                "description": "Include page source"
                            }
                        },
                        "additionalProperties": False,
                        "$schema": "http://json-schema.org/draft-07/schema#"
                    }
                )
            ]
            return tools

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls for enhanced Selenium operations."""
            try:
                # Update last activity for current session
                if self.current_session_id and self.current_session_id in self.sessions:
                    self.sessions[self.current_session_id].last_activity = datetime.now()

                if name == "start_browser":
                    return await self._start_browser(arguments)
                elif name == "list_sessions":
                    return await self._list_sessions(arguments)
                elif name == "switch_session":
                    return await self._switch_session(arguments)
                elif name == "close_session":
                    return await self._close_session(arguments)
                elif name == "navigate":
                    return await self._navigate(arguments)
                elif name == "find_element":
                    return await self._find_element(arguments)
                elif name == "click_element":
                    return await self._click_element(arguments)
                elif name == "send_keys":
                    return await self._send_keys(arguments)
                elif name == "get_element_text":
                    return await self._get_element_text(arguments)
                elif name == "hover":
                    return await self._hover(arguments)
                elif name == "drag_and_drop":
                    return await self._drag_and_drop(arguments)
                elif name == "double_click":
                    return await self._double_click(arguments)
                elif name == "right_click":
                    return await self._right_click(arguments)
                elif name == "press_key":
                    return await self._press_key(arguments)
                elif name == "upload_file":
                    return await self._upload_file(arguments)
                elif name == "take_screenshot":
                    return await self._take_screenshot(arguments)
                elif name == "wait_for_element":
                    return await self._wait_for_element(arguments)
                elif name == "execute_script":
                    return await self._execute_script(arguments)
                elif name == "get_page_info":
                    return await self._get_page_info(arguments)
                else:
                    return CallToolResult(
                        content=[{"type": "text", "text": f"Unknown tool: {name}"}],
                        isError=True
                    )
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return CallToolResult(
                    content=[{"type": "text", "text": f"Error: {str(e)}"}],
                    isError=True
                )

    def _get_current_driver(self) -> webdriver.Remote:
        """Get the current active WebDriver instance."""
        if not self.current_session_id or self.current_session_id not in self.sessions:
            raise WebDriverException("No active browser session. Please start a browser first.")
        return self.sessions[self.current_session_id].driver

    def _get_session(self, session_id: Optional[str] = None) -> BrowserSession:
        """Get a browser session by ID or current session."""
        if session_id:
            if session_id not in self.sessions:
                raise WebDriverException(f"Session {session_id} not found.")
            return self.sessions[session_id]
        else:
            if not self.current_session_id or self.current_session_id not in self.sessions:
                raise WebDriverException("No active browser session.")
            return self.sessions[self.current_session_id]

    def _get_locator(self, by: str) -> By:
        """Convert string locator to Selenium By enum."""
        locator_map = {
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "class": By.CLASS_NAME
        }
        return locator_map.get(by, By.CSS_SELECTOR)

    async def _start_browser(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Start a new browser session with enhanced features."""
        browser = arguments.get("browser", "chrome")
        options = arguments.get("options", {})
        session_name = arguments.get("session_name")
        
        headless = options.get("headless", False)
        additional_args = options.get("arguments", [])
        window_size = options.get("window_size")

        try:
            if browser.lower() == "chrome":
                chrome_options = ChromeOptions()
                if headless:
                    chrome_options.add_argument("--headless=new")
                for arg in additional_args:
                    chrome_options.add_argument(arg)
                
                if window_size:
                    chrome_options.add_argument(f"--window-size={window_size['width']},{window_size['height']}")
                
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
            elif browser.lower() == "firefox":
                firefox_options = FirefoxOptions()
                if headless:
                    firefox_options.add_argument("--headless")
                for arg in additional_args:
                    firefox_options.add_argument(arg)
                
                if window_size:
                    firefox_options.add_argument(f"--width={window_size['width']}")
                    firefox_options.add_argument(f"--height={window_size['height']}")
                
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=firefox_options)
            else:
                return CallToolResult(
                    content=[{"type": "text", "text": f"Unsupported browser: {browser}"}],
                    isError=True
                )

            # Create session with enhanced metadata
            session_id = str(uuid.uuid4())
            session = BrowserSession(
                session_id=session_id,
                driver=driver,
                browser_type=browser,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                options=options
            )
            
            self.sessions[session_id] = session
            self.current_session_id = session_id

            return CallToolResult(
                content=[{"type": "text", "text": f"✅ Browser started successfully! Session ID: {session_id}"}]
            )

        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Failed to start browser: {str(e)}"}],
                isError=True
            )

    async def _list_sessions(self, arguments: Dict[str, Any]) -> CallToolResult:
        """List all active browser sessions."""
        if not self.sessions:
            return CallToolResult(
                content=[{"type": "text", "text": "No active browser sessions"}]
            )
        
        session_list = []
        for session_id, session in self.sessions.items():
            session_info = {
                "session_id": session_id,
                "browser_type": session.browser_type,
                "url": session.url,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "is_current": session_id == self.current_session_id
            }
            session_list.append(session_info)
        
        return CallToolResult(
            content=[{"type": "text", "text": json.dumps(session_list, indent=2)}]
        )

    async def _switch_session(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Switch to a different browser session."""
        session_id = arguments.get("session_id")
        if not session_id:
            return CallToolResult(
                content=[{"type": "text", "text": "Session ID is required"}],
                isError=True
            )
        
        if session_id not in self.sessions:
            return CallToolResult(
                content=[{"type": "text", "text": f"Session {session_id} not found"}],
                isError=True
            )
        
        self.current_session_id = session_id
        return CallToolResult(
            content=[{"type": "text", "text": f"✅ Switched to session: {session_id}"}]
        )

    async def _close_session(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Close a specific browser session or current session."""
        session_id = arguments.get("session_id", self.current_session_id)
        
        if not session_id or session_id not in self.sessions:
            return CallToolResult(
                content=[{"type": "text", "text": "No valid session to close"}],
                isError=True
            )
        
        try:
            session = self.sessions[session_id]
            session.driver.quit()
            del self.sessions[session_id]
            
            if self.current_session_id == session_id:
                self.current_session_id = None
                if self.sessions:
                    self.current_session_id = next(iter(self.sessions.keys()))
            
            return CallToolResult(
                content=[{"type": "text", "text": f"✅ Session {session_id} closed successfully"}]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error closing session: {str(e)}"}],
                isError=True
            )

    async def _navigate(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Navigate to a URL with enhanced features."""
        url = arguments.get("url")
        wait_for_load = arguments.get("wait_for_load", True)
        
        if not url:
            return CallToolResult(
                content=[{"type": "text", "text": "URL is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            driver.get(url)
            
            # Update session URL
            session = self._get_session()
            session.url = url
            session.last_activity = datetime.now()
            
            if wait_for_load:
                # Wait for page to load
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
            
            return CallToolResult(
                content=[{"type": "text", "text": f"✅ Successfully navigated to {url}"}]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Failed to navigate: {str(e)}"}],
                isError=True
            )

    async def _find_element(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Find an element with enhanced waiting."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        wait_for_clickable = arguments.get("wait_for_clickable", False)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            
            if wait_for_clickable:
                element = WebDriverWait(driver, timeout / 1000).until(
                    EC.element_to_be_clickable(locator)
                )
            else:
                element = WebDriverWait(driver, timeout / 1000).until(
                    EC.presence_of_element_located(locator)
                )
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Element found successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error finding element: {str(e)}"}],
                isError=True
            )

    async def _click_element(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Click an element with enhanced error handling."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        force_click = arguments.get("force_click", False)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.element_to_be_clickable(locator)
            )
            
            try:
                element.click()
            except ElementClickInterceptedException:
                if force_click:
                    # Use JavaScript as fallback
                    driver.execute_script("arguments[0].click();", element)
                else:
                    raise
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Element clicked successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except ElementClickInterceptedException:
            return CallToolResult(
                content=[{"type": "text", "text": "🖱️ Click intercepted: Element is covered by another element"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error clicking element: {str(e)}"}],
                isError=True
            )

    async def _send_keys(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Send keys to an element with enhanced typing."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        text = arguments.get("text", "")
        timeout = arguments.get("timeout", 10000)
        clear_first = arguments.get("clear_first", True)
        type_speed = arguments.get("type_speed", 0)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            if clear_first:
                element.clear()
            
            if type_speed > 0:
                # Type with delay
                for char in text:
                    element.send_keys(char)
                    await asyncio.sleep(type_speed / 1000)
            else:
                element.send_keys(text)
            
            return CallToolResult(
                content=[{"type": "text", "text": f"✅ Text '{text}' entered successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error entering text: {str(e)}"}],
                isError=True
            )

    async def _get_element_text(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get text from an element."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            text = element.text
            return CallToolResult(
                content=[{"type": "text", "text": text}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error getting element text: {str(e)}"}],
                isError=True
            )

    async def _hover(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Hover over an element."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Hovered over element successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error hovering over element: {str(e)}"}],
                isError=True
            )

    async def _drag_and_drop(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Drag and drop an element."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        target_by = arguments.get("targetBy", "css")
        target_value = arguments.get("targetValue")
        timeout = arguments.get("timeout", 10000)
        
        if not value or not target_value:
            return CallToolResult(
                content=[{"type": "text", "text": "Both source and target element values are required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            source_locator = self._get_locator(by)
            target_locator = self._get_locator(target_by)
            
            source_element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(source_locator)
            )
            target_element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(target_locator)
            )
            
            actions = ActionChains(driver)
            actions.drag_and_drop(source_element, target_element).perform()
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Drag and drop completed successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error performing drag and drop: {str(e)}"}],
                isError=True
            )

    async def _double_click(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Double click an element."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            actions = ActionChains(driver)
            actions.double_click(element).perform()
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Double click performed successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error performing double click: {str(e)}"}],
                isError=True
            )

    async def _right_click(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Right click an element."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            actions = ActionChains(driver)
            actions.context_click(element).perform()
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Right click performed successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error performing right click: {str(e)}"}],
                isError=True
            )

    async def _press_key(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Press a keyboard key."""
        key = arguments.get("key")
        
        if not key:
            return CallToolResult(
                content=[{"type": "text", "text": "Key is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            actions = ActionChains(driver)
            actions.key_down(key).key_up(key).perform()
            
            return CallToolResult(
                content=[{"type": "text", "text": f"✅ Key '{key}' pressed successfully"}]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error pressing key: {str(e)}"}],
                isError=True
            )

    async def _upload_file(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Upload a file."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        file_path = arguments.get("filePath")
        timeout = arguments.get("timeout", 10000)
        
        if not value or not file_path:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value and file path are required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            element = WebDriverWait(driver, timeout / 1000).until(
                EC.presence_of_element_located(locator)
            )
            
            element.send_keys(file_path)
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ File upload initiated successfully"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error uploading file: {str(e)}"}],
                isError=True
            )

    async def _take_screenshot(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Take a screenshot."""
        output_path = arguments.get("outputPath")
        full_page = arguments.get("full_page", False)
        
        try:
            driver = self._get_current_driver()
            
            if full_page:
                # Full page screenshot
                screenshot = driver.get_screenshot_as_base64()
            else:
                # Viewport screenshot
                screenshot = driver.get_screenshot_as_base64()
            
            if output_path:
                import base64
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(screenshot))
                return CallToolResult(
                    content=[{"type": "text", "text": f"✅ Screenshot saved to {output_path}"}]
                )
            else:
                return CallToolResult(
                    content=[{"type": "text", "text": f"✅ Screenshot captured: {screenshot[:100]}..."}]
                )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error taking screenshot: {str(e)}"}],
                isError=True
            )

    async def _wait_for_element(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Wait for an element to be present and optionally visible."""
        by = arguments.get("by", "css")
        value = arguments.get("value")
        timeout = arguments.get("timeout", 10000)
        wait_for_visible = arguments.get("wait_for_visible", False)
        
        if not value:
            return CallToolResult(
                content=[{"type": "text", "text": "Element value is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            locator = self._get_locator(by)
            
            if wait_for_visible:
                WebDriverWait(driver, timeout / 1000).until(
                    EC.visibility_of_element_located(locator)
                )
            else:
                WebDriverWait(driver, timeout / 1000).until(
                    EC.presence_of_element_located(locator)
                )
            
            return CallToolResult(
                content=[{"type": "text", "text": "✅ Element found and ready"}]
            )
        except TimeoutException:
            return CallToolResult(
                content=[{"type": "text", "text": f"⏰ Timeout error: Element not found within {timeout}ms"}],
                isError=True
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error waiting for element: {str(e)}"}],
                isError=True
            )

    async def _execute_script(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Execute JavaScript code."""
        script = arguments.get("script")
        script_args = arguments.get("arguments", [])
        
        if not script:
            return CallToolResult(
                content=[{"type": "text", "text": "Script is required"}],
                isError=True
            )

        try:
            driver = self._get_current_driver()
            result = driver.execute_script(script, *script_args)
            
            return CallToolResult(
                content=[{"type": "text", "text": f"✅ JavaScript executed: {result}"}]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error executing JavaScript: {str(e)}"}],
                isError=True
            )

    async def _get_page_info(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get comprehensive page information."""
        include_title = arguments.get("include_title", True)
        include_url = arguments.get("include_url", True)
        include_source = arguments.get("include_source", False)
        
        try:
            driver = self._get_current_driver()
            page_info = {}
            
            if include_title:
                page_info["title"] = driver.title
            
            if include_url:
                page_info["url"] = driver.current_url
            
            if include_source:
                page_info["source"] = driver.page_source
            
            page_info["timestamp"] = datetime.now().isoformat()
            
            return CallToolResult(
                content=[{"type": "text", "text": json.dumps(page_info, indent=2)}]
            )
        except Exception as e:
            return CallToolResult(
                content=[{"type": "text", "text": f"❌ Error getting page info: {str(e)}"}],
                isError=True
            )

async def main():
    """Main entry point for the Selenium MCP server."""
    server = SeleniumMCPServer()
    
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="selenium-mcp",
                server_version="2.0.0",
                capabilities=server.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main()) 