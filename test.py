# python
# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
#from kivy.properties import ObjectProperty

class ScreenOne(Screen):

    def __init__ (self,**kwargs):
        super (ScreenOne, self).__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        my_label1 = Label(text="BlaBlaBla on screen 1", font_size='24dp')
        my_button1 = Button(text="Go to screen 2",size_hint_y=None, size_y=100)
        my_button1.bind(on_press=self.changer)
        my_box1.add_widget(my_label1)
        my_box1.add_widget(my_button1)
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current = 'screen2'

class ScreenTwo(Screen):

    def __init__(self,**kwargs):
        super (ScreenTwo,self).__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        my_label1 = Label(text="BlaBlaBla on screen 2",font_size='24dp')
        my_button1 = Button(text="Go to screen 1",size_hint_y=None, size_y=100)
        my_button1.bind(on_press=self.changer)
        my_box1.add_widget(my_label1)
        my_box1.add_widget(my_button1)
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current = 'screen1'

class TestApp(App):

        def build(self):
            my_screenmanager = ScreenManager()
            screen1 = ScreenOne(name='screen1')
            screen2 = ScreenTwo(name='screen2')
            my_screenmanager.add_widget(screen1)
            my_screenmanager.add_widget(screen2)
            return my_screenmanager

if __name__ == '__main__':
    TestApp().run()