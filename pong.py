"""
Simple Pong game implemented with Python turtle
by Alper Kaplan
"""
import time
import turtle

running = True
pause = False
wn = turtle.Screen()
p1 = turtle.Turtle()
p2 = turtle.Turtle()
score_style = ("Helvetica", 32, 'normal', 'bold')


def draw_screen():
    """Initializes window with turtle.Screen().

    Returns
    -------
    wn: turtle.Screen()
        Window.
    """
    global wn
    wn.title("Pong by Alper Kaplan")
    wn.bgcolor("black")
    wn.setup(width=800, height=600)
    init_key_event_listener(wn)
    wn.tracer(0)

    return wn


def init_key_event_listener(window: turtle.Turtle()):
    window.onkey(p1_up, "W")
    window.onkey(p1_up, "w")
    window.onkey(p1_down, "S")
    window.onkey(p1_down, "s")
    window.onkey(p2_up, "Up")
    window.onkey(p2_down, "Down")
    window.onkey(quit_game, "Q")
    window.onkey(quit_game, "q")
    window.onkey(pause_game, "p")
    window.onkey(pause_game, "P")
    window.listen()


def draw_player(p, starting_point):
    p.speed(0)
    p.shape("square")
    p.color("white")
    p.shapesize(stretch_wid=5, stretch_len=1)
    p.penup()
    p.goto(starting_point, 0)
    return p


def draw_ball(ball):
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 270)
    return ball


def draw_score(score, pos_x):
    score.speed(0)
    score.color('white')
    score.penup()
    score.goto(pos_x, 200)
    score.write('0', font=score_style, align='center')
    score.hideturtle()
    return score


def init_game():
    """Initialize game by drawing the screen and other necessary items, such as players, ball and scores

    Returns
    -------
        p1: turtle.Turtle()
            Player 1.

        p2: turtle.Turtle()
            Player 2.

        ball: turtle.Turtle()

        p1_score: turtle.Turtle()
            Player 1's score.

        p2_score: turtle.Turtle()
            Player 2's score.
    """
    global p1, p2
    draw_screen()

    p1 = draw_player(p1, -350)
    p2 = draw_player(p2, 350)

    ball = draw_ball(turtle.Turtle())

    p1_score = draw_score(score=turtle.Turtle(), pos_x=-150)
    p2_score = draw_score(score=turtle.Turtle(), pos_x=150)

    return p1, p2, ball, p1_score, p2_score


def game_loop(game_var: tuple):
    p1, p2, ball, p1_score, p2_score = game_var[0], game_var[1], game_var[2], game_var[3], game_var[4]

    p1_score_int, p2_score_int = 0, 0

    ball_dx, ball_dy = 0, 270
    ball_dir_x, ball_dir_y = 'left', 'down'

    while running:
        if pause:
            wn.update()
            continue

        wn.update()

        p1_x, p1_y = p1.pos()[0], p1.pos()[1]
        p2_x, p2_y = p2.pos()[0], p2.pos()[1]
        ball_x, ball_y = ball.pos()[0], ball.pos()[1]

        ball_dir_x = find_ball_dir_on_x_axis(ball_x, ball_y, ball_dir_x, p1_x, p1_y, p2_x, p2_y)
        ball_dir_y = find_ball_dir_on_y_axis(ball_y, ball_dir_y)
        ball_dx, ball_dy = next_ball_coordinates(ball_dir_x, ball_dir_y, ball_dx, ball_dy)

        ball_dx, ball_dy, ball_dir_x, p1_score_int, p2_score_int = handle_goal(ball_x, ball_dir_x, p1, p1_score, p1_score_int, p1_x,
                                                                               p2, p2_score, p2_score_int, p2_x, ball_dx, ball_dy)

        ball.goto(ball_dx, ball_dy)
        tick(fps=250)


def handle_goal(ball_x, ball_dir_x, p1, p1_score, p1_score_int, p1_x,
                p2, p2_score, p2_score_int, p2_x, ball_dx, ball_dy):
    if ball_x < p1_x - 40:
        p2_score_int += 1
        p2_score.clear()
        p2_score.write(arg=str(p2_score_int), font=score_style, align='center')

        ball_dx, ball_dy, ball_dir_x = 0, 270, 'left'

        p1.setpos(-350, 0)
        p2.setpos(350, 0)
    elif ball_x > p2_x + 40:
        p1_score_int += 1
        p1_score.clear()
        p1_score.write(arg=str(p1_score_int), font=score_style, align='center')

        ball_dx, ball_dy, ball_dir_x = 0, 270, 'right'

        p1.setpos(-350, 0)
        p2.setpos(350, 0)

    return ball_dx, ball_dy, ball_dir_x, p1_score_int, p2_score_int


def next_ball_coordinates(dir_x, dir_y, dx, dy):
    """Finds ball's next coordinates.

    Parameters
    ----------
    dir_x: str
        Specifies ball's x-axis direction.

    dir_y: str
        Specifies ball's y-axis direction.

    dx: int


    dy: int


    Returns
    -------

    """
    if dir_x is 'left':
        dx -= 1
    elif dir_x is 'right':
        dx += 1
    if dir_y is 'down':
        dy -= 1
    elif dir_y is 'up':
        dy += 1
    return dx, dy


def find_ball_dir_on_y_axis(ball_y, dir_y):
    if ball_y == 285:
        dir_y = 'down'
    elif ball_y == -285:
        dir_y = 'up'
    return dir_y


def find_ball_dir_on_x_axis(ball_x, ball_y, dir_x, p1_x, p1_y, p2_x, p2_y):
    if (p2_x - 20 < ball_x < p2_x + 20) and (p2_y - 50 < ball_y < p2_y + 50):
        dir_x = 'left'
    elif (p1_x - 20 < ball_x < p1_x + 20) and (p1_y - 50 < ball_y < p1_y + 50):
        dir_x = 'right'
    return dir_x


def p1_up():
    if not pause:
        global p1
        if p1.pos()[1] < 240:
            p1.goto(p1.pos()[0], p1.pos()[1] + 30)


def p1_down():
    if not pause:
        global p1
        if p1.pos()[1] > -240:
            p1.goto(p1.pos()[0], p1.pos()[1] - 30)


def p2_up():
    if not pause:
        global p2
        if p2.pos()[1] < 240:
            p2.goto(p2.pos()[0], p2.pos()[1] + 30)


def p2_down():
    if not pause:
        global p2
        if p2.pos()[1] > -240:
            p2.goto(p2.pos()[0], p2.pos()[1] - 30)


def quit_game():
    turtle.done()


def pause_game():
    global pause
    pause = not pause
    print(pause)


tick_frame = 0
tick_fps = 20000000  # real raw FPS
tick_t0 = time.time()


def tick(fps=60):
    global tick_frame, tick_fps, tick_t0
    n = tick_fps / fps
    tick_frame += n

    while n > 0:
        n -= 1

    if time.time() - tick_t0 > 1:
        tick_t0 = time.time()
        tick_fps = tick_frame
        tick_frame = 0


if __name__ == "__main__":
    game_var = init_game()
    game_loop(game_var)
