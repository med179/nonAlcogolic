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
from datetime import date
#from kivy.properties import ObjectProperty


#Config.set('graphics', 'resizable', 1)
#Config.set('graphics', 'width', 1080)
#Config.set('graphics', 'height', 1920)


class NonAlcogolic(App):

    def build(self):
        myScreenmanager = ScreenManager()
        startScreen = StartScreen(name='StartScreen')
        secondScreen = SecondScreen(name='SecondScreen')
        programScreen = Program(name='ProgramScreen')
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
        secondScreenLayout = BoxLayout()
        oneDayBtn   = Button(text="Один день", size_hint_y=None, size_y=100, on_press=self.changerOneDay)
        oneMonthBtn = Button(text="Один месяц", size_hint_y=None, size_y=100, on_press=self.changerOneMonth)
        oneYearBtn = Button(text="Один год", size_hint_y=None, size_y=100, on_press=self.changerOneYear)
        secondScreenLayout.add_widget(oneDayBtn)
        secondScreenLayout.add_widget(oneMonthBtn)
        secondScreenLayout.add_widget(oneYearBtn)
        self.add_widget(secondScreenLayout)

    def changerOneDay(self,*args):
        self.deltaTime = date(0, 0, 1)
        self.manager.current = 'ProgramScreen'
        
    def changerOneMonth(self,*args):
        self.deltaTime = date(0, 1, 0)
        self.manager.current = 'ProgramScreen'
        
    def changerOneYear(self,*args):
        self.deltaTime = date(1, 0, 0)
        self.manager.current = 'ProgramScreen'

        
class Program(Screen):

    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)       
        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть', 'Болею, доктор запретил', 'Аллергия']

        programLayout = BoxLayout()
        timerOneLbl = Label(text = 'Timer 1')
        timerTwoLbl = Label(text = 'Timer 2')
        menuBtn = Button(text="Menu", size_hint_y=None, size_y=100, on_press=self.changer)
        proposalBtn = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press = self.btnPress)
        programLayout.add_widget(menuBtn)       
        programLayout.add_widget(timerOneLbl)
        programLayout.add_widget(timerTwoLbl)
        programLayout.add_widget(proposalBtn)
        self.add_widget(programLayout)
        
        # эту бурду в другой метод
        presentDay = date.today()
        finalDay = presentDay + self.deltaTime
        timerOneLbl.text = "Сегодня" + str(presentDay)
        timerTwoLbl.text = "Финал" + str(finalDay)
        
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

