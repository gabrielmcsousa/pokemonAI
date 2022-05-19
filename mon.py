class Pokemon(object):
    
    def __init__(self, type, pos, name):
        self.type = type
        self.position = pos
        self.name = name
    

class PokeType():
    Water = "W"
    Electric = "C"
    Flying = "M"
    Fire = "L"