# PYLedX
Pi52 ABSMiniTowerKit Ice Tower LED Fans Custom Color Python Example

Installation guide:
-------------------
0.   Make sure you followed all steps in https://wiki.52pi.com/index.php?title=ZP-0128 to make it work
1.   Run "sudo pip install rpi_ws281x"
2.   Test the pyledx.py script by running sudo python3 pyledx.py
3.   Play with the flags (-c, --white, --purple, etc...)
4.   Confirm it's working
5.   Place the pyledx.py file on a directory you'll remember, we'll use the following path
     /home/surce/pyledx.py
6.   Disable minitower_moodlight.service by using the following command
     sudo systemctl disable minitower_moodlight.service
7.   Modify the ExecStart from service minitower_moodlight.service
     sudo nano /lib/systemd/system/minitower_moodlight.service
8.   Comment the line ExecStart=sudo /usr/bin/moodlight & with an # before
9.   Add the following ExecStart instead
     ExecStart=/bin/bash -c '/usr/bin/python3 /home/surce/pyledx.py &'
10.  Enable minitower_moodlight.service by using the following command
     sudo systemctl enable minitower_moodlight.service
11.  Reboot to confirm it's working and enjoy!

PS:  You can also play with ExecStart by using:
     ExecStart=/bin/bash -c '/usr/bin/python3 /home/surce/pyledx.py --purple -c &'
     ExecStart=/bin/bash -c '/usr/bin/python3 /home/surce/pyledx.py --white -c &'
