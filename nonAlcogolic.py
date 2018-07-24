# python
# -*- coding: utf-8 -*-
# Добавил строку из мастрерславля, после которой все заработало.... хер знает, может поможет. Это для кодировок.
from __future__ import unicode_literals


# У МЕНЯ НИХЕРА НЕ ЗАПУСКАЕТСЯ!!!!!!!!
# from PIL import Image, ImageDraw, ImageFilter
# И
# from kivy.graphics.vertex_instructions import RoundedRectangle



from datetime import date, timedelta, datetime
from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import *
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.properties import ListProperty, NumericProperty
from kivy.storage.dictstore import DictStore
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.effectwidget import EffectWidget, EffectBase
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.widget import Widget

# Clock.max_iteration = sys.maxint
Clock.max_iteration = 100000

SHADOW_RADIUS = 15.0

divider = 1
width = 1080.0
height = 1704.0
sideSpacerSiseHint = size_hint = [180 / width, 1]

Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', int(width / divider))
Config.set('graphics', 'height', int(height / divider))

#насколько я понял, эта хрень нужна для теней. Но как она работает полностью  я не понимаю.
def rounded_rectangle(self, xy, corner_radius, fill=None, outline=None):
    ulpt = xy[0]
    brpt = xy[1]
    self.rectangle([(ulpt[0], ulpt[1] + corner_radius), (brpt[0], brpt[1] - corner_radius)], fill=fill, outline=outline)
    self.rectangle([(ulpt[0] + corner_radius, ulpt[1]), (brpt[0] - corner_radius, brpt[1])], fill=fill, outline=outline)
    self.pieslice([ulpt, (ulpt[0] + corner_radius * 2, ulpt[1] + corner_radius * 2)], 180, 270, fill=fill, outline=outline)
    self.pieslice([(brpt[0] - corner_radius * 2, brpt[1] - corner_radius * 2), brpt], 0, 90, fill=fill, outline=outline)
    self.pieslice([(ulpt[0], brpt[1] - corner_radius * 2), (ulpt[0] + corner_radius * 2, brpt[1])], 90, 180, fill=fill, outline=outline)
    self.pieslice([(brpt[0] - corner_radius * 2, ulpt[1]), (brpt[0], ulpt[1] + corner_radius * 2)], 270, 360, fill=fill, outline=outline)


#Это тоже для теней.
class RoundedWidget(Widget):
    def __init__(self, **kwargs):
        super(RoundedWidget, self).__init__(**kwargs)
        self.background_color = (1, 1, 1, 0)
        if kwargs.has_key('background_color'):
            background_color = kwargs['background_color']
        else:
            background_color = (1, 1, 1, 0)
        with self.canvas.before:
            Color(rgba=background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20, ])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

#Вот это здесь зачем непонятно.
class RoundedFlatButton(ButtonBehavior, RoundedWidget, Label):
    pass


effect_drop_shadow = '''
#define M_PI 3.1415926535897932384626433832795
vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords) {{
    vec2 coords2;
    float x, y;
    float radius, sampling, surface;
    vec4 tint, shadow;
    coords2 = coords + vec2({offset_x:f}, {offset_y:f}) ;
    radius = {radius:f};
    sampling = {sampling:f};
    tint = vec4({r:f}, {g:f}, {b:f}, {a:f});
    if (color.a >= .99)
        return color;
    surface = (sampling * M_PI * radius * radius) / 2.;
    shadow = vec4(0., 0., 0., 0.);
    for (x = -radius; x < radius; x += sampling)
        for (y = -radius; y < radius; y += sampling)
            if (length(vec2(x, y)) <= radius)
                shadow += texture2D(
                    texture,
                    vec2(coords2.x + x, coords2.y + y) / resolution
                    ).a * tint / surface;
    return color + shadow * (shadow.a - color.a);
}}
'''


class DropShadowEffect(EffectBase):
    '''Add DropShadow to the input.'''
    offset = ListProperty([0, 0])
    tint = ListProperty([0, 0, 0, 1])
    radius = NumericProperty(1)
    sampling = NumericProperty(1)

    def __init__(self, *args, **kwargs):
        super(DropShadowEffect, self).__init__(*args, **kwargs)
        self.fbind('offset', self.do_glsl)
        self.fbind('tint', self.do_glsl)
        self.fbind('radius', self.do_glsl)
        self.fbind('sampling', self.do_glsl)
        self.do_glsl()

    def on_size(self, *args):
        self.do_glsl()

    def do_glsl(self, *args):
        self.glsl = effect_drop_shadow.format(
            offset_x=self.offset[0],
            offset_y=self.offset[1],
            radius=self.radius,
            sampling=self.sampling,
            r=self.tint[0],
            g=self.tint[1],
            b=self.tint[2],
            a=self.tint[3],
        )


class RoundedShadowButton(BoxLayout):
    def __init__(self, **kwargs):
        super(RoundedShadowButton, self).__init__(**kwargs)
        if kwargs.has_key('shadow_color'):
            self.shadow_color = kwargs['shadow_color']
        else:
            self.shadow_color = (1, 1, 1, 0)
        self.bind(size=self.update_rect)
        self.effect = EffectWidget(size_hint=[1, 1])
        self.button = RoundedFlatButton(**kwargs)
        self.button.pos = (SHADOW_RADIUS / divider, SHADOW_RADIUS / divider)
        self.button.size_hint = [None, None]
        self.effect.add_widget(self.button)
        self.effect.effects = [DropShadowEffect(radius=SHADOW_RADIUS / divider, tint=[0, 0, 0, 0.8])]
        self.add_widget(self.effect)

    def update_rect(self, *args):
        ow, oh = self.size[0], self.size[1]
        self.button.size = (ow - SHADOW_RADIUS * 2 / divider, oh - SHADOW_RADIUS * 2 / divider)

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
        startScreen = StartScreen(name='StartScreen', settings=settings)
        secondScreen = SecondScreen(name='SecondScreen', settings=settings)
        programScreen = Program(name='ProgramScreen', settings=settings)
        menuScreen = Menu(name='MenuScreen', settings=settings)
        warningOne = WarningOne(name='WarningOne')
        warningTwo = WarningTwo(name='WarningTwo')
        warningThree = WarningThree(name='WarningThree', settings=settings)
        oneRazNotKontrabas = OneRazNotKontrabas(name='OneRazNotKontrabas')
        twoRazIsKontrabas = TwoRazIsKontrabas(name='TwoRazIsKontrabas', settings=settings)
        myScreenmanager.add_widget(startScreen)
        myScreenmanager.add_widget(secondScreen)
        myScreenmanager.add_widget(programScreen)
        myScreenmanager.add_widget(menuScreen)
        myScreenmanager.add_widget(oneRazNotKontrabas)
        myScreenmanager.add_widget(twoRazIsKontrabas)
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
        self.settings = kwargs['settings']
        btnLayout = BoxLayout(orientation='horizontal')
        centerColumnLayout = BoxLayout(orientation='vertical')
        leftSpacer = Widget(size_hint=sideSpacerSiseHint)
        rightSpacer = Widget(size_hint=sideSpacerSiseHint)
        topSpacer = Widget(size_hint=[1, .7])
        bottomSpacer = Widget(size_hint=[1, .065])
        firstBtn = RoundedShadowButton(
            text=markup_text(size=50, color='FFFFFF', text='ПЕРЕСТАТЬ ПИТЬ!'),
            markup=True,
            size_hint=[1, 116 / height],
            background_color=(0x0 / 255.0, 0xd6 / 255.0, 0xd6 / 255.0, 1),
            shadow_color=(0x19, 0xb6, 0xbb, 1),
            # background_normal='',
            on_press=self.changer
        )
        btnLayout.add_widget(leftSpacer)
        centerColumnLayout.add_widget(topSpacer)
        centerColumnLayout.add_widget(firstBtn)
        centerColumnLayout.add_widget(bottomSpacer)
        btnLayout.add_widget(centerColumnLayout)
        btnLayout.add_widget(rightSpacer)

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
    __isKontrabas = False

    def __init__(self):
        self.__store = DictStore('user.dat')
        if self.__store.store_exists('finalDay') and self.__store.get('finalDay')['data']:
            self.__startDay = self.__store.get('startDay')['data']
            self.__finalDay = self.__store.get('finalDay')['data']
            self.__count = self.__store.get('count')['data']
            self.__isKontrabas = self.__store.get('isKontrabas')['data']
            self.__isNotReady = False
        else:
            self.reset()

    def parseDate(self, dateText):
        if dateText:
            return datetime.strptime(dateText, "%S-%M-%H %d-%m-%Y")
        else:
            None

    def reset(self):
        self.__isNotReady = True
        self.__startDay = None
        self.__finalDay = None
        self.__count = 0
        self.__isKontrabas = False
        self.__store.put('finalDay', data=None)
        self.__store.put('count', data=0)
        self.__store.put('isKontrabas', data=False)

    def __getattr__(self, attr):
        if attr == 'isNotReady':
            return self.__isNotReady
        if attr == 'startDay':
            return self.parseDate(self.__startDay)
        if attr == 'finalDay':
            return self.parseDate(self.__finalDay)
        if attr == 'counter':
            return self.__count
        if attr == 'isKontrabas':
            return self.__isKontrabas
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
        if key == 'isKontrabas':
            self.__isKontrabas = value
            self.__store.put('isKontrabas', data=value)
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

        parentLayout = BoxLayout(orientation='vertical')
        self.menuLayout = BoxLayout(orientation='horizontal', size_hint=[1, 200 / height])
        self.blancMenuLayoutWidget = Widget(size_hint=[880 / width, 1])
        menuButton = Button(text=markup_text(size=40, color='000000', text=u'\ue9bd', font='icomoon'), background_color=(1, 1, 1, 1), background_normal='', markup=True, size_hint=[200 / width, 1], on_press=self.changer)
        self.menuLayout.add_widget(self.blancMenuLayoutWidget)
        self.menuLayout.add_widget(menuButton)
        parentLayout.add_widget(self.menuLayout)

        mainLayout = BoxLayout(orientation='horizontal')
        leftSpacer = Widget(size_hint=sideSpacerSiseHint)
        rightSpacer = Widget(size_hint=sideSpacerSiseHint)
        mainLayout.add_widget(leftSpacer)

        self.programLayoutWidth = 940.0
        programLayout = BoxLayout(orientation='vertical')

        self.cntLabelWidget, self.cntLbl, self.cntTxtLbl = self.getCountWidget(markup_text(size=46, color='92290E', text='ПРЕДЛОЖИЛИ\nВЫПИТЬ', font='Roboto-Black'))
        goneLabelWidget, self.goneLbl, self.goneTxtLbl = self.getCountWidget(markup_text(size=46, color='75868F', text='ПРОШЛО', font='Roboto-Black'))
        leftLabelWidget, self.leftLbl, self.leftTxtLbl = self.getCountWidget(markup_text(size=46, color='75868F', text='ОСТАЛОСЬ', font='Roboto-Black'))

        horisontalUpperButtonSpacer = Widget(size_hint=[1, 144 / height])
        buttonProposal = RoundedShadowButton(
            text=markup_text(size=50, color='FFFFFF', text='МНЕ ПРЕДЛОЖИЛИ ВЫПИТЬ'),
            markup=True,
            size_hint=[1, 145 / height],
            background_color=(0x92 / 255.0, 0x29 / 255.0, 0x0e / 255.0, 1),  # 92290E
            shadow_color=(0x4E, 0x16, 0x08, 1),  # 4E1608
            on_press=self.btnPress
        )
        horisontalBottomButtonSpacer = Widget(size_hint=[1, 135 / height])

        programLayout.add_widget(self.cntLabelWidget)
        programLayout.add_widget(goneLabelWidget)
        programLayout.add_widget(leftLabelWidget)
        programLayout.add_widget(horisontalUpperButtonSpacer)
        programLayout.add_widget(buttonProposal)
        programLayout.add_widget(horisontalBottomButtonSpacer)
        mainLayout.add_widget(programLayout)
        mainLayout.add_widget(rightSpacer)
        parentLayout.add_widget(mainLayout)
        self.add_widget(parentLayout)
        Clock.schedule_interval(self.updateLabels, 1)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def getCountWidget(self, text):
        widgetHeight = 384.0
        mainLayout = BoxLayout(orientation='vertical', size_hint=[1, widgetHeight / height])
        labelOne = Label(text=text, markup=True, size_hint=[1, 122.0 / widgetHeight], halign='left', valign='center')
        labelOne.bind(size=labelOne.setter('text_size'))
        addLayout = BoxLayout(orientation='horizontal', size_hint=[1, 224.0 / widgetHeight])
        counterLabel = Label(text='', markup=True, size_hint=[0.571, 1.39], halign='right', valign='top')
        counterLabel.bind(size=counterLabel.setter('text_size'))
        textLabel = Label(text='', markup=True, size_hint=[0.429, 1], halign='left', valign='bottom')
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
        excuse = self.excuses[randint(0, len(self.excuses) - 1)]
        # textLabel = Label(text=markup_text(size=80, color='000000', text=exсuse, bold=False), markup=True, size_hint=(0.8, 0.8), valign='top')
        # textLabel.bind(size=textLabel.setter('text_size'))
        # popup = ModalView(title="ОТМАЗКА НА СЕГОДНЯ",
        #               title_color=(0x75 / 255.0, 0x86 / 255.0, 0x8F / 255.0, 1),  # 75868F
        #               title_size=46 / divider,
        #               #background='white',
        #               background_color=(1, 1, 1, 0),
        #               separator_color=(1, 1, 1, 1),
        #               content=textLabel,
        #               size_hint=(.7, .5))

        popup = ModalView(size_hint=[0.8, 0.6])
        effectWidget = EffectWidget(size_hint=[1.2, 1.2])
        effectLayout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=[1, 1])
        popupWidget = RoundedWidget(size_hint=[0.9, 0.9], background_color=(1, 1, 1, 1), shadow_color=(70, 70, 70, 1))
        widgetLayout = BoxLayout(orientation='vertical')

        def popupUpdate(instance, *args):
            x, y = instance.size
            widgetLayout.size = (x - 100, y - 100)
            w, h = instance.pos
            widgetLayout.pos = (w + 50, h + 50)

        popupWidget.bind(size=popupUpdate, pos=popupUpdate)  # popupButton.setter('text_size'))
        captionLabel = Label(text=markup_text(size=46, color='75868F', text='ОТМАЗКА НА СЕГОДНЯ', font='Roboto-Black'), markup=True, size_hint=(1, 0.35), valign='top', halign='left')
        captionLabel.bind(size=captionLabel.setter('text_size'))
        textLabel = Button(text=markup_text(size=80, color='000000', text=excuse, bold=False), markup=True, size_hint=(1, 0.65), valign='top', halign='left', background_color=(0, 0, 0, 0), on_press=popup.dismiss)
        textLabel.bind(size=textLabel.setter('text_size'))
        widgetLayout.add_widget(captionLabel)
        widgetLayout.add_widget(textLabel)
        popupWidget.add_widget(widgetLayout)
        effectLayout.add_widget(popupWidget)
        effectWidget.add_widget(effectLayout)
        effectWidget.effects = [DropShadowEffect(radius=SHADOW_RADIUS / divider, tint=[0, 0, 0, 0.7])]
        popup.add_widget(effectWidget)
        popup.background_color = (0.2, 0.2, 0.2, 0.6)

        popup.open()


class Menu(Screen):

    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        topBlankWidget = Widget(size_hint=[1, .1])
        bottomBlankWidget = Widget(size_hint=[1, .1])
        buttonsLayout = BoxLayout(orientation='vertical', spacing=30, size_hint=[1, 1])
        oneWeekBtn = Button(
            text=markup_text(size=80, color='92290E', text="ПЕРЕСТАТЬ НЕ ПИТЬ", font='Roboto-Black'),
            halign='center',
            valign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changerWarningOneScr
        )
        oneWeekBtn.bind(size=oneWeekBtn.setter('text_size'))
        if not self.settings.isKontrabas:
            colorForIDrink = 'F1BA18'
        else:
            colorForIDrink = '92290E'
        self.iDrinkBtn = Button(
            text=markup_text(size=80, color=colorForIDrink, text="Я ВЫПИЛ", font='Roboto-Black'),
            halign='center',
            valign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.changer)
        self.iDrinkBtn.bind(size=self.iDrinkBtn.setter('text_size'))
        oneYearBtn = Button(
            text=markup_text(size=80, color='74858E', text="ЗАКРЫТЬ МЕНЮ", font='Roboto-Black'),
            halign='center',
            valign='center',
            markup=True,
            size_hint=[1, .3],
            background_color=(1, 1, 1, 1),
            background_normal='',
            on_press=self.closeMenu)
        oneYearBtn.bind(size=oneYearBtn.setter('text_size'))
        buttonsLayout.add_widget(topBlankWidget)
        buttonsLayout.add_widget(oneWeekBtn)
        buttonsLayout.add_widget(self.iDrinkBtn)
        buttonsLayout.add_widget(oneYearBtn)
        buttonsLayout.add_widget(bottomBlankWidget)
        self.add_widget(buttonsLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def on_enter(self, *args):
        if not self.settings.isKontrabas:
            colorForIDrink = 'F1BA18'
        else:
            colorForIDrink = '92290E'
        self.iDrinkBtn.text = markup_text(size=80, color=colorForIDrink, text="Я ВЫПИЛ", font='Roboto-Black')

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def closeMenu(self, *args):
        self.manager.current = 'ProgramScreen'

    def changer(self, *args):
        self.settings.startDay = datetime.now()
        if not self.settings.isKontrabas:
            self.settings.isKontrabas = True
            self.manager.current = 'OneRazNotKontrabas'
        else:
            self.manager.current = 'TwoRazIsKontrabas'

    def changerWarningOneScr(self, *args):
        self.manager.current = 'WarningOne'


def buildWarningForm(textLbl, textBtn1, eventBtn1, textBtn2, eventBtn2):
    buttonSizeHint = [1, 100 / height]
    mainLayout = BoxLayout(orientation='horizontal')
    leftSpacer = Widget(size_hint=sideSpacerSiseHint)
    rightSpacer = Widget(size_hint=sideSpacerSiseHint)
    mainLayout.add_widget(leftSpacer)
    warninLayout = BoxLayout(orientation='vertical', spacing=50)
    lblLayout = AnchorLayout(size_hint_y=0.5)
    warninLbl = Label(text=markup_text(size=80, color='92290E', text=textLbl, bold=False, font='Roboto-Black'),
                      markup=True,
                      size_hint_x=0.8,
                      haligh='center',
                      valign='center')
    warninLbl.bind(size=warninLbl.setter('text_size'))
    lblLayout.add_widget(warninLbl)
    warninLayout.add_widget(lblLayout)
    if not textBtn1 or not textBtn2:
        bottomBlankWidget1 = Widget(size_hint=buttonSizeHint)
        warninLayout.add_widget(bottomBlankWidget1)
    if textBtn1:
        button1 = RoundedShadowButton(
            text=markup_text(size=50, color='FFFFFF', text=textBtn1),
            markup=True,
            size_hint=buttonSizeHint,
            background_color=(0x92 / 255.0, 0x29 / 255.0, 0x0e / 255.0, 1),  # 92290E
            shadow_color=(0x4E, 0x16, 0x08, 1),  # 4E1608
            on_press=eventBtn1
        )
        warninLayout.add_widget(button1)
    if textBtn2:
        button2 = RoundedShadowButton(
            text=markup_text(size=50, color='FFFFFF', text=textBtn2),
            markup=True,
            size_hint=buttonSizeHint,
            background_color=(0x0 / 255.0, 0xd6 / 255.0, 0xd6 / 255.0, 1),
            shadow_color=(0x19, 0xb6, 0xbb, 1),
            on_press=eventBtn2
        )
        warninLayout.add_widget(button2)

    bottomBlankWidget2 = Widget(size_hint_x=1, size_hint_y=0.035)
    warninLayout.add_widget(bottomBlankWidget2)

    mainLayout.add_widget(warninLayout)
    mainLayout.add_widget(rightSpacer)
    return mainLayout


class OneRazNotKontrabas(Screen):
    def __init__(self, **kwargs):
        super(OneRazNotKontrabas, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        warninLayout = buildWarningForm('ЭХ... НУ ЧТОЖ ТЫ...\nОДИН РАЗ НЕ КОНТРАБАС, ХОТЯ САМ ПОНИМАЕШЬ...', None, None, "OK, НЕ БУДУ БОЛЬШЕ ПИТЬ", self.changerCancel)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


class TwoRazIsKontrabas(Screen):
    def __init__(self, **kwargs):
        super(TwoRazIsKontrabas, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[4, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        warninLayout = buildWarningForm('ЭТА ПРОГРАММА ДЛЯ МУЖИКОВ, А НЕ ДЛЯ ТЕБЯ!', "Я НЕ МУЖИК", self.changerNext, None, None)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerNext(self, *args):
        self.settings.reset()
        self.manager.current = 'StartScreen'


class WarningOne(Screen):
    def __init__(self, **kwargs):
        super(WarningOne, self).__init__(**kwargs)
        with self.canvas:
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        warninLayout = buildWarningForm('ТЫ ЖЕ ОБЕЩАЛ НЕ ПИТЬ! МУЖИК ВСЕГДА ДЕРЖИТ СЛОВО. ТЫ ЧТО, НЕ МУЖИК?', "Я НЕ МУЖИК", self.changerNext, "ЛАДНО, НЕ БУДУ ПИТЬ", self.changerCancel)
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
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        warninLayout = buildWarningForm('КАК ТЫ ПОТОМ БУДЕШЬ СМОТРЕТЬ В ГЛАЗА СВОИМ ДРУЗЬЯМ, КОТОРЫЕ ВЕРИЛИ ТЕБЕ?', "НИКАК, Я ДЕРЬМО", self.changerNext, "ОК, Я ПЕРЕДУМАЛ. НЕ БУДУ ПИТЬ", self.changerCancel)
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
            Color(rgba=[1, 1, 1, 1])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.settings = kwargs['settings']
        warninLayout = buildWarningForm('И ПОСЛЕ ЭТОГО ТЫ СЧИТАЕШЬ СЕБЯ АЛЬФА САМЦОМ?', "НЕТ, Я ЛОХ", self.changerNext, "НЕ БУДУ ТАК БОЛЬШЕ! ИЗВИНИТЕ!", self.changerCancel)
        self.add_widget(warninLayout)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def changerNext(self, *args):
        self.settings.reset()
        self.manager.current = 'StartScreen'

    def changerCancel(self, *args):
        self.manager.current = 'ProgramScreen'


if __name__ == "__main__":
    NonAlcogolic().run()
