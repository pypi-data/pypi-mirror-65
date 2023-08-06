import locale
import os
import subprocess
import platform

from medlib.constants import PANEL_HEIGHT
from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE

from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_classification import IniClassification
from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_control import IniControl

from medlib.mediamodel.media_appendix import MediaAppendix

from medlib.mediamodel.extra import QHLine, clearLayout

from PyQt5.QtWidgets import QGridLayout, QPlainTextEdit, QSizePolicy
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QColor, QFont, QTextCursor
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

from medlib.card_ini import JSON_SECTION_TITLES
from medlib.card_ini import JSON_SECTION_GENERAL
from medlib.card_ini import JSON_SECTION_STORYLINE
from medlib.card_ini import JSON_SECTION_TOPIC
from medlib.card_ini import JSON_SECTION_LYRICS
from medlib.card_ini import JSON_SECTION_CLASSIFICATION
from medlib.card_ini import JSON_SECTION_CONTROL
from medlib.card_ini import JSON_NODE_APPENDIXES
from cardholder.card_data_interface import CardDataInterface

FOLDER_TYPE_COLLECTOR='collector'
FOLDER_TYPE_STORAGE='storage'

class MediaBase(CardDataInterface):
    """
    This object represents the MediaBase
    """
   
    @staticmethod
    def sort_key(arg):
        """
        """
        return locale.strxfrm(arg.getOrderTitle()) if arg.control.getOrderBy() == 'title' else arg.getNameOfFolder() if arg.control.getOrderBy() == 'folder' else arg.getNameOfFolder() 
    
    def __init__(self, titles, control, general=None, classification=None):
        """
        This is the constructor of the MediaCollector
        ________________________________________
        input:
                titles             IniTitles         represents the [titles] section
                control            IniControl        represents the [control] section
                general            IniGeneral        represents the [general] section
                classification     IniClassification represents the [classification] section
        """
        super().__init__()
        
        NoneType = type(None)
        assert issubclass(titles.__class__, IniTitles)
        assert issubclass(control.__class__, IniControl)
        assert issubclass(general.__class__, (IniGeneral, NoneType)), general.__class__
        assert issubclass(classification.__class__, (NoneType, IniClassification)), classification.__class__
        
        self.parentCollector = None
        self.mediaAppendixList = []
        self.titles = titles
        self.control = control
        self.general = general if general else IniGeneral()
        self.classification = classification if classification else IniClassification()
        
        self.neededTagField = False
        self.widget = None
        self.grid_layout = None
        
        self.card = None
        self.index = 0
        
# -
    def setIndex(self, index):
        self.index = index
        
    def getIndex(self):
        return self.index
    
#    def setCard(self, card):
#        self.card = card
#        
#    def getCard(self):
#        return self.card
        
    def getListOfChildCardData(self):
        mcl = self.getMediaCollectorList()
        msl = self.getMediaStorageList()
        sum_list = mcl + msl
        return sum_list        
        
    def getListOfCardDataInThisLevel(self):
        parent_collector = self.getParentCollector()
        if parent_collector:
            mcl = parent_collector.getMediaCollectorList()
            msl = parent_collector.getMediaStorageList()
            sum_list = mcl + msl
        else:
            sum_list = None
        if sum_list:
            return sum_list
        else:
            None
# -
        
    def search(self, withShift, forWho, byWhat):
        """
        searchFunction( forWho, byWhat )    - A search function when you click on a link on the card.
                                              For example on a Director or Actor ...
                                              It has two parameters:
                                                -forWho is the text you clicked on
                                                -byWhat is the title_id of the group. for example for the
                                                 directors: title_director or actors: title_actor ...
        """
        print("Search for '" + forWho + "' by " + byWhat, "With Shift" if withShift else "")
        
    def getTranslatedTitleList(self, title_list, index = None):

        title = self.getTranslatedTitle()
        card_data_list = self.getListOfChildCardData()
        
        title_list.append({"title": title, "card-list": card_data_list, "index": index})
        
        pc = self.getParentCollector()
        if pc:
            return pc.getTranslatedTitleList(title_list, self.getIndex())
        else:
            return self
        
    def getFormattedTitleList(self, title_list, index = None):
        """
        Returns a list gathered in the hierarchy from the actual collector till root
        One element in the list:
            "title"
            "collector"
            "card-list"
            "index"        
        """
        
        title = self.getFormattedTitle()
        card_data_list = self.getListOfChildCardData()
        
        title_list.append({"title": title, "collector": self, "card-list": card_data_list, "index": index})
        
        pc = self.getParentCollector()
        if pc:
            return pc.getFormattedTitleList(title_list, self.getIndex())
        else:
            return self
        
            
        
    def getRoot(self):
        """
            Gives back the root of the media hierarchy
            Basically it is a MediaCollector
        """
        pc = self.getParentCollector()
        if pc:
            return pc.getRoot()
        else:
            return self

    def getParentCollector(self):
        return self.parentCollector
        
    def setParentCollector(self, parentCollector):
        self.parentCollector = parentCollector
        
    def getNameOfFolder(self):
        raise NotImplementedError
        
    def getPathOfImage(self):
        raise NotImplementedError
    
    def getPathOfCard(self):
        raise NotImplementedError

    def getBackgroundColor(self):
        raise NotImplementedError
    
    def getFolderType(self):
        raise NotImplementedError
            
    def getTranslatedTitle(self):
        return self.titles.getTranslatedTitle()
    
    def getFormattedTitle(self):
        return self.titles.getFormattedTitle(self)

    def getOrderTitle(self):
        return self.titles.getOrderTitle(self)
    
    def getTranslatedStoryline(self, storyline):
        return storyline.getTranslatedStoryline()

    def getTranslatedGenreList(self):
        return self.general.getTranslatedGenreList(self.control.getCategory())
    
    def getTranslatedThemeList(self):
        return self.general.getTranslatedThemeList()

    def getTranslatedRecipeTypeList(self):
        return self.general.getTranslatedRecipeTypeList(self.control.getCategory())

    def setGui(self, gui):
        self.gui = gui
        
        for appendix in self.mediaAppendixList:
            appendix.setGui(gui)        
        
    def getGui(self):
        return self.gui

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
        """
        Returns back the [control] section.
        _________________________________________________________________________________________________
        input:
        output:
                control       IniControl
        """
        return self.control
    
    def getGeneral(self):
        """
        Returns back the [general] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniGeneral
        """
        return self.general

    def getClassification(self):
        """
        Returns back the [classification] section.
        _________________________________________________________________________________________________
        input:
        output:
                general       IniClassification
        """
        return self.classification

    def addMediaAppendix(self, mediaAppendix):
        """
        Adds a new MediaAppendix to this MediaStorage
        It is ordered accordingly the language by the control.orderby
        _____________________________________________________________
        input:
                mediaAppendix    MediaAppendix    the MediaAppendix to add
        """
        
        assert issubclass(mediaAppendix.__class__, MediaAppendix), mediaAppendix.__class__

        # Add the MediaStorage
        self.mediaAppendixList.append(mediaAppendix)
        
        # Sort the list
        #self.sortMediaStorage()        

    # --------------------------------------------
    # --------------- Image ---------------------
    # --------------------------------------------
    def getWidgetImage(self, mainWidget, scale):

        # layout of this widget => three columns
        image_layout = QHBoxLayout()
        
        # space between the three grids
        image_layout.setSpacing(1)
        
        # margin around the widget
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = self.getQLabelToHoldImage()
        widget.setStyleSheet('background: black')
        widget.setAlignment(Qt.AlignCenter)
        widget.setLayout(image_layout)

        pixmap = QPixmap( self.getPathOfImage( ) )
        
        # if card image was not found
        if pixmap.isNull():            

            # then a blank image appears
            smaller_pixmap = QPixmap(PANEL_HEIGHT * scale, PANEL_HEIGHT * scale)
            smaller_pixmap.fill(QColor('gray'))
        elif pixmap.width() >= pixmap.height():
            smaller_pixmap = pixmap.scaledToWidth(PANEL_HEIGHT * scale)
        else:
            smaller_pixmap = pixmap.scaledToHeight(PANEL_HEIGHT * scale)

        widget.setMinimumHeight(PANEL_HEIGHT * scale)
        widget.setMinimumWidth(PANEL_HEIGHT * scale)
        widget.setPixmap(smaller_pixmap)
        
        return widget         
        
    # --------------------------------------------
    # ------------- Middle - Text part -----------
    # --------------------------------------------
                 
    def getWidgetCardInformationText(self, mainWidget, scale):
        """  _________________________________________
            |  Title                                  |
            |_________________________________________|       
            |  One line Info                          |
            |_________________________________________|       
            |  General Info                           |
            |_________________________________________|
            |  Media Appendix                         |
            |_________________________________________|            
        """
#       ┌────────────── CardInformationTextWidget ───────────────┐
        class CardInformationTextWidget(QWidget):
            def __init__(self, scale):
                QWidget.__init__(self)
            
                self.scale = scale
                self.general_widget = None

                # layout of this widget => four rows
                self.cardinfo_layout = QVBoxLayout()
                self.cardinfo_layout.setAlignment(Qt.AlignTop)
        
                # space between the three grids
                self.cardinfo_layout.setSpacing(1)
        
                # margin around the widget
                self.cardinfo_layout.setContentsMargins(0, 0, 0, 0)

                self.setLayout(self.cardinfo_layout)

            def addTitleWidget(self, widget):
                self.cardinfo_layout.addWidget(widget) 
                self.cardinfo_layout.addWidget(QHLine())

            def addOneLineWidget(self, widget):
                self.cardinfo_layout.addWidget(widget) 

            def addGeneralWidget(self, widget):
                self.general_widget = widget
                self.cardinfo_layout.addWidget(widget) 

            def addMediaAppendixWidget(self, widget):
                self.cardinfo_layout.addWidget(widget) 
            
            def setFocusTagField(self, value):
                if self.general_widget:
                    self.general_widget.setFocusTagField(value)
#       └────────────── CardInformationTextWidget ───────────────┘
        
        widget = CardInformationTextWidget(scale)

        # --- TITLE ---
        #  _________________________________________
        # | Icon | Title                            |
        # |______|__________________________________|
        #
        widget.addTitleWidget(self.titles.getWidget(self, scale))
        
        # --- ONLINE INFO ---"
        #  _________________________________________
        # | Year: Length: Country: Sound: Sutitle:  |
        # |_________________________________________|
        #
        widget.addOneLineWidget(self.general.getWidgetOneLine(self, scale))
        
        # --- GENERAL INFO ---
        #  ___________________________________________________________________________
        # | Director/Maker:                             |                             |
        # |                                             |                             |
        # | Writer/Author:                              |                             |
        # |                                             |                             |
        # | Actor/Performer/Lecturer/Contributor/Voice: |                             |
        # |                                             |                             |
        # | Genre :                                     |                             |
        # |                                             |                             |
        # | Theme:                                      |                             |
        # |_____________________________________________|_____________________________|
        # | Storyline/Topic/Lyrics/-:                   |                             |
        # |_____________________________________________|_____________________________|
        # | Tags:                                       |                             |
        # |_____________________________________________|_____________________________|
        #
        widget.addGeneralWidget(self.general.getWidget(mainWidget, self, scale))

        # --- MEDIA APPENDIX ---
        widget.addMediaAppendixWidget(self.getWidgetMediaAppendix(scale))
        
        # --- Stretch ---
#        cardinfo_layout.addStretch(1)
#        label = QLabel()
#        label.setMinimumHeight(0)
#        label.setFixedHeight(0)
#        cardinfo_layout.addWidget(label)        
        
        return widget

    def getWidgetMediaAppendix(self, sizeRate):
        """
            Media Appendix
        """
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setLayout(layout)
        
        if self.getMediaAppendixList():
            layout.addWidget(QHLine())

        for media_appendix in self.getMediaAppendixList():
            layout.addWidget(media_appendix.getWidget(self, sizeRate))
        
        return widget
    
    # --------------------------------------------
    # ----------------- STORYLINE ----------------
    # --------------------------------------------
    def getWidgetGeneralInfoStoryLine(self, parent, scale, value):
        if value:
            
            widget_value = QPlainTextEdit(parent)
            
            widget_value.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            
            widget_value.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
            widget_value.setReadOnly(True)
            widget_value.setMinimumHeight( (PANEL_FONT_SIZE + 3) * scale )

            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget_value.setSizePolicy(sizePolicy)

            [ widget_value.appendPlainText(line) for line in value.split('\\n')]

            widget_value.moveCursor(QTextCursor.Start)
            # - eliminate the padding from the top - #            
            widget_value.document().setDocumentMargin(0)
            widget_value.setStyleSheet("QPlainTextEdit {padding-left:5px; padding-top:0px; border:0px;}")
            
            return widget_value

        return None

    # --------------------------------------------
    # ------------- Classification ---------------
    # --------------------------------------------
    def getWidgetClassification(self, mainWidget, scale):
        """   __________
             | Rate     |
             |__________|
             | Favorite |            
             |__________|
             | New      |
             |__________|
             | +        |
             |__________|
        """
        return self.classification.getWidget(mainWidget, self, scale)
    
    # --------------------------------------------
    # --------------------------------------------
    # --------------- WIDGET -------------------
    # --------------------------------------------
    # --------------------------------------------
                        
    def getWidget(self, scale):
        """  ___________________________________________________
            |         |                        |                |
            |         |                        |                |
            |  Image  |  Card Information Text | Classification |
            |         |                        |                |
            |_________|________________________|________________|
        """
#       ┌──────────────────── MainWidget ──────────────────────┐
        class MainWidget(QWidget):
            def __init__(self, media, scale):
                QWidget.__init__(self)
            
                self.scale = scale
                self.media = media
            
                self.image_widget = None
                self.card_information_widget = None        
                self.classification_widget = None

                self.grid_layout = QGridLayout()

                # space between the three grids
                self.grid_layout.setSpacing(10)
        
                # margin around the widget
                self.grid_layout.setContentsMargins(0, 0, 0, 0)
        
                # stretch out the middle part
                self.grid_layout.setColumnStretch(1, 1)

                self.setLayout(self.grid_layout)

                self.setStyleSheet('background: ' + media.getBackgroundColor())
                                 
                self.setAttribute(Qt.WA_StyledBackground, True)
            
                self.neededTagField = False
                
                self.setMaximumHeight((PANEL_HEIGHT) * scale)
                self.setMinimumHeight((PANEL_HEIGHT) * scale)
            
            def addImageWidget(self, get_image_widget_method):
                self.get_image_widget_method = get_image_widget_method
                self.image_widget = get_image_widget_method(self, self.scale)
                self.grid_layout.addWidget(self.image_widget, 0, 0)
            
            def addCardInformationWidget(self, get_card_information_widget_method):
                self.get_card_information_widget_method = get_card_information_widget_method
                self.card_information_widget = get_card_information_widget_method(self, self.scale)            
                self.grid_layout.addWidget(self.card_information_widget, 0, 1)
            
            def addClassificationWidget(self, get_classification_widget_method):
                self.get_classification_widget_method = get_classification_widget_method
                self.classification_widget = get_classification_widget_method(self, self.scale)
                self.grid_layout.addWidget(self.classification_widget, 0, 2)
            
            def getLayout(self):
                return self.grid_layout
        
            def regenerate(self):
                """
                This method is called when the user clicked on the + (Add) button
                """
                # Remove all widget from the layout       
                clearLayout(self.grid_layout)

                # --- Image ---
                self.image_widget = self.get_image_widget_method(self, self.scale)
                self.grid_layout.addWidget(self.image_widget, 0, 0)            
        
                # --- Card Information ---
                self.card_information_widget = self.get_card_information_widget_method(self, self.scale)            
                self.grid_layout.addWidget(self.card_information_widget, 0, 1)
        
                # --- Classification ---
                self.classification_widget = self.get_classification_widget_method(self, self.scale)
                self.grid_layout.addWidget(self.classification_widget, 0, 2)
        
                if self.isNeededTagField():
                    
                    # The Tag input field into FOCUS
                    self.card_information_widget.setFocusTagField(True)
                else:
                    
                    # This (MainWidget) into FOCUS
                    self.setFocus()

            def setNeededTagField(self, value):
                self.neededTagField = value
        
            def isNeededTagField(self):
                return self.neededTagField
#       └──────────────────── MainWidget ──────────────────────┘

        if True: #not self.grid_layout:

            self.widget = MainWidget(self, scale)
        
            # --- Image ---
            self.widget.addImageWidget(self.getWidgetImage)
        
            # --- Card Information ---
            self.widget.addCardInformationWidget(self.getWidgetCardInformationText)
        
            # --- Classification ---
            self.widget.addClassificationWidget(self.getWidgetClassification)
        
        return self.widget
    
    def getMediaAppendixList(self):
        return self.mediaAppendixList

    def getQLabelToHoldImage(self):
        raise NotImplementedError
    
    # TODO    
    def isInFocus(self):
        """
            It indicates that the actual media (MediaCollector/MediaStorage) is selected to 
            be controlled by mouse.
            Practically it means that the media is a Card, and the Card is in the foreground
        """
        return True
    
    def getJson(self):
        json = {}
        
        json.update({JSON_SECTION_TITLES: self.titles.getJson()} if self.titles.getJson() else {})
        json.update({JSON_SECTION_GENERAL: self.general.getJson()} if self.general.getJson() else {})

        json.update({JSON_SECTION_STORYLINE: self.general.getStoryline().getJson()} if self.general.getStoryline().getJson() else {})
        json.update({JSON_SECTION_TOPIC: self.general.getTopic().getJson()} if self.general.getTopic().getJson() else {})
        json.update({JSON_SECTION_LYRICS: self.general.getLyrics().getJson()} if self.general.getLyrics().getJson() else {})

        json.update({JSON_SECTION_CLASSIFICATION: self.classification.getJson()} if self.classification.getJson() else {})
        json.update({JSON_SECTION_CONTROL: self.control.getJson()} if self.control.getJson() else {})
        
        json.update({JSON_NODE_APPENDIXES: [c.getJson() for c in self.mediaAppendixList]} if self.mediaAppendixList else {}) 
        
        return json
    
    