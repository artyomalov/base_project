from uvicorn import run
from logging import getLogger, DEBUG
from asyncio.exceptions import CancelledError

from create_app import create_app

logger = getLogger("logger")
logger.setLevel(DEBUG)

app = create_app()

if __name__ == "__main__":
    try:
        run(
            app="main:app",
            reload=True,
            log_level="debug",
            host="localhost",
            port=8000,
        )
    except CancelledError:
        logger.log("App has been stopped")

    except KeyboardInterrupt:
        logger.log("App has been stopped now")
