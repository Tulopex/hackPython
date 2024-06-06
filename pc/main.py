import platform
import psutil
import os

try:
    import wmi
    wmi_available = True
except ImportError:
    wmi_available = False

try:
    import py3nvml.py3nvml as nvml
    nvml_available = True
except ImportError:
    nvml_available = False

def get_system_info():
    info = {}

    info['Operating System'] = platform.system() + " " + platform.release()

    # Процессор
    info['Processor'] = platform.processor()

    # Оперативная память
    info['Total RAM'] = str(round(psutil.virtual_memory().total / (1024 ** 3))) + " GB"

    if wmi_available:
        c = wmi.WMI()
        for board_id in c.Win32_BaseBoard():
            info['Motherboard'] = board_id.Product
        for gpu in c.Win32_VideoController():
            info['GPU'] = gpu.Name
    else:
        info['Motherboard'] = "N/A"
        info['GPU'] = "N/A"

    return info

def save_info_to_file(info, filename):
    with open(filename, 'w') as file:
        for key, value in info.items():
            file.write(f"{key}: {value}\n")

if __name__ == "__main__":
    system_info = get_system_info()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'output.txt')
    save_info_to_file(system_info, output_file)
