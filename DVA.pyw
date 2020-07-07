from kivy.config import Config
from meta.app_config import app_icon_path, app_resizable, app_width, app_height

Config.set('graphics', 'resizable', app_resizable)
Config.set('graphics', 'width', app_width)
Config.set('graphics', 'height', app_height)
Config.set('kivy', 'window_icon', app_icon_path)

from gfx.frontend import Application, ScreenManager
from py.core import load_log
from py.objects import Log, Request

logs = [] # It needs to be in here because there are calls made to it outside of main scope.
sm = ScreenManager()

if __name__ == '__main__':

    load_log('Match_Events', False)
    load_log('Requests', True)

    Digital_Volleyball_Assistant = Application()
    Digital_Volleyball_Assistant.run()
