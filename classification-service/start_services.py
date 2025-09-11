import click
import asyncio
import uvicorn
import subprocess

@click.command()
@click.option('--host', default='0.0.0.0', help='Host to bind the services')
@click.option('--port1', default=8001, help='Port for FastAPI service')
@click.option('--port2', default=8002, help='Port for MCP server')
def start_services(host, port1, port2):
    async def run_uvicorn():
        config = uvicorn.Config("src.api.classifier_api:app", host=host, port=port1)
        server = uvicorn.Server(config)
        return await server.serve()

    async def run_mcp_server():
        process = await asyncio.create_subprocess_exec(
            "uv", "run", "python", "-m", "src.mcp.classifier_mcp_server",
            "--host", host, "--port", str(port2)
        )
        await process.wait()

    async def main():
        await asyncio.gather(run_uvicorn(), run_mcp_server())

    asyncio.run(main())

if __name__ == "__main__":
    start_services()