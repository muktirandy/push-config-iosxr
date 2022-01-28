import time
from datetime import datetime
from netmiko import ConnectHandler
from device_target import devices
from rich import print

today = datetime.today().strftime('%Y-%m-%d')

failed_ssh_list = []

tic = time.perf_counter()
for ip in devices:
    try:
        device = {
            'device_type': 'cisco_xr',
            'host': ip,
            'username': 'epnm',
            'password': "3pnM1s4t!",
            'ssh_config_file': '/home/randymukti/.ssh/proxy_epnm',
            'conn_timeout': 40,
            'banner_timeout': 40
        }

        net_connect = ConnectHandler(**device)
        net_connect.config_mode()
        net_connect.send_command("netconf agent tty throttle memory 600")
        net_connect.commit()
        net_connect.disconnect() 
        print("Success insert and commit config for IP = {}".format(ip))

    
    except Exception as e:
        print(e)
        print("Error SSH to device = {}".format(ip))
        failed_ssh_list.append(ip)
    
toc = time.perf_counter()
print(f"Script running in {toc - tic:0.4f} seconds")

print(f"[red]SSH failed list =  {failed_ssh_list}[/red]")
