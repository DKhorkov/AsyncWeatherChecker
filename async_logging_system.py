import aiologger
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
from tempfile import NamedTemporaryFile


__log_file: NamedTemporaryFile = NamedTemporaryFile()
__file_handler: AsyncFileHandler = AsyncFileHandler(filename=__log_file.name)

logger: Logger = Logger.with_default_handlers(
    name='async_logger',
    level=aiologger.logger.LogLevel.DEBUG
)
logger.add_handler(__file_handler)

