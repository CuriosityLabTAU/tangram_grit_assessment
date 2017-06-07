from interaction_control import *
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window

from kivy.app import App
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

class PartyScreenRoom(Screen):
    the_tablet = None

    def __init__(self, the_tablet):
        self.the_tablet = the_tablet
        super(Screen, self).__init__()

    def on_enter(self, *args):
        print("on_enter first_screen_room")
        self.the_tablet.change_state('party_screen')


    def init_balloons(self, tangrams_solved):
        # display the number of tangrams solved (by the Robot and Child).
        i = 0
        # for balloon in self.ids['balloons_won_widget'].ids:
        while i < 12:
            i += 1
            if (i <= tangrams_solved):
                self.ids['party_screen_balloons_widget'].ids["balloon" + str(i)].opacity = 1
                print("visible", i)
            else:
                self.ids['party_screen_balloons_widget'].ids["balloon" + str(i)].opacity = 0
                print("invisible", i)




class PartyScreenBackground(Widget):
    pass

class PartyScreenBalloonsWidget(Widget):
    pass

