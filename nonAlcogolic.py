# python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
from random import randint

from PIL import Image, ImageDraw, ImageFilter
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Texture
from kivy.graphics import *
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.storage.dictstore import DictStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
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

divider = 1
width = 1080.0
height = 1704.0


Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', int(width / divider))
Config.set('graphics', 'height', int(height / divider))


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


class RoundedButton(ButtonBehavior, Label):
    _shadows = {
        1: (1, 3, 0.4),
        2: (3, 6, 0.16),
        3: (10, 20, 0.19),
        4: (14, 28, 0.25),
        5: (19, 38, 0.30)
    }

    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.shadow_texture = None
        self.elevation = 1
        if kwargs.has_key('background_color'):
            background_color = kwargs['background_color']
        else:
            background_color = (1, 1, 1, 0)
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

    def update_rect(self, *args):
        x, y = self.pos[0], self.pos[1]
        self.rect.pos = (x + 10 / divider, y + 12 / divider)
        ow, oh = self.size[0], self.size[1]
        self.rect.size = (ow - 20 / divider, oh - 20 / divider)
        self._create_shadow()

    # def on_elevation(self, *args, **kwargs):
    #    #self._create_shadow()
    #    pass

    def _create_shadow(self, *args):
        # print "update shadow"
        w, h = self.size[0], self.size[1]
        shadow_data = self._shadows[self.elevation]
        offset_x = 0
        offset_y = 0
        radius = shadow_data[1]
        ow, oh = w - 20 / divider, h - 20 / divider
        t1 = self._create_boxshadow(ow, oh, radius, shadow_data[2])
        self.shadow1.texture = t1
        self.shadow1.size = w, h
        self.shadow1.pos = self.pos
        # self.shadow1.pos = self.x - (w - ow) / 2. + offset_x, self.y - (h - oh) / 2. - offset_y

    def _create_boxshadow(self, ow, oh, radius, alpha):
        # We need a bigger texture to correctly blur the edges
        w = ow + radius * 6.0 / divider
        h = oh + radius * 6.0 / divider
        w = int(w)
        h = int(h)
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        im = Image.new('RGBA', (w, h), self.shadow_color)

        draw = ImageDraw.Draw(im)
        # the rectangle to be rendered needs to be centered on the texture
        x0, y0 = (w - ow) / 2., (h - oh) / 2.
        x1, y1 = x0 + ow - 1, y0 + oh - 1
        rounded_rectangle(draw, ((x0, y0), (x1, y1)), 20, fill=(0, 0, 0, int(255 * alpha)))
        # im = im.filter(ImageFilter.GaussianBlur(radius * RAD_MULT))
        im = im.filter(ImageFilter.BLUR)
        texture.blit_buffer(im.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    # def on_touch_down(self, touch):
    #    if self.collide_point(touch.x, touch.y):
    #        self._orig_elev = self.elevation
    #        self.elevation = 5

    # def on_touch_up(self, touch):
    #    if self.collide_point(touch.x, touch.y):
    #        self.elevation = self._orig_elev


def markup_text(size, color, text, bold=True, font=None):
    if bold:
        bs = '[b]'
        be = '[/b]'
    else:
        bs = ''
        be = ''

    if not font:
        font = 'RobotoCondensed-Bold' if bold else 'RobotoCondensed-Regular'

    return '[size=' + str(size / divider) + '][color=' + color + '][font=' + font + ']' + bs + text + be + '[/font][/color][/size]'


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
            text=markup_text(size=50, color='FFFFFF', text='ПЕРЕСТАТЬ ПИТЬ!'),
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
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        secondScreenLayout = BoxLayout(orientation='horizontal')
        horizontalBlancLayoutOne = Widget(size_hint=[.25, 1])
        horizontalBlancLayoutTwo = Widget(size_hint=[.25, 1])
        verticalBlancLayoutOne = Widget(size_hint=[1, .2])
        verticalBlancLayoutTwo = Widget(size_hint=[1, .2])
        buttonsLayout = BoxLayout(orientation='vertical', spacing=30, size_hint=[1, 1])
        alignSpacesNum = 17
        oneWeekBtn = Button(
            text=markup_text(size=46, color='5F3C03', text=' ' * alignSpacesNum + "НА ") + markup_text(size=300, color='5F3C03', text='1') + markup_text(size=46, color='5F3C03', text=' НЕДЕЛЮ'),
            halign='left',
            markup=True,
            size_hint=[1, .25],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerOneWeek
        )
        oneWeekBtn.bind(size=oneWeekBtn.setter('text_size'))
        oneMonthBtn = Button(
            text=markup_text(size=46, color='74858E', text=' ' * alignSpacesNum + "НА ") + markup_text(size=300, color='74858E', text='1') + markup_text(size=46, color='74858E', text=' МЕСЯЦ'),
            halign='left',
            markup=True,
            size_hint=[1, .25],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerOneMonth)
        oneMonthBtn.bind(size=oneMonthBtn.setter('text_size'))
        oneYearBtn = Button(
            text=markup_text(size=46, color='F1BA18', text=' ' * alignSpacesNum + "НА ") + markup_text(size=300, color='F1BA18', text='1') + markup_text(size=46, color='F1BA18', text=' ГОД'),
            halign='left',
            markup=True,
            size_hint=[1, .25],
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
    secondsNames = [' СЕКУНДА ', ' СЕКУНДЫ ', ' СЕКУНД ']
    minutesNames = [' МИНУТА ', ' МИНУТЫ ', ' МИНУТ ']
    hoursNames = [' ЧАС ', ' ЧАСА ', ' ЧАСОВ ']
    daysNames = [' ДЕНЬ ', ' ДНЯ ', ' ДНЕЙ ']
    cntNames = [' РАЗ ', ' РАЗА ', ' РАЗ ']

    excuses = ["Панкреатит – врачи запретили",
               "А вдруг я будущая мать? Мне нельзя",
               "Аллергия на алкоголь, меня раздует",
               "Закодировался и пока не подобрал код",
               "Временно перешел на колеса – от них лучше прет",
               "Принял ислам, там запрещено",
               "Меня покусала бешеная белка, пока нельзя",
               "Сейчас делаю детокс печени, пить нельзя",
               "Мне нельзя — я алкоголик",
               "Решил стать альфасамцом и тренирую силу воли",
               "Перестали в театр пускать пьяным",
               "Не буду – пьяным меня тянет кататься на карусели",
               "Вступил в секту, а там главные правила - сухой закон и зеленые галстуки",
               "Не хочу пьяным возвращаться домой",
               "Узнал, что алкоголь это вредно",
               "Хочу дожить до пенсии",
               "Узнал что в алкоголе много калорий – от него толстеют",
               "Перестал понимать трезвых людей",
               "Устал от случайных сексуальных связей",
               "Нога чешется, когда пью",
               "Слишком много хорошего в последнее время",
               "Вступил в клуб анонимных алкоголиков, а вы знаете, как меня зовут",
               "Надоели зеленые человечки",
               "Я слишком любвеобильный, когда пьяный",
               "Когда напьюсь, у меня в голове рождаются слишком умные мысли, и окружающие перестают меня понимать",
               "Боюсь перекачаться, поднимая стакан",
               "В мире слишком много глупости – не время пить",
               "Я бы хотел, но не хочу",
               "Жена запретила",
               "Сегодня свидание, не хочу чтобы она сразу поняла, что я алкоголик",
               "Когда выпиваю, начинаю петь на испанском",
               "Завтра анализы сдавать",
               "Меня прет от трезвого состояния – такое редко бывает",
               "Вечером тараканов травить буду",
               "Я беременный и мне нельзя",
               "Поспорил на 100$ что неделю не буду пить",
               "У меня безалкогольная диета",
               "Я за рулем",
               "Меня покусал бешеный слон и пока нельзя",
               "Проиграл в карты, что не буду пить. А карточный долг священен",
               "Хочу узнать что такое алкогольная депривация",
               "Меня покусал бешеный хомячок и пока нельзя",
               "Голоса мне говорят, что пока не стоит"
               ]

    def __init__(self, **kwargs):
        super(Program, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        mainLayout = BoxLayout(orientation='horizontal')
        verticalBlancLayoutOne = Widget(size_hint=[140 / width, 1])
        mainLayout.add_widget(verticalBlancLayoutOne)

        self.programLayoutWidth = 940.0
        programLayout = BoxLayout(orientation='vertical', size_hint=[self.programLayoutWidth / width, 1])

        self.menuLayout = BoxLayout(orientation='horizontal', size_hint=[1, 144 / height])
        self.blancMenuLayoutWidget = Widget(size_hint=[800 / self.programLayoutWidth, 1])
        menuButton = Button(text=markup_text(size=40, color='000000', text=u'\ue9bd', font='icomoon'), background_color=(1, 1, 1, 1), background_normal='', markup=True, size_hint=[140 / self.programLayoutWidth, 1], on_press=self.changer)
        self.menuLayout.add_widget(self.blancMenuLayoutWidget)
        self.menuLayout.add_widget(menuButton)
        programLayout.add_widget(self.menuLayout)

        self.cntLabelWidget, self.cntLbl, self.cntTxtLbl = self.getCountWidget(markup_text(size=46, color='92290E', text='ПРЕДЛОЖИЛИ\nВЫПИТЬ', font='Roboto-Black'))
        goneLabelWidget, self.goneLbl, self.goneTxtLbl = self.getCountWidget(markup_text(size=46, color='75868F', text='ПРОШЛО', font='Roboto-Black'))
        leftLabelWidget, self.leftLbl, self.leftTxtLbl = self.getCountWidget(markup_text(size=46, color='75868F', text='ОСТАЛОСЬ', font='Roboto-Black'))

        ##buttonProposal = Button(text='Мне предложили выпить', size_hint_y=None, size_y=100, on_press=self.btnPress)
        horisontalUpperButtonSpacer = Widget(size_hint=[1, 143 / height])
        buttonProposal = RoundedButton(
            text=markup_text(size=50, color='FFFFFF', text='МНЕ ПРЕДЛОЖИЛИ ВЫПИТЬ'),
            markup=True,
            size_hint=[800 / self.programLayoutWidth, 150 / height],
            background_color=(0x92 / 255.0, 0x29 / 255.0, 0x0e / 255.0, 1),  # 92290E
            shadow_color=(0x4E, 0x16, 0x08, 1),  # 4E1608
            on_press=self.btnPress
        )
        horisontalBottomButtonSpacer = Widget(size_hint=[1, 130 / height])

        programLayout.add_widget(self.cntLabelWidget)
        programLayout.add_widget(goneLabelWidget)
        programLayout.add_widget(leftLabelWidget)
        programLayout.add_widget(horisontalUpperButtonSpacer)
        programLayout.add_widget(buttonProposal)
        programLayout.add_widget(horisontalBottomButtonSpacer)
        mainLayout.add_widget(programLayout)
        self.add_widget(mainLayout)
        Clock.schedule_interval(self.updateLabels, 1)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def getCountWidget(self, text):
        widgetHeight = 384.0
        mainLayout = BoxLayout(orientation='vertical', size_hint=[1, widgetHeight / height])
        labelOne = Label(text=text, markup=True, size_hint=[1, 122.0 / widgetHeight], halign='left', valign='center')
        labelOne.bind(size=labelOne.setter('text_size'))
        addLayout = BoxLayout(orientation='horizontal', size_hint=[1, 224.0 / widgetHeight])
        counterLabel = Label(text='', markup=True, size_hint=[491.0 / self.programLayoutWidth, 1.39], halign='right', valign='top')
        counterLabel.bind(size=counterLabel.setter('text_size'))
        textLabel = Label(text='', markup=True, size_hint=[449.0 / self.programLayoutWidth, 1], halign='left', valign='bottom')
        textLabel.bind(size=textLabel.setter('text_size'))
        addLayout.add_widget(counterLabel)
        addLayout.add_widget(textLabel)
        horizontalBlankBottomWidget = Widget(size_hint=[1, 50.0 / widgetHeight])
        mainLayout.add_widget(labelOne)
        mainLayout.add_widget(addLayout)
        mainLayout.add_widget(horizontalBlankBottomWidget)
        return mainLayout, counterLabel, textLabel

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def updateLabels(self, *args):
        if self.settings.finalDay:
            currentDate = datetime.now()
            diffGone = currentDate - self.settings.startDay
            diffLeft = self.settings.finalDay - currentDate
            self.cntLbl.text = markup_text(size=300, color='92290E', text=str(self.settings.counter))
            self.cntTxtLbl.text = markup_text(size=46, color='92290E', text=self.cntNames[self.getNumOfVariant(self.settings.counter)], font='Roboto-Black')
            cnt, txt = self.getTextForTimers(diffGone)
            self.goneLbl.text = markup_text(size=300, color='75868F', text=cnt)
            self.goneTxtLbl.text = markup_text(size=46, color='75868F', text=txt, font='Roboto-Black')
            cnt, txt = self.getTextForTimers(diffLeft)
            self.leftLbl.text = markup_text(size=300, color='75868F', text=cnt)
            self.leftTxtLbl.text = markup_text(size=46, color='75868F', text=txt, font='Roboto-Black')
        # self.show_marks1(self.menuLayout)
        # self.show_marks2(self.leftTxtLbl)

    def show_marks1(self, widget):
        # Indicate the position of the anchors with a red top marker
        widget.canvas.before.clear()
        with widget.canvas.before:
            Color(1, 0, 0, 0.5)
            Rectangle(pos=widget.pos, size=widget.size)

    def show_marks2(self, widget):
        # Indicate the position of the anchors with a red top marker
        widget.canvas.before.clear()
        with widget.canvas.before:
            Color(0, 1, 0, 0.5)
            Rectangle(pos=widget.pos, size=widget.size)

    def getNumOfVariant(self, num):
        chk = num % 10
        if chk == 1 and num != 11:
            return 0
        if 1 < chk < 5 and not [12, 13, 14].__contains__(num):
            return 1
        return 2

    def getTextForTimers(self, diff):
        if diff.days <= 0:
            if diff.seconds < 60:
                return str(diff.seconds), self.secondsNames[self.getNumOfVariant(diff.seconds)]
            else:
                diffMinutes = diff.seconds / 60
                if diffMinutes < 60:
                    return str(diffMinutes), self.minutesNames[self.getNumOfVariant(diffMinutes)]
                else:
                    diffHours = diffMinutes / 60
                    return str(diffHours), self.hoursNames[self.getNumOfVariant(diffHours)]

        else:
            return str(diff.days), self.daysNames[self.getNumOfVariant(diff.days)]

    def changer(self, *args):
        self.manager.current = 'MenuScreen'

    def btnPress(self, *args):
        self.settings.counter += 1
        # всплывает попап с отмазкой
        exuse = self.excuses[randint(0, len(self.excuses) - 1)]
        textLabel = Label(text=markup_text(size=80, color='000000', text=exuse, bold=False), markup=True, size_hint=(0.8, 0.8), valign='top')
        textLabel.bind(size=textLabel.setter('text_size'))
        popup = Popup(title="ОТМАЗКА НА СЕГОДНЯ",
                      title_color=(0x75 / 255.0, 0x86 / 255.0, 0x8F / 255.0, 1),  # 75868F
                      title_size=46 / divider,
                      background='white',
                      separator_color=(1, 1, 1, 1),
                      content=textLabel,
                      size_hint=(.7, .5))
        popup.open()


class Menu(Screen):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        verticalBlancLayoutTwo = Widget(size_hint=[1, .1])
        buttonsLayout = BoxLayout(orientation='vertical', spacing=30, size_hint=[1, 1])
        oneWeekBtn = Button(
            text=markup_text(size=80, color='92290E', text="ПЕРЕСТАТЬ НЕ ПИТЬ", font='Roboto-Black'),
            halign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerWarningOneScr
        )
        oneWeekBtn.bind(size=oneWeekBtn.setter('text_size'))
        oneMonthBtn = Button(
            text=markup_text(size=80, color='F1BA18', text="Я ВЫПИЛ", font='Roboto-Black'),
            halign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changer)
        oneMonthBtn.bind(size=oneMonthBtn.setter('text_size'))
        oneYearBtn = Button(
            text=markup_text(size=80, color='74858E', text="ЗАКРЫТЬ МЕНЮ", font='Roboto-Black'),
            halign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.closeMenu)
        oneYearBtn.bind(size=oneYearBtn.setter('text_size'))
        buttonsLayout.add_widget(oneWeekBtn)
        buttonsLayout.add_widget(oneMonthBtn)
        buttonsLayout.add_widget(oneYearBtn)
        buttonsLayout.add_widget(verticalBlancLayoutTwo)
        self.add_widget(buttonsLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def closeMenu(self, *args):
        self.manager.current = 'ProgramScreen'

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
