import time
import logging
import requests
import socket
import netifaces
import psutil
import re
import smtplib

# Set up logging
logging.basicConfig(filename='pi_network_monitor.log', level=logging.INFO)

# Set up email alerts
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'
TO_EMAIL = 'recipient@example.com'

# Set up network and system metrics
NETWORK_INTERFACES = ['wlan0']
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_USAGE_THRESHOLD = 90
TEMPERATURE_THRESHOLD = 80
WIFI_SIGNAL_THRESHOLD = -70

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_network_interfaces():
    interfaces = netifaces.interfaces()
    results = []
    for interface in interfaces:
        try:
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                ip_address = addrs[netifaces.AF_INET][0]['addr']
                mac_address = addrs[netifaces.AF_LINK][0]['addr']
                results.append((interface, ip_address, mac_address))
        except Exception as e:
            logging.error(f'Error getting network interface {interface}: {e}')
    return results

def test_connectivity(host):
    try:
        socket.create_connection((host, 80))
        return True
    except OSError:
        return False

def get_network_traffic():
    traffic = psutil.net_io_counters()
    return traffic.bytes_sent, traffic.bytes_recv

def get_wifi_signal_strength():
    try:
        output = subprocess.check_output(['iwconfig', 'wlan0'])
        match = re.search(r'ESSID:"(.*)"  \((.*)\)', output.decode())
        if match:
            signal_strength = match.group(2)
            return signal_strength
    except Exception as e:
        logging.error(f'Error getting Wi-Fi signal strength: {e}')
    return 'Unknown'

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent

def get_memory_usage():
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    return memory_percent

def get_disk_usage():
    disk_info = psutil.disk_usage('/')
    disk_percent = disk_info.percent
    return disk_percent

def get_temperature():
    temperature = psutil.sensors_temperatures()['cpu_thermal'][0].current
    return temperature

def send_email(subject, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f'Subject: {subject}\n\n{body}'
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg)
        server.quit()
    except Exception as e:
        logging.error(f'Error sending email: {e}')

def main():
    while True:
        # Check network status
        ip_address = get_ip_address()
        logging.info(f'IP address: {ip_address}')
        network_interfaces = get_network_interfaces()
        logging.info(f'Network interfaces: {network_interfaces}')
        for interface in NETWORK_INTERFACES:
            if interface not in [nic[0] for nic in network_interfaces]:
                send_email('Network interface down', f'The {interface} network interface is down.')
        for interface, ip_address, mac_address in network_interfaces:
            if test_connectivity(ip_address) is False:
                send_email('Network connectivity lost', f'The {interface} network interface has lost connectivity.')
        network_traffic = get_network_traffic()
        logging.info(f'Network traffic: {network_traffic}')
        wifi_signal_strength = get_wifi_signal_strength()
        logging.info(f'Wi-Fi signal strength: {wifi_signal_strength}')
        if int(wifi_signal_strength) < WIFI_SIGNAL_THRESHOLD:
            send_email('Weak Wi-Fi signal', f'The Wi-Fi signal strength is weak ({wifi_signal_strength}).')

        # Check system metrics
        cpu_usage = get_cpu_usage()
        logging.info(f'CPU usage: {cpu_usage}%')
        if cpu_usage > CPU_THRESHOLD:
            send_email('High CPU usage', f'The CPU usage is high ({cpu_usage}%).')
        memory_usage = get_memory_usage()
        logging.info(f'Memory usage: {memory_usage}%')
        if memory_usage > MEMORY_THRESHOLD:
            send_email('High memory usage', f'The memory usage is high ({memory_usage}%).')
        disk_usage = get_disk_usage()
        logging.info(f'Disk usage: {disk_usage}%')
        if disk_usage > DISK_USAGE_THRESHOLD:
            send_email('High disk usage', f'The disk usage is high ({disk_usage}%).')
        temperature = get_temperature()
        logging.info(f'Temperature: {temperature}°C')
        if temperature > TEMPERATURE_THRESHOLD:
            send_email('High temperature', f'The temperature is high ({temperature}°C).')

        # Sleep for 60 seconds
        time.sleep(60)

if __name__ == '__main__':
    main()
