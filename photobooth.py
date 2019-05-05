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
import configparser
from PIL import Image
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE



offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
file_path ="/home/pi/photobooth/" #path of the photobooth programm
server_path="/var/www/html/" #path to the Webserverfiles
debug = False #set to True for debugging

#Variables to change as needed
led_pin = 7    # LED pin
btn_pin = 18   # pin for the button
ausloser = 16
debounce = 0.3 # how long to debounce the button. Add more time if the button triggers too many times.
camera = picamera.PiCamera()
camera.vflip =True
camera.resolution =(2048,1536)



#GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin,GPIO.OUT) # LED 
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button
GPIO.setup(ausloser, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button

# initialize pygame
pygame.init()
if debug is True:
   monitor_w = 320
   monitor_h = 240
   pygame.display.set_mode((monitor_w, monitor_h))
   screen = pygame.display.get_surface()
   pygame.display.set_caption('Photo Booth Pics')
   
else:
   monitor_w, monitor_h = pygame.display.Info().current_w, pygame.display.Info().current_h
   pygame.mouse.set_visible(False) #hide the mouse cursor 
   pygame.display.set_mode((monitor_w, monitor_h))
   screen = pygame.display.get_surface()
   pygame.display.set_caption('Photo Booth Pics')
   pygame.display.toggle_fullscreen()

def show_image(image_path):

	# clear the screen white
	screen.fill( (255,255,255))

	# load the image
	img = pygame.image.load(image_path)
	img = img.convert() 

	# rescale the image to fit the current display
	img = pygame.transform.scale(img, (monitor_w,monitor_h))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

def starting():
    
    shoot()
    show_image(str(file_path)+'media/processing.jpg')    
    camera.stop_preview()
    if debug is True:
       print('Montage')
    subprocess.call("montage -geometry 960x540+ -tile 2x2 -background '#336699' -geometry +50+50 "+str(file_path)+"/image1.jpg "+str(file_path)+"image2.jpg "+str(file_path)+"image3.jpg "+str(file_path)+"montage_temp.jpg", shell=True)
    subprocess.call("composite -gravity center "+str(file_path)+"media/overlay.png  "+str(file_path)+"montage_temp.jpg  "+str(file_path)+"montage.jpg", shell = True)
    # LED a
    zeit=time.strftime('%d-%I.%M.%S') 
    subprocess.call('sudo cp '+str(file_path)+'montage.jpg '+str(server_path)+'images/karte'+zeit+'.jpg', shell=True)
    if debug is True:
        print('collage')
    subprocess.call('sudo convert '+str(file_path)+'montage.jpg -resize 320x240 '+str(server_path)+'thumbs/karte'+zeit+'.jpg',shell=True)
    GPIO.output(7, GPIO.LOW)
    img = Image.open(str(file_path)+'montage.jpg')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tobytes(), size=img.size)
    o.alpha = 255 #128
    o.layer = 3
    
    sleep(5)
    show_image(str(file_path)+'media/intro.jpg')      
    camera.remove_overlay(o)
    del img
    del pad
  
    
    return;
def delete():
    subprocess.call('sudo rm -r '+str(server_path)+'images/*', shell=True)
    subprocess.call('sudo rm -r '+str(server_path)+'thumbs/*', shell=True)
    return;

def shoot():
  y=3
  for x  in range(1,y+1):
    if debug is True:
        print('Foto '+ str(x))
    if x >1:
        show_image(str(file_path)+'media/nextone.jpg')
    else:
        show_image(str(file_path)+'media/getready.jpg')
    sleep(2)
    #camera.iso = 1600
    camera.rotation = 90
    camera.start_preview()
    #for debugging: camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
    countdown_overlay('test')
    show_image(str(file_path)+'media/smile.jpg')
    camera.stop_preview()
    sleep(1)
    camera.capture(str(file_path)+'image'+str(x)+'.jpg')
    img = Image.open(str(file_path)+'image'+str(x)+'.jpg')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tobytes(), size=img.size)
    o.alpha = 128
    o.layer = 3

    #show_image(str(file_path)+'image'+str(x)+'.jpg')
    zeit=time.strftime('%d-%I.%M.%S') 
    subprocess.call('sudo cp '+str(file_path)+'image'+str(x)+'.jpg '+str(server_path)+'images/image'+zeit+'.jpg', shell=True)
    subprocess.call('sudo convert '+str(file_path)+'image'+str(x)+'.jpg -resize 320x240 '+str(server_path)+'thumbs/image'+zeit+'.jpg',shell=True)
    sleep(3)
    camera.remove_overlay(o)
    del img
    del pad
  return;


def countdown_overlay(ggg):
  countdown=4
  
  for i  in range(countdown,0,-1):
   
    img = Image.open(str(file_path)+'media/'+str(i)+'.jpg')
    pad = Image.new('RGB', (
      ((img.size[0] + 31) // 32) * 32,
      ((img.size[1] + 15) // 16) * 16,
      ))
    pad.paste(img, (0, 0))
    o = camera.add_overlay(pad.tobytes(), size=img.size)
    o.alpha = 90 #128
    o.layer = 3
    sleep(1)
    camera.remove_overlay(o)
  del img
  del pad
  return;



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

show_image(str(file_path)+'media/intro.jpg')  
# Dauersschleife
while 1:
  
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
          elif event.key == pygame.K_d:
              delete()
                  
   # LED off
  GPIO.output(7, GPIO.LOW)

  # read GPIO
  if GPIO.input(18) == GPIO.LOW:
    pygame.quit()
    # Warte 100 ms
    time.sleep(0.1)
    
    
  if GPIO.input(16) == GPIO.LOW:
    # goto starting
    GPIO.output(7, GPIO.HIGH)
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
