# SPDX-FileCopyrightText: 2024-present dh031200 <imbird0312@gmail.com>
#
# SPDX-License-Identifier: MIT
from time import sleep
from pathlib import Path

import cv2
import numpy as np

from .maps import get_test_map


class Ball:
    def __init__(self):
        self.location = [0, 0]
        self.state = 1  # Up [-1,1] Down
        self.direction = 0  # Left [-4,4] Right
        self.previous_state = 1
        self.jump_speed = 1

    def set_location(self, loc):
        print(f"loc : {loc}")
        self.location = loc

    def change_state(self):
        self.state *= -1

    def next(self):
        y = self.location[0] + self.jump_speed
        x = self.location[1] + self.direction
        return y, x

    def move(self):
        self.location[0] += self.jump_speed
        self.location[1] += self.direction
        self.jump_speed += 1
        if self.jump_speed == 0:
            self.state = 1


class Env:
    def __init__(self):
        self.map = get_test_map()
        self.block_images = self.get_block_images()
        self.canvas = None
        self.make()

    @staticmethod
    def get_block_images():
        blocks = ["blank", "default", "jump", "bomb", "rock", "left", "right", "blank"]
        return [
            cv2.imread(f"{Path(__file__).parent}/assets/{blocks[i]}.png")
            for i in range(len(blocks))
        ]

    def get_start_point(self):
        y, x = np.argwhere(self.map == -1)[0]
        return [y * 32, x * 32 + 16]

    def make(self):
        """
        0: blank
        1: default
        2: jump
        3: bomb
        4: rock
        5: arrow (left)
        6: arrow (right)
        """
        h, w = self.map.shape
        canvas = np.full((h * 32, w * 32, 3), (0, 0, 0), dtype=np.uint8)
        for i in range(h):
            for j in range(w):
                canvas[i * 32 : (i + 1) * 32, j * 32 : (j + 1) * 32] = (
                    self.block_images[self.map[i][j]]
                )
        return canvas

    @property
    def block_map(self):
        return self.make()


class BounceBall:
    def __init__(self):
        self.env = Env()
        self.ball = Ball()
        self.ball.set_location(self.env.get_start_point())

    def draw_ball(self, canvas):
        y, x = self.ball.location
        canvas[y - 3 : y + 4, x - 3 : x + 4] = (255, 255, 255)
        return canvas

    def bounce_check(self, _env):
        _next_loc = self.ball.next()
        for i in range(
            self.ball.state, self.ball.jump_speed + self.ball.state, self.ball.state
        ):
            if sum(_env[self.ball.location[0] + i + 4, _next_loc[1]]) != 0:
                self.ball.jump_speed = i
                return True
        return False

    def show(self):
        while True:
            _env = self.env.block_map
            flag = self.bounce_check(_env)
            self.ball.move()
            if flag:
                self.ball.change_state()
                self.ball.jump_speed = -10

            canvas = self.draw_ball(_env)
            cv2.imshow("bounce_ball", canvas)
            key = cv2.waitKeyEx(10)
            if key == 0x1B:
                break
            elif key == ord("d"):
                self.ball.direction += 1
                self.ball.direction = min(self.ball.direction, 4)
            elif key == ord("a"):
                self.ball.direction -= 1
                self.ball.direction = max(self.ball.direction, -4)
            sleep(0.01)

        cv2.destroyAllWindows()


__all__ = "Ball", "Env", "BounceBall"
