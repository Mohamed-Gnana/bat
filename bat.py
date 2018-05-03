from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

FROM_RIGHT = 1
FROM_LEFT = 2
FROM_TOP = 3
FROM_BOTTOM = 4

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
leftp1 = 0
leftp2 = 0

deltaX = 1
deltaY = 1

time_interval = 10  # try  2,5,7 msec


class RECTA:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top


ball = RECTA(100, 100, 120, 120)  # initial position of the ball


wall = RECTA(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)  # initial position of the bat
# Initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  # l,r,b,t,n,f

    glMatrixMode(GL_MODELVIEW)


def DrawRectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex(rect.left, rect.bottom, 0)  # Left - Bottom
    glVertex(rect.right, rect.bottom, 0)
    glVertex(rect.right, rect.top, 0)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def drawText(string, x, y):
    glLineWidth(2)
    glColor(1, 1, 0)  # Yellow Color
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(0.13, 0.13, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)


def Test_Ball_Wall(ball, wall):  # Collision Detection between Ball and Wall
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM

    if ball.right >= wall.right:
        return FROM_RIGHT
    if ball.left <= wall.left:
        return FROM_LEFT
    if ball.top >= wall.top:
        return FROM_TOP
    if ball.bottom <= wall.bottom:
        return FROM_BOTTOM


def Test_Ball_player_1(ball, player_1):  # Collision Detection between Ball and Bat
    if ball.bottom <= player_1.top and ((ball.left >= player_1.left and ball.left <= player_1.right) or (ball.right <= player_1.right and ball.right >= player_1.left)) and deltaY == -1: #(try this)
        return True
    return False
def Test_Ball_player_2(ball, player_2):  # Collision Detection between Ball and Bat
    if ball.top >= player_2.bottom and ((ball.left >= player_2.left and ball.left <= player_2.right) or (ball.right <= player_2.right and ball.right >= player_2.left)) and deltaY == 1: #(try this)
        return True
    return False

# Key Board Messages
def keyboard(key, x, y):
    global leftp1
    global leftp2
    if key == b"q":
        sys.exit(0)
    if key == b'r':
        leftp1 += 10
    if key == b'e' :
        leftp1 -= 10
    if key == b'f':
        leftp2 += 10
    if key == b'g':
        leftp2 -= 10



keyboard_x = WINDOW_WIDTH - 30
def arrow_press(key, x, y):
    global keyboard_x
    if key == GLUT_KEY_LEFT:
        keyboard_x -= 20
    elif key == GLUT_KEY_RIGHT:
        keyboard_x += 20

mouse_x = 0


def MouseMotion(x, y):
    global mouse_x
    mouse_x = x


def Timer(v):
    Display()

    glutTimerFunc(time_interval, Timer, 1)


player_2Result = 0
player_1Result = 0


def Display():
    global player_2Result
    global player_1Result
    global FROM_RIGHT
    global FROM_LEFT
    global FROM_TOP
    global FROM_BOTTOM
    global deltaX
    global deltaY
    global leftp1
    global leftp2
    global  player_2
    global player_1
    player_1 = RECTA(leftp1,0 , 60, 10)
    player_2 = RECTA(WINDOW_WIDTH - leftp2,WINDOW_HEIGHT - 10,WINDOW_WIDTH,WINDOW_HEIGHT)
    glClear(GL_COLOR_BUFFER_BIT)
    string = "player_2 : " + str(player_2Result)
    drawText(string, 10, 440)
    string = "player_1 :  " + str(player_1Result)
    drawText(string, 10, 400)

    ball.left = ball.left + deltaX  # updating ball's coordinates
    ball.right = ball.right + deltaX
    ball.top = ball.top + deltaY
    ball.bottom = ball.bottom + deltaY

    glColor(1, 1, 1)  # White color

    DrawRectangle(ball)

    if Test_Ball_Wall(ball, wall) == FROM_RIGHT:
        deltaX = -1

    if Test_Ball_Wall(ball, wall) == FROM_LEFT:
        deltaX = 1

    if Test_Ball_Wall(ball, wall) == FROM_TOP:
        deltaY = -1

    if Test_Ball_Wall(ball, wall) == FROM_BOTTOM:
        deltaY = 1
        #player_2Result = player_2Result + 1

    #player_1.left = mouse_x - leftp1
    #player_1.right = mouse_x + 30
    #player_2.left = keyboard_x - leftp2
    #player_2.right = keyboard_x + 30
    DrawRectangle(player_1)
    DrawRectangle(player_2)
    if Test_Ball_player_1(ball, player_1) == True:
        glColor(1, 0, 0)
        DrawRectangle(player_1)
        DrawRectangle(ball)
        deltaY = 1
        player_1Result = player_1Result + 1
    if Test_Ball_player_2(ball, player_2) == True:
        glColor(1, 0, 0)
        DrawRectangle(player_2)
        DrawRectangle(ball)
        deltaY = -1
        player_2Result = player_2Result + 1
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Simple Ball Bat OpenGL game");
    glutDisplayFunc(Display)
    glutTimerFunc(time_interval, Timer, 1)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_press)
    glutPassiveMotionFunc(MouseMotion)
    init()
    glutMainLoop()


main()

