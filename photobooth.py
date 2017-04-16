#!/usr/bin/env python
import os
import glob
import RPi.GPIO as GPIO
from time import sleep
import atexit
import picamera
import time
import subprocess
import os
from PIL import Image
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


#############################
### Variables that Change ###
#############################
# Do not change these variables, as the code will change it anyway
monitor_w = 1024   # width of the display monitor
monitor_h = 768   # height of the display monitor
transform_x = monitor_w # how wide to scale the jpg when replaying
transfrom_y = monitor_h # how high to scale the jpg when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
file_path ="/home/pi/photobooth/" #path of the photobooth programm
server_path="/var/www/html/" #path to the Webserverfiles

# initialize pygame
pygame.init()
pygame.display.set_mode((monitor_w, monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption('Photo Booth Pics')
pygame.mouse.set_visible(False) #hide the mouse cursor
pygame.display.toggle_fullscreen()
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (monitor_w * img_h) / img_w 

    if (ratio_h < monitor_h):
        #Use horizontal black bars
        #print "horizontal black bars"
        transform_y = ratio_h
        transform_x = monitor_w
        offset_y = (monitor_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > monitor_h):
        #Use vertical black bars
        #print "vertical black bars"
        transform_x = (config.monitor_h * img_w) / img_h
        transform_y = config.monitor_h
        offset_x = (config.monitor_w - transform_x) / 2
        offset_y = 0
    else:
        #No need for black bars as photo ratio equals screen ratio
        #print "no black bars"
        transform_x = config.monitor_w
        transform_y = config.monitor_h
        offset_y = offset_x = 0

    # uncomment these lines to troubleshoot screen ratios
#     print str(img_w) + " x " + str(img_h)
#     print "ratio_h: "+ str(ratio_h)
#     print "transform_x: "+ str(transform_x)
#     print "transform_y: "+ str(transform_y)
#     print "offset_y: "+ str(offset_y)
#     print "offset_x: "+ str(offset_x)

# display one image on screen

def show_image(image_path):

	# clear the screen
	screen.fill( (0,0,0) )

	# load the image
	img = pygame.image.load(image_path)
	img = img.convert() 

	# set pixel dimensions based on image
	set_demensions(img.get_width(), img.get_height())

	# rescale the image to fit the current display
	img = pygame.transform.scale(img, (transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

def starting():
    camera.start_preview()
    shoot()
    GPIO.output(7, GPIO.HIGH) 
    img = Image.open(str(file_path)+'processing.png')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tostring(), size=img.size)
    o.alpha = 255 #128
    o.layer = 3
    
    print('Montage')
    subprocess.call("montage -geometry 960x540+ -tile 2x2 -background '#336699' -geometry +50+50 "+str(file_path)+"/image1.jpg "+str(file_path)+"image2.jpg "+str(file_path)+"image3.jpg "+str(file_path)+"montage_temp.jpg", shell=True)
    subprocess.call("composite -gravity center "+str(file_path)+"overlay.png  "+str(file_path)+"montage_temp.jpg  "+str(file_path)+"montage.jpg", shell = True)
    # LED a
    zeit=time.strftime('%d-%I.%M.%S') 
    subprocess.call('cp '+str(file_path)+'montage.jpg '+str(server_path)+'images/karte'+zeit+'.jpg', shell=True)
    print('collage')
    subprocess.call('convert '+str(file_path)+'montage.jpg -resize 320x240 '+str(server_path)+'thumbs/karte'+zeit+'.jpg',shell=True)
    GPIO.output(7, GPIO.LOW)
    camera.remove_overlay(o)
    del img
    del pad
    img = Image.open(str(file_path)+'montage.jpg')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tostring(), size=img.size)
    o.alpha = 255 #128
    o.layer = 3
    sleep(5)
    camera.remove_overlay(o)
    del img
    del pad
  
    camera.stop_preview()
    return;
	
def shoot():
  y=3
  for x  in range(1,y+1):
    print('Foto '+ str(x))
    countdown_overlay('test')
    camera.capture(str(file_path)+'image'+str(x)+'.jpg')
    zeit=time.strftime('%d-%I.%M.%S') 
    subprocess.call('cp '+str(file_path)+'image'+str(x)+'.jpg '+str(server_path)+'images/image'+zeit+'.jpg', shell=True)
    subprocess.call('convert '+str(file_path)+'image'+str(x)+'.jpg -resize 320x240 '+str(server_path)+'thumbs/image'+zeit+'.jpg',shell=True)

    sleep(1)
  return;

def countdown_overlay(ggg):
  n=4
  for i  in range(1,n+1):
	#gc.collect()
    img = Image.open(str(file_path)+str(i)+'.png')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tostring(), size=img.size)
    o.alpha = 100 #128
    o.layer = 3
    sleep(1)
    camera.remove_overlay(o)
  del img
  del pad
  return;

#Variables to change as needed
led_pin = 7    # LED pin
btn_pin = 18   # pin for the button
ausloser = 16
debounce = 0.3 # how long to debounce the button. Add more time if the button triggers too many times.
camera = picamera.PiCamera()
camera.vflip =True
camera.resolution =(1024,768)


#GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin,GPIO.OUT) # LED 
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button
GPIO.setup(ausloser, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button

def cleanup():
  print('Goodbye.')
  GPIO.cleanup()
atexit.register(cleanup) 

run_state = False
def check_light():
	if run_state:
		GPIO.output(led_pin,True)
		print("LED on")
		camera.start_preview()
	else:
		GPIO.output(led_pin,False)
		print("LED off")
		camera.stop_preview()
		
print('Push Button')
print('Press Ctrl+C to exit')

# Dauersschleife
while 1:
  show_image(str(file_path)+'intro.jpg')
  for event in pygame.event.get():
  # Spiel beenden, wenn wir ein QUIT-Event finden.
      if event.type == pygame.QUIT:
          running = False
          pygame.quit()
 
            # Wir interessieren uns auch für "Taste gedrückt"-Events.
      if event.type == pygame.KEYDOWN:
                # Wenn Escape gedrückt wird, posten wir ein QUIT-Event in Pygames Event-Warteschlange.
          if event.key == pygame.K_ESCAPE:
              pygame.event.post(pygame.event.Event(pygame.QUIT))
              pygame.quit()
          elif event.key == pygame.K_SPACE:
              starting()
   # LED immer ausmachen
  GPIO.output(7, GPIO.LOW)

  # GPIO lesen
  if GPIO.input(18) == GPIO.LOW:
    # LED an
    GPIO.output(7, GPIO.HIGH)
    pygame.quit()
    # Warte 100 ms
    time.sleep(0.1)
    
    
  if GPIO.input(16) == GPIO.LOW:
    # LED an
    starting()

   
    


try:	
	while True:
		GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
		sleep(debounce)
		if run_state:
			run_state = False
		else:
			run_state = True
		print("Button pressed")
		check_light()
except KeyboardInterrupt:
	print('\nScript Exited.')
