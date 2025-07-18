import asyncio
from fastmcp import Client

async def main():
    async with Client("mcp_server.py") as mcp_client:
        print(await mcp_client.list_tools())


if __name__ == "__main__":
    test = asyncio.run(main())