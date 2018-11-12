def diceImage(k):
    """recover te image of te dice"""
    url = "https://www.wpclipart.com/recreation/" + \
          "games/dice/die_face_" + str(k) + ".png"
    return Image(url)

class Die:
    """a dice class that can be rolled to move players"""
    def __init__(self, center=(0, 0), width=20):
        self._center = center
        self._images = []
        for i in range(6):
            die = diceImage(i + 1)
            die.scale(width / die.size()[0])
            die.moveTo(center)
            self._images.append(die)
        self._value = 6
        self.setValue(6)

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
