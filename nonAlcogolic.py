# python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
from random import randint

import kivy.properties as props
from PIL import Image, ImageDraw, ImageFilter
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Texture
from kivy.graphics import *
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.storage.dictstore import DictStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.widget import Widget

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


def rounded_rectangle(self, xy, corner_radius, fill=None, outline=None):
    ulpt = xy[0]
    brpt = xy[1]
    self.rectangle([(ulpt[0], ulpt[1] + corner_radius), (brpt[0], brpt[1] - corner_radius)], fill=fill, outline=outline)
    self.rectangle([(ulpt[0] + corner_radius, ulpt[1]), (brpt[0] - corner_radius, brpt[1])], fill=fill, outline=outline)
    self.pieslice([ulpt, (ulpt[0] + corner_radius * 2, ulpt[1] + corner_radius * 2)], 180, 270, fill=fill, outline=outline)
    self.pieslice([(brpt[0] - corner_radius * 2, brpt[1] - corner_radius * 2), brpt], 0, 90, fill=fill, outline=outline)
    self.pieslice([(ulpt[0], brpt[1] - corner_radius * 2), (ulpt[0] + corner_radius * 2, brpt[1])], 90, 180, fill=fill, outline=outline)
    self.pieslice([(brpt[0] - corner_radius * 2, ulpt[1]), (brpt[0], ulpt[1] + corner_radius * 2)], 270, 360, fill=fill, outline=outline)


RAD_MULT = 1.5  # PIL GBlur seems to be stronger than Chrome's so I lower the radius


class RoundedButton(Button):
    shadow_texture = props.ObjectProperty(None)

    elevation = props.NumericProperty(1)
    _shadow_clock = None

    _shadows = {
        1: (1, 3, 0.4),
        2: (3, 6, 0.16),
        3: (10, 20, 0.19),
        4: (14, 28, 0.25),
        5: (19, 38, 0.30)
    }

    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        background_color = self.background_color
        if kwargs.has_key('shadow_color'):
            self.shadow_color = kwargs['shadow_color']
        else:
            self.shadow_color = (1, 1, 1, 0)
        self.background_color = (1, 1, 1, 0)
        with self.canvas.before:
            Color(rgba=(0, 1, 1, 1))
            self.shadow1 = Rectangle(pos=self.pos, size=self.size, texture=self.shadow_texture)
            Color(rgba=background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self._update_shadow = Clock.create_trigger(self._create_shadow)

    def update_rect(self, *args):
        x, y = self.pos[0], self.pos[1]
        self.rect.pos = (x + 10, y + 12)
        ow, oh = self.size[0], self.size[1]
        self.rect.size = (ow - 20, oh - 20)
        self._update_shadow()

    def on_elevation(self, *args, **kwargs):
        self._update_shadow()

    def _create_shadow(self, *args):
        # print "update shadow"
        w, h = self.size[0], self.size[1]
        shadow_data = self._shadows[self.elevation]
        offset_x = 0
        offset_y = 0
        radius = shadow_data[1]
        ow, oh = w - 20, h - 20
        t1 = self._create_boxshadow(ow, oh, radius, shadow_data[2])
        self.shadow1.texture = t1
        self.shadow1.size = w, h
        self.shadow1.pos = self.pos
        # self.shadow1.pos = self.x - (w - ow) / 2. + offset_x, self.y - (h - oh) / 2. - offset_y

    def _create_boxshadow(self, ow, oh, radius, alpha):
        # We need a bigger texture to correctly blur the edges
        w = ow + radius * 6.0
        h = oh + radius * 6.0
        w = int(w)
        h = int(h)
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        im = Image.new('RGBA', (w, h), self.shadow_color)

        draw = ImageDraw.Draw(im)
        # the rectangle to be rendered needs to be centered on the texture
        x0, y0 = (w - ow) / 2., (h - oh) / 2.
        x1, y1 = x0 + ow - 1, y0 + oh - 1
        rounded_rectangle(draw, ((x0, y0), (x1, y1)), 20, fill=(0, 0, 0, int(255 * alpha)))
        im = im.filter(ImageFilter.GaussianBlur(radius * RAD_MULT))
        texture.blit_buffer(im.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    # def on_touch_down(self, touch):
    #    if self.collide_point(touch.x, touch.y):
    #        self._orig_elev = self.elevation
    #        self.elevation = 5

    # def on_touch_up(self, touch):
    #    if self.collide_point(touch.x, touch.y):
    #        self.elevation = self._orig_elev


class NonAlcogolic(App):

    def build(self):
        settings = MySettings()
        myScreenmanager = ScreenManager(transition=FadeTransition())
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
            Color(rgba=[1, 1, 1, 1])
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
            background_color=(0x0 / 255.0, 0xd6 / 255.0, 0xd6 / 255.0, 1),
            shadow_color=(0x19, 0xb6, 0xbb, 1),
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
            Color(rgba=[255.0 / 255.0, 255.0 / 255.0, 255.0 / 255.0, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        secondScreenLayout = BoxLayout(orientation='horizontal')
        horizontalBlancLayoutOne = Widget(size_hint=[.25, 1])
        horizontalBlancLayoutTwo = Widget(size_hint=[.25, 1])
        verticalBlancLayoutOne = Widget(size_hint=[1, .1])
        verticalBlancLayoutTwo = Widget(size_hint=[1, .2])
        buttonsLayout = BoxLayout(orientation='vertical', spacing=30, size_hint=[1, 1])
        alignSpacesNum = 78
        oneWeekBtn = Button(
            text="[size=16][color=5F3C03][b]" + ' ' * alignSpacesNum + "НА[/size][size=100]1[/size][size=16]НЕДЕЛЮ[/b][/color][/size]",
            halign='left',
            markup=True,
            size_hint=[1, .15],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerOneWeek
        )
        oneWeekBtn.bind(size=oneWeekBtn.setter('text_size'))
        oneMonthBtn = Button(
            text="[size=16][color=74858E][b]" + ' ' * alignSpacesNum + "НА[/size][size=100]1[/size][size=16]МЕСЯЦ[/color][/b][/size]",
            halign='left',
            markup=True,
            size_hint=[1, .15],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerOneMonth)
        oneMonthBtn.bind(size=oneMonthBtn.setter('text_size'))
        oneYearBtn = Button(
            text="[size=16][color=F1BA18][b]" + ' ' * alignSpacesNum + "НА[/size][size=100]1[/size][size=16]ГОД[/b][/color][/size]",
            halign='left',
            markup=True,
            size_hint=[1, .15],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerOneYear)
        oneYearBtn.bind(size=oneYearBtn.setter('text_size'))
        secondScreenLayout.add_widget(horizontalBlancLayoutOne)
        buttonsLayout.add_widget(verticalBlancLayoutOne)
        buttonsLayout.add_widget(oneWeekBtn)
        buttonsLayout.add_widget(oneMonthBtn)
        buttonsLayout.add_widget(oneYearBtn)
        buttonsLayout.add_widget(verticalBlancLayoutTwo)
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
                      separator_color=(1, 1, 1, 1),
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
