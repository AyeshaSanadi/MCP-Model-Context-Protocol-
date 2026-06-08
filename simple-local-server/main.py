from fastmcp import FastMCP
import random 


# create a FastMCP server instance
mcp = FastMCP(name="Simple Server")

@mcp.tool
def print_name(name: str) -> str:
    """This function used to print name"""
    return f"Your name is: {name}"


@mcp.tool
def add_numbers(n1: int, n2: int) -> int:
    """This function used to add two numbers"""
    return n1 + n2


if __name__ == "__main__":
    mcp.run()
