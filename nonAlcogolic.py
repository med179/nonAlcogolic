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
        my_screenmanager = ScreenManager()
        timer = Timer()
        screen1 = StartScreen(name = 'StartScreen')
        screen3 = Program(name = 'ProgramScreen', timer = timer)
        screen2 = SecondScreen(name = 'SecondScreen', timer = timer, data = screen3)
        screen4 = Menu(name = 'MenuScreen', timer = timer)
        my_screenmanager.add_widget(screen1)
        my_screenmanager.add_widget(screen2)
        my_screenmanager.add_widget(screen3)
        my_screenmanager.add_widget(screen4)
        return my_screenmanager

class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        
        startScreen = BoxLayout()

        firstButton = Button(
            text="Начать не пить!!!", 
            size_hint_y=None, 
            size_y=100
            )
        firstButton.bind(on_press=self.changer)

        startScreen.add_widget(firstButton)
        self.add_widget(startScreen)


    def changer(self,*args):
        self.manager.current = 'SecondScreen'


class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.presentDay = date.today()

        secondScreen = BoxLayout()

        oneDay = Button(
            text="Один день", 
            size_hint_y=None, 
            size_y=100,
            on_press=self.changerOneDay
            )
        
        oneMonth = Button(
            text="Один месяц", 
            size_hint_y=None, 
            size_y=100,
            on_press=self.changerOneMonth
            )

        oneYear = Button(
            text="Один год", 
            size_hint_y=None, 
            size_y=100,
            on_press=self.changerOneYear            
            )

        secondScreen.add_widget(oneDay)
        secondScreen.add_widget(oneMonth)
        secondScreen.add_widget(oneYear)
        self.add_widget(secondScreen)


    def changerOneDay(self,*args):
        self.deltaTime = timedelta(1)
        self.manager.current = 'ProgramScreen'
        self.timerOne.text = "Сегодня TEST" + str(self.presentDay)

    def changerOneMonth(self,*args):
        self.deltaTime = timedelta(30)
        self.manager.current = 'ProgramScreen'
        self.timerOne.text = "Сегодня TEST" + str(self.presentDay)

    def changerOneYear(self,*args):
        self.deltaTime = timedelta(365)
        self.manager.current = 'ProgramScreen'
        self.timerOne.text = "Сегодня TEST" + str(self.presentDay)


class Timer():
    def build(self, *args):
        pass


class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        self.deltaTime = timedelta(0)
        program = BoxLayout()
        menuButton = Button(
            text="Menu", 
            size_hint_y=None, 
            size_y=100
            )
        menuButton.bind(on_press=self.changer)

        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть', 'Болею, доктор запретил', 'Аллергия']
        #Нужны вызвать метод из другого класса или 
        # просто забрать переменную. ПРи этом нужно помнить, 
        # что экземпляр класса создается в самом начале, до того, 
        # как нажата конопка
        presentDay = date.today()
        #finalDay = presentDay + self.deltaTime


        self.timerOne = Label(text = 'Timer 1')
        self.timerOne.text = "Сегодня" + str(presentDay)
        timerTwo = Label(text = 'Timer 2')
        #timerTwo.text = "Финал" + str(finalDay)
        buttonProposal = Button(
            text='Мне предложили выпить', 
            size_hint_y=None, 
            size_y=100,
            on_press = self.btnPress
            )
        program.add_widget(menuButton)       
        program.add_widget(self.timerOne)
        program.add_widget(timerTwo)
        program.add_widget(buttonProposal)
        self.add_widget(program)

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
            
            menuScreen = BoxLayout()

            returnToProgramButton = Button(
                text="Закрыть меню", 
                size_hint_y=None, 
                size_y=100
                )
            returnToProgramButton.bind(on_press=self.changer)

            menuScreen.add_widget(returnToProgramButton)
            self.add_widget(menuScreen)
    
    def changer(self,*args):
        self.manager.current = 'ProgramScreen'


if __name__ == "__main__":
    NonAlcogolic().run()

