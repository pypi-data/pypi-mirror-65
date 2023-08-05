"""
This package is simple client to interact with Sonic 
via its socket protocol
Please note that it is still under development
"""
from __future__ import annotations

import time
import datetime
import socket
import logging
from collections import deque
from enum import Enum
from typing import List


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('pysonic')
ESCAPE = r'\\'


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
        wait_for(self._reader, b'STARTED')
        logger.debug(f'Started {mode} on socket {self._socket}')

        self.created_at = datetime.datetime.utcnow()

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

    def __init__(
            self, 
            ip, 
            port, 
            password,
            mode,
            size=10,
            auto_reconnect=True,
            conn_ttl=300, # seconds
            ):
        self.size = size
        self.conn_in_used = set()

        self.ip = ip
        self.port = port
        self.password = password
        self.mode = mode

        # use deque
        self.pool = deque(maxlen=size)
        for i in range(size):
            conn = Connection.open_connection(ip, port, password, mode)
            self.pool.append(conn)

        self.auto_reconnect = auto_reconnect
        self.conn_ttl = conn_ttl

    @classmethod
    def get_pool(cls, ip, port, password, mode: Mode, *args, **kwargs):
        if mode not in cls.pools:
            cls.pools[mode] = cls(ip, port, password, mode, *args, **kwargs)
        return cls.pools[mode]

    def get_connection(self):
        for conn in self.pool:
            if self._check_if_conn_is_stale(conn):
                self._renew_conn(conn)
                return self.get_connection()
            if conn not in self.conn_in_used:
                self.conn_in_used.add(conn)
                logger.debug(f"Obtained connection {conn}")
                return conn
        raise ConnectionLimitExceeded()

    def _renew_conn(self, conn):
        self.pool.remove(conn)
        if conn in self.conn_in_used:
            self.conn_in_used.remove(conn)
        new_conn = Connection \
                .open_connection(self.ip, self.port, self.password, self.mode)
        self.pool.append(new_conn)

    def _check_if_conn_is_stale(self, conn):
        live_time = (datetime.datetime.utcnow() - conn.created_at) \
                .total_seconds()
        if live_time > self.conn_ttl:
            return True
        return False

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

    def _send(self, cmd):
        logger.debug(f"Sending command: {cmd}")
        self.conn.writer.write(cmd)

    def mode(self, mode: Mode):
        if mode == Mode.SEARCH:
            return SearchClient(self.host, self.port, self.password)
        return IngestClient(self.host, self.port, self.password)

    def ping(self):
        self._send(b'PING\n')
        return self._wait_for(b'PONG') == b'PONG'

    def _wait_for(self, response: bytes, timeout=5):
        return wait_for(self.conn.reader, response, timeout)

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
        if '"' in text:
            text = text.replace('"', r'\"')
        cmd = bytes(f'PUSH {collection} {bucket} {object} "{text}"\n', 'utf-8')
        self._send(cmd)
        self._wait_for(b'OK')
        logger.info(f'Push {object}-{text} done.')

    def pop(self):
        pass

    def count(self, collection: str, bucket: str = None, object: str = None):
        cmd = f'COUNT {collection}'
        if bucket:
            cmd += f' {bucket}'
            if object:
                cmd += f' {object}'
        cmd = bytes(cmd + '\n', 'utf-8')
        self._send(cmd)
        res = self._wait_for(b'RESULT')
        return self._parse_result(res)

    def flushc(self, collection: str):
        cmd = bytes(f'FLUSHC {collection}\n', 'utf-8')
        self._send(cmd)
        res = self._wait_for(b'RESULT')
        return self._parse_result(res)

    def flushb(self, collection: str, bucket: str):
        cmd = bytes(f'FLUSHB {collection} {bucket}\n', 'utf-8')
        self._send(cmd)
        res = self._wait_for(b'RESULT')
        return self._parse_result(res)

    def flusho(self, collection: str, bucket: str, object: str):
        cmd = bytes(f'FLUSHB {collection} {bucket} {object}\n', 'utf-8')
        self._send(cmd)
        res = self._wait_for(b'RESULT')
        return self._parse_result(res)

    def _parse_result(self, line):
        return int(line.split(b' ')[1])


class SearchClient(Client):
    def __init__(self, host, port, password):
        self._pool = Pool.get_pool(host, port, password, Mode.SEARCH)

    def query(self, collection: str, bucket: str, terms: str, limit=10, offset=0):
        cmd = bytes(f'QUERY {collection} {bucket} "{terms}" LIMIT({limit}) OFFSET({offset})\n', 'utf-8')
        self._send(cmd)

        pending = self._wait_for(b'PENDING')
        event_id = self._parse_event_id(pending)
        results = self._wait_for(event_id)
        return self._parse_query_results(results)

    def suggest(self, collection: str, bucket: str, word: str, limit=10):
        cmd = bytes(f'SUGGEST {collection} {bucket} "{word}" LIMIT({limit})\n', 'utf-8')
        self._send(cmd)
        pending = self._wait_for(b'PENDING')
        event_id = self._parse_event_id(pending)
        results = self._wait_for(event_id)
        return self._parse_query_results(results)


def wait_for(reader, response: bytes, timeout=5):
    start = time.time()
    while True:
        if time.time() > start + timeout:
            raise TimeoutException()
        line = reader.readline()
        line = line.replace(b'\n', b'').replace(b'\r', b'')
        if response in line:
            return line
        elif line == b'':
            continue
        else:
            raise UnexpectedResponseException(str(line))


class ConnectionLimitExceeded(Exception):
    pass


class UnexpectedResponseException(Exception):
    pass


class TimeoutException(Exception):
    pass
