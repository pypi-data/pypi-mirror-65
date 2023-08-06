import asyncio
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def handle_exception(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    print(context)
    exception = context.get('exception')
    logging.error(f'Exception raised: {context["message"]}')

    if type(exception) == ConnectionAbortedError:
        logger.error('Connection aborted')

    # cancel all running tasks
    logger.debug('Close all loop tasks')
    for task in asyncio.Task.all_tasks():
        logger.debug('Close task %s' % task)
        task.cancel()

    # close loop
    loop.stop()
