# MCP Configuration Guide

This guide shows you how to configure the Selenium MCP Server with different MCP clients.

## Quick Setup (Recommended)

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Use the simple configuration:**
   
   Copy `config/mcp_client_config.json` to your MCP client's configuration location, or use:
   
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

## Configuration Options

### Option 1: Installed Package (Recommended)

If you've installed the package with `pip install -e .`:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Option 2: Direct File Execution

For direct file execution, use absolute paths:

**Windows:**
```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["C:\\path\\to\\selenium-mcp-server\\src\\selenium_mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\selenium-mcp-server\\src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["/path/to/selenium-mcp-server/src/selenium_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/selenium-mcp-server/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Option 3: Console Script

If the package is installed, you can use the console script:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "selenium-mcp-server"
    }
  }
}
```

## Client-Specific Configuration

### MCP Clients (Cursor AI, Claude Desktop, etc.)

Copy the configuration from `config/mcp_client_config.json` to your MCP client's config file:

**Claude Desktop:** `~/.config/claude-desktop/config.json` (Linux/macOS) or `%APPDATA%\claude-desktop\config.json` (Windows)
**Cursor AI:** `~/.cursor/mcp_config.json` or your Cursor AI MCP configuration location
**Other MCP Clients:** Check your client's documentation for the config file location

### Installation and Setup

1. **Install the package:**
   ```bash
   pip install -e .
   ```

2. **Use the generic configuration:**
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

### Troubleshooting "0 Tools Enabled"

If you're seeing "0 tools enabled" in Cursor AI:

1. **Make sure the package is installed:**
   ```bash
   pip install -e .
   ```

2. **Verify the module works:**
   ```bash
   python -c "import selenium_mcp_server; print('Module found!')"
   ```

3. **Check if the entry point works:**
   ```bash
   selenium-mcp-server --help
   ```

4. **Alternative: Use the console script entry point:**
   ```json
   {
     "mcpServers": {
       "selenium": {
         "command": "selenium-mcp-server"
       }
     }
   }
   ```



## Environment Variables

- `PYTHONUNBUFFERED=1`: Ensures Python output is not buffered
- `SELENIUM_LOG_LEVEL=INFO`: Sets logging level (DEBUG, INFO, WARNING, ERROR)
- `PYTHONPATH`: Points to the directory containing the Python modules

## Troubleshooting

### "Module not found" errors
- Make sure you've installed the package: `pip install -e .`
- Check that the `PYTHONPATH` points to the correct directory
- Verify the file paths are correct for your system

### "Command not found" errors
- Ensure Python is in your system PATH
- Try using the full path to Python: `C:\\Python312\\python.exe` (Windows) or `/usr/bin/python3` (Linux/macOS)

### Permission errors
- On Windows, try running your MCP client as administrator
- On Linux/macOS, check file permissions: `chmod +x src/selenium_mcp_server.py`

## Testing Your Configuration

After configuring, test with a simple command:

```json
{
  "name": "list_sessions",
  "arguments": {}
}
```

This should return an empty list if no sessions are active, confirming the server is working. 