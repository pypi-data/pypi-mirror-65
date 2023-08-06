import asyncio
import json
import logging
from typing import Any, Dict, Optional

from aioconsole import ainput

from piteau.exceptions import handle_exception

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Chat client handling message emission and reception

    Arguments:
        server_host: ip address of remote server
        server_port: port of remote server

    !!! example

        ```python
            client = Client(
                server_host='localhost',
                server_port=1234,
            )
            client.run()
        ```


    """

    def __init__(
        self, server_host: str = 'localhost', server_port: int = 1234,
    ) -> None:
        self.server_host = server_host
        self.server_port = server_port

        # init event loop
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.loop.set_exception_handler(handle_exception)

        # init writer and reader
        self.writer: Optional[asyncio.streams.StreamWriter] = None
        self.reader: Optional[asyncio.streams.StreamReader] = None

    def send_message(self, message: str) -> None:
        """
        Send message to server

        Arguments:
            message: to send to server

        """
        if not self.writer:
            raise ConnectionAbortedError('Client has no active writer')

        self.writer.write(message.encode('utf8'))

    async def wait_for_message(self) -> None:
        """
        Listen for user input and send input to server.
        """
        logger.debug('wait for user input')
        while True:
            message = await ainput('>>>')
            if message:
                if message == ':q':
                    self.send_message(message)
                    break
                else:
                    logger.debug('send %s to server' % message)
                    self.send_message(message)

    async def on_new_message(self, data: Dict[str, Any]) -> None:
        """
        Handle a new message received by server.
        This method simply prints it with a `<<<` prefix.

        Arguments:
            data: dictionary containing `from` (=sender id) and `message` keys
        """
        print(f'<<< {data["from"]} > {data["message"]}')

    async def receive_messages(self) -> None:
        """
        Listen messages one by one received from server.

        !!! note
            after decoding, messages received are json with the following format:
            ```json
                {
                    "from": str, // sender id
                    "message": str, // message
                }
            ```

        For each message, this method decodes the received json and "fire and forget"
        a task with `self.on_new_message()` method.
        """
        while True:
            if not self.reader:
                raise ConnectionAbortedError('No socket reader')
            # message received one by one because server add \n after every message
            data = await self.reader.readline()
            if not data:
                logger.warning('Empty message received from server')
                raise ConnectionAbortedError('Empty message received from server')
            logger.debug('Message received from server %s' % data.decode())
            asyncio.ensure_future(self.on_new_message(data=json.loads(data.decode())))

    def close(self) -> None:
        """Close sever connection and interrupt client."""
        logger.info('Close client writer')
        if self.writer:
            self.writer.close()

    async def start(self) -> None:
        """
        Start server connection

        Raise:
            ConnectionRefusedError: if connection to server failed

        """
        logger.debug('Register the open socket to wait for data')
        try:
            self.reader, self.writer = await asyncio.open_connection(
                host=self.server_host, port=self.server_port,
            )
        except OSError:
            raise ConnectionRefusedError('Impossible to find server')

    def run(self) -> None:
        """
        Run client by starting an event loop that listen to user input and
        server messages.
        """
        try:
            self.loop.run_until_complete(self.start())
            self.loop.create_task(self.wait_for_message())
            self.loop.create_task(self.receive_messages())
            self.loop.run_forever()

        except KeyboardInterrupt:
            logger.warning('Client closed manually by user')
        # exceptions raised by tasks are handled in handle_exception
        except Exception as e:
            logger.error('Uncatched exception %s' % e)
        finally:
            logger.info('Close client')
            self.close()
            logger.debug('Close loop')
            self.loop.close()


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    client = BaseClient(server_host='localhost', server_port=1234)
    client.run()
