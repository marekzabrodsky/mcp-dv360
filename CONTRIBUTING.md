# 🤝 Contributing to DV360 MCP Server

Thank you for your interest in contributing to the DV360 MCP Server! This guide will help you get started.

## 📋 Prerequisites

- Python 3.10 or higher
- Google Cloud Platform account with DV360 API access
- Service Account credentials for testing
- Familiarity with MCP (Model Context Protocol)

## 🛠️ Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/marekzabrodsky/mcp-dv360.git
cd mcp-dv360
pip install -r requirements.txt
```

### 2. Configure Test Credentials

```bash
# Copy your service account key
cp /path/to/your/credentials.json ~/.config/dv360/test-credentials.json

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="~/.config/dv360/test-credentials.json"
```

### 3. Run Tests

```bash
# Test basic functionality
python3 test_server.py

# Test with real credentials
python3 test_real_credentials.py

# Full system verification
python3 final_verification.py
```

## 🧪 Testing Your Changes

### Unit Tests
```bash
# Test individual components
python3 -m pytest tests/ -v
```

### Integration Tests
```bash
# Test MCP server functionality
python3 test_mcp_startup.py

# Test DV360 API integration
python3 test_dv360_data.py
```

### End-to-End Testing
```bash
# Complete system test
python3 final_verification.py
```

## 📁 Project Structure

```
src/dv360_mcp_server/
├── server.py          # Main MCP server implementation
├── dv360_client.py    # DV360 API client
├── config.py          # Configuration management
└── __init__.py

tests/                  # Test files
docs/                   # Documentation
requirements.txt        # Python dependencies
```

## 🔧 Adding New Features

### 1. DV360 API Functions

Add new functions to `src/dv360_mcp_server/dv360_client.py`:

```python
async def your_new_function(self, parameter):
    """Your function description."""
    try:
        # Implementation
        return result
    except Exception as e:
        logger.error(f"Error in your_new_function: {e}")
        raise
```

### 2. MCP Tools

Add new tools to `src/dv360_mcp_server/server.py`:

```python
Tool(
    name="your_tool_name",
    description="What your tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "parameter": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["parameter"]
    }
)
```

### 3. MCP Resources

Add new resources for data access:

```python
Resource(
    uri="dv360://your-resource",
    name="Your Resource",
    description="Resource description",
    mimeType="application/json"
)
```

## 📝 Code Style

- Follow PEP 8 formatting
- Use type hints where appropriate
- Add docstrings to all functions
- Include error handling and logging
- Keep functions focused and testable

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description:** Clear description of the issue
2. **Steps to reproduce:** Exact steps that trigger the bug
3. **Expected behavior:** What should happen
4. **Actual behavior:** What actually happens
5. **Environment:** Python version, OS, DV360 account details
6. **Logs:** Relevant error messages or logs

## ✨ Feature Requests

For new features, please include:

1. **Use case:** Why is this feature needed?
2. **Description:** What should the feature do?
3. **API impact:** How would it affect the current API?
4. **Implementation ideas:** Any thoughts on implementation

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Make** your changes with tests
4. **Test** thoroughly with `final_verification.py`
5. **Commit** with clear messages
6. **Push** to your fork
7. **Create** a Pull Request

### Pull Request Checklist

- [ ] Tests pass locally
- [ ] New features have tests
- [ ] Documentation updated
- [ ] No sensitive data in commits
- [ ] Clear commit messages
- [ ] Ready for review

## 📞 Getting Help

- **Issues:** [GitHub Issues](https://github.com/marekzabrodsky/mcp-dv360/issues)
- **Discussions:** Use GitHub Discussions for questions
- **Documentation:** Check existing docs first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for helping make DV360 MCP Server better! 🎉