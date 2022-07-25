# Raspberry Pi I2C OLED status monitor

Python Script based on luma.oled library to display various stats for a Network Assisted Storage ( NAS )

Shows:
- CPU Usage 
- Uptime
- CPU Temp
- RAM Usage
- IP Address ( Wifi / Ethernet or Both )
- Network Transfers and Recieved in Bytes ( Wifi / Ethernet or Both )
- Disk Usage ( SD Card / Attached drives )

## Dependencies:
TBC

## How to use:

1. Copy the file in systemctl folder to /lib/systemd/system/ 

2.  ` sudo systemctl start startup.service ` to verify if code works

3.  ` sudo systemctl enable startup.service ` to enable it for startup

4.  You can then reboot ur pi and test if the code works accordingly.
    
    You can also run ` sudo systemctl status startup.service ` to check any error logs in case
