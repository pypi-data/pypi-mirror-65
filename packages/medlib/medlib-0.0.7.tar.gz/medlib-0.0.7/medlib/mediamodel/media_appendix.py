import locale
from builtins import object

from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.paths_appendix import PathsAppendix
from medlib.mediamodel.qlabel_to_link_on_cllick import QLabelToLinkOnClick

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette
from medlib.card_ini import JSON_SECTION_TITLES, JSON_SECTION_CONTROL
from medlib.gui.player import PlayerThread

class MediaAppendix(object):
            
    """
    This object represents the MediaAppendix
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getTranslatedTitle()) if arg.control.getOrderBy() == 'title' else arg.container_paths.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.container_paths.getNameOfFolder() 
    
    def __init__(self, pathsAppendix, titles, control):
        """
        This is the constructor of the MediaAppendix
        ________________________________________
        input:
                pathsAppendix   PathsAppendix     paths to the media content (card.ini, image.jpg, media)
                titles          IniTitles         represents the [titles] section
                control         IniControl        represents the [control] section      
        """
        super().__init__()
        
        assert issubclass(pathsAppendix.__class__, PathsAppendix), pathsAppendix.__class__
        assert issubclass(titles.__class__, IniTitles), titles.__class__
        
        self.pathsAppendix = pathsAppendix
        self.titles = titles
        self.control = control

    def getTitles(self):
        """
        Returns back the [titles] section.
        _________________________________________________________________________________________________
        input:
        output:
                titles       IniTitles
        """
        return self.titles        
    
    def getControl(self):
        return self.control

    # --------------------------------------------
    # ---------------- Widget --------------------
    # --------------------------------------------
    def getWidget(self, media, scale):
        """  _________________________________________
            | Icon | Title                            |
            |______|__________________________________|
        """
        #widget = MediaAppendix.LinkWidget(self, scale)
        widget = MediaAppendix.QLinkLabelToAppendixMedia(media, self, self.titles.getTranslatedTitle(), self.isInFocus, self.getPathOfMedia(), scale)
        return widget
    
    def getPathOfMedia(self):
        return self.pathsAppendix.getPathOfMedia()
    
    def getTypeOfMedia(self):
        return self.control.getMedia()
    
    def isInFocus(self):
        return True
    
    def setGui(self, gui):
        self.gui = gui
        
    def getGui(self):
        return self.gui

    class QLinkLabelToAppendixMedia( QLabelToLinkOnClick ):

        def __init__(self, media, appendix_media, text, funcIsSelected, pathOfMedia, scale):
            super().__init__(media, text, funcIsSelected)        
            self.pathOfMedia = pathOfMedia
            self.scale = scale
            self.appendix_media = appendix_media
            self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold))

        def toDoOnClick(self):        
            gui = self.media.getGui()
            gui.control_panel.control_buttons_holder.image_or_appendix_on_click([{
                    'media-index': 0,
                    'media-path': self.pathOfMedia, 
                    'media-type': self.media.getControl().getMedia()}])

#            PlayerThread.play([{
#                'media-index': 0,
#                'media-path': self.pathOfMedia, 
#                'media-type': self.appendix_media.getControl().getMedia()}])
                
        def enterEvent(self, event):
            super().enterEvent(event)
            font = self.font()
            font.setUnderline(True)
            self.setFont(font)

            self.origPalette = self.palette()
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.blue)
            
            self.setPalette(palette)            
            
        def leaveEvent(self, event):
            super().leaveEvent(event)
            font = self.font()
            font.setUnderline(False)
            self.setFont(font)
            
            self.setPalette(self.origPalette)

    def getJson(self):
        json = {}

        json['paths-appendix'] = self.pathsAppendix.getJson()        
        json.update({JSON_SECTION_TITLES: self.titles.getJson()} if self.titles.getJson() else {})
        json.update({JSON_SECTION_CONTROL: self.control.getJson()} if self.control.getJson() else {})
        
        return json

    