import socket
import threading


class Sock:
    """
    An abstraction over a python socket object.

    Usage:

    .. highlight:: python
    .. code-block:: python

        import errorship

        s = errorship.sock.Sock(host="localhost", port=8125)
        s.send("some-data")
    """

    def __init__(self, host, port, DOING_TESTS=False):
        """
        Parameters:
            host:	the host of the DogStatsd `agent/server <https://docs.datadoghq.com/agent>`_
            port: the port of the DogStatsd `agent/server <https://docs.datadoghq.com/agent>`_
            DOING_TESTS: whether this class is been accesed during test runs
        """
        if not isinstance(host, str):
            raise TypeError("`host` should be of type:: `str` You entered: {0}".format(type(host)))
        if not isinstance(port, int):
            raise TypeError("`port` should be of type:: `int` You entered: {0}".format(type(port)))

        self.host = host
        self._check_hostname()
        self.port = port
        self.DOING_TESTS = DOING_TESTS
        self.encoding = "utf8"
        self.socket = None

        self._LOCK = threading.Lock()

    def _check_hostname(self):
        """
        checks that the host passed in to `Sock` is valid

        Raises `socket.gaierror` or `OSError` if Sock.host is invalid
        see: https://sourcegraph.com/github.com/python/cpython@04ec7a1f7a5b92187a73cd02670958444c6f2220/-/blob/Lib/test/test_urllibnet.py#L134:16
        """
        socket.gethostbyname(self.host)

    def _get_socket(self):
        """
        get a socket in a thread safe way
        """
        self._LOCK.acquire()
        try:
            if not self.socket:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                sock.setblocking(False)

                sock.connect((self.host, self.port))

                self.socket = sock
        finally:
            self._LOCK.release()
            return self.socket

    def send(self, data):
        try:
            sock = self._get_socket()
            sock.send(data.encode(self.encoding))
        except Exception as e:
            self._handle_send_error(e=e)

    def _handle_send_error(self, e):
        # we do not know what happened, as a precaution;
        # we need to bring down the socket
        self.close()
        if self.DOING_TESTS:
            raise e
        else:
            return

    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None
