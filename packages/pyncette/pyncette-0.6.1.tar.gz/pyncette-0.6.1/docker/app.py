import logging

from prometheus_client import start_http_server

from pyncette import Context
from pyncette import FailureMode
from pyncette import Pyncette
from pyncette.prometheus import prometheus_middleware
from pyncette.prometheus import prometheus_repository
from pyncette.sqlite import sqlite_repository

logger = logging.getLogger(__name__)

app = Pyncette(
    sqlite_database="pyncette.db",
    repository_factory=prometheus_repository(sqlite_repository),
)
app.middleware(prometheus_middleware)


@app.task(schedule="* * * * * */2")
async def hello_world(context: Context):
    logger.info("Hello, world!")


if __name__ == "__main__":
    start_http_server(port=9699, addr="0.0.0.0")
    app.main()
