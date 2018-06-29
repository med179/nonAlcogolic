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

#from kivy.properties import ObjectProperty


#Config.set('graphics', 'resizable', 1)
#Config.set('graphics', 'width', 1080)
#Config.set('graphics', 'height', 1920)


class NonAlcogolic(App):

    def build(self):
        timer = Timer()
        myScreenmanager = ScreenManager()
        startScreen = StartScreen(name='StartScreen')
        secondScreen = SecondScreen(name='SecondScreen', timer = timer)
        programScreen = Program(name='ProgramScreen', timer = timer)
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
        oneDayBtn = Button(text="Один день", size_hint_y=None, size_y=100, on_press=self.changerOneDay)
        oneMonthBtn = Button(text="Один месяц", size_hint_y=None, size_y=100, on_press=self.changerOneMonth)
        oneYearBtn = Button(text="Один год", size_hint_y=None, size_y=100, on_press=self.changerOneYear)
        secondScreenLayout.add_widget(oneDayBtn)
        secondScreenLayout.add_widget(oneMonthBtn)
        secondScreenLayout.add_widget(oneYearBtn)
        self.add_widget(secondScreenLayout)

    #тут сделать рефакторинг
    def changerOneDay(self,*args):
        self.deltaTime = timedelta(1)
        self.manager.current = 'ProgramScreen'

    def changerOneMonth(self,*args):
        self.deltaTime = timedelta(30)
        self.manager.current = 'ProgramScreen'

    def changerOneYear(self,*args):
        self.deltaTime = timedelta(365)
        self.manager.current = 'ProgramScreen'


class Timer():
    pass



class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        self.deltaTime = timedelta(0)
        programLayout = BoxLayout()
        menuButton = Button(text="Menu", size_hint_y=None, size_y=100, on_press=self.changer)
  
        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть', 'Болею, доктор запретил', 'Аллергия']

        #Нужны вызвать метод из другого класса или 
        # просто забрать переменную. ПРи этом нужно помнить, 
        # что экземпляр класса создается в самом начале, до того, 
        # как нажата конопка
        presentDay = date.today()
        #finalDay = presentDay + self.deltaTime


        self.timerOneLbl = Label(text = 'Timer 1')
        self.timerOneLbl.text = "Сегодня" + str(presentDay)
        timerTwoLbl = Label(text = 'Timer 2')
        #timerTwo.text = "Финал" + str(finalDay)
        buttonProposal = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press = self.btnPress)
        programLayout.add_widget(menuButton)       
        programLayout.add_widget(self.timerOneLbl)
        programLayout.add_widget(timerTwoLbl)
        programLayout.add_widget(buttonProposal)
        self.add_widget(programLayout)

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

