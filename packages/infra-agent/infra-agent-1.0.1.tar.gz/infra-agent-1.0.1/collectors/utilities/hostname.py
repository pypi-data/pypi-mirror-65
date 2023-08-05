import logging
import re
import socket

from collectors.utilities.process_output import get_subprocess_output

VALID_HOSTNAME_RFC_1123_PATTERN = re.compile(
    r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
MAX_HOSTNAME_LEN = 255

log = logging.getLogger(__name__)


def is_valid_hostname(hostname):
    if hostname.lower() in set([
        'localhost',
        'localhost.localdomain',
        'localhost6.localdomain6',
        'ip6-localhost',
    ]):
        log.warning("Hostname: %s is local" % hostname)
        return False
    if len(hostname) > MAX_HOSTNAME_LEN:
        log.warning("Hostname: %s is too long (max length is  %s characters)" % (hostname, MAX_HOSTNAME_LEN))
        return False
    if isinstance(hostname, bytes):
        hostname = hostname.decode('utf-8')
    if VALID_HOSTNAME_RFC_1123_PATTERN.match(hostname) is None:
        log.warning("Hostname: %s is not complying with RFC 1123" % hostname)
        return False
    return True


def _get_hostname_unix():
    try:
        # try fqdn
        out, _, rtcode = get_subprocess_output(['/bin/hostname', '-f'], log)
        if rtcode == 0:
            return out.strip()
    except Exception:
        return None


def get_hostname():
    """
    Get the canonical host name this agent should identify as. This is
    the authoritative source of the host name for the agent.
    Tries, in order:
      * 'hostname -f' (on unix)
      * socket.gethostname()
    """
    hostname = None

    unix_hostname = _get_hostname_unix()
    if unix_hostname and is_valid_hostname(unix_hostname):
        hostname = unix_hostname

    # fall back on socket.gethostname(), socket.getfqdn() is too unreliable
    if hostname is None:
        try:
            socket_hostname = socket.gethostname()
        except socket.error:
            socket_hostname = None
        if socket_hostname and is_valid_hostname(socket_hostname):
            hostname = socket_hostname

    if hostname is None:
        log.critical(
            'Unable to reliably determine host name. You can define one in cs-agent.conf or in your hosts file')
        raise Exception(
            'Unable to reliably determine host name. You can define one in cs-agent.conf or in your hosts file')
    if hostname and isinstance(hostname, bytes):
        hostname = hostname.decode('utf-8')
    return hostname


def host_ip_addr():
    """
    * Get the host ip address by hostname.
    * If it is not retrieved, get from the eth0 interface.

    :return:
    """
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)

    if ip_addr != '127.0.0.1':
        return ip_addr
    try:
        import netfaces as ni
        ni.ifaddresses('eth0')
        ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
        log.debug('IP address found through eth0 ->'.format(ip))
        return ip
    except Exception as ex:
        log.error('netfaces exception', exc_info=ex)
        pass

    return '127.0.0.1'
