import random
from datetime import datetime
import json
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "sign_up_screen"

    def log_in(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and uname != '':
            if pword == users[uname]["password"] and pword != '':
                self.manager.transition.direction = 'left'
                self.manager.current = "login_screen_success"
            else:
                self.ids.login_wrong.text = "Wrong password."
        else:
            self.ids.login_wrong.text = "Username does not exist, please Sign up."


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        try:
            with open("quotes/" + feel.lower() + ".txt", encoding="utf8") as file:
                lines = file.readlines()
            self.ids.quote.text = random.choice(lines)
        except FileNotFoundError:
            self.ids.quote.text = "Try another feeling."


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()