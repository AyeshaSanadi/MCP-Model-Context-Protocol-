from fastmcp import FastMCP
from main import app  #importing fastapi instance

# converting fastapi app to mcp server
mcp = FastMCP.from_fastapi(
    app=app,
    name="Student Management Server",
)

if __name__ == "__main__":
    mcp.run()

