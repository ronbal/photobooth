# Raspberry Pi photobooth
a raspberry Pi photobooth.

The program shoots 3 Pictures per session. After shooting the Pictures the program made a collage. Each picture and the collage is copied to /var/www/html/images. Thumbnails are automatically generated in /var/www/html/thumbs. Your guests can acces the Pictures via a Webgallery at http://yourip/


Photobooth python Program by Ronny Schönfeld

## what you need:
1. Raspberry Pi
2. PiCamera
3. Button on GPIO 16 & 18
4. Apache Webserver
5. PHP5


#Installation

### first Update & upgrade
```
sudo apt-get update
sudo apt-get upgrade
```
### install Apache Webserver:
```
sudo apt-get install apache2
```
### install php5:
```
sudo apt-get install php5
```
### get the repository:
```
git clone https://github.com/ronbal/photobooth
```

###install imagemagick
```
sudo apt-get install imagemagick
```



### Please add the folders:
/var/www/hmtl/images
/var/www/hmtl/thumbs
```
mkdir /var/www/html/images
mkdir /var/www/html/thumbs
```


### copy the Webserver Files to you /var/www/hmtl/demo/
```
sudo cp -R /home/pi/photobooth/webserver/* /var/www/html
```
### to autostart on reboot:
```
sudo nano /etc/rc.local
```
add the line
python3 /home/pi/photobooth/photobooth.py

```
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi
python3 /home/pi/photobooth/photobooth.py&
exit 0
```


