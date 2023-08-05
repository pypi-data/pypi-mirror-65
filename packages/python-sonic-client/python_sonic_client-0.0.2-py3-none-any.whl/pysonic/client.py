"""
This package is simple client to interact with Sonic 
via its socket protocol
Please note that it is still under development
"""
from __future__ import annotations

import time
import socket
import logging
from enum import Enum
from typing import List


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pysonic')


class Mode(str, Enum):
    SEARCH = 'search'
    INGEST = 'ingest'


class Connection:
    """
    TCP socket wrapper
    """
    def __init__(self, socket, password, mode):
        self._socket = socket
        self._reader = self._socket.makefile('rb', 0)
        self._writer = self._socket.makefile('wb', 0)
        self.mode = mode

        cmd = bytes(f'START {mode} {password}\n', 'utf-8')
        self._writer.write(cmd)
        if b'STARTED' in self._reader.readline():
            logger.debug(f'Started {mode} on socket {self._socket}')

    def __repr__(self):
        return f'<Connection {self._socket.getsockname()} ({self.mode})>'

    @classmethod
    def open_connection(cls, ip, port, password, mode):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        s.settimeout(10)
        s.connect((ip, port))
        buf = s.recv(1024)
        if b'CONNECTED' in buf:
            return cls(s, password, mode)

    @property
    def reader(self):
        return self._reader

    @property
    def writer(self):
        return self._writer

    def close(self):
        return self._socket.close()


class Pool:
    """
    Pool to manage socket connections
    """
    pools = {}

    def __init__(self, ip, port, password, mode, size=10):
        self.size = size
        self.conn_in_used = set()
        self.pool = []
        for i in range(size):
            conn = Connection.open_connection(ip, port, password, mode)
            self.pool.append(conn)

    @classmethod
    def get_pool(cls, ip, port, password, mode: Mode):
        if mode not in cls.pools:
            cls.pools[mode] = cls(ip, port, password, mode)
        return cls.pools[mode]

    def get_connection(self):
        for conn in self.pool:
            if conn not in self.conn_in_used:
                self.conn_in_used.add(conn)
                logger.debug(f"Obtained connection {conn}")
                return conn
        raise ConnectionLimitExceeded()

    def release(self, conn):
        self.conn_in_used.remove(conn)
        logger.debug(f"{conn} released.")


class Client:
    """
    API to communicate with Sonic db
    """
    host = None
    port = None
    password = None

    def __init__(self, 
            host: str = '127.0.0.1', 
            port: int = 1491, 
            password: str = 'SecretPassword',
            size=10,):
        self.host = host
        self.port = port
        self.password = password

        self.conn = None
        self._pool = None

    def __enter__(self):
        self.conn = self._pool.get_connection()
        return self

    def __exit__(self, *args):
        self._pool.release(self.conn)

    def mode(self, mode: Mode):
        if mode == Mode.SEARCH:
            return SearchClient(self.host, self.port, self.password)
        return IngestClient(self.host, self.port, self.password)

    def ping(self):
        self.conn.writer.write(b'PING\n')
        return self.wait_for(b'PONG') == b'PONG'

    def wait_for(self, response: bytes, timeout=5):
        start = time.time()
        while True:
            if time.time() > start + timeout:
                raise TimeoutException()
            line = self.conn.reader.readline()
            if response in line:
                return line.replace(b'\n', b'').replace(b'\r', b'')
            elif line == b'':
                continue
            else:
                raise UnexpectedResponseException(str(line))

    @staticmethod
    def _parse_event_id(line: bytes):
        id_ = line.split(b' ')[1]
        return id_.replace(b'\n', b'').replace(b'\r', b'')

    @staticmethod
    def _parse_query_results(line: bytes) -> List[str]:
        parts = line.replace(b'\n', b'').replace(b'\r', b'').split(b' ')
        results = parts[3:]
        return [r.decode('utf-8') for r in results]


class IngestClient(Client):
    def __init__(self, host, port, password):
        self._pool = Pool.get_pool(host, port, password, Mode.INGEST)

    def push(self, collection: str, bucket: str, object: str, text: str) -> None:
        cmd = bytes(f'PUSH {collection} {bucket} {object} "{text}"\n', 'utf-8')
        self.conn.writer.write(cmd)
        self.wait_for(b'OK')
        logger.info(f'Push {object}-{text} done.')


class SearchClient(Client):
    def __init__(self, host, port, password):
        self._pool = Pool.get_pool(host, port, password, Mode.SEARCH)

    def query(self, collection: str, bucket: str, terms: str, limit=10, offset=0):
        cmd = bytes(f'QUERY {collection} {bucket} "{terms}"\n', 'utf-8')
        self.conn.writer.write(cmd)

        pending = self.wait_for(b'PENDING')
        event_id = self._parse_event_id(pending)
        results = self.wait_for(event_id)
        return self._parse_query_results(results)

    def suggest(self, collection: str, bucket: str, word: str, limit=10):
        cmd = bytes(f'SUGGEST {collection} {bucket} "{word}" LIMIT({limit})\n', 'utf-8')
        self.conn.writer.write(cmd)
        pending = self.wait_for(b'PENDING')
        event_id = self._parse_event_id(pending)
        results = self.wait_for(event_id)
        return self._parse_query_results(results)


class ConnectionLimitExceeded(Exception):
    pass


class UnexpectedResponseException(Exception):
    pass


class TimeoutException(Exception):
    pass


