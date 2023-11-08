import tkinter
import random

# definitions
WIDTH = 700
HEIGHT = 600
BG_COLOR = 'black'
MAIN_BALL_COLOR = 'blue'
MAIN_BALL_RADIUS = 40
BAD_COLOR = 'red'
COLORS = ['gray', 'fuchsia', BAD_COLOR, 'pink', 'cyan', 'teal', 'yellow', BAD_COLOR, 'green',  'gold', 'chartreuse', BAD_COLOR, 'aqua']
NUM_OF_BALLS = 15
MAX_RADIUS = 45
MIN_RADIUS = 20
INIT_DX = 1
INIT_DY = 1
ZERO = 0

# class ball
class Ball():
    def __init__(self, x, y, r, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy

    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=self.color,
                            outline = self.color if self.color != BAD_COLOR else 'white')

    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill=BG_COLOR,
                           outline=BG_COLOR)

    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a * a + b * b) ** 0.5 <= self.r + ball.r

    def move(self):
        # collision with the walls
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= ZERO):
            self.dy = -self.dy
        # the balls collision
        for ball in balls:
            if self.is_collision(ball):
                if ball.color != BAD_COLOR:  # not a bad ball (!red)
                    ball.hide()
                    balls.remove(ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:  # bad ball (red)
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        if self.dx * self.dy != 0:
            self.draw()


# mouse events
def mouse_click(event):
    global main_ball
    if event.num == 1:                                                  # left mouse button
        if 'main_ball' not in globals():                                # start
            main_ball = Ball(event.x, event.y, MAIN_BALL_RADIUS, MAIN_BALL_COLOR, INIT_DX, INIT_DY)
            if main_ball.x > WIDTH / 2:
                main_ball.dx = -main_ball.dx
            if main_ball.y > HEIGHT / 2:
                main_ball.dy = -main_ball.dy
            main_ball.draw()
        else:                                                           # turn left
            if main_ball.dy * main_ball.dx > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3:                                               # right mouse button: turn right
        if main_ball.dy * main_ball.dx > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy


# create a list of objects-balls
def create_list_of_balls(number):
    list = []
    while len(list) < number:
        next_ball = Ball(random.choice(range(MAX_RADIUS, WIDTH - MAX_RADIUS)),
                         random.choice(range(MAX_RADIUS, HEIGHT - MAX_RADIUS)),
                         random.choice(range(MIN_RADIUS, MAX_RADIUS)),
                         random.choice(COLORS))
        is_collision = False
        for ball in list:
            if next_ball.is_collision(ball):
                is_collision = True
                break
        if not is_collision:
            list.append(next_ball)
            next_ball.draw()
    return list


# count the number of bad balls
def count_bad_balls(list_of_balls):
    result = 0
    for ball in list_of_balls:
        if ball.color == BAD_COLOR:
            result += 1
    return result


# games main loop
def main():
    if 'main_ball' in globals():
        main_ball.move()
        if len(balls) - num_of_bad_balls == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="YOU WON!", font="Arial 30", fill="lime")
            main_ball.dx = main_ball.dy = 0
        elif main_ball.dx * main_ball.dy == 0:
            canvas.create_text(WIDTH - 500, HEIGHT - 50, text="YOU LOSE!", font="Arial 30", fill="red")
    root.after(10, main)


# create a window, the canvas and start game
root = tkinter.Tk()
root.title("COLLIDING BALLS")
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-2>', mouse_click, '+')
canvas.bind('<Button-3>', mouse_click, '+')
balls = create_list_of_balls(NUM_OF_BALLS)
num_of_bad_balls = count_bad_balls(balls)
if 'main_ball' in globals():  # for restart
    del main_ball
main()
root.mainloop()
