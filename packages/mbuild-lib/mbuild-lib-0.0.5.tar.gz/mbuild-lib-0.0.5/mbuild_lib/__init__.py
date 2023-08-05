

class u():
    def __init__(self):
        pass

    @property
    def distance(self):
        return 2.0

class mBuild():
    def __init__(self,port=0):
        pass
    
    def connect(self,port=0):
        return mBuild(port)
    
    @property
    def ultrasonic(self):
        return Ultrasonic(self)

    def _Ultrasonic(self):
        return u()

class Ultrasonic():
    def __init__(self,board):
        self._board = board
        self._ultrasonic = [self._board._Ultrasonic()]

    def distance(self,idx=1):
        return self._ultrasonic[idx-1].distance

class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value


boards = {}
def connect(port=0):
    global boards
    key_port = 'k{0}'.format(port)
    if key_port in boards:
        return boards[key_port]
    boards[key_port]=mBuild(port)
    return boards[key_port]

ultrasonic = connect(0).ultrasonic