# Selenium MCP Server - Generic Setup Guide

## 🚀 **Seamless Installation for Any User**

This guide provides a **generic solution** that works across all devices and users without manual installation.

## 📋 **Quick Setup (Recommended)**

### 1. **Download the Launcher**
Download these two files to your project directory:
- `mcp_launcher.py` - Automatic installer and launcher
- `mcp_config_generic.json` - MCP configuration

### 2. **Configure MCP Client**
Add this to your MCP configuration file (e.g., `mcp.json`):

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["mcp_launcher.py"]
    }
  }
}
```

### 3. **That's It!**
The launcher will automatically:
- ✅ Install `selenium-mcp-server` if not present
- ✅ Start the server with proper error handling
- ✅ Work on Windows, Mac, and Linux
- ✅ Handle different Python environments

## 🔧 **How It Works**

The `mcp_launcher.py` script:
1. **Checks** if `selenium-mcp-server` is installed
2. **Installs** the package automatically if missing
3. **Starts** the MCP server with proper async handling
4. **Handles errors** gracefully with informative messages

## 📁 **File Structure**
```
your-project/
├── mcp_launcher.py          # Automatic launcher
├── mcp_config_generic.json  # MCP configuration
└── mcp.json                 # Your MCP config (add the server config here)
```

## 🌟 **Benefits**

- **Zero Manual Installation** - Works out of the box
- **Cross-Platform** - Windows, Mac, Linux
- **Automatic Updates** - Always gets the latest version
- **Error Handling** - Clear error messages if something goes wrong
- **User-Friendly** - No technical knowledge required

## 🔍 **Troubleshooting**

If you encounter issues:

1. **Check Python Installation**: Ensure Python 3.8+ is installed
2. **Check Internet Connection**: Required for package download
3. **Check Permissions**: May need admin rights on some systems
4. **Check Logs**: Look for error messages in stderr

## 📝 **Example Usage**

Once configured, your MCP client will automatically:
- Install the latest `selenium-mcp-server` package
- Start the server with version logging
- Provide access to all Selenium automation tools

**No manual steps required!** 🎉 