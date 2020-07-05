from kivy.config import Config
import os

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '500')
Config.set('kivy', 'window_icon', os.getcwd() + '/gfx/match/serve_ball.png')

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
