import asyncio
import json
import logging
import uuid
from typing import Any, Dict

logger = logging.getLogger(__name__)


class BaseServer:
    """
    Basic asynchronous chat server.

    This server only redirect messages received from a client to all other clients.

    Arguments:
        host: host or ip to run the server on
        port: port to run the server on

    !!! example

        ```python
            server = BaseServer(host='localhost', port=1234)
            server.run()
        ```
    """

    def __init__(self, host: str = 'localhost', port: int = 1234,) -> None:
        self.host: str = host
        self.port: int = port
        self.clients: Dict[str, Any] = {}

    async def send_message(self, message: str, client_id: str) -> None:
        """
        Send a message to a client.

        Arguments:
            message: message to send
            client_id: client id to send the message to (see `BaseServer.on_new_client`)
        """
        self.clients[client_id]['writer'].write(message.encode('utf8'))
        await self.clients[client_id]['writer'].drain()

    async def on_new_message(self, from_client_id: str, message: str) -> None:
        """
        Send a message to all connected clients.

        Arguments:
            from_client_id: client id defined in `BaseServer.on_new_client`
            message: message to send to all clients

        """
        logger.debug('Dispatch from %s to all: "%s"' % (from_client_id, message,))
        message = json.dumps({'from': from_client_id, 'message': message})
        for client_id, client in self.clients.items():
            logger.debug('Send message to %s: "%s"' % (client_id, message,))
            await self.send_message(
                client_id=client_id, message=message,
            )

    def register_client(self, client_writer: asyncio.streams.StreamWriter) -> str:
        """
        Register a new client in `self.clients`

        Arguments:
            client_writer: client writer object

        Returns:
            client_id as a random 4 char string.

        """
        client_id = str(uuid.uuid4())[:4]
        self.clients[client_id] = {'writer': client_writer}
        return client_id

    async def on_new_client(
        self,
        client_reader: asyncio.streams.StreamReader,
        client_writer: asyncio.streams.StreamWriter,
    ) -> None:
        """
        Register a newly connected client.

        This method

         - set an id to the client
         - register the client in `self.clients`
         - wait for client messages and dispatch them to all other clients

        Arguments:
            client_reader: reader object to read client messages from
            client_writer: writer object used to send messages to the client

        !!! tip
            if the client send `:q` as a message, it will be disconnected.

        """
        logger.debug('New client connected.')
        client_id = self.register_client(client_writer=client_writer)
        while True:
            new_message = (await client_reader.read(255)).decode()
            logger.debug('New message received: %s' % new_message)
            if not new_message or new_message == ':q':
                logger.info('Disconnect client %s' % client_id)
                break
            await self.on_new_message(from_client_id=client_id, message=new_message)
        client_writer.close()
        del self.clients[client_id]
        logger.info('Nb connected clients: %s' % len(self.clients.keys()))

    def run(self) -> None:
        """
        Run client by starting an event loop that listen to user input and
        server messages.
        """
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(
                asyncio.start_server(
                    client_connected_cb=self.on_new_client,
                    host=self.host,
                    port=self.port,
                    loop=loop,
                )
            )
            loop.run_forever()
        except KeyboardInterrupt:
            logger.warning('Server closed manually')
        finally:
            logger.info('Close connection to all clients')
            for client_id, client in self.clients.items():
                client['writer'].close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = BaseServer(host='localhost', port=1234)
    server.run()
