import psutil

def get_network_traffic():
    """
    Get the network traffic of the Raspberry Pi.
    """
    traffic = psutil.net_io_counters()
    return traffic.bytes_sent, traffic.bytes_recv
