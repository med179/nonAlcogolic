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
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from random import randint
from datetime import date, timedelta, datetime
from kivy.clock import Clock
import sys

Clock.max_iteration = sys.maxint


# Нормальные переходы:
# FadeTransition
# WipeTransition
# FallOutTransition ???
# RiseInTransition ???

# from kivy.properties import ObjectProperty


# Config.set('graphics', 'resizable', 1)
# Config.set('graphics', 'width', 1080)
# Config.set('graphics', 'height', 1920)


class NonAlcogolic(App):
    # def build_config(self, config):
    #    config.setdefaults('section1', {
    #        'startDay': date.today(),
    #        'finalDay': date.today()
    #    })

    def build(self):
        settings = Settings(self.config)
        myScreenmanager = ScreenManager(transition=SlideTransition(direction='up'))
        startScreen = StartScreen(name='StartScreen')
        secondScreen = SecondScreen(name='SecondScreen', settings=settings)
        programScreen = Program(name='ProgramScreen', settings=settings)
        menuScreen = Menu(name='MenuScreen')
        warningOne = WarningOne(name='WarningOne')
        warningTwo = WarningTwo(name='WarningTwo')
        warningThree = WarningThree(name='WarningThree')
        myScreenmanager.add_widget(startScreen)
        myScreenmanager.add_widget(secondScreen)
        myScreenmanager.add_widget(programScreen)
        myScreenmanager.add_widget(menuScreen)
        myScreenmanager.add_widget(warningOne)
        myScreenmanager.add_widget(warningTwo)
        myScreenmanager.add_widget(warningThree)
        if(settings.isNotReady):
            myScreenmanager.current = 'StartScreen'
        else:
            myScreenmanager.current = 'ProgramScreen'
        return myScreenmanager


class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        startScreenLayout = BoxLayout(orientation='vertical')
        firstBtn = Button(text="Начать не пить!!!", size_hint_y=None, size_y=100, on_press=self.changer)
        startScreenLayout.add_widget(firstBtn)
        self.add_widget(startScreenLayout)

    def changer(self, *args):
        self.manager.current = 'SecondScreen'


class SecondScreen(Screen):

    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.settings = kwargs['settings']
        secondScreenLayout = BoxLayout(orientation='vertical')
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

    def changerOneWeek(self, *args):
        self.setDateParameters(7)

    def changerOneMonth(self, *args):
        self.setDateParameters(30)

    def changerOneYear(self, *args):
        self.setDateParameters(365)


class Settings:
    def __init__(self, config):
        self.config = config
        self._finalDay = Config.getdefault('nonalco', 'startDay', None)
        self._startDay = Config.getdefault('nonalco', 'finalDay', None)
        self._isNotReady = False

    def parseDate(dateText):
        if dateText:
            return datetime
        else:
            None

    def __getattr__(self, item):
        if item == 'isNotReady':
            return self._isNotReady
        if item == 'startDay':
            return Settings.parseDate(self._startDay)
        if item == 'finalDay':
            return Settings.parseDate(self._finalDay)
        raise AttributeError

    def __setattr__(self, key, value):
        if key == 'startDay':
            self._startDay = value
        if key == 'finalDay':
            self._finalDay = value


class Program(Screen):
    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        self.counter = 0
        self.settings = kwargs['settings']
        programLayout = BoxLayout(orientation='vertical')
        menuButton = Button(text="Menu", size_hint_y=None, size_y=100, on_press=self.changer)
        self.excuse = ['Я не могу больше пить', 'Принимаю антибиотки, нельзя смешивать с алкоголем - можно сдохнуть',
                       'Болею, доктор запретил', 'Аллергия']
        self.counterLbl = Label(text='Получено предложений выпить: 0')
        self.timerGoneLbl = Label(text='Timer 1')
        self.timerLeftLbl = Label(text='Timer 2')
        buttonProposal = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press=self.btnPress)
        programLayout.add_widget(menuButton)
        programLayout.add_widget(self.counterLbl)
        programLayout.add_widget(self.timerGoneLbl)
        programLayout.add_widget(self.timerLeftLbl)
        programLayout.add_widget(buttonProposal)
        self.add_widget(programLayout)
        Clock.schedule_interval(self.updateLabels, 1)

    def updateLabels(self, *args):
        currentDate = date.today()
        self.timerGoneLbl.text = 'Прошло дней: ' + str((currentDate - self.settings.startDay).days)
        self.timerLeftLbl.text = 'Осталось дней: ' + str((self.settings.finalDay - currentDate).days)
        self.counterLbl.text = 'Получено предложений выпить: ' + str(self.counter)

    def changer(self, *args):
        self.manager.current = 'MenuScreen'

    def btnPress(self, *args):
        self.counter += 1
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
        menuScreenLayout = BoxLayout(orientation='vertical')
        returnToProgramBtn = Button(text="Закрыть меню", size_hint_y=None, size_y=100, on_press=self.changer)
        iWantToDrinkBtn = Button(text="Я хочу выпить", size_hint_y=None, size_y=100, on_press=self.changerWarningOneScr)
        iDrankItBtn = Button(text="Я выпил", size_hint_y=None, size_y=100, on_press=self.changer)
        menuScreenLayout.add_widget(returnToProgramBtn)
        menuScreenLayout.add_widget(iWantToDrinkBtn)
        menuScreenLayout.add_widget(iDrankItBtn)
        self.add_widget(menuScreenLayout)

    def changer(self, *args):
        self.manager.current = 'ProgramScreen'

    def changerWarningOneScr(self, *args):
        self.manager.current = 'WarningOne'


class WarningOne(Screen):
    def __init__(self, **kwargs):
        super(WarningOne, self).__init__(**kwargs)
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='Ты же обещал не пить! Мужик всегда держит слово. Ты что, не мужик?', halign='center',
                          valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Я не мужик", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Ok, не буду пить.", size_hint_y=None, size_y=100, on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)

    def changerNext(self, *args):
        self.manager.current = 'WarningTwo'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


class WarningTwo(Screen):
    def __init__(self, **kwargs):
        super(WarningTwo, self).__init__(**kwargs)
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='Как ты потом будешь смотреть в глаза своим друзьям, которые верили тебе?',
                          halign='center', valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Никак, я дерьмо.", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Ладно, я передумал. Не буду пить.", size_hint_y=None, size_y=100,
                           on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)

    def changerNext(self, *args):
        self.manager.current = 'WarningThree'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


class WarningThree(Screen):
    def __init__(self, **kwargs):
        super(WarningThree, self).__init__(**kwargs)
        warninLayout = BoxLayout(orientation='vertical')
        lblLayout = AnchorLayout()
        warninLbl = Label(text='И после этого ты считаешь себя альфасамцом?', halign='center', valign='top')
        lblLayout.add_widget(warninLbl)
        warninBtn = Button(text="Нет, я лох.", size_hint_y=None, size_y=100, on_press=self.changerNext)
        cancelBtn = Button(text="Я не буду так больше. Извините.", size_hint_y=None, size_y=100,
                           on_press=self.changerCancel)
        warninLayout.add_widget(lblLayout)
        warninLayout.add_widget(warninBtn)
        warninLayout.add_widget(cancelBtn)
        self.add_widget(warninLayout)

    def changerNext(self, *args):
        self.manager.current = 'StartScreen'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


if __name__ == "__main__":
    NonAlcogolic().run()
