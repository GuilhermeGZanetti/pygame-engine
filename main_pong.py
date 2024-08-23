
import random
import pygame as pg


def main():
    pg.init()

    # create a surface on screen that has the size of 700 x 200
    screen = pg.display.set_mode((900, 400))

    ball_pos_x = 450
    ball_pos_y = 200

    v_x = 0.2
    v_y = 0.2

    p1_pos_x = 10
    p1_pos_y = 200
    p1_v = 0

    p2_pos_x = 885
    p2_pos_y = 200
    p2_v = 0

    player_width = 5
    player_height = 100

    goals_p_left = 0
    goals_p_right = 0

    font = pg.font.SysFont(None, 48)

    finish_game = False

    # main loop
    while not finish_game:
        # event handling, gets all event from the event queue
        for event in pg.event.get():
            if (event.type == pg.KEYUP and ((event.key == pg.K_w) or (event.key == pg.K_s))):
                p1_v = 0
            if (event.type == pg.KEYUP and ((event.key == pg.K_i) or (event.key == pg.K_j))):
                p2_v = 0
            if (event.type == pg.KEYDOWN and event.key == pg.K_w):
                p1_v -= 0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_s):
                p1_v += 0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_i):
                p2_v -= 0.5
            if (event.type == pg.KEYDOWN and event.key == pg.K_j):
                p2_v += 0.5

            # only do something if the event is of type QUIT
            if (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                finish_game = True

        ball_pos_x += v_x
        ball_pos_y += v_y

        p1_pos_y += p1_v
        p2_pos_y += p2_v

        if(p1_pos_y + player_height > screen.get_height()):
            p1_pos_y = screen.get_height() - player_height
        if(p1_pos_y < 0):
            p1_pos_y = 0

        if(p2_pos_y + player_height > screen.get_height()):
            p2_pos_y = screen.get_height() - player_height
        if(p2_pos_y < 0):
            p2_pos_y = 0

        if (ball_pos_y >= 400) or (ball_pos_y <= 0):
            v_y = -v_y

        if (ball_pos_x >= 900):
            goals_p_left += 1
            # reset game
            ball_pos_x = 450
            ball_pos_y = 200
            v_x = random.choice([-0.2, 0.2])
            v_y = random.choice([-0.2, 0.2])

        if (ball_pos_x <= 0):
            goals_p_right += 1
            # reset game
            ball_pos_x = 400
            ball_pos_y = 200
            v_x = random.choice([-0.2, 0.2])
            v_y = random.choice([-0.2, 0.2])

        if (abs(ball_pos_x - p1_pos_x) < 5) and (ball_pos_y >= p1_pos_y) and (ball_pos_y <= (p1_pos_y + player_height)):
            v_x = 0.2

        if (abs(ball_pos_x - p2_pos_x) < 5) and (ball_pos_y >= p2_pos_y) and (ball_pos_y <= (p2_pos_y + player_height)):
            v_x = -0.2

        screen.fill((255, 255, 255))
        pg.draw.circle(screen, (0, 0, 0), (ball_pos_x, ball_pos_y), 5)

        pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(
            p1_pos_x, p1_pos_y, player_width, player_height))

        pg.draw.rect(screen, (0, 0, 0), pg.rect.Rect(
            p2_pos_x, p2_pos_y, player_width, player_height))

        img = font.render(f'{goals_p_left} x {goals_p_right}', True, (0, 0, 0))
        screen.blit(img, (450, 20))

        pg.display.flip()


if __name__ == "__main__":
    main()