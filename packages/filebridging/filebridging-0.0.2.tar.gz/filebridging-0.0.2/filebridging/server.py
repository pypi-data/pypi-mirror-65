"""Server class.

May be a local server or a publicly reachable server.

Arguments
    - host: localhost, IPv4 address or domain (e.g. www.example.com)
    - port: port to reach (must be enabled)
    - certificate [optional]: server certificate for SSL
    - key [optional]: needed only for standalone clients
"""

import argparse
import asyncio
import collections
import logging
import os
import ssl
from typing import Union


class Server:
    def __init__(self, host='localhost', port=5000, ssl_context=None,
                 buffer_chunk_size=10 ** 4, buffer_length_limit=10 ** 4):
        self._host = host
        self._port = port
        self._ssl_context = ssl_context
        self.connections = collections.OrderedDict()
        # Dict of queues of bytes
        self.buffers = collections.OrderedDict()
        # How many bytes per chunk
        self._buffer_chunk_size = buffer_chunk_size
        # How many chunks in buffer
        self._buffer_length_limit = buffer_length_limit
        self._working = False
        self._server = None
        self._ssl_context = None

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def buffer_length_limit(self) -> int:
        return self._buffer_length_limit

    @property
    def buffer_chunk_size(self) -> int:
        return self._buffer_chunk_size

    @property
    def working(self) -> bool:
        return self._working

    @property
    def server(self) -> asyncio.base_events.Server:
        return self._server

    @property
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    @property
    def buffer_is_full(self):
        return (
                sum(len(buffer)
                    for buffer in self.buffers.values())
                >= self.buffer_length_limit
        )

    def set_ssl_context(self, ssl_context: ssl.SSLContext):
        self._ssl_context = ssl_context

    async def run_reader(self, reader, connection_token):
        while 1:
            try:
                # Wait one second if buffer is full
                while self.buffer_is_full:
                    await asyncio.sleep(1)
                    continue
                input_data = await reader.read(self.buffer_chunk_size)
                if connection_token not in self.buffers:
                    break
                self.buffers[connection_token].append(input_data)
            except ConnectionResetError as e:
                logging.error(e)
                break
            except Exception as e:
                logging.error(f"Unexpected exception:\n{e}", exc_info=True)

    async def run_writer(self, writer, connection_token):
        consecutive_interruptions = 0
        errors = 0
        while connection_token in self.buffers:
            try:
                input_data = self.buffers[connection_token].popleft()
            except IndexError:
                # Slow down if buffer is empty; after 1.5 s of silence, break
                consecutive_interruptions += 1
                if consecutive_interruptions > 3:
                    break
                await asyncio.sleep(.5)
                continue
            else:
                consecutive_interruptions = 0
            if not input_data:
                break
            try:
                writer.write(input_data)
                await writer.drain()
            except ConnectionResetError as e:
                logging.error(e)
                break
            except Exception as e:
                logging.error(e, exc_info=True)
                errors += 1
                if errors > 3:
                    break
                await asyncio.sleep(0.5)
        writer.close()

    async def connect(self,
                      reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter):
        """Connect with client.

        Decide whether client is sender or receiver and start transmission.
        """
        client_hello = await reader.readline()
        client_hello = client_hello.decode('utf-8').strip('\n').split('|')
        if len(client_hello) != 4:
            await self.refuse_connection(writer=writer,
                                         message="Invalid client_hello!")
            return
        connection_token = client_hello[1]
        if connection_token not in self.connections:
            self.connections[connection_token] = dict(
                sender=False,
                receiver=False
            )

        async def _write(message: Union[list, str, bytes],
                         terminate_line=True) -> int:
            # Adapt
            if type(message) is list:
                message = '|'.join(map(str, message))
            if type(message) is str:
                if terminate_line:
                    message += '\n'
                message = message.encode('utf-8')
            if type(message) is not bytes:
                return 1
            try:
                writer.write(message)
                await writer.drain()
            except ConnectionResetError:
                logging.error("Client disconnected.")
            except Exception as e:
                logging.error(f"Unexpected exception:\n{e}", exc_info=True)
            else:
                return 0  # On success, return 0
            # On exception, disconnect and return 1
            self.disconnect(connection_token=connection_token)
            return 1

        if client_hello[0] == 's':  # Sender client connection
            if self.connections[connection_token]['sender']:
                await self.refuse_connection(
                    writer=writer,
                    message="Invalid token! "
                            "A sender client is already connected!\n"
                )
                return
            self.connections[connection_token]['sender'] = True
            self.connections[connection_token]['file_name'] = client_hello[2]
            self.connections[connection_token]['file_size'] = client_hello[3]
            self.buffers[connection_token] = collections.deque()
            logging.info("Sender is connecting...")
            index, step = 0, 1
            while not self.connections[connection_token]['receiver']:
                index += 1
                if index >= step:
                    if await _write("Waiting for receiver..."):
                        return
                    step += 1
                    index = 0
                await asyncio.sleep(.5)
            # Send start signal to client
            if await _write("start!"):
                return
            logging.info("Incoming transmission starting...")
            await self.run_reader(reader=reader,
                                  connection_token=connection_token)
            logging.info("Incoming transmission ended")
        elif client_hello[0] == 'r':  # Receiver client connection
            if self.connections[connection_token]['receiver']:
                await self.refuse_connection(
                    writer=writer,
                    message="Invalid token! "
                            "A receiver client is already connected!\n"
                )
                return
            self.connections[connection_token]['receiver'] = True
            logging.info("Receiver is connecting...")
            index, step = 0, 1
            while not self.connections[connection_token]['sender']:
                index += 1
                if index >= step:
                    if await _write("Waiting for sender..."):
                        return
                    step += 1
                    index = 0
                await asyncio.sleep(.5)
            # Send file information and start signal to client
            if await _write(
                    ['s',
                     'hidden_token',
                     self.connections[connection_token]['file_name'],
                     self.connections[connection_token]['file_size']]
            ):
                return
            if await _write("start!"):
                return
            await self.run_writer(writer=writer,
                                  connection_token=connection_token)
            logging.info("Outgoing transmission ended")
            self.disconnect(connection_token=connection_token)
        else:
            await self.refuse_connection(writer=writer,
                                         message="Invalid client_hello!")
            return

    def disconnect(self, connection_token: str) -> None:
        del self.buffers[connection_token]
        del self.connections[connection_token]

    def run(self):
        loop = asyncio.get_event_loop()
        logging.info("Starting file bridging server...")
        try:
            loop.run_until_complete(self.run_server())
        except KeyboardInterrupt:
            print()
            logging.info("Stopping...")
            # Cancel connection tasks (they should be done but are pending)
            for task in asyncio.all_tasks(loop):
                task.cancel()
            loop.run_until_complete(
                self.server.wait_closed()
            )
        loop.close()
        logging.info("Stopped.")

    async def run_server(self):
        self._server = await asyncio.start_server(
            ssl=self.ssl_context,
            client_connected_cb=self.connect,
            host=self.host,
            port=self.port,
        )
        async with self.server:
            logging.info("Running at `{s.host}:{s.port}`".format(s=self))
            await self.server.serve_forever()

    @staticmethod
    async def refuse_connection(writer: asyncio.StreamWriter,
                                message: str = None):
        """Send a `message` via writer and close it."""
        if message is None:
            message = "Connection refused!\n"
        writer.write(
            message.encode('utf-8')
        )
        await writer.drain()
        writer.close()


def main():
    # noinspection SpellCheckingInspection
    log_formatter = logging.Formatter(
        "%(asctime)s [%(module)-15s %(levelname)-8s]     %(message)s",
        style='%'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # noinspection PyUnresolvedReferences
    asyncio.selector_events.logger.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)

    # Parse command-line arguments
    cli_parser = argparse.ArgumentParser(description='Run server',
                                         allow_abbrev=False)
    cli_parser.add_argument('--host', type=str,
                            default=None,
                            required=False,
                            help='server address')
    cli_parser.add_argument('--port', type=int,
                            default=None,
                            required=False,
                            help='server port')
    cli_parser.add_argument('--certificate', type=str,
                            default=None,
                            required=False,
                            help='server SSL certificate')
    cli_parser.add_argument('--key', type=str,
                            default=None,
                            required=False,
                            help='server SSL key')
    args = vars(cli_parser.parse_args())
    host = args['host']
    port = args['port']
    certificate = args['certificate']
    key = args['key']

    # If host and port are not provided from command-line, try to import them
    if host is None:
        try:
            from config import host
        except ImportError:
            host = None
    if port is None:
        try:
            from config import port
        except ImportError:
            port = None

    # If import fails, prompt user for host or port
    while host is None:
        host = input("Enter host:\t\t\t\t\t\t")
    while port is None:
        try:
            port = int(input("Enter port:\t\t\t\t\t\t"))
        except ValueError:
            logging.info("Invalid port. Enter a valid port number!")
            port = None

    try:
        if certificate is None or not os.path.isfile(certificate):
            from config import certificate
        if key is None or not os.path.isfile(key):
            from config import key
        if not os.path.isfile(certificate):
            certificate = None
        if not os.path.isfile(key):
            key = None
    except ImportError:
        certificate = None
        key = None
    ssl_context = None
    if certificate and key:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certificate, key)
    else:
        logging.warning(
            "Please consider using SSL. To do so, add in `config.py` or "
            "provide via Command Line Interface the path to a valid SSL "
            "key and certificate. Example:\n\n"
            "key = 'path/to/secret.key'\n"
            "certificate = 'path/to/certificate.crt'"
        )
    server = Server(
        host=host,
        port=port,
        ssl_context=ssl_context
    )
    server.run()


if __name__ == '__main__':
    main()
