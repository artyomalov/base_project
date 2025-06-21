from uvicorn import run
from logging import getLogger, DEBUG
from asyncio.exceptions import CancelledError

from create_app import create_app

logger = getLogger("logger")
logger.setLevel(DEBUG)


if __name__ == "__main__":
    app = create_app()

    try:
        run(
            app="main:app",
            reload=True,
            log_level="debug",
            host="0.0.0.0",
            port=8000,
        )
    except CancelledError:
        logger.log("App has been stopped")

    except KeyboardInterrupt:
        logger.log("App has been stopped now")
