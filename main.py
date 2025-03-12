from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color
from random import randint, choice
import string

class Bubble(Widget):
    def __init__(self, letter, **kwargs):
        super().__init__(**kwargs)
        self.letter = letter
        self.size = (50, 50)
        self.x = randint(50, 350)
        self.y = 0

        with self.canvas:
            Color(0.26, 0.65, 0.96, 1)  # Blue color
            self.circle = Ellipse(pos=self.pos, size=self.size)
            self.label = Label(text=self.letter, center=self.center, font_size=24)
            self.add_widget(self.label)

        self.bind(pos=self.update_position)

    def update_position(self, *args):
        self.circle.pos = self.pos
        self.label.center = self.center

class BubbleGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.level = 1
        self.speed = 2
        self.bubbles = []
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.create_bubble, 1)

    def create_bubble(self, dt):
        if len(self.bubbles) < 10:
            letter = choice(string.ascii_uppercase)
            bubble = Bubble(letter)
            self.add_widget(bubble)
            self.bubbles.append(bubble)

    def update(self, dt):
        to_remove = []
        for bubble in self.bubbles:
            bubble.y += self.speed
            if bubble.y > self.height:
                to_remove.append(bubble)

        for bubble in to_remove:
            self.bubbles.remove(bubble)
            self.remove_widget(bubble)

        if self.score >= self.level * 10 and self.level < 10:
            self.level += 1
            self.speed += 0.5

    def on_touch_down(self, touch):
        for bubble in self.bubbles:
            if bubble.collide_point(*touch.pos):
                self.score += 1
                self.bubbles.remove(bubble)
                self.remove_widget(bubble)

class BubbleApp(App):
    def build(self):
        return BubbleGame()

if __name__ == '__main__':
    BubbleApp().run()
