"""Receiver and sender client class.

Arguments
    - host: localhost, IPv4 address or domain (e.g. www.example.com)
    - port: port to reach (must be enabled)
    - action: either [S]end or [R]eceive
    - file_path: file to send / destination folder
    - token: session token (6-10 alphanumerical characters)
    - certificate [optional]: server certificate for SSL
    - key [optional]: needed only for standalone clients
    - password [optional]: necessary to end-to-end encryption
    - standalone [optional]: allow client-to-client communication (the host
    must be reachable by both clients)
"""

import argparse
import asyncio
import collections
import logging
import os
import random
import ssl
import string
import sys
from typing import Union

from . import utilities


class Client:
    """Sender or receiver client.

    Create a Client object providing host, port and other optional parameters.
    Then, run it with `Client().run()` method
    """
    def __init__(self, host='localhost', port=5000, ssl_context=None,
                 action=None,
                 standalone=False,
                 buffer_chunk_size=10 ** 4,
                 buffer_length_limit=10 ** 4,
                 file_path=None,
                 password=None,
                 token=None):
        self._host = host
        self._port = port
        self._ssl_context = ssl_context
        self._action = action
        self._standalone = standalone
        self._stopping = False
        self._reader = None
        self._writer = None
        # Shared queue of bytes
        self.buffer = collections.deque()
        # How many bytes per chunk
        self._buffer_chunk_size = buffer_chunk_size
        # How many chunks in buffer
        self._buffer_length_limit = buffer_length_limit
        self._file_path = file_path
        self._working = False
        self._token = token
        self._password = password
        self._ssl_context = None
        self._encryption_complete = False
        self._file_name = None
        self._file_size = None
        self._file_size_string = None

    @property
    def host(self) -> str:
        """Host to reach.

        For standalone clients, you must be able to listen this host.
        """
        return self._host

    @property
    def port(self) -> int:
        """Port number."""
        return self._port

    @property
    def action(self) -> str:
        """Client role.

        Possible values:
        - `send`
        - `receive`
        """
        return self._action

    @property
    def standalone(self) -> bool:
        """Tell whether client should run as server as well."""
        return self._standalone

    @property
    def stopping(self) -> bool:
        return self._stopping

    @property
    def reader(self) -> asyncio.StreamReader:
        return self._reader

    @property
    def writer(self) -> asyncio.StreamWriter:
        return self._writer

    @property
    def buffer_length_limit(self) -> int:
        """Max number of buffer chunks in memory.

        You may want to reduce this limit to allocate less memory, or increase
        it to boost performance.
        """
        return self._buffer_length_limit

    @property
    def buffer_chunk_size(self) -> int:
        """Length (bytes) of buffer chunks in memory.

        You may want to reduce this limit to allocate less memory, or increase
        it to boost performance.
        """
        return self._buffer_chunk_size

    @property
    def file_path(self) -> str:
        """Path of file to send or destination folder."""
        return self._file_path

    @property
    def working(self) -> bool:
        return self._working

    @property
    def ssl_context(self) -> ssl.SSLContext:
        return self._ssl_context

    def set_ssl_context(self, ssl_context: ssl.SSLContext):
        self._ssl_context = ssl_context

    @property
    def token(self):
        """Session token.

        6-10 alphanumerical characters to provide to server to link sender and
        receiver.
        """
        return self._token

    @property
    def password(self):
        """Password for file encryption or decryption."""
        return self._password

    @property
    def encryption_complete(self):
        return self._encryption_complete

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_size(self):
        return self._file_size

    @property
    def file_size_string(self):
        """Formatted file size (e.g. 64.22 MB)."""
        return self._file_size_string

    async def run_client(self) -> None:
        if self.action == 'send':
            file_name = os.path.basename(os.path.abspath(self.file_path))
            file_size = os.path.getsize(os.path.abspath(self.file_path))
            # File size increases after encryption
            # "Salted_" (8 bytes) + salt (8 bytes)
            # Then, 1-16 bytes are added to make file_size a multiple of 16
            # i.e., (32 - file_size mod 16) bytes are added to original size
            if self.password:
                file_size += 32 - (file_size % 16)
            self.set_file_information(
                file_name=file_name,
                file_size=file_size
            )
        if self.standalone:
            server = await asyncio.start_server(
                ssl=self.ssl_context,
                client_connected_cb=self._connect,
                host=self.host,
                port=self.port,
            )
            async with server:
                logging.info("Running at `{s.host}:{s.port}`".format(s=self))
                await server.serve_forever()
        else:
            try:
                reader, writer = await asyncio.open_connection(
                    host=self.host,
                    port=self.port,
                    ssl=self.ssl_context
                )
            except (ConnectionRefusedError, ConnectionResetError) as exception:
                logging.error(f"Connection error: {exception}")
                return
            await self.connect(reader=reader, writer=writer)

    async def _connect(self, reader: asyncio.StreamReader,
                       writer: asyncio.StreamWriter):
        """Wrap connect method to catch exceptions.

        This is required since callbacks are never awaited and potential
        exception would be logged at loop.close().
        Only standalone clients need this wrapper, regular clients might use
        connect method directly.
        """
        try:
            return await self.connect(reader, writer)
        except KeyboardInterrupt:
            print()
        except Exception as e:
            logging.error(e)

    async def connect(self,
                      reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter):
        """Communicate with the server or the other client.

        Send information about the client (connection token, role, file name
        and size), get information from the server (file name and size), wait
        for start signal and then send or receive the file.
        """
        self._reader = reader
        self._writer = writer

        async def _write(message: Union[list, str, bytes],
                         terminate_line=True) -> int:
            """Framework for `asyncio.StreamWriter.write` method.

            Create string from list, encode it, send and drain writer.
            Return 0 on success, 1 on error.
            """
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
            # On exception, return 1
            return 1

        if self.action == 'send' or not self.standalone:
            if await _write(
                    [self.action[0], self.token,
                     self.file_name, self.file_size]
            ):
                return
        # Wait for server start signal
        while 1:
            server_hello = await self.reader.readline()
            if not server_hello:
                logging.error("Server disconnected.")
                return
            server_hello = server_hello.decode('utf-8').strip('\n').split('|')
            if self.action == 'receive' and server_hello[0] == 's':

                self.set_file_information(file_name=server_hello[2],
                                          file_size=server_hello[3])
            elif (
                    self.standalone
                    and self.action == 'send'
                    and server_hello[0] == 'r'
            ):
                # Check token
                if server_hello[1] != self.token:
                    if await _write("Invalid session token!"):
                        return
                    return
            elif server_hello[0] == 'start!':
                break
            else:
                logging.info(f"Server said: {'|'.join(server_hello)}")
            if self.standalone:
                if await _write("start!"):
                    return
                break
        if self.action == 'send':
            await self.send(writer=self.writer)
        else:
            await self.receive(reader=self.reader)

    async def encrypt_file(self, input_file, output_file):
        """Use openssl to encrypt the input_file.

        The encrypted file will overwrite `output_file` if it exists.
        """
        self._encryption_complete = False
        logging.info("Encrypting file...")
        stdout, stderr = ''.encode(), ''.encode()
        try:
            _subprocess = await asyncio.create_subprocess_shell(
                "openssl enc -aes-256-cbc "
                "-md sha512 -pbkdf2 -iter 100000 -salt "
                f"-in \"{input_file}\" -out \"{output_file}\" "
                f"-pass pass:{self.password}"
            )
            stdout, stderr = await _subprocess.communicate()
        except Exception as e:
            logging.error(
                "Exception {e}:\n{o}\n{er}".format(
                    e=e,
                    o=stdout.decode().strip(),
                    er=stderr.decode().strip()
                )
            )
        logging.info("Encryption completed.")
        self._encryption_complete = True

    async def send(self, writer: asyncio.StreamWriter):
        """Encrypt and send the file.

        Caution: if no password is provided, the file will be sent as clear
        text.
        """
        self._working = True
        file_path = self.file_path
        if self.password:
            file_path = self.file_path + '.enc'
            # Remove already-encrypted file if present (salt would differ)
            if os.path.isfile(file_path):
                os.remove(file_path)
            asyncio.ensure_future(
                self.encrypt_file(
                    input_file=self.file_path,
                    output_file=file_path
                )
            )
            # Give encryption an edge
            while not os.path.isfile(file_path):
                await asyncio.sleep(.5)
        logging.info("Sending file...")
        bytes_sent = 0
        with open(file_path, 'rb') as file_to_send:
            while not self.stopping:
                output_data = file_to_send.read(self.buffer_chunk_size)
                if not output_data:
                    # If encryption is in progress, wait and read again later
                    if self.password and not self.encryption_complete:
                        await asyncio.sleep(1)
                        continue
                    break
                try:
                    writer.write(output_data)
                    await asyncio.wait_for(writer.drain(), timeout=3.0)
                except ConnectionResetError:
                    print()  # New line after progress_bar
                    logging.error('Server closed the connection.')
                    self.stop()
                    break
                except asyncio.exceptions.TimeoutError:
                    print()  # New line after progress_bar
                    logging.error('Server closed the connection.')
                    self.stop()
                    break
                bytes_sent += len(output_data)
                new_progress = min(
                    int(bytes_sent / self.file_size * 100),
                    100
                )
                self.print_progress_bar(
                    progress=new_progress,
                    bytes_=bytes_sent,
                )
        print()  # New line after progress_bar
        writer.close()
        return

    async def receive(self, reader: asyncio.StreamReader):
        """Download the file and decrypt it.

        If no password is provided, the file cannot be decrypted.
        """
        self._working = True
        file_path = os.path.join(
            os.path.abspath(
                self.file_path
            ),
            self.file_name
        )
        original_file_path = file_path
        if self.password:
            file_path += '.enc'
        logging.info("Receiving file...")
        with open(file_path, 'wb') as file_to_receive:
            bytes_received = 0
            while not self.stopping:
                input_data = await reader.read(self.buffer_chunk_size)
                bytes_received += len(input_data)
                new_progress = min(
                    int(bytes_received / self.file_size * 100),
                    100
                )
                self.print_progress_bar(
                    progress=new_progress,
                    bytes_=bytes_received
                )
                if not input_data:
                    break
                file_to_receive.write(input_data)
        print()  # New line after sys.stdout.write
        if bytes_received < self.file_size:
            logging.warning("Transmission terminated too soon!")
            if self.password:
                logging.error("Partial files can not be decrypted!")
                return
        logging.info("File received.")
        if self.password:
            logging.info("Decrypting file...")
            stdout, stderr = ''.encode(), ''.encode()
            try:
                _subprocess = await asyncio.create_subprocess_shell(
                    "openssl enc -aes-256-cbc "
                    "-md sha512 -pbkdf2 -iter 100000 -salt -d "
                    f"-in \"{file_path}\" -out \"{original_file_path}\" "
                    f"-pass pass:{self.password}"
                )
                stdout, stderr = await _subprocess.communicate()
                logging.info("Decryption completed.")
            except Exception as e:
                logging.error(
                    "Exception {e}:\n{o}\n{er}".format(
                        e=e,
                        o=stdout.decode().strip(),
                        er=stderr.decode().strip()
                    )
                )
                logging.info("Decryption failed", exc_info=True)

    def stop(self, *_):
        if self.working:
            logging.info("Received interruption signal, stopping...")
            self._stopping = True
            if self.writer:
                self.writer.close()
        else:
            raise KeyboardInterrupt("Not working yet...")

    def set_file_information(self, file_name=None, file_size=None):
        if file_name is not None:
            self._file_name = file_name
        if file_size is not None:
            self._file_size = int(file_size)
            self._file_size_string = utilities.get_file_size_representation(
                self.file_size
            )

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                self.run_client()
            )
        except KeyboardInterrupt:
            print()
            logging.error("Interrupted")
            for task in asyncio.all_tasks(loop):
                task.cancel()
            if self.writer:
                self.writer.close()
            loop.run_until_complete(
                self.wait_closed()
            )
        loop.close()

    @utilities.timed_action(interval=0.4)
    def print_progress_bar(self, progress: int, bytes_: int):
        """Print client progress bar.

        `progress` % = `bytes_string` transferred
        out of `self.file_size_string`.
        """
        action = {
            'send': "Sending",
            'receive': "Receiving"
        }[self.action]
        bytes_string = utilities.get_file_size_representation(
            bytes_
        )
        utilities.print_progress_bar(
            prefix=f"\t\t\t{action} `{self.file_name}`: ",
            done_symbol='#',
            pending_symbol='.',
            progress=progress,
            scale=5,
            suffix=(
                " completed "
                f"({bytes_string} "
                f"of {self.file_size_string})"
            )
        )

    @staticmethod
    async def wait_closed() -> None:
        """Give time to cancelled tasks to end properly.

        Sleep .1 second and return.
        """
        await asyncio.sleep(.1)


def get_action(action):
    """Parse abbreviations for `action`."""
    if not isinstance(action, str):
        return
    elif action.lower().startswith('r'):
        return 'receive'
    elif action.lower().startswith('s'):
        return 'send'


def get_file_path(path, action='receive'):
    """Check that file `path` is correct and return it."""
    path = os.path.abspath(
        os.path.expanduser(path)
    )
    if (
            isinstance(path, str)
            and action == 'send'
            and os.path.isfile(path)
    ):
        return path
    elif (
            isinstance(path, str)
            and action == 'receive'
            and os.access(os.path.dirname(path), os.W_OK)
    ):
        return path
    elif path is not None:
        logging.error(f"Invalid file: `{path}`")


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
    cli_parser = argparse.ArgumentParser(description='Run client',
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
                            help='server SSL key (required only for '
                                 'SSL-secured standalone client)')
    cli_parser.add_argument('--action', type=str,
                            default=None,
                            required=False,
                            help='[S]end or [R]eceive')
    cli_parser.add_argument('--path', type=str,
                            default=None,
                            required=False,
                            help='File path to send / folder path to receive')
    cli_parser.add_argument('--password', '--p', '--pass', type=str,
                            default=None,
                            required=False,
                            help='Password for file encryption or decryption')
    cli_parser.add_argument('--token', '--t', '--session_token', type=str,
                            default=None,
                            required=False,
                            help='Session token '
                                 '(must be the same for both clients)')
    cli_parser.add_argument('--standalone',
                            action='store_true',
                            help='Run both as client and server')
    cli_parser.add_argument('others',
                            metavar='R or S',
                            nargs='*',
                            help='[S]end or [R]eceive (see `action`)')
    args = vars(cli_parser.parse_args())
    host = args['host']
    port = args['port']
    certificate = args['certificate']
    key = args['key']
    action = get_action(args['action'])
    file_path = args['path']
    password = args['password']
    token = args['token']
    standalone = args['standalone']

    # If host and port are not provided from command-line, try to import them
    sys.path.append(os.path.abspath('.'))
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
    # Take `s`, `r` etc. from command line as `action`
    if action is None:
        for arg in args['others']:
            action = get_action(arg)
            if action:
                break
    if action is None:
        try:
            from config import action
            action = get_action(action)
        except ImportError:
            action = None
    if file_path is None:
        try:
            from config import file_path
            file_path = get_action(file_path)
        except ImportError:
            file_path = None
    if password is None:
        try:
            from config import password
        except ImportError:
            password = None
    if token is None:
        try:
            from config import token
        except ImportError:
            token = None
    if certificate is None or not os.path.isfile(certificate):
        try:
            from config import certificate
        except ImportError:
            certificate = None
    if key is None or not os.path.isfile(key):
        try:
            from config import key
        except ImportError:
            key = None

    # If import fails, prompt user for host or port
    new_settings = {}  # After getting these settings, offer to store them
    while host is None:
        host = input("Enter host:\t\t\t\t\t\t")
        new_settings['host'] = host
    while port is None:
        try:
            port = int(input("Enter port:\t\t\t\t\t\t"))
        except ValueError:
            logging.info("Invalid port. Enter a valid port number!")
            port = None
        new_settings['port'] = port
    while action is None:
        action = get_action(
            input("Do you want to (R)eceive or (S)end a file?\t\t")
        )
    if file_path is not None and (
            (action == 'send'
             and not os.path.isfile(os.path.abspath(file_path)))
            or (action == 'receive'
                and not os.path.isdir(os.path.abspath(file_path)))
    ):
        file_path = None
    while file_path is None:
        if action == 'send':
            file_path = get_file_path(
                path=input(f"Enter file to send:\t\t\t\t\t"),
                action=action
            )
            if file_path and not os.path.isfile(os.path.abspath(file_path)):
                file_path = None
        elif action == 'receive':
            file_path = get_file_path(
                path=input(f"Enter destination folder:\t\t\t\t"),
                action=action
            )
            if file_path and not os.path.isdir(os.path.abspath(file_path)):
                file_path = None
    if password is None:
        logging.warning(
            "You have provided no password for file encryption.\n"
            "Your file will be unencoded unless you provide a password in "
            "config file."
        )
    if token is None and action == 'send':
        # Generate a random [6-10] chars-long alphanumerical token
        token = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits
            )
            for _ in range(random.SystemRandom().randint(6, 10))
        )
        logging.info(
            "You have not provided a token for this connection.\n"
            f"A token has been generated for you:\t\t\t{token}\n"
            "Your peer must be informed of this token.\n"
            "For future connections, you may provide a custom token writing "
            "it in config file."
        )
    while token is None or not (6 <= len(token) <= 10):
        token = input("Please enter a 6-10 chars token.\t\t\t")
    if new_settings:
        answer = utilities.timed_input(
            "You may store the following configuration values in "
            "`config.py`.\n\n" + '\n'.join(
                '\t\t'.join(map(str, item))
                for item in new_settings.items()
            ) + '\n\n'
                'Do you want to store them?\t\t\t\t',
            timeout=3
        )
        if answer:
            with open('config.py', 'a') as configuration_file:
                configuration_file.writelines(
                    [
                        f'{name} = "{value}"\n'
                        if type(value) is str
                        else f'{name} = {value}\n'
                        for name, value in new_settings.items()
                    ]
                )
            logging.info("Configuration values stored.")
        else:
            logging.info("Proceeding without storing values...")
    ssl_context = None
    if certificate and key and standalone:  # Standalone client
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH
        )
        ssl_context.load_cert_chain(certificate, key)
    elif certificate:  # Server-dependent client
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH
        )
        ssl_context.load_verify_locations(certificate)
    else:
        logging.warning(
            "Please consider using SSL. To do so, add in `config.py` or "
            "provide via Command Line Interface the path to a valid SSL "
            "certificate. Example:\n\n"
            "certificate = 'path/to/certificate.crt'"
        )
    logging.info("Starting client...")
    client = Client(
        host=host,
        port=port,
        ssl_context=ssl_context,
        action=action,
        standalone=standalone,
        file_path=file_path,
        password=password,
        token=token
    )
    client.run()
    logging.info("Stopped client")


if __name__ == '__main__':
    main()
