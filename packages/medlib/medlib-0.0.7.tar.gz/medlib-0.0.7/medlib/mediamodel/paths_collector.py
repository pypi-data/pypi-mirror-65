class PathsCollector(object):
    """
    This class represents the paths to the container elements
    """
    
    def __init__(self, nameFolder, pathCard, pathImage, pathIcon):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            nameFolder        string        name of the folder of the MediaContainer
            pathCard          string        path to the ini file - for storing data
            pathImage         string        path to the jpeg file - for showing the image
            pathIcon          string        path to the png file - for showing in the title
        """
        self.nameFolder = nameFolder
        self.pathCard = pathCard
        self.pathImage = pathImage
        self.pathIcon = pathIcon        
        
    def __str__(self):
        return self.getJson()
        
    def getNameOfFolder(self):
        return self.nameFolder
        
    def getPathOfCard(self):
        return self.pathCard
    
    def getPathOfImage(self):
        return self.pathImage 

    def getPathOfIcon(self):
        return self.pathIcon 

    def getJson(self):
        json = {}
        
        json.update({} if self.getNameOfFolder() is None or not self.getNameOfFolder() else {'name-of-folder': self.getNameOfFolder()})
        json.update({} if self.getPathOfCard() is None or not self.getPathOfCard() else {'path-of-card': self.getPathOfCard()})
        json.update({} if self.getPathOfImage() is None or not self.getPathOfImage() else {'path-of-image': self.getPathOfImage()})
        json.update({} if self.getPathOfIcon() is None or not self.getPathOfIcon() else {'path-of-icon': self.getPathOfIcon()})
        
        return json
        