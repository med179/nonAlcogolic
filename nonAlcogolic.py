#nonAlcogolic

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.widget import Widget


Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'width', 1080)
Config.set('graphics', 'height', 1920)

class StartScreen(App):
    def build(self):
        startScreen = AnchorLayout ()

        #скорее всего, тут нужно использовать картинку. Будет лучше выглядеть. 
        buttonStart = Button(
            text = 'Начать не пить', 
            on_press = self.btnPress()
            )
        startScreen.add_widget(buttonStart)
        return startScreen
        

    def btnPress(self):
        #тут должен быть переход на второй активити и запускаться таймеры
        pass

class Program(BoxLayout):
    def build(self):
        self.excuse = ['Я не могу больше пить']

        program = BoxLayout()
        timerOne = Label()
        timerTwo = Label()
        buttonProposal = Button(
            text = 'Мне предложили выпить', 
            on_press = self.btnPress()
            )
        
        program.add_widget(timerOne)
        program.add_widget(timerTwo)
        program.add_widget(buttonProposal)

        return program

    def btnPress(self):
    #всплывает попап с отмазкой
        print(self.excuse[0])
        pass

    


class Menu(BoxLayout):
    def build(self):
        #тут нужно все продумать
        menu = BoxLayout()

        return menu 


if __name__ == "__main__":
    StartScreen().run()

