import os
import re
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import threading

TEAMS_LOG = os.path.join(os.getenv("APPDATA"), "Microsoft\\Teams\\logs.txt")

DEBUG = False

def main():
    # Initialize Modbus client
    mehdi = ModbusClient(host='192.168.47.153', port=502, unit_id=1, auto_open=True)
    
    # Create threads
    teams_status_thread = threading.Thread(target=monitor_teams_status)
    modbus_control_thread = threading.Thread(target=update_modbus_registers, args=(mehdi,))

    # Start threads
    teams_status_thread.start()
    modbus_control_thread.start()

    # Wait for threads to finish
    teams_status_thread.join()
    modbus_control_thread.join()

def monitor_teams_status():
    status="Away"
    while True:
        status, logTime = getLatestStatus(TEAMS_LOG)
        print("MS Teams status: " + status + " (" + logTime + ")")
        
        update_status(status)

        if DEBUG:
            # Don't infinite loop on DEBUG mode
            break

def update_modbus_registers(mehdi):
    while True:
        status = get_status()

        if status in ["Busy", "DoNotDisturb", "InAMeeting", "Presenting", "OnThePhone"]:
            # Turn LED to RED
            print("  Turning light RED...")
            mehdi.write_multiple_registers(2097, [1, 1])

        elif status in ["Away", "BeRightBack"]:
            # Turn LED to YELLOW
            print("  Turning light YELLOW...")
            mehdi.write_multiple_registers(2097, [1, 3])
        elif status in ["Available"]:
            # turn LED to GREEN
            print("  Turning light GREEN...")
            mehdi.write_multiple_registers(2097, [1,0])
            

def getLatestStatus(logfile):
    """Read and parse MS Teams logfile to get the last presence status.

    Returns:
        (status, logTime)
    """
    status = ""

    try:
        with open(logfile, "r") as f:
            for line in f:
                if "(current state: " not in line:
                    continue
                logTime = re.search("^(.+) (.+) (.+) (.+) (.+) GMT+", line).group(5)
                logStatus = re.search(".*\(current state: (.+) -> (.+)\)", line).group(2)

                if logStatus not in ["ConnectionError", "NewActivity", "Unknown"]:
                    status = logStatus

        return (status, logTime)

    except Exception as e:
        print(e)
def update_status(new_status):
    global current_status
    current_status = new_status

def get_status():
    global current_status
    return current_status

if __name__ == "__main__":
    current_status = ""  # Shared variable between threads
    main()
