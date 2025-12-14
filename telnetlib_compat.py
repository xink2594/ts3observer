"""
Simple telnetlib compatibility layer for Python 3.13+
This provides basic telnet functionality using socket
"""
import socket
import time


class Telnet:
    """Simple Telnet client implementation"""
    
    def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        if host is not None:
            self.open(host, port, timeout)
    
    def open(self, host, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host."""
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)
        
    def write(self, buffer):
        """Write a byte string to the socket."""
        if isinstance(buffer, str):
            buffer = buffer.encode('ascii')
        self.sock.send(buffer)
    
    def read_until(self, match, timeout=None):
        """Read until a given byte string is encountered or until timeout."""
        if isinstance(match, str):
            match = match.encode('ascii')
        
        data = b''
        while True:
            try:
                self.sock.settimeout(timeout if timeout else 1)
                chunk = self.sock.recv(1024)
                if not chunk:
                    break
                data += chunk
                if match in data:
                    break
            except socket.timeout:
                break
        return data
    
    def read_very_eager(self):
        """Read all data available right now."""
        try:
            self.sock.settimeout(0.1)
            data = b''
            while True:
                chunk = self.sock.recv(1024)
                if not chunk:
                    break
                data += chunk
        except (socket.timeout, socket.error):
            pass
        return data
    
    def close(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
            self.sock = None