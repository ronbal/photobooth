# photobooth
a raspberry Pi photobooth.

The program shoots 4 Pictures per session. After shooting the Pictures the program made a collage. Each picture and the collage is copied to /var/www/html/demo/images. Thumbnails are automatically generated in /var/www/html/demo/thumbs. Your guests can acces the Pictures via a Webgallery at http://yourip/demo


#Photobooth python Program by Ronny Schönfeld

#what you need:
1. Raspberry Pi
2. PiCamera
3. Button on GPIO 16 & 18
4. Apache Webserver
5. PHP5


#Installation

first Update & upgrade
```
sudo apt-get update
sudo apt-get upgrade
```
install Apache Webserver:
```
sudo apt-get install apache2
```
install php5:
```
sudo apt-get install php5
```

Please add the folders:
/var/www/hmtl/images
/var/www/hmtl/thumbs

get the repository:
```
git clone https://github.com/ronbal/photobooth
```
copy the Photoboth Folder to your /home/pi/photobooth folder
copy the Webserver Files to you /var/www/hmtl/demo/
