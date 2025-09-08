from langchain_core.tools import tool

# Define tools exactly as shown in the example
@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a.

    Args:
        a: first int (the number to subtract from)
        b: second int (the number to subtract)
    """
    return a - b

def get_tools():
    """Get all available tools"""
    return [add, multiply, divide, subtract]

def get_tools_by_name():
    """Get tools indexed by name for easy lookup"""
    tools = get_tools()
    return {tool.name: tool for tool in tools}