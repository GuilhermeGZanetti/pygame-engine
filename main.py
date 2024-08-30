"""pong"""
import random
import pygame as pg

from projetos.pong.models import Ball, Paddle
from src.utils import Position, Velocity

BALL_START_POSITION: Position = Position(450, 200)

def main():
    pg.init()

    # create a surface on screen that has the size of 700 x 200
    screen = pg.display.set_mode((900, 400))

    ball: Ball = Ball(BALL_START_POSITION, Velocity(0.2, 0.2))

    p1: Paddle = Paddle(Position(10, 200), 0, 100, 5)
    p2: Paddle = Paddle(Position(885, 200), 0, 100, 5)

    goals_p_left = 0
    goals_p_right = 0

    font = pg.font.SysFont(None, 48)

    finish_game = False

    # main loop
    while not finish_game:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if (event.type == pg.KEYUP and ((event.key == pg.K_w) or (event.key == pg.K_s))):
                p1.velocity.y = 0
            if (event.type == pg.KEYUP and ((event.key == pg.K_i) or (event.key == pg.K_j))):
                p2.velocity.y = 0
            if (event.type == pg.KEYDOWN and event.key == pg.K_w):
                p1.velocity.y = -0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_s):
                p1.velocity.y = 0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_i):
                p2.velocity.y = -0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_j):
                p2.velocity.y = 0.5

            # only do something if the event is of type QUIT
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                finish_game = True

        ball.position.x += ball.velocity.x
        ball.position.y += ball.velocity.y

        p1.position.y += p1.velocity.y
        p2.position.y += p2.velocity.y

        if(p1.position.y + p1.height > screen.get_height()):
            p1.position.y = screen.get_height() - p1.height
        if(p1.position.y < 0):
            p1.position.y = 0

        if(p2.position.y + p2.height > screen.get_height()):
            p2.position.y = screen.get_height() - p2.height
        if(p2.position.y < 0):
            p2.position.y = 0

        if (ball.position.y >= 400) or (ball.position.y <= 0):
            ball.velocity.y = -ball.velocity.y

        if (ball.position.x >= 900):
            goals_p_left += 1
            # reset game
            ball.position.x = 450
            ball.position.y = 200
            ball.velocity.x = random.choice([-0.2, 0.2])
            ball.velocity.y = random.choice([-0.2, 0.2])

        if (ball.position.x <= 0):
            goals_p_right += 1
            # reset game
            ball.position.x = 400
            ball.position.y = 200
            ball.velocity.x = random.choice([-0.2, 0.2])
            ball.velocity.y = random.choice([-0.2, 0.2])

        if (abs(ball.position.x - p1.position.x) < 5) and (ball.position.y >= p1.position.x) and (ball.position.y <= (p1.position.y + p1.height)):
            ball.velocity.x = 0.2

        if (abs(ball.position.x - p2.position.x) < 5) and (ball.position.y >= p2.position.y) and (ball.position.y <= (p2.position.y + p2.height)):
            ball.velocity.x = -0.2

        screen.fill((255, 255, 255))
        pg.draw.circle(screen, (0, 0, 0), (ball.position.x, ball.position.y), 5)
        
        p1.draw(screen=screen)
        p2.draw(screen=screen)

        img = font.render(f'{goals_p_left} x {goals_p_right}', True, (0, 0, 0))
        screen.blit(img, (450, 20))

        pg.display.flip()


if __name__ == "__main__":
    main()