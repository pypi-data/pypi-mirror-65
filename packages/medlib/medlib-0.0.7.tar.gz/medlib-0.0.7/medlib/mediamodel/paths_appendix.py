from medlib.mediamodel.paths_storage import PathsStorage

class PathsAppendix(PathsStorage):
    """
    This class represents the paths to the content elements
    """
    
    def __init__(self, name_folder, path_card, path_image, path_media):
        """
        This is the constructor of the ContainerPaths class
        ___________________________________________________
        input:
            name_folder        string        name of the folder of the MediaContainer
            path_card          string        path to the ini file - for storing data
            path_image         string        path to the jpeg file - for showing the image
            path_media         string        path to the media file - to play/show
        """
        super().__init__(name_folder, path_card, path_image, None, path_media)

    def getPathOfMedia(self):
        return self.pathMedia
    
    def getJson(self):
        json = super().getJson()
        
        json['path-of-media'] = self.getPathOfMedia()
        
        return json