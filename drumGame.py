
import random, copy, midiFile
from tkinter import *


class Rect(object):
    def __init__(self, x, y, x1, y1, color, text = None):
        self.x=x
        self.x1=x1
        self.y=y
        self.y1=y1
        self.color=color
        self.text = text

    def draw(self, canvas):
        canvas.create_rectangle(self.x,self.y,self.x1,self.y1,fill=self.color)
        if self.text != None:
            canvas.create_text((self.x1+self.x)/2, (self.y1+self.y)/2, text = self.text, fill = "white")


class Dot(object):

    # Model
    def __init__(self, x, y, color, r = 30):
        self.x = x
        self.y = y
        self.r = r
        self.fill = color
        self.time = 0 #Time is used for dots that shrink

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
    data.undrawnNotes = midiFile.midiBeatTimes('AULDLANG.mid')['notes']
    data.dots = [ ]
    data.time = 0
    data.simpleDot = 30
    data.xButton = 80 #x position of guitar dots
    data.medDot = 35 #sizes
    data.largerDot = 40
    data.smallDot = 25
    data.score = 0
    data.clicked = True
    data.shrinkingDots = [] #Dots you missed
    data.clickDots = [] #Main 3 guitar dots
    data.clickDot1 = Dot(data.xButton, data.height/3, "black", r=data.simpleDot)
    data.clickDot2 = Dot(data.xButton, data.height/2, "black", r=data.simpleDot)
    data.clickDot3 = Dot(data.xButton, data.height*2/3, "black", r=data.simpleDot)
    data.clickDots.extend([data.clickDot1, data.clickDot2, data.clickDot3])
    data.paused = False
    data.menu = True
    data.menuRect = []

def mousePressed(event, data):
    if data.menu:
        data.menu = False

def redrawAll(canvas, data):
    if not data.menu and not data.paused:
        canvas.create_rectangle(10, data.height/3 - 30, data.width, data.height*2/3+30, fill = "gray")
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
    elif data.menu and not data.paused:
        back = Rect(data.width/6, data.height/6, data.width*5/6,data.height*5/6, "gray")
        data.menuRect.append(back)
        button1 = Rect(data.width/5,data.height/5, data.width*4/5, data.height*2/5, "black", "Click to start game!")
        data.menuRect.append(button1)
        for rect in data.menuRect:
            rect.draw(canvas)

def keyPressed(event, data, canvas):
    if not data.menu and not data.paused:
        data.clicked = False
        moreDots = []
        if event.keysym == "Up":
            for dots in data.dots:
                # if not dots.containsPoint(data.xButton, data.height/2):
                if dots.distanceToPoint(data.xButton, data.height / 2) > 20: #If not close
                    moreDots.append(dots)
                elif dots.distanceToPoint(data.xButton, data.height / 2) > 7: #If somewhat close
                    data.clickDot2.r = data.medDot #Increase size for guitar dot
                    data.clickDot2.time = 3 #Lasts .3 secs
                    data.score += 5
                    data.clicked = True
                else: #IF really close
                    data.clickDot2.r = data.largerDot 
                    data.clickDot2.time = 5
                    data.score += 10
                    data.clicked = True
            if data.clicked == False:
                data.clickDot2.r = data.smallDot
                data.clickDot2.time = 3
                data.score -= 2

            data.dots = moreDots

        elif event.keysym == "Left":
            for dots in data.dots:
                if dots.distanceToPoint(data.xButton, data.height / 3) > 20:
                    moreDots.append(dots)
                elif dots.distanceToPoint(data.xButton, data.height / 3) > 7:
                    data.clickDot1.r = data.medDot
                    data.clickDot1.time = 3
                    data.score += 5
                    data.clicked = True
                else:
                    data.clickDot1.r = data.largerDot
                    data.clickDot1.time = 5
                    data.score += 10
                    data.clicked = True
            if data.clicked == False:
                data.clickDot1.r = data.smallDot
                data.clickDot1.time = 3
                data.score -= 2
            data.dots = moreDots

        elif event.keysym == "Right":
            for dots in data.dots:
                if dots.distanceToPoint(data.xButton, data.height * 2 / 3) > 20:
                    moreDots.append(dots)
                elif dots.distanceToPoint(data.xButton, data.height *2 / 3) > 7:
                    data.clickDot3.r = data.medDot
                    data.clickDot3.time = 3
                    data.score += 5
                    data.clicked = True
                else:
                    data.clickDot3.r = data.largerDot
                    data.clickDot3.time = 5
                    data.score += 10
                    data.clicked = True
            if data.clicked == False:
                data.clickDot3.r = data.smallDot
                data.clickDot3.time = 3
                data.score -= 2
            data.dots = moreDots


def timerFired(data):
    if not data.menu and not data.paused:
        data.time += 1


        newNotes = copy.deepcopy(data.undrawnNotes)

        for note in data.undrawnNotes:
            convertedNoteTime = note[1] * 10

            if convertedNoteTime <= data.time:

                lane = int(random.randint(2,4))

                color = None
                if lane == 2:
                    color = "blue"
                elif lane == 3:
                    color = "green"
                else:
                    color = "red"
                data.dots.append(MovingDot(data.width, data.height * lane / 6, color))
                newNotes.remove(note)
        data.undrawnNotes = newNotes

        newDots = []
        for dot in data.shrinkingDots:
            if type(dot) != Dot:
                dot.move(data)
                if dot.r > 5: #Removes small dots
                    newDots.append(dot)
                    if dot.time > 2: #Shrinks every .2 sec
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
                    data.score -= 10 #If missed
                    data.shrinkingDots.append(dot)
                    dot.r -= 5
        data.dots = newDots

        for dot in data.clickDots: #Guitar dots
            dot.time -= 1
            if dot.time == 0:
                dot.r = data.simpleDot

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
    data.timerDelay = 100 # milliseconds
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