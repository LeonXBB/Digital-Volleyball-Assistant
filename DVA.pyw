'''
Main script of the app. It is responsible for starting the application, creating and configuring GUI 
window, as well as loading and (if necessary) restoring logs, as well as creating screen manager for the
GUI.

First, we're setting window's  graphical parameters, including its resizableness and icon, according to
app config.
Then, we create logs list and screen manager. They need to be available as they are called from other 
places, so they not under '__main__' name.
After that, if said name is actually '__main__', we load logs using respective core funtion, and creating
and running the app itself.
'''

from kivy.config import Config
from meta.app_config import app_icon_path, app_resizable, app_width, app_height

Config.set('graphics', 'resizable', app_resizable)
Config.set('graphics', 'width', app_width)
Config.set('graphics', 'height', app_height)
Config.set('kivy', 'window_icon', app_icon_path)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from gfx.frontend import Application, ScreenManager
from py.core import load_log

logs = []
sm = ScreenManager()

if __name__ == '__main__':

    load_log('Match_Events', False)
    load_log('Requests', True)

    Digital_Volleyball_Assistant = Application()
    Digital_Volleyball_Assistant.run()
