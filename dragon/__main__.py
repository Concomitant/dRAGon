import uvicorn

from .webapi import app


def main() -> None:
    """Run the dRAGon web API using Uvicorn."""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
