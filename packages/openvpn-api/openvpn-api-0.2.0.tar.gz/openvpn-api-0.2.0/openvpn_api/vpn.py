import logging
import socket
import re
import contextlib
import openvpn_status
import openvpn_api.util as util
import openvpn_api.util.errors as errors
from openvpn_api.models.state import State
from openvpn_api.models.stats import ServerStats

logger = logging.getLogger(__name__)


class VPNType:
    IP = 'ip'
    UNIX_SOCKET = 'socket'


class VPN:
    _mgmt_host = None  # Management interface host
    _mgmt_port = None  # Management interface port
    _mgmt_socket = None  # Management interface UNIX socket
    _type = None  # VPNType object to choose between IP (host:port) and socket
    _socket = None

    _release = None  # OpenVPN release string
    _state = None  # State object
    stats = ServerStats()  # Stats object
    sessions = []  # Client sessions

    def __init__(self,
                 host=None,
                 port=None,
                 socket=None):
        if (socket and host) or (socket and port) or (not socket and not host and not port):
            raise errors.VPNError('Must specify either socket or host and port')
        if socket:
            self._mgmt_socket = socket
            self._type = VPNType.UNIX_SOCKET
        else:
            self._mgmt_host = host
            self._mgmt_port = port
            self._type = VPNType.IP

    @property
    def type(self):
        """Get VPNType object for this VPN.
        """
        return self._type

    @property
    def mgmt_address(self):
        """Get address of management interface.
        """
        if self.type == VPNType.IP:
            return '{}:{}'.format(self._mgmt_host, self._mgmt_port)
        else:
            return str(self._mgmt_socket)

    def connect(self):
        """Connect to management interface socket.
        """
        try:
            if self.type == VPNType.IP:
                self._socket = socket.create_connection((self._mgmt_host, self._mgmt_port), timeout=3)

            else:
                self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._socket.connect(self._mgmt_socket)
            resp = self._socket_recv()
            assert resp.startswith('>INFO'), 'Did not get expected response from interface when opening socket.'
            return True
        except (socket.timeout, socket.error) as e:
            raise errors.ConnectError(str(e)) from None

    def disconnect(self, _quit=True):
        """Disconnect from management interface socket.
        """
        if self._socket is not None:
            if _quit:
                self._socket_send('quit\n')
            self._socket.close()
            self._socket = None

    @property
    def is_connected(self):
        """Determine if management interface socket is connected or not.
        """
        return self._socket != None

    @contextlib.contextmanager
    def connection(self):
        """Create context where management interface socket is open and close when done.
        """
        self.connect()
        try:
            yield
        finally:
            self.disconnect()

    def _socket_send(self, data):
        """Convert data to bytes and send to socket.
        """
        self._socket.send(bytes(data, 'utf-8'))

    def _socket_recv(self):
        """Receive bytes from socket and convert to string.
        """
        return self._socket.recv(4096).decode('utf-8')

    def send_command(self, cmd):
        """Send command to management interface and fetch response.
        """
        if not self.is_connected:
            raise errors.NotConnectedError("You must be connected to the management interface to issue commands.")
        logger.debug('Sending cmd: %r', cmd.strip())
        self._socket_send(cmd + '\n')
        if cmd.startswith('kill') or cmd.startswith('client-kill'):
            return
        resp = self._socket_recv()
        if cmd.strip() not in ('load-stats', 'signal SIGTERM'):
            while not resp.strip().endswith('END'):
                resp += self._socket_recv()
        logger.debug('Cmd response: %r', resp)
        return resp

    # Interface commands and parsing

    @staticmethod
    def has_prefix(line):
        return line.startswith('>INFO') or \
               line.startswith('>CLIENT') or \
               line.startswith('>STATE')

    def _get_version(self):
        """Get OpenVPN version from socket.
        """
        raw = self.send_command('version')
        for line in raw.splitlines():
            if line.startswith('OpenVPN Version'):
                return line.replace('OpenVPN Version: ', '')
        raise errors.ParseError('Unable to get OpenVPN version, no matches found in socket response.')

    @property
    def release(self):
        """OpenVPN release string.
        """
        if self._release is None:
            self._release = self._get_version()
        return self._release

    @property
    def version(self):
        """OpenVPN version number.
        """
        if self.release is None:
            return None
        match = re.search(r'OpenVPN (?P<version>\d+.\d+.\d+)', self.release)
        if not match:
            raise errors.ParseError('Unable to parse version from release string.')
        return match.group('version')

    def _get_state(self):
        """Get OpenVPN state from socket.
        """
        raw = self.send_command('state')
        for line in raw.splitlines():
            if self.has_prefix(line):
                continue
            if line.strip() == 'END':
                break
            parts = line.split(',')
            # 0 - Unix timestamp of server start (UTC?)
            up_since = parts[0]
            # 1 - Connection state
            state_name = util.nonify_string(parts[1])
            # 2 - Connection state description
            desc_string = util.nonify_string(parts[2])
            # 3 - TUN/TAP local v4 address
            local_virtual_v4_addr = util.nonify_string(parts[3])
            # 4 - Remote server address (client only)
            remote_addr = util.nonify_string(parts[4])
            # 5 - Remote server port (client only)
            remote_port = util.nonify_int(parts[5])
            # 6 - Local address
            local_addr = util.nonify_string(parts[6])
            # 7 - Local port
            local_port = util.nonify_int(parts[7])
            return State(up_since=up_since,
                         state_name=state_name,
                         desc_string=desc_string,
                         local_virtual_v4_addr=local_virtual_v4_addr,
                         remote_addr=remote_addr,
                         remote_port=remote_port,
                         local_addr=local_addr,
                         local_port=local_port)

    @property
    def state(self):
        """OpenVPN daemon state.
        """
        if self._state is None:
            self._state = self._get_state()
        return self._state

    def cache_data(self):
        """Cached some metadata about the connection.
        """
        _ = self.release
        _ = self.state

    def clear_cache(self):
        """Clear cached state data about connection.
        """
        self._release = None
        self._state = None

    def send_sigterm(self):
        """Send a SIGTERM to the OpenVPN process.
        """
        raw = self.send_command('signal SIGTERM')
        if raw.strip() != 'SUCCESS: signal SIGTERM thrown':
            raise errors.ParseError('Did not get expected response after issuing SIGTERM.')
        self.disconnect(_quit=False)

    def get_stats(self):
        """Get latest VPN stats.
        """
        raw = self.send_command('load-stats')
        for line in raw.splitlines():
            if not line.startswith('SUCCESS'):
                continue
            match = re.search(r'SUCCESS: nclients=(?P<nclients>\d+),bytesin=(?P<bytesin>\d+),bytesout=(?P<bytesout>\d+)', line)
            if not match:
                raise errors.ParseError('Unable to parse stats from load-stats response.')
            return ServerStats(client_count=match.group('nclients'),
                               bytes_in=match.group('bytesin'),
                               bytes_out=match.group('bytesout'))
        raise errors.ParseError('Did not get expected response from load-stats.')

    def get_status(self):
        """Get current status from VPN.

        Uses openvpn-status library to parse status output:
        https://pypi.org/project/openvpn-status/
        """
        raw = self.send_command('status 1')
        return openvpn_status.parse_status(raw)
