import os

app_title = 'Digital Volleyball Assistant'
app_version = '0.1.0'
app_resizable = False
app_width = 700
app_height = 500
app_icon_path = os.getcwd() + '/gfx/match/serve_ball.png'
app_background_picture = 'classic'
language_code = 1
server_ip = 'http://httpbin.org'
no_internet_method = 'popup' # either popup or 'loop' for stacking requests into a queue to be sent later while main loops continues.
# Hasn't been tested yet. #TODO integrate it (time out for requests, notification bar, queue)
