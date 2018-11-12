"""Monopoly"""

from cs110graphics import *
import random
WINDOW = None

class Board:
    """The Monopoly Game Board"""
    def __init__(self, center):
        self._center = center
        self._image = []
        #upload the board's url
        self._board = Image("https://s-media-cache-ak0.pinimg.com/736x/5f/26/39/5f2639d8345e3912e9676260b4c0c676.jpg", self._center, 600, 600)
        self._image.append(self._board)
        
    
    
    def addTo(self, win):
        """add the boad and cards to the window"""
        for img in self._image:
            win.add(img)

def diceImage(k):
    """recover te image of te dice"""
    url = "https://www.wpclipart.com/recreation/" + \
          "games/dice/die_face_" + str(k) + ".png"
    return url

class Die(EventHandler):
    """a dice class that can be rolled to move players"""
    def __init__(self, controller, center=(0, 0), width=50, height=50):
        EventHandler.__init__(self)
        self._center = center
        self._controller = controller
        self._images = []
        for i in range(6):
            die = Image(diceImage(i + 1), self._center, width, height)
            die.addHandler(self)
            self._images.append(die)
        self._value = 6
        self.setValue(6)
        
        #enable the dice for  a player's turn
        self._enable = True
        
        

    def addTo(self, win):
        """add a dice to the window"""
        for img in self._images:
            win.add(img)

    def getValue(self):
        """return te value of te dice"""
        return self._value
        
    def setValue(self, n):
        """set the value of the dice"""
        for i in range(6):
            if i + 1 == n:
                self._images[i].setDepth(0)
            else:
                self._images[i].setDepth(1)
        self._value = n
        
    def roll(self):
        """roll the dice"""
        self.setValue(random.randrange(6) + 1)
        
    def turnOn(self):
        """enable the dice"""
        self._enable = True
        
    def turnOff(self):
        """disable the dice"""
        self._enable = False
        
    def getEnable(self):
        """return the status of enable"""
        return self._enable
            
class Pawn:
    """a pawn class"""
    def __init__(self, number, color, center=(600-62.5, 600-20)):
        self._center = center
        self._count = 0
        
        self._image = []
        #Build the rectangle at the starting point of the board
        self._rectangle = Rectangle(25, 25, self._center)
        self._color = color
        self._rectangle.setFillColor(self._color)
        self._rectangle.setDepth(2)
        self._image.append(self._rectangle)
        
        #build the text, used to identify the pawn
        self._text = Text(str(number), self._center, 15)
        self._text.setDepth(1)
        self._image.append(self._text)
        
    def addTo(self, win):
        """add the pawn to the window"""
        for img in self._image:
            win.add(img)
            
    def move(self, count):
        """move the pawn around the board"""
        if count > 40:
            count = count - 40
        
        elif count == 0:
            pass
        
        elif count >= 1 and count <= 10:
            for obj in self._image:
                obj.moveTo((495 - (count - 1) * 48.5, 580))
        
        elif count >= 11 and count <= 20:
            for obj in self._image:
                obj.moveTo((20, 495 - (count - 11) * 48.5))
        
        elif count >= 21 and count <= 30:
            for obj in self._image:
                obj.moveTo((58.5 + (count - 20) * 48.5, 20))
                
        elif count >= 31 and count <= 40:
            for obj in self._image:
                obj.moveTo((580, 58.5 + (count - 30) * 48.5))
                
#Program works good before properties
#I can move pieces around board, money is a work in process
#make property class and print the car

class Button(EventHandler):
    """a button class"""
    
    def __init__(self, function, controller, text, center=(675, 50), width=50, height=25, color='green'):
        EventHandler.__init__(self)
        self._function = function
        self._controller = controller
        self._rect = Rectangle(width, height, center)
        self._rect.setFillColor('Green')
        self._color = color
        self._text = Text(text, center, 12)
        self._enabled = True
        self.setEnabled(True)
        self._rect.addHandler(self)
        
    def addTo(self, win):
        """add the information to the window"""
        win.add(self._rect)
        win.add(self._text)
        
    def enable(self):
        """enable the button"""
        self.setEnabled(True)
        
    def disable(self):
        """disable the button"""
        self.setEnabled(False)
        
    def setEnabled(self, val):
        """change the status of the button"""
        self._enabled = val
        if self._enabled:
            self._rect.setFillColor(self._color)
        else:
            self._rect.setFillColor('red')
            
    def isEnable(self):
        return self._enabled
        
    def handleMousePress(self):
        """mouse press"""
        self.click()
        
    def click(self):
        """whenn the mouse is clicked we will activate the button"""
        if self._enabled:
            self._function()




class Controller:
    """This will run the game and manage turns for the players"""
    def __init__(self, players, win):
        colors = ['yellow', 'blue', 'green', 'red']
        self._win = win
        
        #list of players
        self._players = []
        #list of current player locations
        self._playerLocations = []
        #turn tracker
        self._turn = 0
        #list of money
        self._money = []
        self._moneyCounter = []
        
        #build players
        for i in range(players):
            self._player = Pawn(i + 1, colors[i])
            self._player.addTo(self._win)
            self._players.append(self._player)
            
            #build list of player locations, everyone starts at 0.
            self._playerLocations.append(0)
            
            #build a list of player money
            self._money.append(1500)
        
        
        
        self._die1 = Die(self, (650, 100))
        self._die1.addTo(self._win)
        
        self._die2 = Die(self, (700, 100))
        self._die2.addTo(self._win)
        
        #Build a button for the die
        self._button = Button(self.rollDie, self, 'Roll Dice')#function, text)
        self._button.addTo(win)
        
        
        
        
        #add the money
        for i in range (len(self._money)):
            self._moneyCounter.append((Text(('Player ' + str(i + 1) + ' : $' + str(self._money[i])), (100, 700 + i * 20), 15)))
            win.add(self._moneyCounter[i])
            
            
        
        
        #build a button to buy properties
        
    
    
   
    def changeMoney(self, dollars):
        """change the value of a players money"""
        #update the money count
        self._money[self._turn] = self._money[self._turn] + dollars
        #replace the string
        self._moneyCounter[self._turn].setTextString('Player ' + str(self._turn + 1) + ' : $' + str(self._money[self._turn]))
        
            
    def changePawnLocation(self, value):
        """Change the pawn's location"""
        self._playerLocations[self._turn] = self._playerLocations[self._turn]\
        + value
        self.takeTurn()
        
        
        
    def movePawn(self):
        """move the pawn on the board after rolling the die"""
        
        #Check to see if location is greater than 40, if they are than reset
        if self._playerLocations[self._turn] > 40:
            self._playerLocations[self._turn] =\
            self._playerLocations[self._turn] - 40
            
            #add 200 for passing go
            self.changeMoney(200)
        
        
        #move the pawn to the new location    
        self._players[self._turn].move(self._playerLocations[self._turn])
        
       #show the property card
        #self._properties.showCard(self._turn)
    
        
    def rollDie(self):
        """roll both die when the button is clicked"""
        input('hello')
        self._button.disable()
        
        #self._properties.hideCard()
        
        self._die1.roll()
        self._die2.roll()
        
        value = int(self._die1.getValue()) + int(self._die2.getValue())
        
        
        self.changePawnLocation(value)
    
    
    def takeTurn(self):
        """take the turns"""
            
        self.movePawn()
        
        #HERE I WILL PUT A CHECK FOR PROPERTY BUTTONS
        
        #if self._properties.getAvailable(self._turn):
        #    self._propertyBuyButton.enable()
        
        
        #while not self._propertyBuyButton.isEnable():
        #Turn Counter    
        if self._turn >= len(self._players) - 1:
            self._turn = 0
            self._button.enable()
            
            
        else:
            self._turn = self._turn + 1
            self._button.enable()                
    
        
                
            
            
def first(win):
    """Test Function"""
    global WINDOW
    WINDOW = win
    
    #make the window larger
    win.setHeight(800)
    win.setWidth(800)
    board = Board((300, 300))
    board.addTo(win)
    control = Controller(1, win)
   
    
    #properties = Properties(Controller(1,win), win)
    
    
StartGraphicsSystem(first)