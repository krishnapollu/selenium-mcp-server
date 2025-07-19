# Publishing to PyPI Guide

This guide explains how to publish the selenium-mcp-server package to PyPI so it can be installed by general users.

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/
2. **TestPyPI Account**: Create an account at https://test.pypi.org/ (for testing)
3. **API Token**: Generate an API token in your PyPI account settings

## Step 1: Test on TestPyPI

First, test the package on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ selenium-mcp-server
```

## Step 2: Publish to PyPI

Once tested, publish to the main PyPI:

```bash
# Upload to PyPI
python -m twine upload dist/*
```

## Step 3: Verify Installation

Test that users can install the package:

```bash
# Install from PyPI
pip install selenium-mcp-server

# Test the module
python -c "import selenium_mcp_server; print('✅ Success!')"
```

## Configuration for Users

After publishing, users can use this configuration:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "pip", "install", "--user", "selenium-mcp-server", "&&", "python", "-m", "selenium_mcp_server"]
    }
  }
}
```

## Updating the Package

To update the package:

1. Update the version in `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload: `python -m twine upload dist/*`

## Troubleshooting

- **Authentication**: Use your PyPI API token when prompted
- **Version conflicts**: Ensure version numbers are unique
- **Dependencies**: Make sure all dependencies are available on PyPI 