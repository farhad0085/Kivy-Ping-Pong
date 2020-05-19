from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty,
                             ObjectProperty)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_y *= -1
            self.score += 1

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # latest position = current velocity + current position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    paddle_1 = ObjectProperty(None)
    paddle_2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(10,10).rotate(randint(0,360))

    def update(self, dt):
        self.ball.move()

        #bounce off top and bottom
        if self.ball.y < 0:
            self.ball.velocity_y *= -1
            self.paddle_2.score += 1

        if self.ball.y > self.height - 50:
            self.ball.velocity_y *= -1
            self.paddle_1.score += 1

        # bounce off right and left
        if (self.ball.x < 0) or (self.ball.x > self.width - 50):
            self.ball.velocity_x *= -1

        self.paddle_1.bounce_ball(self.ball)
        self.paddle_2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.y < self.height / 1/4:
            self.paddle_1.center_x = touch.x

        if touch.y > self.height * 3/4:
            self.paddle_2.center_x = touch.x


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0) # means 60 fps
        return game

PongApp().run()