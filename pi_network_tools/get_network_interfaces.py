import netifaces


def get_network_interfaces():
    """
    Get the network interfaces of the Raspberry Pi.
    """
    interfaces = netifaces.interfaces()
    results = []
    for interface in interfaces:
        try:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                ip_address = addrs[netifaces.AF_INET][0]["addr"]
                mac_address = addrs[netifaces.AF_LINK][0]["addr"]
                results.append((interface, ip_address, mac_address))
        except Exception as e:
            print(f"Error getting network interface {interface}: {e}")
    return results
