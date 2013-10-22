class RecordClass():
    def __init__(self,type,coords,tag,text,size,color):
        self.type=type
        self.coords=coords
        self.tag=tag
        self.text=text
        self.size=size
        self.color=color
    def getCoords(self):
        return self.coords
    def getType(self):
        return self.type
    def getTag(self):
        return self.tag
    def getText(self):
        return self.text
    def getSize(self):
        return self.size
    def getColor(self):
        return self.color