#PyMonitor 1.3.2b for Raspberry Pi by Surce Beats
#Version: 1.3.2b
#URL: http://surcebeats.com
#Email: info@surcebeats.com

#Import modules needed to work
import os
import datetime
import subprocess
import math
import docker

sleeptime = 1

# Get the directory from where the script will be launched (MAY NEED TO BE MODIFIED)
run_dir = "/home/surce/Scripts/PyMonitor"

#PyMonitor Version for logging
pyversion = "1.3.2b"

# Get the current date and time as a string in the format 'yy-mm-dd hh:mm:ss'
current_time = datetime.datetime.now().strftime('%H:%M:%S')
current_date = datetime.datetime.now().strftime('%y_%m_%d')

# Join run_dir path along with date path and create the folder if it doesn't exists
daily_folder_path = os.path.join(run_dir, "logs")
os.makedirs(daily_folder_path, exist_ok=True)

# Create a logfile name based on the current date and time
logfile = os.path.join(daily_folder_path, f"pm_{current_date.replace(':', '_')}.log")

# Create a logfile name based on the current date and time
cfgfile = os.path.join(run_dir, "pymonitor.conf")

# Read the pymonitor.conf file to set ongoing variables
linebreak = [line.strip() for line in open(cfgfile, "r")]
config_temp_maximum = linebreak[1]
config_temp_critic = linebreak[4]
config_temp_shutdown = linebreak[7]
config_download_speed = linebreak[10]
config_containers_all = linebreak[13]
config_containers_heating = linebreak[16]
config_containers_critic = linebreak[19]
config_containers_download = linebreak[22]

# Import the CPUTemperature class from gpiozero and check temp
from gpiozero import CPUTemperature
cputemp = int(CPUTemperature().temperature)

# Set the maximum and critical temperatures for the CPU in Celsius
cpu_maxtemp = int(config_temp_maximum)
cpu_critictemp = int(config_temp_critic)
cpu_shutdowntemp = int(config_temp_shutdown)

#Set the download speed threshold
download_speed_threshold = int(config_download_speed)

# Run the 'ifstat' command to check the download speed for interface 'wlan0'
downspeed = math.trunc(float(os.popen("ifstat -i wlan0 3s 1 | awk 'NR==3 {print $1}'").read().strip()))

# Run the 'pidof' command to check if the 'dd' backup process is running
backuprun = os.popen("pidof -x dd").read().strip()

# Define three strings of container names separated by '*'
cont_total = config_containers_all
cont_heating = config_containers_heating
cont_critic = config_containers_critic
cont_download = config_containers_download

# Define a function to print output to the console and to the log file
def printLog(*args):
    print(*args, sep='')
    with open(logfile, 'a') as file:
        file.write(''.join(str(arg) for arg in args))
        file.write("\n")

"""
def printLog(*args, **kwargs):
    print(*args, **kwargs)
    with open(logfile,'a+') as file:
        print(*args, **kwargs, file=file)
"""

# Define a function to check if a Docker container is running
def is_container_running(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        return container.status == "running"
    except docker.errors.NotFound:
        return False

# Define a function to start Docker containers
def start_containers(container_list):
    for container in container_list.split("*"):
        if not is_container_running(container):
            printLog("↑↑↑ Starting       >   ", container)
            subprocess.run(["sudo", "docker", "start", container], stdout=subprocess.DEVNULL)
        else:
            printLog("--↑ Nothing        >   ", container)

# Define a function to stop Docker containers
def stop_containers(container_list):
    for container in container_list.split("*"):
        if is_container_running(container):
            printLog("↓↓↓ Stopping       >   ", container)
            subprocess.run(["sudo", "docker", "stop", container], stdout=subprocess.DEVNULL)
        else:
            printLog("--↓ Nothing        >   ", container)

print("")
print("--------------------------------------------------")
print("")
printLog("Time               >   ", current_time)
printLog("Version            >   PyMonitor ", pyversion)
printLog("Logfile            >   ", logfile)
printLog("Download speed     >   ", downspeed,"KB/s")
printLog("> Threshold speed  >   ", download_speed_threshold,"KB/s")
printLog("CPU                >   ", cputemp,"ºC")
printLog("> CPU Max          >   ", cpu_maxtemp,"ºC")
printLog("> CPU Critic       >   ", cpu_critictemp,"ºC")
printLog("> CPU Shutdown     >   ", cpu_shutdowntemp,"ºC")

if not backuprun:
    # Backup not running
    printLog("Backup             >   Not running")
    printLog("")

    if downspeed < download_speed_threshold:
        #System is not downloading data or is under download_speed_threshold
        if cputemp <= cpu_maxtemp:
            # Temperature equal or lower than HEATING
            printLog("►►► Not downloading (", downspeed, "KB/s), cool temperature (", cputemp, "ºc)")
            printLog("")
            start_containers(cont_total)
        elif cputemp > cpu_critictemp:
            if cputemp > cpu_shutdowntemp:
                # Temperature is above CRITIC and SHUTDOWN limit, shut down system
                printLog("►►► Temperature is above SHUTDOWN limit, shutting down system! (", cputemp, "ºc)")
                printLog("")
                os.system("sudo shutdown -h now")
            else:
                # Temperature is above CRITIC limit but below SHUTDOWN limit, stop CRITIC containers
                printLog("►►► Not downloading (", downspeed, "KB/s), temperature is CRITIC (", cputemp, "ºc)")
                printLog("")
                stop_containers(cont_heating)
                stop_containers(cont_critic)
        else:
            # Temperature higher than HEATING but lower than CRITIC
            printLog("►►► Not downloading (", downspeed, "KB/s), temperature is high (", cputemp, "ºc)")
            printLog("")
            stop_containers(cont_heating)
            stop_containers(cont_download)
    else:
        #System is downloading data and is over download_speed_threshold
        if cputemp >= cpu_critictemp:
            if cputemp > cpu_shutdowntemp:
                # Temperature is above shutdown limit, shut down system
                printLog("►►► Temperature is above SHUTDOWN limit, shutting down system! (", cputemp, "ºc)")
                printLog("")
                os.system("sudo shutdown -h now")
            else:
                # Temperature is above critical limit but below shutdown limit, stop critical containers
                printLog("►►► System download at (", downspeed, "KB/s), temperature is CRITIC (", cputemp, "ºc)")
                printLog("")
                stop_containers(cont_heating)
                stop_containers(cont_critic)
        elif cputemp > cpu_maxtemp:
            # Temperature higher than HEATING but lower than CRITIC
            printLog("►►► System download at (", downspeed, "KB/s), temperature is high (", cputemp, "ºc)")
            printLog("")
            stop_containers(cont_heating)
        else:
            # Temperature equal or lower than HEATING
            printLog("►►► System download at (", downspeed, "KB/s), cool temperature (", cputemp, "ºc)")
            printLog("")
            start_containers(cont_total)
else:
    # Backup running
    printLog("Backup             >   Running")
    printLog("> Backup           >   Process PID: ", backuprun)
    printLog("> Backup           >   Waiting until finished to start container")

printLog("")
printLog("--------------------------------------------------")
printLog("")
