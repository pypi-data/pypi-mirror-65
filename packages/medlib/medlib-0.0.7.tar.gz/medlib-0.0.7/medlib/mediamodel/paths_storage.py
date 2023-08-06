from medlib.mediamodel.paths_collector import PathsCollector

class PathsStorage(PathsCollector):
    """
    This class represents the paths to the content elements
    """
    
    def __init__(self, nameFolder, pathCard, pathImage, pathIcon, pathMedia):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            nameFolder        string        name of the folder of the MediaContainer
            pathCard          string        path to the ini file - for storing data
            pathImage         string        path to the Image file - for showing the image
            pathIcon          string        path to the Icon file - for showing in the title
            pathMedia         string        path to the media file - to play/show
        """
        super().__init__(nameFolder, pathCard, pathImage, pathIcon)
        self.pathMedia = pathMedia
        
    def getPathOfMedia(self):
        return self.pathMedia

    
    def getJson(self):
        json = super().getJson()
        
        json.update({} if self.getPathOfMedia() is None or not self.getPathOfMedia() else {'path-of-media': self.getPathOfMedia()})
        
        return json
    