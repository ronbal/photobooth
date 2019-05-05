import subprocess
from subprocess import STDOUT, check_call
import os
from time import sleep
WorkingDir = os.getcwd()
print("Starting update")
check_call(['sudo', 'apt-get', 'update', '-y'])
print("Starting upgrade")
check_call(['sudo', 'apt-get', 'upgrade', '-y'])
print("installing apache2")
check_call(['sudo', 'apt-get', 'install', 'apache2', '-y'])
print("installing php5")
check_call(['sudo', 'apt-get', 'install', 'php', '-y'])
print("installing imagemagick")
check_call(['sudo', 'apt-get', 'install', 'imagemagick', '-y'])
print("make directory images")
subprocess.call('sudo mkdir /var/www/html/images', shell=True)
print("make directory thumbs for thumbnmails")
subprocess.call('sudo mkdir /var/www/html/thumbs', shell=True)
print("copy webserver files")
subprocess.call('sudo cp -R /home/pi/photobooth/webserver/* /var/www/html', shell=True)
print("delete the old index.html")
subprocess.call('sudo rm -r /var/www/html/index.html', shell=True)
print("copy rc.local")
subprocess.call('sudo cp -R /home/pi/photobooth/rc.local /etc/rc.local', shell=True)
print("setting rights")
subprocess.call('sudo chmod 755 /etc/rc.local', shell=True)
subprocess.call('sudo chmod +x /home/pi/photobooth/photobooth.py', shell=True)
print("your PHOTOBOOTH is ready")
print("please start the photobooth with:")
print("python3 /home/pi/photobooth/photobooth.py")

for x in range(10,0,-1):
    print('#rebooting in: '+str(x)+' seconds. Press ctrl+c to stop')
    sleep(1)
subprocess.call('sudo reboot', shell=True)

