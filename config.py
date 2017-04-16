#Config settings to change behavior of photo booth
monitor_w = 320    # width of the display monitor
monitor_h = 240    # height of the display monitor
file_path = '/home/pi/photobooth/' # path of the photobooth program
server_path = '/var/www/html/demo/' # path to save images
debounce = 0.3 # how long to debounce the button. Add more time if the button triggers too many times.
camera_iso = 800    # adjust for lighting issues. Normal is 100 or 200. Sort of dark is 400. Dark is 800 max.
                    # available options: 100, 200, 320, 400, 500, 640, 800
