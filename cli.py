import logging

import typer
import uvicorn

app = typer.Typer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.command()
def run_api():
    from src.api import main

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",  # noqa: S104
        port=main.config.server.port,
        loop="uvloop",
        reload=main.config.server.reload,
        workers=main.config.server.workers,
        root_path=main.config.server.root_path,
        use_colors=True,
    )


@app.command()
def run_consumer():
    from src.consumer import main

    uvicorn.run(main.application, use_colors=True, lifespan="on")


if __name__ == "__main__":
    app()
