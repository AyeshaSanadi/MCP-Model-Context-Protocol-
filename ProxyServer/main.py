from fastmcp import FastMCP

# it required authentication and it is paid
mcp = FastMCP.as_proxy("https://neighbouring-lavender-mole.fastmcp.app/mcp", name="remote_mcp_server_proxy")

if __name__ == "__main__":
    mcp.run()
