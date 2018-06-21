# python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.properties import ObjectProperty


Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 1080)
Config.set('graphics', 'height', 1920)


class NonAlcogolic(App):

    def build(self):
        my_screenmanager = ScreenManager()
        screen1 = StartScreen(name='screen1')
        screen2 = Program(name='screen2')
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)

        my_screenmanager.current = 'screen1'
        return my_screenmanager    


class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        #скорее всего, тут нужно использовать картинку. Будет лучше выглядеть.
        startScreen = BoxLayout()

        my_button1 = Button(text="Go to screen 2", on_press=self.changer)
        # my_button1.bind(on_press=self.changer)
        buttonStart = Button(text='Начать не пить', on_press=self.btnPress)

        startScreen.add_widget(buttonStart)
        startScreen.add_widget(my_button1)

    def changer(self,*args):
        self.manager.current = 'screen2'
        
    def btnPress(self):
        #тут должен быть переход на второй активити и запускаться таймеры
        pass


class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        my_button1 = Button(text="Go to screen 1", on_press=self.changer)
        #my_button1.bind(on_press=self.changer)

        self.excuse = ['Я не могу больше пить']

        program = BoxLayout()
        timerOne = Label()
        timerTwo = Label()
        buttonProposal = Button(text='Мне предложили выпить', on_press=self.btnPress)
        
        program.add_widget(timerOne)
        program.add_widget(timerTwo)
        program.add_widget(buttonProposal)
        program.add_widget(my_button1)

    def changer(self, *args):
        self.manager.current = 'screen1'

    def btnPress(self, *args):
        #всплывает попап с отмазкой
        print(self.excuse[0])
        pass


class Menu(BoxLayout):
    def build(self):
        #тут нужно все продумать
        menu = BoxLayout()
        return menu


if __name__ == "__main__":
    NonAlcogolic().run()

