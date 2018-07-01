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
from random import randint
from datetime import date, timedelta
from kivy.clock import Clock
import sys

Clock.max_iteration = sys.maxint



#from kivy.properties import ObjectProperty


#Config.set('graphics', 'resizable', 1)
#Config.set('graphics', 'width', 1080)
#Config.set('graphics', 'height', 1920)


class NonAlcogolic(App):

    def build(self):
        settings = Settings()
        
        myScreenmanager = ScreenManager()
        startScreen = StartScreen(name='StartScreen')
        secondScreen = SecondScreen(name='SecondScreen', settings = settings)
        programScreen = Program(name='ProgramScreen', settings = settings)
        menuScreen = Menu(name='MenuScreen')


        myScreenmanager.add_widget(startScreen)
        myScreenmanager.add_widget(secondScreen)
        myScreenmanager.add_widget(programScreen)
        myScreenmanager.add_widget(menuScreen)
        return myScreenmanager
    
    
class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        startScreenLayout = BoxLayout()
        firstBtn = Button(text="Начать не пить!!!", size_hint_y=None, size_y=100, on_press=self.changer)
        startScreenLayout.add_widget(firstBtn)
        self.add_widget(startScreenLayout)

    def changer(self,*args):
        self.manager.current = 'SecondScreen'

  
class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.settings = kwargs['settings']   
        secondScreenLayout = BoxLayout()
        oneWeekBtn = Button(text="Одну неделю", size_hint_y=None, size_y=100, on_press=self.changerOneWeek)
        oneMonthBtn = Button(text="Один месяц", size_hint_y=None, size_y=100, on_press=self.changerOneMonth)
        oneYearBtn = Button(text="Один год", size_hint_y=None, size_y=100, on_press=self.changerOneYear)
        secondScreenLayout.add_widget(oneWeekBtn)
        secondScreenLayout.add_widget(oneMonthBtn)
        secondScreenLayout.add_widget(oneYearBtn)
        self.add_widget(secondScreenLayout)

    def setDateParameters(self, days):     
        self.manager.current = 'ProgramScreen'
        self.settings.startDay = date.today()
        self.settings.finalDay = self.settings.startDay + timedelta(days)

    def changerOneWeek(self,*args):
        self.setDateParameters(7)

    def changerOneMonth(self,*args):
        self.setDateParameters(30)

    def changerOneYear(self,*args):
        self.setDateParameters(365)


class Settings():
    finalDay = date.today()
    startDay = date.today()



class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        self.settings = kwargs['settings']   
        programLayout = BoxLayout()
        menuButton = Button(text="Menu", size_hint_y=None, size_y=100, on_press=self.changer)
        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть', 'Болею, доктор запретил', 'Аллергия']
        self.timerGoneLbl = Label(text = 'Timer 1')
        self.timerLeftLbl = Label(text = 'Timer 2')
        buttonProposal = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press = self.btnPress)
        programLayout.add_widget(menuButton)       
        programLayout.add_widget(self.timerGoneLbl)
        programLayout.add_widget(self.timerLeftLbl)
        programLayout.add_widget(buttonProposal)
        self.add_widget(programLayout)
        Clock.schedule_interval(self.updateLabels, 1)

    def updateLabels(self, *args):
        currentDate = date.today()
        self.timerGoneLbl.text = 'Прошло дней: ' + str((currentDate - self.settings.startDay).days)
        self.timerLeftLbl.text = 'Осталось дней: ' + str((self.settings.finalDay - currentDate).days)

    def changer(self, *args):
        self.manager.current = 'MenuScreen'

    def btnPress(self, *args):
        #всплывает попап с отмазкой
        numberOfExuse = self.excuse[randint(0, len(self.excuse) - 1)]
        popup = Popup(title= "Отмазка на сегодня",
                separator_color = (0, 0, 1, 1),  
                content = Label(
                text='[color=33ff33][b]' + str(numberOfExuse) + '[/b][/color]', 
                markup = True, 
                font_size = 20), 
                size_hint = (.7, .5))
        popup.open()
        print(self.excuse[0])
        pass


class Menu(Screen):
    
    def __init__(self, **kwargs):
            super(Menu, self).__init__(**kwargs)           
            menuScreenLayout = BoxLayout()
            returnToProgramBtn = Button(text="Закрыть меню", size_hint_y=None, size_y=100, on_press=self.changer)
            menuScreenLayout.add_widget(returnToProgramBtn)
            self.add_widget(menuScreenLayout)
    
    def changer(self,*args):
        self.manager.current = 'ProgramScreen'


if __name__ == "__main__":
    NonAlcogolic().run()

