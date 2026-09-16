from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

positions_of_man = [0.0, 450, 450]  
angle_of_player = 0.0 
more_activity_of_player = 5
Count_of_kiling = 0
Count_of_missedshots = 0
Cannot_play_anymore = False
spinning_of_cam = 0.0  
height_of_cam = 400.0
radious_of_cam = 600.0
modes_of_cam = 0 
automode_activates = False
activates_alter_cam = False
shotsss = []  
foe_in_game = []  
space_of_grid = 600
size_of_Tile = 60
foe_pulse = 0.0



def init_foe_in_game():
    global foe_in_game
    foe_in_game = []
    for _ in range(5):
        relive_char_foe(None)




def relive_char_foe(index):
    global foe_in_game
    while True:
        x = random.randint(-space_of_grid + 50, space_of_grid - 50)
        y = random.randint(-space_of_grid + 50, space_of_grid - 50)
        if math.sqrt((x - positions_of_man[0])**2 + (y - positions_of_man[1])**2) > 200:
            break

    
    new_foe = [x, y, random.randint(15, 25), random.random() * 100]


    if index is None:
        foe_in_game.append(new_foe)
    else:
        foe_in_game[index] = new_foe


init_foe_in_game()

def text_sketching(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def sketch_grid_wall ():
    for i in range(-space_of_grid, space_of_grid, size_of_Tile):
        for j in range(-space_of_grid, space_of_grid, size_of_Tile):
            if ((i + j) // size_of_Tile) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glBegin(GL_QUADS)
            glVertex3f(i, j, 0)
            glVertex3f(i + size_of_Tile, j, 0)
            glVertex3f(i + size_of_Tile, j + size_of_Tile, 0)
            glVertex3f(i, j + size_of_Tile, 0)
            glEnd()



    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-space_of_grid, space_of_grid, 0)
    glVertex3f(space_of_grid, space_of_grid, 0)
    glVertex3f(space_of_grid, space_of_grid, 60)
    glVertex3f(-space_of_grid, space_of_grid, 60)
    glEnd()



    #blue
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-space_of_grid, -space_of_grid, 0)
    glVertex3f(space_of_grid, -space_of_grid, 0)
    glVertex3f(space_of_grid, -space_of_grid, 60)
    glVertex3f(-space_of_grid, -space_of_grid, 60)
    glEnd()



    #cyan
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-space_of_grid, -space_of_grid, 0)
    glVertex3f(-space_of_grid, space_of_grid, 0)
    glVertex3f(-space_of_grid, space_of_grid, 60)
    glVertex3f(-space_of_grid, -space_of_grid, 60)
    glEnd()



    #magenta
    glColor3f(0.8, 0.0, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(space_of_grid, -space_of_grid, 0)
    glVertex3f(space_of_grid, space_of_grid, 0)
    glVertex3f(space_of_grid, space_of_grid, 60)
    glVertex3f(space_of_grid, -space_of_grid, 60)
    glEnd()



def sketch_man():
    glPushMatrix()
    glTranslatef(positions_of_man[0], positions_of_man[1], positions_of_man[2])
    glRotatef(angle_of_player, 0, 0, 1)


    if Cannot_play_anymore:
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 15, 0)

    glColor3f(0.3, 0.4, 0.2) 
    glPushMatrix()
    glScalef(20, 20, 40)
    glTranslatef(0, 0, 0.4)
    glutSolidCube(1)
    glPopMatrix()



    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 42)
    gluSphere(gluNewQuadric(), 12, 16, 16)
    glPopMatrix()



    # legsofman
    glColor3f(0.0, 0.0, 0.9)
    glPushMatrix()
    glTranslatef(-6, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 4, 15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(6, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 4, 15, 10, 10)
    glPopMatrix()


    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(0, 5, 30)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 2, 35, 10, 10)
    glPopMatrix()

    glPopMatrix()

def sketch_foe_in_game ():
    global foe_pulse
    foe_pulse += 0.05
    for foe in foe_in_game:
        ex, ey, base_r, phase = foe
        radi_curr = base_r + 5 * math.sin(foe_pulse + phase)

        glPushMatrix()
        glTranslatef(ex, ey, radi_curr)
        
        glColor3f(1.0, 0.0, 0.0)
        gluSphere(gluNewQuadric(), radi_curr, 16, 16)
        
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, 0, radi_curr * 0.6)
        gluSphere(gluNewQuadric(), radi_curr * 0.4, 10, 10)
        
        glPopMatrix()



def sketch_shotsss():
    glColor3f(1.0, 0.8, 0.0)
    for bullet in shotsss:
        glPushMatrix()
        glTranslatef(bullet[0], bullet[1], 30)
        glutSolidCube(8)
        glPopMatrix()



def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, 1.25, 1.0, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    if modes_of_cam == 1:
        rad = math.radians(angle_of_player + 90)
        eyeX = positions_of_man[0] - 30 * math.sin(rad)
        eyeY = positions_of_man[1] + 30 * math.cos(rad)
        eyeZ = 45 
        
        center_of_X = eyeX + 100 * math.sin(rad)
        center_of_Y = eyeY + 100 * math.cos(rad)
        center_of_Z = 40
        
        if automode_activates and activates_alter_cam:
            eyeZ = 120
            center_of_Z = 10
            
        gluLookAt(eyeX, eyeY, eyeZ, center_of_X, center_of_Y, center_of_Z, 0, 0, 1)


    else:
        rad = math.radians(spinning_of_cam)
        eyeX = positions_of_man[0] + radious_of_cam * math.cos(rad)
        eyeY = positions_of_man[1] + radious_of_cam * math.sin(rad)
        eyeZ = height_of_cam
        gluLookAt(eyeX, eyeY, eyeZ, positions_of_man[0], positions_of_man[1], positions_of_man[2], 0, 0, 1)



def keyboardListener(key, x, y):
    global angle_of_player, positions_of_man, automode_activates, activates_alter_cam, Cannot_play_anymore, more_activity_of_player, Count_of_kiling, Count_of_missedshots
    
    if key == b'r' or key == b'R':
        more_activity_of_player = 5
        Count_of_kiling = 0
        Count_of_missedshots = 0
        positions_of_man = [0.0, 0.0, 0.0]
        angle_of_player = 0.0
        Cannot_play_anymore = False
        automode_activates = False
        activates_alter_cam = False
        init_foe_in_game()
        return

    if Cannot_play_anymore:
        return

    speedmovement = 15.0
    speedrotation = 5.0
    rad = math.radians(angle_of_player + 90)


    if key == b'w' or key == b'W':
        positions_of_man[0] += speedmovement * math.sin(rad)
        positions_of_man[1] += speedmovement * math.cos(rad)
    elif key == b's' or key == b'S':
        positions_of_man[0] -= speedmovement * math.sin(rad)
        positions_of_man[1] -= speedmovement * math.cos(rad)
    elif key == b'a' or key == b'A':
        angle_of_player += speedrotation
    elif key == b'd' or key == b'D':
        angle_of_player -= speedrotation
    elif key == b'c' or key == b'C':
        automode_activates = not automode_activates
    elif key == b'v' or key == b'V':
        if automode_activates:
            activates_alter_cam = not activates_alter_cam


    positions_of_man[0] = max(-space_of_grid + 20, min(space_of_grid - 20, positions_of_man[0]))
    positions_of_man[1] = max(-space_of_grid + 20, min(space_of_grid - 20, positions_of_man[1]))



def specialKeyListener(key, x, y):
    global spinning_of_cam, height_of_cam
    if key == GLUT_KEY_LEFT:
        spinning_of_cam += 4.0
    elif key == GLUT_KEY_RIGHT:
        spinning_of_cam -= 4.0
    elif key == GLUT_KEY_UP:
        height_of_cam += 15.0
    elif key == GLUT_KEY_DOWN:
        height_of_cam = max(50.0, height_of_cam - 15.0)



def shot_now():
    rad = math.radians(angle_of_player + 90)
    dx = math.sin(rad) * 20.0
    dy = math.cos(rad) * 20.0
    shotsss.append([positions_of_man[0], positions_of_man[1], dx, dy])



def mouseListener(button, state, x, y):
    global modes_of_cam
    if Cannot_play_anymore: return
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not automode_activates:
            shot_now()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        modes_of_cam = 1 - modes_of_cam 



def updating_in_gameloop ():
    global Cannot_play_anymore, more_activity_of_player, Count_of_kiling, Count_of_missedshots, angle_of_player
    if Cannot_play_anymore: return

    if more_activity_of_player <= 0 or Count_of_missedshots >= 10:
        Cannot_play_anymore = True
        return

    if automode_activates:
        angle_of_player = (angle_of_player + 8.0) % 360
        rad = math.radians(angle_of_player + 90)

        for foe in foe_in_game:
            ex, ey = foe[0], foe[1]
            vec_to_foe = [ex - positions_of_man[0], ey - positions_of_man[1]]
            distancess = math.sqrt(vec_to_foe[0]**2 + vec_to_foe[1]**2)
            if distancess > 0:
                x__directions, y__directions = math.sin(rad), math.cos(rad)
                proj = (vec_to_foe[0]*x__directions + vec_to_foe[1]*y__directions) / distancess
                if proj > 0.995:
                    shot_now()
                    break

    rem_shotsss = []

    for bullet in shotsss:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
    
        if abs(bullet[0]) > space_of_grid or abs(bullet[1]) > space_of_grid:
            Count_of_missedshots += 1
            continue

        hit = False
        for idx, foe in enumerate(foe_in_game):
            ex, ey, r, _ = foe
            if math.sqrt((bullet[0] - ex)**2 + (bullet[1] - ey)**2) < (r + 10):
                Count_of_kiling += 1
                relive_char_foe(idx)
                hit = True
                break

        if not hit:
            rem_shotsss.append(bullet)
    shotsss[:] = rem_shotsss

    for idx, foe in enumerate(foe_in_game):
        ex, ey = foe[0], foe[1]
        dx = positions_of_man[0] - ex
        dy = positions_of_man[1] - ey
        distancess = math.sqrt(dx**2 + dy**2)

        
        if distancess > 0:
            foe[0] += (dx / distancess) * 2.5
            foe[1] += (dy / distancess) * 2.5



        if distancess < 25:
            more_activity_of_player -= 1
            relive_char_foe(idx)



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()
    sketch_grid_wall ()
    sketch_shotsss()
    sketch_man()
    sketch_foe_in_game ()

    text_sketching(20, 750, f"Player Life Remaining: {more_activity_of_player}")
    text_sketching(20, 720, f"Game Score: {Count_of_kiling}")
    text_sketching(20, 690, f"Player Bullet Missed: {Count_of_missedshots}/10")

    
    if automode_activates:
        text_sketching(20, 660, "CHEAT MODE ACTIVE", GLUT_BITMAP_HELVETICA_14)
        if activates_alter_cam:
            text_sketching(20, 640, "AUTOMATIC PERSPECTIVE TRACKING (V)", GLUT_BITMAP_HELVETICA_14)

    if Cannot_play_anymore:
        text_sketching(400, 400, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
        text_sketching(370, 360, "Press 'R' to Restart the Session", GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()


def idle():
    updating_in_gameloop ()
    glutPostRedisplay()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Bullet Frenzy - 3D Engine")


    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()



if __name__ == "__main__":
    main()