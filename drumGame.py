# oopyDotsDemo.py
# starts with betterDotsDemo and adds:
#   * a dotCounter that counts all the instances of Dot or its subclasses
#   * a MovingDot subclass of Dot that scrolls horizontally
#   * a FlashingMovingDot subclass of MovingDot that flashes and moves

import random
from tkinter import *

class Dot(object):
    dotCount = 0

    # Model
    def __init__(self, x, y, color, r = 30):
        self.x = x
        self.y = y
        self.r = r
        self.fill = color
        self.clickCount = 0
        self.time = 0

    # View
    def draw(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill=self.fill)

    # Controller
    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def distanceToPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return d

class MovingDot(Dot):
    # Model
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.speed = -10 # default initial speed

    # Controller
    def move(self, data):
        self.x += self.speed
        if (self.x > data.width):
            self.x = 0

    def shrink(self):
        self.r -= 5
        self.time = 0


# Core animation code

def init(data):
    data.dots = [ ]
    data.time = 0
    data.simpleDot = 30
    data.xButton = 80
    data.medDot = 35
    data.largerDot = 40
    data.dotTime = 0
    data.score = 0
    data.shrinkingDots = []
    data.clickDots = []
    data.clickDot1 = Dot(data.xButton, data.height/3, "black", r=data.simpleDot)
    data.clickDot2 = Dot(data.xButton, data.height/2, "black", r=data.simpleDot)
    data.clickDot3 = Dot(data.xButton, data.height*2/3, "black", r=data.simpleDot)
    data.clickDots.extend([data.clickDot1, data.clickDot2, data.clickDot3])

def mousePressed(event, data):
    pass

def redrawAll(canvas, data):
    canvas.create_text(data.width/2, 10, text="%d Points" % data.score)
    canvas.create_rectangle(data.xButton + 10, data.height/3 - 15, data.width, data.height/3 +15, fill = "darkred")
    canvas.create_rectangle(data.xButton + 10, data.height*2/3 -15, data.width, data.height*2/3 +15, fill = "darkred")
    canvas.create_rectangle(data.xButton+10, data.height/2 - 15, data.width, data.height/2 +15, fill = "darkred")
    # canvas.create_oval(data.xButton - data.ovalRadius1, data.height/3 + data.ovalRadius1, data.xButton+data.ovalRadius1, data.height/3 - data.ovalRadius1, fill = "black")
    # data.clickDot1.draw(canvas)
    # canvas.create_oval(data.xButton - data.ovalRadius2, data.height/2- data.ovalRadius2, data.xButton+data.ovalRadius2, data.height/2 + data.ovalRadius2, fill = "black")
    # canvas.create_oval(data.xButton - data.ovalRadius3, data.height*2/3- data.ovalRadius3, data.xButton+data.ovalRadius3, data.height*2/3 + data.ovalRadius3, fill = "black")
    for dot in data.clickDots:
        dot.draw(canvas)
    for dot in data.dots:
        dot.draw(canvas)
    for dot in data.shrinkingDots:
        dot.draw(canvas)

def keyPressed(event, data, canvas):
    moreDots = []
    if event.keysym == "Up":
        for dots in data.dots:
            # if not dots.containsPoint(data.xButton, data.height/2):
            if dots.distanceToPoint(data.xButton, data.height / 2) > 16:
                moreDots.append(dots)
            elif dots.distanceToPoint(data.xButton, data.height / 2) > 7:
                data.clickDot2.r = data.medDot
                data.clickDot2.time = 3
                data.score += 5
            else:
                data.clickDot2.r = data.largerDot
                data.clickDot2.time = 5
                data.score += 10

        data.dots = moreDots

    elif event.keysym == "Left":
        for dots in data.dots:
            if dots.distanceToPoint(data.xButton, data.height / 3) > 16:
                moreDots.append(dots)
            elif dots.distanceToPoint(data.xButton, data.height / 3) > 7:
                data.clickDot1.r = data.medDot
                data.clickDot1.time = 3
                data.score += 5
            else:
                data.clickDot1.r = data.largerDot
                data.clickDot1.time = 5
                data.score += 10
        data.dots = moreDots

    elif event.keysym == "Right":
        for dots in data.dots:
            if dots.distanceToPoint(data.xButton, data.height * 2 / 3) > 16:
                moreDots.append(dots)
            elif dots.distanceToPoint(data.xButton, data.height *2 / 3) > 7:
                data.clickDot3.r = data.medDot
                data.clickDot3.time = 3
                data.score += 5
            else:
                data.clickDot3.r = data.largerDot
                data.clickDot3.time = 5
                data.score += 10
        data.dots = moreDots


def timerFired(data):
    data.time += 1
    data.dotTime += 1
    if data.time % 10 == 0:
        lane = random.randint(2, 4)
        color = None
        if lane == 2:
            color = "blue"
        elif lane == 3:
            color = "green"
        else:
            color = "red"
        data.dots.append(MovingDot(data.width, data.height * lane / 6, color))

    newDots = []
    for dot in data.shrinkingDots:
        if type(dot) != Dot:
            dot.move(data)
            if dot.r > 5:
                newDots.append(dot)
                if dot.time > 1:
                    dot.shrink()
            dot.time += 1
    data.shrinkingDots = newDots


    newDots = []
    for dot in data.dots:
        if type(dot) != Dot:
            dot.move(data)
            if dot.x > data.xButton - dot.r:
                newDots.append(dot)
            else:
                data.score -= 10
                data.shrinkingDots.append(dot)
                dot.r -= 5
    data.dots = newDots

    for dot in data.clickDots:
        dot.time -= 1
        if dot.time == 0:
            dot.r = data.simpleDot
                

    if data.dotTime % 4 == 0:
        data.ovalRadius1 = 30
        data.ovalRadius2 = 30
        data.ovalRadius3 = 30 

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 500)