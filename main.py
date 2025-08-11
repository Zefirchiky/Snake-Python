import random
import time
import os
import pygame as pg

pg.init()

WIDTH, HEIGHT = 1000, 800
DIS = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Snake")

H_WIDTH, H_HEIGHT = WIDTH // 2, HEIGHT // 2

SNAKE_SPEED = 20
SNAKE_SCALE = 18
SNAKE_HITBOX_SCALE = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 20

if WIDTH % SNAKE_HITBOX_SCALE != 0 or HEIGHT % SNAKE_HITBOX_SCALE != 0:
    raise ValueError("The width and height must be multiples of the snake's hitbox")

squares_map = [
    [0 for _ in range(HEIGHT // SNAKE_HITBOX_SCALE)]
    for _ in range(WIDTH // SNAKE_HITBOX_SCALE)
]

squares_map_size = {"height": len(squares_map[0]), "width": len(squares_map)}


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        pg.draw.rect(
            DIS,
            RED,
            [
                self.x * SNAKE_HITBOX_SCALE,
                self.y * SNAKE_HITBOX_SCALE,
                SNAKE_HITBOX_SCALE,
                SNAKE_HITBOX_SCALE,
            ],
        )


class Snake:
    def __init__(self):
        self.color = WHITE
        self.do_grow = False
        self.is_alive = True

    def create(self):
        self.body = [
            [squares_map_size["width"] // 2 - 1, squares_map_size["height"] // 2],
            [squares_map_size["width"] // 2, squares_map_size["height"] // 2],
            [squares_map_size["width"] // 2 + 1, squares_map_size["height"] // 2],
        ]
        self.direction = [1, 0]

    def check_food_collision(self, food_list):
        for i, food in enumerate(food_list):
            if food.x == self.body[-1][0] and food.y == self.body[-1][1]:
                print(i, food.x, food.y, self.body[-1])
                food_list.pop(i)
                food_list.append(
                    Food(
                        random.randint(0, squares_map_size["width"]),
                        random.randint(0, squares_map_size["height"]),
                    )
                )
                self.do_grow = True

    def ch_direct(self, keys):
        dx = keys[pg.K_d] - keys[pg.K_a]
        dy = keys[pg.K_s] - keys[pg.K_w]
        if dx or dy:
            if (dx and dx == -self.direction[0]) or (dy and dy == -self.direction[1]):
                self.is_alive = False
            self.direction = [dx, 0] if dx else [0, dy]

    def move(self, keys):
        self.ch_direct(keys)
        if not self.do_grow:
            del self.body[0]
        else:
            self.do_grow = False
            
        if (
            self.body[-1][0] + self.direction[0] > squares_map_size["width"]
        ):  # if head more than display width, teleport on left
            self.body.append([0, self.body[-1][1] + self.direction[1]])

        elif (
            self.body[-1][0] + self.direction[0] < 0
        ):  # if head less than display width, teleport on right
            self.body.append(
                [squares_map_size["width"], self.body[-1][1] + self.direction[1]]
            )

        elif (
            self.body[-1][1] + self.direction[1] > squares_map_size["height"]
        ):  # if head more than display height, teleport on top
            self.body.append([self.body[-1][0] + self.direction[0], 0])

        elif (
            self.body[-1][1] + self.direction[1] < 0
        ):  # if head less than display height, teleport on bottom
            self.body.append(
                [self.body[-1][0] + self.direction[0], squares_map_size["height"]]
            )

        else:
            self.body.append(
                [
                    self.body[-1][0] + self.direction[0],
                    self.body[-1][1] + self.direction[1],
                ]
            )

    def draw(self):
        for x, y in self.body:
            pg.draw.rect(
                DIS,
                self.color,
                [
                    x * SNAKE_HITBOX_SCALE,
                    y * SNAKE_HITBOX_SCALE,
                    SNAKE_HITBOX_SCALE,
                    SNAKE_HITBOX_SCALE,
                ],
            )


def main():
    run = True
    snake = Snake()
    food_list = [
        Food(
            random.randint(0, squares_map_size["width"]),
            random.randint(0, squares_map_size["height"]),
        )
        for _ in range(0, 5)
    ]
    clock = pg.time.Clock()
    snake.create()
    while run:
        DIS.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        keys = pg.key.get_pressed()
        for food in food_list:
            food.draw()
        snake.move(keys)
        snake.check_food_collision(food_list)
        if not snake.is_alive:
            run = False
        snake.draw()
        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
