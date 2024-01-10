import subprocess
import os
import platform

def get_wifi_passwords_linux():
    try:
        wifi_data = subprocess.check_output(['ls', '/etc/NetworkManager/system-connections']).decode('utf-8').split('\n')
        print("{:<30} {}".format("Wifi Name", "Password"))
        print("----------------------------------------")
        for wifi_name in wifi_data:
            if wifi_name:
                path = f"/etc/NetworkManager/system-connections/{wifi_name}"
                wifi_pass = subprocess.check_output(['sudo', 'cat', path]).decode('utf-8').split('\n')
                password = next((line.split('=')[1] for line in wifi_pass if line.startswith("psk=")), "")
                print("{:<30} {}".format(wifi_name, password))
    except Exception as e:
        print(f"Error: {e}")

def get_wifi_passwords_windows():
    try:
        wifi = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')
        profiles = [i.split(":")[1].strip() for i in wifi if "All User Profile" in i]
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], stderr=subprocess.STDOUT).decode('utf-8').split('\n')
                password = next((b.split(":")[1].strip() for b in results if "Key Content" in b), "")
                print("{:<30} {}".format(i, password))
            except subprocess.CalledProcessError:
                print("{:<30} {}".format(i, "ENCODING ERROR"))
    except subprocess.CalledProcessError as e:
        if "The Wireless AutoConfig Service (wlansvc) is not running" in str(e.output):
            print("Error: The Wireless AutoConfig Service (wlansvc) is not running. "
                  "Please start the wlansvc service and try again.")
        else:
            print(f"Error: {e.output.decode()}")

if os.name == 'posix' and platform.system() == 'Linux':
    get_wifi_passwords_linux()
elif os.name == 'nt':
    get_wifi_passwords_windows()
else:
    print("Unsupported Operating System")
