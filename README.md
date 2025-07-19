# Selenium MCP Server

[![CI](https://github.com/krishnapollu/selenium-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/krishnapollu/selenium-mcp-server/actions/workflows/ci.yml)

A powerful Model Context Protocol (MCP) server that brings Selenium WebDriver automation to AI assistants. This server enables AI tools like Claude Desktop to control web browsers programmatically, making web automation accessible through natural language commands.

## What This Does

Ever wanted to tell an AI assistant to "go to Google, search for something, and take a screenshot"? This MCP server makes that possible. It provides a bridge between AI assistants and web browsers, allowing for sophisticated web automation workflows.

## Key Features

### 🚀 **Multiple Browser Sessions**
Run multiple browsers simultaneously - perfect for comparing different websites or handling complex workflows that require multiple browser instances.

### 🎯 **Smart Element Interaction**
- Find and interact with elements using various locator strategies
- Enhanced waiting mechanisms that actually work
- Force click with JavaScript fallback when normal clicks fail
- Type text with configurable speed (useful for avoiding detection)

### ⚡ **JavaScript Execution**
Execute custom JavaScript code directly in the browser - great for advanced interactions, data extraction, or custom automation logic.

### 📸 **Screenshot & File Operations**
Take screenshots (including full-page captures) and upload files with ease.

### 🛡️ **Robust Error Handling**
Specific error messages that actually help you debug issues, rather than generic failures.

### 📊 **Session Management**
List, switch between, and manage multiple browser sessions with detailed metadata tracking.

## Quick Start

### 1. Install the Package

```bash
pip install -e .
```

The server uses `webdriver-manager` to automatically handle browser drivers, so you don't need to manually download ChromeDriver or GeckoDriver.

### 2. Configure Your MCP Client

#### For General Users (Recommended)

**Option 1: Simple Configuration (if package is already installed)**
```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"]
    }
  }
}
```

**Option 2: Windows with Auto-Installation**
```json
{
  "mcpServers": {
    "selenium": {
      "command": "powershell",
      "args": ["-Command", "pip install --user selenium-mcp-server; python -m selenium_mcp_server"]
    }
  }
}
```

**Option 3: Linux/Mac with Auto-Installation**
```json
{
  "mcpServers": {
    "selenium": {
      "command": "bash",
      "args": ["-c", "pip install --user selenium-mcp-server && python -m selenium_mcp_server"]
    }
  }
}
```

#### For Developers (Local Installation)

If you have the code locally:

**Configuration Locations:**
- **Cursor AI:** `%USERPROFILE%\.cursor\mcp_config.json` (Windows)
- **Claude Desktop:** `%APPDATA%\claude-desktop\config.json` (Windows)
- **Other MCP Clients:** Check your client's documentation

### 3. Test the Server

```bash
# For general users
pip install selenium-mcp-server
python -m selenium_mcp_server

# For developers
python -m selenium_mcp_server
```

**Note**: 
- The package is now available on PyPI for easy installation
- Works on any machine with Python installed
- No need to download or clone the repository
- Ready-to-use configuration files in `config/` directory

## Available Tools

### Browser Management

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `start_browser` | Launch a new browser session | `browser`, `options`, `session_name` |
| `list_sessions` | Show all active sessions | None |
| `switch_session` | Switch to a different session | `session_id` |
| `close_session` | Close a specific session | `session_id` (optional) |

### Navigation & Page Info

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `navigate` | Go to a URL | `url`, `wait_for_load` |
| `get_page_info` | Get page details | `include_title`, `include_url`, `include_source` |

### Element Interaction

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `find_element` | Find an element | `by`, `value`, `timeout`, `wait_for_clickable` |
| `click_element` | Click an element | `by`, `value`, `timeout`, `force_click` |
| `send_keys` | Type text | `by`, `value`, `text`, `clear_first`, `type_speed` |
| `get_element_text` | Get element text | `by`, `value`, `timeout` |
| `wait_for_element` | Wait for element | `by`, `value`, `timeout`, `wait_for_visible` |

### Advanced Actions

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `hover` | Hover over element | `by`, `value`, `timeout` |
| `drag_and_drop` | Drag and drop | `by`, `value`, `targetBy`, `targetValue` |
| `double_click` | Double click | `by`, `value`, `timeout` |
| `right_click` | Right click | `by`, `value`, `timeout` |
| `press_key` | Press keyboard key | `key` |
| `execute_script` | Run JavaScript | `script`, `arguments` |

### File Operations

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `upload_file` | Upload a file | `by`, `value`, `filePath`, `timeout` |
| `take_screenshot` | Take screenshot | `outputPath`, `full_page` |

## Real-World Examples

### Example 1: Google Search Automation

```json
[
  {
    "name": "start_browser",
    "arguments": {
      "browser": "chrome",
      "options": {"headless": false},
      "session_name": "search_session"
    }
  },
  {
    "name": "navigate",
    "arguments": {
      "url": "https://www.google.com",
      "wait_for_load": true
    }
  },
  {
    "name": "send_keys",
    "arguments": {
      "by": "name",
      "value": "q",
      "text": "Selenium automation tutorial",
      "clear_first": true
    }
  },
  {
    "name": "press_key",
    "arguments": {"key": "Enter"}
  },
  {
    "name": "take_screenshot",
    "arguments": {
      "outputPath": "search_results.png",
      "full_page": true
    }
  }
]
```

### Example 2: Multi-Session Workflow

```json
[
  {
    "name": "start_browser",
    "arguments": {
      "browser": "chrome",
      "session_name": "main"
    }
  },
  {
    "name": "start_browser",
    "arguments": {
      "browser": "firefox",
      "options": {"headless": true},
      "session_name": "background"
    }
  },
  {
    "name": "list_sessions",
    "arguments": {}
  }
]
```

### Example 3: JavaScript Data Extraction

```json
[
  {
    "name": "navigate",
    "arguments": {"url": "https://example.com"}
  },
  {
    "name": "execute_script",
    "arguments": {
      "script": "return Array.from(document.querySelectorAll('h1, h2, h3')).map(h => h.textContent);"
    }
  }
]
```

## Locator Strategies

The server supports all standard Selenium locator strategies:

- **`id`**: Find by element ID (fastest)
- **`css`**: Find by CSS selector (most flexible)
- **`xpath`**: Find by XPath (most powerful)
- **`name`**: Find by name attribute
- **`tag`**: Find by tag name
- **`class`**: Find by class name

## Error Handling

The server provides meaningful error messages instead of generic failures:

- **⏰ Timeout errors**: When elements don't appear within the specified time
- **🔍 Element not found**: When locators don't match any elements
- **🖱️ Click intercepted**: When elements are covered by other elements
- **🚫 Session errors**: When browser startup fails

## Common Use Cases

### Web Scraping
Use `execute_script` to extract data from complex pages, or `get_element_text` for simple text extraction.

### Form Automation
Fill out forms with `send_keys`, handle file uploads, and submit with `click_element`.

### Testing
Take screenshots, verify element presence, and automate user workflows.

### Monitoring
Set up automated checks that navigate to pages and verify content.

## Troubleshooting

### Browser Won't Start
- Make sure Chrome or Firefox is installed
- Check that `webdriver-manager` can access the internet
- Try running with `headless: false` to see what's happening

### Elements Not Found
- Double-check your locator strategy and value
- Use browser dev tools to verify the element exists
- Try increasing the timeout value
- Use `wait_for_element` to ensure the page is fully loaded

### Permission Issues
- Ensure the script has write permissions for screenshot directories
- Use absolute paths for file uploads

### Performance Issues
- Use headless mode for faster execution
- Close unused sessions with `close_session`
- Consider using `type_speed` to avoid being detected as a bot

## Project Structure

```
selenium-mcp-server/
├── src/                    # Source code
│   ├── selenium_mcp_server.py
│   ├── main.py            # Main entry point
│   └── run_server.py      # Server runner
├── scripts/                # Utility scripts
│   ├── cleanup.py         # Cleanup utility
│   └── install_dependencies.py # Dependency installer
├── tests/                  # Test files
│   ├── run_tests.py       # Test runner
│   └── *.py              # Individual tests
├── docs/                   # Documentation
├── examples/               # Example usage
├── config/                 # Configuration files
├── README.md              # Main documentation
├── requirements.txt       # Dependencies
├── setup.py               # Package setup
└── .gitignore             # Git exclusions
```

## Development

### Running Tests
```bash
# Use the test runner (recommended)
python tests/run_tests.py

# Or run individual tests
python tests/interactive_test.py
python tests/test_browser_management.py
python tests/test_error_handling.py
python tests/test_selenium_mcp.py
```

### Utility Scripts
```bash
# Install dependencies
python scripts/install_dependencies.py

# Clean up project
python scripts/cleanup.py
```

### Continuous Integration

This project includes GitHub Actions CI that automatically runs tests on every push and pull request. The CI workflow:

- ✅ Tests server initialization
- ✅ Tests basic browser functionality
- ✅ Tests error handling
- ✅ Checks Python syntax
- ✅ Tests package installation
- ✅ Runs on Ubuntu with Chrome and Firefox

See `.github/workflows/ci.yml` for details.

### Debug Mode
Enable detailed logging by modifying the logging level in the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Found a bug? Have an idea for a new feature? Feel free to open an issue or submit a pull request. This project is actively maintained and welcomes contributions.

## License

MIT License - feel free to use this in your own projects.

---

**Note**: This server is designed for legitimate automation tasks. Please respect websites' terms of service and robots.txt files when using this tool. 