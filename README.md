# TeamStatus LED Controller

## Overview

This Python script provides a practical solution for integrating Microsoft Teams' online status with an IO-Link Master (TURCK TBEN-S2-4IOL) to control an RGB LED (BANNER K50L2). The goal is to represent Microsoft Teams' user statuses through the color of the LED, creating a visual indicator of team members' availability.

## Dependencies

Ensure you have the necessary Python libraries installed using:

```bash
pip install pyModbusTCP
```

## Hardware Configuration

1. **IO-Link Master (TURCK TBEN-S2-4IOL):**
   - IP Address: 192.168.47.153
   - Port: 502
   - Unit ID: 1

2. **Ultrasonic Sensor (TURCK RU40U-M18M-AP8X2-H1151):**
   - Connected to Port 1 of the IO-Link Master.

3. **RGB LED (BANNER K50L2):**
   - Connected to Port 4 of the IO-Link Master.

## Microsoft Teams Log File

Make sure to set the correct Teams log file path in the script:

```python
TEAMS_LOG = os.path.join(os.getenv("APPDATA"), "Microsoft\\Teams\\logs.txt")
```
## Usage
Run the script by executing the following command in your terminal:

```bash
python script_name.py
```

## Microsoft Teams Status Mapping
1. **Red LED:**
    - Busy, DoNotDisturb, InAMeeting, Presenting, OnThePhone
2. **Yellow LED:**
    - Away, BeRightBack
3. **Green LED:**
    - Available

## Debugging

To enable debug mode, set the DEBUG variable to True:

```python
DEBUG = True 
```

## Notes:

- Make sure that your are in windows, if you are using Linux or MacOs make sure that you have past the right path
- The script utilizes threading for concurrently monitoring Teams status and updating the IO-Link Master.
- Microsoft Teams' presence information is extracted from the log file located at the specified path.
- Ensure the Modbus TCP parameters match your IO-Link Master configuration.
The script continuously runs until manually terminated.



Feel free to customize the script according to your specific hardware setup and preferences. If you encounter any issues, refer to the script's print statements and adjust as needed.