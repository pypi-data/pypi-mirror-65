class CardDataInterface(object):
    
    def setIndex(self, index):
        raise NotImplementedError
    
    def getIndex(self):
        raise NotImplementedError
    
    def getListOfCardDataInThisLevel( self ):
        raise NotImplementedError
    
    def getParentCollector(self):
        raise NotImplementedError
