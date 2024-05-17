import socket

def test_connectivity(host):
    """
    Test connectivity to a host.
    """
    try:
        socket.create_connection((host, 80))
        return True
    except OSError:
        return False
