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
        self._board = Image("https://cs.hamilton.edu/~zkleinba/images/"+\
        "hamiltopolyboard2.jpg", self._center, 600, 600)
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

class Die():
    """a dice class that can be rolled to move players"""
    def __init__(self, controller, center=(0, 0), width=50, height=50):
        self._center = center
        self._controller = controller
        self._images = []
        
        #generating dice image
        for i in range(6):
            die = Image(diceImage(i + 1), self._center, width, height)
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
    
class Button(EventHandler):
    """a button class"""
    def __init__(self, function, controller, text, center=(675, 50), width=50,\
    height=25, color='green'):
        EventHandler.__init__(self)
        self._function = function
        self._controller = controller
        
        #build the button's shape
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
        
        #checking if the button is enabled
        if self._enabled:
            self._rect.setFillColor(self._color)
        else:
            self._rect.setFillColor('red')
            
    def isEnable(self):
        """check if button is enabled"""
        return self._enabled
        
    def handleMousePress(self):
        """mouse press"""
        self.click()
        
    def click(self):
        """whenn the mouse is clicked we will activate the button"""
        if self._enabled:
            self._function()

class Pawn:
    """a pawn class"""
    def __init__(self, number, color, center=(600-62.5, 600-20)):
        self._center = center
        
        #a pawn's location
        self._count = 0
        
        #the list of images
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
        #add each image to the window
        for img in self._image:
            win.add(img)
            
    def move(self, count):
        """move the pawn around the board"""
        #check the count in order to change the pawn's direction
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
                
    def changeDepth(self, value):
        """change the depth of a pawn"""
        #change each objects depth
        for img in self._image:
            img.setDepth(value)
            
    def moveOffScreen(self):
        """move the pawn off of the screen"""
        #move each object off of the screen
        for obj in self._image:
            obj.moveTo((1000, 1000))

class Property:
    """properties and property cards"""
    def __init__(self, controller):
        self._controller = controller
        
        #build the card
        self._rectangle = Rectangle(140, 175, (300, 700))
        self._rectangle.setFillColor('white')
        self._rectangle.setBorderColor('black')
        self._rectangle.setDepth(100)
        
        #build the base that will be used to hide the card
        self._base = Rectangle(141, 177, (300, 700))
        self._base.setBorderColor('white')
        self._base.setFillColor('white')
        self._base.setDepth(0)
        self._name = Text('', (300, 625), 14)
        self._name.setDepth(1)
        
        #this text will show who owns the property
        self._owner = Text('', (300, 640), 10)
        self._owner.setDepth(1)
        
        #this text will show if the property is available for purchase
        self._purchaseText = Text('', (300, 660, 14))
        self._purchaseText.setDepth(1)
        
        #this text will show if the property is available for rent
        self._rentText = Text('', (300, 680, 14))
        self._rentText.setDepth(1)
        
        self._places = [['Go'],\
        ['Wertimer', False, 100, '', 5],\
        ["Dean's List"],\
        ['Wally J', False, 100, '', 10],\
        ['North', False, 150, '', 15],\
        ['Commons', False, 200, '', 10],\
        ['Dunham', False, 200, '', 20],\
        ['Chance'],\
        ['South', False, 200, '', 25],\
        ['Sken', False, 250, '', 30],\
        ['Campo'],\
        ['Burke Library', False, 300, '', 35],\
        ['Physical Plant', False, 200, '', 15],\
        ['KJ', False, 300, '', 40],\
        ['Taylor Science Center', False, 350, '', 40],\
        ['McEwen', False, 200, '', 10],\
        ['Bundy East', False, 400, '', 45],\
        ['Bundy West', False, 400, '', 50],\
        ["Dean's List"],\
        ['Carnegie', False, 450, '', 55],\
        ['Free Parking'],\
        ['Farmhouse', False, 500, '', 60],\
        ['Milbank', False, 500, '', 65],\
        ['Chance'],\
        ['Babbitt', False, 550, '', 70],\
        ['The Little Pub', False, 200, '', 10],\
        ['Text-Books'],\
        ['Ferguson', False, 600, '', 75],\
        ['The Jitney', False, 200, '', 15],\
        ['Eells', False, 600, '', 80],\
        ['Go To Campo'],\
        ['Moriss House', False, 600, '', 85],\
        ["Dean's List"],\
        ['G-Road', False, 650, '', 90],\
        ['Chance'],\
        ['Howard Diner', False, 200, '', 10],\
        ["Don's Rok", False, 700, '', 95],\
        ['Text-Books'],\
        ['Village Tavern', False, 700, '', 100],\
        ['Off-Campus Housing', False, 750, '', 105],\
        ['Go']]
    
        self._communityChest = [500, 250, 100, 50, 25, 5]
        
        self._chance = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    
    def addTo(self, win):
        """add the card to the window"""
        win.add(self._base)
        win.add(self._rectangle)
        win.add(self._name)
        win.add(self._owner)
        win.add(self._rentText)
        win.add(self._purchaseText)
    
    def showCard(self, numb):
        """show the current card on screen"""
        self._base.setDepth(101)
        self._rectangle.setDepth(2)
        self._name.setTextString(self._places[numb][0])
        
        #only show rent text and sale text if the property can be bought
        if len(self._places[numb]) > 3:
            self._rentText.setTextString('Rent = $'\
            + str(self._places[numb][4]))
            self._purchaseText.setTextString('$'\
            + str(self._places[numb][2]) + ' To Purchase') 
            
            #if it is not owned, say it is for sale
            if not self.getAvailable(numb):
                self._owner.setTextString('Property is for sale')
            
            #if it is owned, say who owns it
            else:
                self._owner.setTextString('Owned by player'\
                + str(self._places[numb][3]))
        
    def hideCard(self):
        """hide the card from the screen"""
        #change depths and clear strings
        self._base.setDepth(0)
        self._rectangle.setDepth(100)
        self._name.setTextString('')
        self._rentText.setTextString('')
        self._purchaseText.setTextString('')
        self._owner.setTextString('')
        
    def getAvailable(self, value):
        """discover if the property is for sale or not"""
        truth = self._places[value][1]
        return truth
        
    def purchase(self, value, player):
        """purchase the property by changing the boolean value"""
        self._places[value][1] = True
        self._places[value][3] = str(player)
        self._owner.setTextString('Owned by player' + str(player))
        
    def cost(self, value):
        """return the cost of buying a property"""
        return self._places[value][2]
        
    def payRent(self, value):
        """return pay rent"""
        return self._places[value][4]
        
    def recieveRent(self, value):
        """return the player who will recieve rent"""
        return self._places[value][3]
        
    def isGo(self, value):
        """return true if it the selected property is Go"""
        if self._places[value][0] == 'Go':
            return True
            
    def isChance(self, value):
        """return true if it the selected property is chance"""
        if self._places[value][0] == 'Chance':
            return True
            
    def isCampo(self, value):
        """return true if it the selected property is campo"""
        if self._places[value][0] == 'Campo':
            return True
            
    def isDean(self, value):
        """return true if it the selected property is dean's list"""
        if self._places[value][0] == "Dean's List":
            return True
            
    def isGoToCampo(self, value):
        """return true if it the selected property is go to campo"""
        if self._places[value][0] == "Go To Campo":
            return True
            
    def isFreeParking(self, value):
        """return true if it the selected property is go to campo"""
        if self._places[value][0] == "Free Parking":
            return True
    
    def isTextBooks(self, value):
        """return true if it the selected property is go to campo"""
        if self._places[value][0] == "Text-Books":
            return True

    def getCommunityChest(self):
        """select one of the items in community chest"""
        return self._communityChest[random.randrange(6)]
        
    def getChance(self):
        """select one of the items in chance"""
        return self._chance[random.randrange(10)]

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
        
        #a list of strings to display money
        self._moneyCounter = []
        
        #text will appear on window stating whos turn it is currently
        self._turnText = Text('Player '\
        + str(self._turn + 1) + "'s turn", (675, 150), 12)
        win.add(self._turnText)
        
        #build players based on the desired number
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
        
        self._properties = Property(self)
        self._properties.addTo(self._win)
        
        #Build a button for the die
        self._button = Button(self.rollDie, self, 'Roll Dice')
        self._button.addTo(win)
        
        #add the money based on how many players
        for i in range(len(self._money)):
            self._moneyCounter.append((Text(('Player ' + str(i + 1)\
            + ' : $' + str(self._money[i])), (100, 625 + i * 20), 15)))
            win.add(self._moneyCounter[i])
        
        #This button will show cards and activate the buy button    
        self._propButton = Button(self.changeCard, self, 'show', (400, 650))
        self._propButton.addTo(self._win)
        self._propButton.setEnabled(False)
            
        #This button will buy properties and activate the end turn button
        self._propertyBuyButton = Button(self.purchaseProperty,\
        self, 'Buy', (400, 680))
        
        #This button cover will hide the buy button when it is inactivated
        self._buttonCover = Rectangle(50, 25, (400, 680))
        self._buttonCover.setFillColor('white')
        self._buttonCover.setBorderColor('white')
        self._buttonCover.setDepth(1)
        self._win.add(self._buttonCover)
        
        #this button will end the turn and move on to the next one
        self._endTurnButton = Button(self.endTurn, self, 'End Turn', (400, 710))
        
        #auxillary text strings that will be used to display messasges
        self._warningText = Text('', (600, 680), 12)
        win.add(self._warningText)
        self._warningText2 = Text('', (600, 690), 12)
        win.add(self._warningText2)
        self._warningText3 = Text('', (600, 700), 12)
        win.add(self._warningText)
        
        #this will display the value on the dice
        self._warningText4 = Text('', (675, 200), 12)
        win.add(self._warningText4)
        
        #another auxillary text string
        self._warningText5 = Text('', (600, 710), 12)
        win.add(self._warningText5)
        
    def changeCard(self):
        """change the card that is shown"""
        
        #disable the show property button
        self._propButton.disable()
        
        #switch cards
        self._properties.showCard(self._playerLocations[self._turn])
        
        #check to see if the property is for sale, if so enable the end turn
        #if it is not for sale, call the special property method
        if self.checkProperty(self._playerLocations[self._turn]):
            self.goToCampo(self._playerLocations[self._turn])
            self.visitingCampo(self._playerLocations[self._turn])
            self.textBooks(self._playerLocations[self._turn])
            self.freeParking(self._playerLocations[self._turn])
            self.deansList(self._playerLocations[self._turn])
            self.chance(self._playerLocations[self._turn])
            
            self._endTurnButton.addTo(self._win)
            self._endTurnButton.enable()
            
        #check to see if the property is owned, if it is not enable buy
        elif not\
        self._properties.getAvailable(self._playerLocations[self._turn]):
            self._buttonCover.setDepth(1000)
            self._propertyBuyButton.addTo(self._win)
            
            self._propertyBuyButton.enable()
            
            #enable end Turn Button incase the player wants to pass
            self._endTurnButton.addTo(self._win)
            self._endTurnButton.enable()
            
        
        else:
            #check to see that it the current player doesnt own the property
            if str(self._turn + 1) != str(self._properties.recieveRent\
            (self._playerLocations[self._turn])):
 
                #subtract the rent from the current player
                if not self.checkMoney((self._properties.payRent\
                (self._playerLocations[self._turn]))):
                    self._warningText2.setTextString('You are bankrupt!')
                    #set money to 0
                    self.changeMoney(self._money[self._turn] * -1)
                    #give money to the owner
                    self.recieveRent(+(self._properties.payRent\
                    (self._playerLocations[self._turn])))
                    self.endGame()
                
                else:    
                    self.changeMoney(-(self._properties.payRent\
                    (self._playerLocations[self._turn])))
                    #add the rent to the owner
                    self.recieveRent(+(self._properties.payRent\
                    (self._playerLocations[self._turn])))
        
        
            self._endTurnButton.addTo(self._win)
            self._endTurnButton.enable()
            
    def checkMoney(self, dollars):
        """check to see if a player has sufficent funds"""
        if self._money[self._turn] + dollars >= 0:
            return True
        
    def changeMoney(self, dollars):
        """change the value of a players money"""
        #update the money count
        self._money[self._turn] = self._money[self._turn] + dollars
        #replace the string
        self._moneyCounter[self._turn].setTextString('Player '\
        + str(self._turn + 1) + ' : $' + str(self._money[self._turn]))
        
    def recieveRent(self, dollars):
        """have a player revieve the rent on a property they own"""
        #find the player that is recieving rent
        player = int(self._properties.recieveRent\
        (self._playerLocations[self._turn])) - 1
        
        #check to see if that player has lost
        if self._money[player] > 0:
            self._money[player] = self._money[player] + dollars
        
            #replace the string
            self._moneyCounter[player].setTextString\
            ('Player ' + str(player + 1) + ' : $' + str(self._money[player]))
            
        else:
            pass
            
    def changePawnLocation(self, value):
        """Change the pawn's location"""
        #update the current player's location
        self._playerLocations[self._turn] = self._playerLocations[self._turn]\
        + value
        
        #call takeTurn
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
        self._propButton.enable()
        
    def rollDie(self):
        """roll both die when the button is clicked"""
        #disable the roll button
        self.endGame()
        self._button.disable()

        #roll both die
        self._die1.roll()
        self._die2.roll()
    
        #retrive the value of both die and add them
        value = int(self._die1.getValue()) + int(self._die2.getValue())
        
        self._warningText4.setTextString('you rolled ' + str(value))
        
        #call changePawnLocation using the cumulative value of the die
        self.changePawnLocation(value)
    
    def takeTurn(self):
        """take the turns"""
        #call the movePawn method    
        self.movePawn()
                
    def purchaseProperty(self):
        """purchase the property"""
        self._propertyBuyButton.disable()
        
        #check to see if the player can afford a property
        if not self.checkMoney(-(self._properties.cost\
        (self._playerLocations[self._turn]))):
            self._warningText.setTextString\
            ('Transaction cannot be completed due to insuffecient funds.')
        
        else:
            #complete the transaction
            self._properties.purchase\
            (self._playerLocations[self._turn], str(self._turn + 1))
        
            self.changeMoney\
            (-(self._properties.cost(self._playerLocations[self._turn])))
            
    def endTurn(self):
        """end the turn and move into the next one"""
        self._properties.hideCard()
        self._warningText.setTextString('')
        self._warningText2.setTextString('')
        self._warningText3.setTextString('')
        self._warningText5.setTextString('')
        
        #adjust the turn counter
        if self._turn >= len(self._players) - 1:
            self._turn = 0
            self.endGame()
            
            #setup for the next turn
            self._button.enable()
            
            self._buttonCover.setDepth(0)
            self._endTurnButton.disable()
            self._turnText.setTextString('Player ' + \
            str(self._turn + 1) + "'s turn")
            self._warningText4.setTextString('')
            
            
        else:
            self._turn = self._turn + 1
            self.endGame()
            
            self._button.enable()
            self._buttonCover.setDepth(0)
            self._endTurnButton.disable()
            
            self._turnText.setTextString\
            ('Player ' + str(self._turn + 1) + "'s turn")
            self._warningText4.setTextString('')
    
    def checkProperty(self, value):
        """check to see if a player has landed on a special property"""
        if self._properties.isChance(value)\
        or self._properties.isGo(value) \
        or self._properties.isCampo(value) \
        or self._properties.isTextBooks(value) \
        or self._properties.isGoToCampo(value)\
        or self._properties.isDean(value)\
        or self._properties.isFreeParking(value):
            return True
            
        else:
            pass
        
    def goToCampo(self, value):
        """activate this function if a player lands on go to campo"""
        
        #check to see if a player landed on go to campo
        if self._properties.isGoToCampo(value):
            self._playerLocations[self._turn] = 10
            self.movePawn()
            self._warningText.setTextString('You are guilty! Go to Campo!')
            self._warningText2.setTextString\
            ('Do not collect $200 for passing Go')
        
        else:
            pass
        
    def visitingCampo(self, value):
        """activate this function if a player lands on campo"""
        
        #check to see if a player landed on campo
        if self._properties.isCampo(value):
            self._warningText.setTextString('Thanks for visiting!')
            self._warningText2.setTextString('Have a nice day!')
            
        else:
            pass
        
    def freeParking(self, value):
        """activate this function if a player lands on free parking"""
        
        #check to see if a player landed on free parking
        if self._properties.isFreeParking(value):
            self._warningText.setTextString('There are always open spots,')
            self._warningText2.setTextString('in the North Lot!')
            
        else:
            pass
        
    def textBooks(self, value):
        """activate this function if a player lands on textBooks"""
        
        #check to see if a player landed on text books
        if self._properties.isTextBooks(value):
            self._warningText.setTextString('You need new texbooks.')
            self._warningText2.setTextString('Pay the bookstore $200')
            
            #check the players money
            if not self.checkMoney(-200):
                self._warningText3.setTextString('You are bankrupt!')
                self.changeMoney(self._money[self._turn] * -1)
                self.endGame()
            
            else:    
                self.changeMoney(-200)
            
        else:
            pass
        
    def deansList(self, value):
        """activate this function when a player lands on Dean's List"""
        #get the value community chest will change
        money = self._properties.getCommunityChest()
        
        #check to see if a player landed on deans list
        if self._properties.isDean(value):
            self._warningText.setTextString\
            ("Congratulations! You made the Dean's List")
            self._warningText2.setTextString('Collect $' + str(money))
            self.changeMoney(money)
            
        else:
            pass
            
    def chance(self, value):
        """activate this function when a player lands on Dean's List"""
        #get the number of spots chance will move a player
        moves = self._properties.getChance()
        
        #check to see if a player landed on chance
        if self._properties.isChance(value):
            self._warningText.setTextString("You landed on Chance")
            self._warningText2.setTextString('Advance ' \
            + str(moves) + ' spots.')
            self._warningText3.setTextString('Pay rent if necessary')
            self._warningText5.setTextString('Click the show button!')
            self.changePawnLocation(moves)
            
        else:
            pass
        
    def endGame(self):
        """if a player's money reaches 0 end the game"""
        
        #this text will say if a player has lost
        text = Text('Player ' + str(self._turn + 1) + \
        ' lost', (100, 720 + self._turn * 10), 12)
        
        #this count will keep tally of the players that have lost
        count = 0
        
        #check to see if the current player has lost in order to skup turn
        if self._money[self._turn] <= 0:
            self._win.add(text)
            self._players[self._turn].moveOffScreen()
            self.endTurn()
            
            #check to see how many players have lost
            for obj in self._money:
                if obj > 0:
                    count = count + 1
            
            #create the winner window        
            if count == 1:
                rectangle = Rectangle(600, 600, (300, 300))
                rectangle.setFillColor('blue')
                rectangle.setDepth(0)
                self._win.add(rectangle)
                
                text = Text('Player ' + str(self._turn + 1) + \
                ' has won.  Congratulations!', (300, 300), 20)
                text.setDepth(0)
                self._win.add(text)
                
                self._button.disable()
        


def first(win):
    """Test Function"""
    global WINDOW
    WINDOW = win
    
    #make the window larger
    win.setHeight(800)
    win.setWidth(800)
    board = Board((300, 300))
    board.addTo(win)
    
    Controller(4, win)
    
StartGraphicsSystem(first)
