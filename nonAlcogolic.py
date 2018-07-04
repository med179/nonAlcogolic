# python
# -*- coding: utf-8 -*-
from kivy.graphics import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from random import randint
from datetime import date, timedelta, datetime
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore
from kivy.graphics.vertex_instructions import RoundedRectangle
from os.path import join
import sys

# Clock.max_iteration = sys.maxint
Clock.max_iteration = 100000


# Нормальные переходы:
# FadeTransition
# WipeTransition
# FallOutTransition ???
# RiseInTransition ???

# from kivy.properties import ObjectProperty


Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 1080)
Config.set('graphics', 'height', 1920)


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        background_color = self.background_color
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(rgba=background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class NonAlcogolic(App):

    def build(self):
        settings = MySettings()
        myScreenmanager = ScreenManager(transition=SlideTransition(direction='up'))
        startScreen = StartScreen(name='StartScreen')
        secondScreen = SecondScreen(name='SecondScreen', settings=settings)
        programScreen = Program(name='ProgramScreen', settings=settings)
        menuScreen = Menu(name='MenuScreen', settings=settings)
        warningOne = WarningOne(name='WarningOne')
        warningTwo = WarningTwo(name='WarningTwo')
        warningThree = WarningThree(name='WarningThree', settings=settings)
        myScreenmanager.add_widget(startScreen)
        myScreenmanager.add_widget(secondScreen)
        myScreenmanager.add_widget(programScreen)
        myScreenmanager.add_widget(menuScreen)
        myScreenmanager.add_widget(warningOne)
        myScreenmanager.add_widget(warningTwo)
        myScreenmanager.add_widget(warningThree)
        if settings.isNotReady:
            myScreenmanager.current = 'StartScreen'
        else:
            myScreenmanager.current = 'ProgramScreen'
        return myScreenmanager


class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        btnLayout = BoxLayout(orientation='horizontal')
        centerColumnLayout = BoxLayout(orientation='vertical')          
        horizontalBlancLayoutOne = Widget(size_hint=[.15, 1])
        horizontalBlancLayoutTwo = Widget(size_hint=[.15, 1])
        verticalBlancLayoutOne = Widget(size_hint=[1, .7])
        verticalBlancLayoutTwo = Widget(size_hint=[1, .07])
        firstBtn = RoundedButton(
            text="[size=50][font=Roboto][b]ПЕРЕСТАТЬ ПИТЬ![/b][/font][/size]",
            markup=True,
            size_hint=[1, .06],
            background_color=(.0, .84, .84, 1),
            # background_normal='',
            on_press=self.changer
            )
        btnLayout.add_widget(horizontalBlancLayoutOne)
        centerColumnLayout.add_widget(verticalBlancLayoutOne)        
        centerColumnLayout.add_widget(firstBtn)
        centerColumnLayout.add_widget(verticalBlancLayoutTwo) 
        btnLayout.add_widget(centerColumnLayout)
        btnLayout.add_widget(horizontalBlancLayoutTwo)

        self.add_widget(btnLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changer(self, *args):
        self.manager.current = 'SecondScreen'


class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        secondScreenLayout = BoxLayout(orientation='horizontal')
        horizontalBlancLayoutOne = Widget(size_hint=[.25, 1])
        horizontalBlancLayoutTwo = Widget(size_hint=[.25, 1])
        buttonsLayout = BoxLayout(orientation='vertical', spacing = 10, size_hint=[1, .3])
        oneWeekBtn = Button(text="Одну неделю", size_hint=[.33, .1], on_press=self.changerOneWeek)
        oneMonthBtn = Button(text="Один месяц", size_hint=[.5, .1], on_press=self.changerOneMonth)
        oneYearBtn = Button(text="Один год", size_hint=[.5, .1], on_press=self.changerOneYear)
        secondScreenLayout.add_widget(horizontalBlancLayoutOne)

        buttonsLayout.add_widget(oneWeekBtn)
        buttonsLayout.add_widget(oneMonthBtn)
        buttonsLayout.add_widget(oneYearBtn)
        secondScreenLayout.add_widget(buttonsLayout)
        
        secondScreenLayout.add_widget(horizontalBlancLayoutTwo)
       
        self.add_widget(secondScreenLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def setDateParameters(self, days):
        self.manager.current = 'ProgramScreen'
        self.settings.startDay = datetime.now()
        self.settings.finalDay = date.today() + timedelta(days)

    def changerOneWeek(self, *args):
        self.setDateParameters(7)

    def changerOneMonth(self, *args):
        self.setDateParameters(30)

    def changerOneYear(self, *args):
        self.setDateParameters(365)


class MySettings(object):
    __finalDay = None
    __startDay = None
    __count = 0
    __isNotReady = True
    __store = None

    def __init__(self):
        self.__store = DictStore('user.dat')
        if self.__store.store_exists('startDay') and self.__store.get('startDay')['data']:
            self.__startDay = self.__store.get('startDay')['data']
            self.__finalDay = self.__store.get('finalDay')['data']
            self.__count = self.__store.get('count')['data']
            self.__isNotReady = False
        else:
            self.__isNotReady = True
            self.__store.put('count', data=0)

    def parseDate(self, dateText):
        if dateText:
            return datetime.strptime(dateText, "%S-%M-%H %d-%m-%Y")
        else:
            None

    def __getattr__(self, attr):
        if attr == 'isNotReady':
            return self.__isNotReady
        if attr == 'startDay':
            return self.parseDate(self.__startDay)
        if attr == 'finalDay':
            return self.parseDate(self.__finalDay)
        if attr == 'counter':
            return self.__count
        return None

    def __setattr__(self, key, value):
        if key == 'startDay':
            if value:
                self.__startDay = value.strftime("%S-%M-%H %d-%m-%Y")
            else:
                self.__startDay = value
            self.__store.put('startDay', data=self.__startDay)
            return
        if key == 'finalDay':
            if value:
                self.__finalDay = value.strftime("%S-%M-%H %d-%m-%Y")
            else:
                self.__finalDay = value
            self.__store.put('finalDay', data=self.__finalDay)
            return
        if key == 'counter':
            self.__count = value
            self.__store.put('count', data=value)
            return
        super(MySettings, self).__setattr__(key, value)

class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        programLayout = BoxLayout(orientation='vertical')
        menuButton = Button(text="Menu", size_hint_y=None, size_y=100, on_press=self.changer)
        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть',
                       'Болею, доктор запретил', 'Аллергия']
        self.counterLbl = Label(text='Получено предложений выпить: ' + str(self.settings.counter))
        self.timerGoneLbl = Label(text='')
        self.timerLeftLbl = Label(text='')
        buttonProposal = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press=self.btnPress)
        programLayout.add_widget(menuButton)
        programLayout.add_widget(self.counterLbl)
        programLayout.add_widget(self.timerGoneLbl)
        programLayout.add_widget(self.timerLeftLbl)
        programLayout.add_widget(buttonProposal)
        self.add_widget(programLayout)
        Clock.schedule_interval(self.updateLabels, 1)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def updateLabels(self, *args):
        if self.settings.finalDay:
            currentDate = datetime.now()
            diffGone = currentDate - self.settings.startDay
            diffLeft = self.settings.finalDay - currentDate
            self.timerGoneLbl.text = self.getTextCountGone(diffGone)
            self.timerLeftLbl.text = self.getTextCountLeft(diffLeft)
            self.counterLbl.text = 'Получено предложений выпить: ' + str(self.settings.counter)

    def getNumOfVariant(self, num):
        chk = num % 10
        if chk == 1 and num != 11:
            return 0
        if 1 < chk < 5 and not [12, 13, 14].__contains__(num):
            return 1
        return 2

    def getTextCountGone(self, diff):
        secondsNames = [' секунда ', ' секунды ', ' секунд ']
        minutesNames = [' минута ', ' минуты ', ' минут ']
        hoursNames = [' час ', ' часа ', ' часов ']
        if diff.days <= 0:
            if diff.seconds < 60:
                return 'Прошло ' + str(diff.seconds) + secondsNames[self.getNumOfVariant(diff.seconds)]
            else:
                diffMinutes = diff.seconds / 60
                diffHours = diffMinutes / 60
                return 'Прошло ' + str(diffMinutes / 60) + hoursNames[self.getNumOfVariant(diffHours)] + str(diffMinutes) + minutesNames[self.getNumOfVariant(diffMinutes)]
        else:
            return 'Прошло дней: ' + str(diff.days)

    def getTextCountLeft(self, diff):
        return 'Осталось дней: ' + str(diff.days)

    def changer(self, *args):
        self.manager.current = 'MenuScreen'

    def btnPress(self, *args):
        self.settings.counter += 1
        # всплывает попап с отмазкой
        numberOfExuse = self.excuse[randint(0, len(self.excuse) - 1)]
        popup = Popup(title="Отмазка на сегодня",
                      separator_color=(0, 0, 1, 1),
                      content=Label(
                          text='[color=33ff33][b]' + str(numberOfExuse) + '[/b][/color]',
                          markup=True,
                          font_size=20),
                      size_hint=(.7, .5))
        popup.open()
        print(self.excuse[0])
        pass


class Menu(Screen):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        menuScreenLayout = BoxLayout(orientation='vertical')
        returnToProgramBtn = Button(text="Закрыть меню", size_hint_y=None, size_y=100, on_press=self.changer)
        iWantToDrinkBtn = Button(text="Перестать не пить", size_hint_y=None, size_y=100, on_press=self.changerWarningOneScr)
        iDrankItBtn = Button(text="Я выпил", size_hint_y=None, size_y=100, on_press=self.changer)
        menuScreenLayout.add_widget(returnToProgramBtn)
        menuScreenLayout.add_widget(iWantToDrinkBtn)
        menuScreenLayout.add_widget(iDrankItBtn)
        self.add_widget(menuScreenLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changer(self, *args):
        self.settings.startDay = datetime.now()
        self.manager.current = 'ProgramScreen'

    def changerWarningOneScr(self, *args):
        self.manager.current = 'WarningOne'


class WarningOne(Screen):
    def __init__(self, **kwargs):
        super(WarningOne, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='Ты же обещал не пить! Мужик всегда держит слово. Ты что, не мужик?', halign='center', valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Я не мужик", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Ok, не буду пить.", size_hint_y=None, size_y=100, on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerNext(self, *args):
        self.manager.current = 'WarningTwo'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


class WarningTwo(Screen):
    def __init__(self, **kwargs):
        super(WarningTwo, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='Как ты потом будешь смотреть в глаза своим друзьям, которые верили тебе?', halign='center', valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Никак, я дерьмо.", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Ладно, я передумал. Не буду пить.", size_hint_y=None, size_y=100, on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerNext(self, *args):
        self.manager.current = 'WarningThree'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


class WarningThree(Screen):
    def __init__(self, **kwargs):
        super(WarningThree, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1.0 / 255.0, 172.0 / 255.0, 194.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='И после этого ты считаешь себя альфасамцом?', halign='center', valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Нет, я лох.", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Я не буду так больше. Извините.", size_hint_y=None, size_y=100, on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerNext(self, *args):
        self.settings.startDay = None
        self.settings.finalDay = None
        self.settings.counter = 0
        self.manager.current = 'StartScreen'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


if __name__ == "__main__":
    NonAlcogolic().run()
