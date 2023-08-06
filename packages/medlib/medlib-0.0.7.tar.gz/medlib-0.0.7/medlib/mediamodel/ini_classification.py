import os

import medlib

from medlib.handle_property import _

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE

from medlib.constants import CLASSIFICATION_TAG_FIELD_BACKGROUND_COLOR
from medlib.constants import CLASSIFICATION_RATE_FIELD_BACKGROUND_COLOR

from medlib.constants import CLASSIFICATION_ICON_TAG_ADD
from medlib.constants import CLASSIFICATION_ICON_TAG_DELETE
from medlib.constants import CLASSIFICATION_ICON_FOLDER
from medlib.constants import CLASSIFICATION_ICON_PREFIX
from medlib.constants import CLASSIFICATION_ICON_FAVORITE_TAG   
from medlib.constants import CLASSIFICATION_ICON_SIZE
from medlib.constants import CLASSIFICATION_ICON_NEW
from medlib.constants import CLASSIFICATION_ICON_EXTENSION
from medlib.constants import ON
from medlib.constants import OFF

from medlib.card_ini import KEY_CLASSIFICATION_RATE
from medlib.card_ini import KEY_CLASSIFICATION_TAG
from medlib.card_ini import KEY_CLASSIFICATION_NEW
from medlib.card_ini import KEY_CLASSIFICATION_FAVORITE

from medlib.card_ini import SECTION_CLASSIFICATION

from medlib.card_ini import JSON_KEY_CLASSIFICATION_RATE
from medlib.card_ini import JSON_KEY_CLASSIFICATION_TAG
from medlib.card_ini import JSON_KEY_CLASSIFICATION_NEW
from medlib.card_ini import JSON_KEY_CLASSIFICATION_FAVORITE

from medlib.mediamodel.extra import FlowLayout

from medlib.handle_property import updateCardIni

from pkg_resources import resource_filename

from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QAbstractSpinBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QSize

import json

class IniClassification(object):
    """
    This class represents the [classification] section in the card.ini file
        -rate
        -favorite
        -new
        -tag
    """
    
    def __init__(self, rate=None, tag_list=[], favorite=None, new=None):
        """
        This is the constructor of the IniClassification class
        ___________________________________________
        input:
            rate        integer     1-10
            tag_list    list        list of tags
            favorite    boolean     True,False
            new         boolean     True,False
        """
        self.rate = rate if (rate is None or (rate >= 0 and rate <= 10)) else 1 if rate < 0 else 10
        self.tag_list = tag_list if tag_list else []
        self.favorite = favorite
        self.new = new
        
    def __str__(self):
        return json.dumps(self.getJson(), indent=4, sort_keys=True)
#        return (
#            "\nRate:     " + (str(self.getRate()) + "\n" if self.getRate() else "") +
#            "Favorite: " + (str(self.getFavorite()) + "\n" if self.getFavorite() is not None else "")+
#            "New:      " + (str(self.getNew()) + "\n" if self.getNew() is not None else "") +
#            "Tags:     " + (self.getTagList() + "\n" if self.getTagList() else "")
#        )
        
        
    def getRate(self):
        return self.rate
    
    def getTagList(self):
        return self.tag_list
    
    def getFavorite(self):
        return self.favorite
    
    def getNew(self):
        return self.new
        
    def setRate(self, rate):
        self.rate = 10 if rate > 10 else 0 if rate < 0 else rate

    def setFavorite(self, favorite):
        self.favorite = favorite

    def setNew(self, new):
        self.new = new
        
    def setTagList(self, tag_list):
        self.tag_list = tag_list
        
    def getJson(self):        
        json = {}
        json.update({} if self.rate is None else {JSON_KEY_CLASSIFICATION_RATE: self.rate})
        json.update({} if self.favorite is None else {JSON_KEY_CLASSIFICATION_FAVORITE : "y" if self.favorite else "n"})
        json.update({} if self.new is None else {JSON_KEY_CLASSIFICATION_NEW: "y" if self.new else "n"})
        json.update({} if self.tag_list is None or not self.tag_list else {JSON_KEY_CLASSIFICATION_TAG: self.tag_list})
        
        return json    
    
    # --------------------------------------------
    # ------------- Classification ---------------
    # --------------------------------------------    
      
    def getWidget(self, mainWidget, media, scale):
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
#       ┌──────────────────── ClassificationWidget ──────────────────────┐        
        class ClassificationWidget(QWidget):
            def __init__(self, media, scale):
                QWidget.__init__(self)
            
                self.scale = scale
                self.media = media

                # layout of this widget => three columns
                self.classification_layout = QVBoxLayout()
                self.classification_layout.setAlignment(Qt.AlignTop)
        
                # space between the three grids
                self.classification_layout.setSpacing(20 * scale)

                # margin around the widget
                self.classification_layout.setContentsMargins(0, 5, 12, 5)

                self.setLayout(self.classification_layout)
                
#                self.setAttribute(Qt.WA_StyledBackground, True)


            def addWidget(self, widget):
                self.classification_layout.addWidget(widget)  
#       └──────────────────── ClassificationWidget ──────────────────────┘    
       
        widget = ClassificationWidget(media, scale)
        
        # --- RATE ---
        widgetRate = self.getWidgetClassificationInfoRate(media, scale)
        widget.addWidget(widgetRate)
        
        # --- FAVORITE ---
        widgetFavorite = self.getWidgetClassificationInfoFavorite(media, scale)
        widget.addWidget(widgetFavorite)

        # --- NEW ---
        widgetNew = self.getWidgetClassificationInfoNew(mainWidget, media, scale)
        widget.addWidget(widgetNew)
        
        # --- ADD ---
        widgetAdd = self.getWidgetAdd(mainWidget, media, scale)
        widget.addWidget(widgetAdd)
        
        return widget
       
    # ---------- #
    # Rate field #
    # ---------- #
    def getWidgetClassificationInfoRate( self, media, scale ):
        
#       ┌──────────────────── MySpinBox ──────────────────────┐        
        class MySpinBox(QSpinBox):
            
            def __init__(self, ini_classification, scale):
                super().__init__()
                self.ini_classification = ini_classification
        
                if self.ini_classification.getRate() is None:
                    self.hide()

                else:
                    self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
                    self.setMaximum(10)
#                    self.setFocusPolicy(Qt.NoFocus)
                    self.lineEdit().setReadOnly(True)
                    self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                    self.lineEdit().setStyleSheet( "QLineEdit{color:black}")
                    self.setStyleSheet( "QSpinBox{background:'" + CLASSIFICATION_RATE_FIELD_BACKGROUND_COLOR + "'}")
                    self.setValue(self.ini_classification.getRate())
                    
                    self.valueChanged.connect(self.classificationRateOnValueChanged)

            def stepBy(self, steps):
                """
                It needs to be override to make deselection after the step.
                If it is not there, the selection color (blue) will be appear on the field
                """
                super().stepBy(steps)
                self.lineEdit().deselect()

            # Mouse Hover in
            def enterEvent(self, event):
                self.update()
                QApplication.setOverrideCursor(Qt.PointingHandCursor)

                self.setButtonSymbols(QAbstractSpinBox.UpDownArrows) #PlusMinus / NoButtons / UpDownArrows        

#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            # Mouse Hover out
            def leaveEvent(self, event):
                self.update()
                QApplication.restoreOverrideCursor()

                self.setButtonSymbols(QAbstractSpinBox.NoButtons) #PlusMinus / NoButtons / UpDownArrows        
        
#                self.card_panel.get_card_holder().setFocus()
                event.ignore()

            def classificationRateOnValueChanged(self):
                 
                # change the value of the rate in the Object
                self.ini_classification.setRate(self.value())
                
                # change the value of the rate in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_RATE, self.value())
                
                # change the value of the rate in the json                
                medlib.input_output.saveJson(media.getRoot())
#       └──────────────────── MySpinBox ──────────────────────┘

    
        widget = MySpinBox(self, scale)        
        return widget
        
    # --------------- #
    # Favorite button #
    # --------------- #
    def getWidgetClassificationInfoFavorite(self, media, scale):
        
#       ┌──────────────────── FavoriteButton ──────────────────────┐    
        class FavoriteButton(QPushButton):
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)
                self.ini_classification = ini_classification
        
                if self.ini_classification.getFavorite() is None:
                    self.hide()
                else:
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_FAVORITE_TAG + "-" + ON + "." + CLASSIFICATION_ICON_EXTENSION)) ), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap( resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_FAVORITE_TAG + "-" + OFF + "." + CLASSIFICATION_ICON_EXTENSION)) ), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(self.ini_classification.getFavorite())
                    
                    self.clicked.connect(self.classificationFavoriteButtonOnClick)
                    
            def classificationFavoriteButtonOnClick(self):

                # change the status of the favorite in the Object
                self.ini_classification.setFavorite(self.isChecked())
                
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_FAVORITE, 'y' if self.isChecked() else 'n')
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())
#       └──────────────────── FavoriteButton ──────────────────────┘

        button = FavoriteButton(self, scale)
        return button

    # ---------- #
    # New button #
    # ---------- #
    def getWidgetClassificationInfoNew(self, mainWidget, media, scale):
#       ┌──────────────────── NewButton ──────────────────────┐
        class NewButton(QPushButton):
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)    
                self.ini_classification = ini_classification
#                self.setFocusPolicy(Qt.NoFocus)

                if self.ini_classification.getNew() is None:
                    self.hide()
                else:        
                    self.setCheckable(True)        
                    icon = QIcon()
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_NEW + "-" + ON + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.On)
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_PREFIX + "-" + CLASSIFICATION_ICON_NEW + "-" + OFF + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.Off)
                    self.setIcon(icon)
                    self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
                    self.setCursor(QCursor(Qt.PointingHandCursor))
                    self.setStyleSheet("background:transparent; border:none")
                    self.setChecked(ini_classification.getNew())
                    
                    self.clicked.connect(self.classificationNewButtonOnClick)
        
            def classificationNewButtonOnClick(self):
                
                # change the status of the favorite in the Object
                self.ini_classification.setNew(self.isChecked())
                
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_NEW, 'y' if self.isChecked() else 'n')
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())
#       └──────────────────── NewButton ──────────────────────┘
        
        button = NewButton(self, scale)
        return button

    # ------------ #
    # + ADD button #
    # ------------ #
    def getWidgetAdd(self, mainWidget, media, scale):

#       ┌──────────────────── AddButton ──────────────────────┐        
        class AddButton(QPushButton):
   
#           ┌───────────────────── AddLabel ──────────────────────┐
            class AddLabel(QLabel):            
                clicked=pyqtSignal()
            
                def __init__(self, parent=None):
                    QLabel.__init__(self, parent)
                    self.setAttribute(Qt.WA_StyledBackground, True)


                def mousePressEvent(self, event):
                    self.clicked.emit()
                
                def enterEvent(self, event):
                    self.update()
                    QApplication.setOverrideCursor(Qt.PointingHandCursor)        
                    event.ignore()
        
                def leaveEvent(self, event):
                    self.update()
                    QApplication.restoreOverrideCursor()        
                    event.ignore()
#           └──────────────────── AddLabel ──────────────────────┘
            
            def __init__(self, ini_classification, scale):
                QPushButton.__init__(self)    
                self.ini_classification = ini_classification

                if self.ini_classification.getNew() is None and self.ini_classification.getFavorite() is None and self.ini_classification.getRate() is None:
                    self.hide()
                else:        

                    icon = QIcon()
                    icon.addPixmap(QPixmap(resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_TAG_ADD + "." + CLASSIFICATION_ICON_EXTENSION))), QIcon.Normal, QIcon.On)

                    self.setIcon(icon)
                    self.setIconSize(QSize(CLASSIFICATION_ICON_SIZE * scale, CLASSIFICATION_ICON_SIZE * scale))
                
                    self.setCursor(QCursor(Qt.PointingHandCursor))

                    self.setStyleSheet("background:transparent; border:none")
                    
                    self.clicked.connect(self.on_click)

            # You clicked on the Add (green cross) button
            def on_click(self):
 
                # Indicates that the TAG FIELD needs to be shown
                mainWidget.setNeededTagField(True)
                
                # Re-paint the widget (with the TAG FIELD)
                mainWidget.regenerate()
#       └──────────────────── AddButton ──────────────────────┘        
        
        button = AddButton(self, scale)
        return button


    def getWidgetTagListButtons(self, mainWidget, media, scale, title_id, get_list_method):
        """
        Adds the tags as buttons        
        """
        
        tag_list = get_list_method()      

        #
        # TAG button
        #
#       ┌──────────────────── TagButtonForSearch ──────────────────────┐        
        class TagButtonForSearch(QPushButton):
            """
            It represents the tag button
            The button has a "delete" icon on the right side.
            If you click on the delete icon, the tag will be removed
            """
#           ┌──────────────────── DeleteLabel ──────────────────────┐            
            class DeleteLabel(QLabel):            
                clicked=pyqtSignal()
            
                def __init__(self, parent):
                    QLabel.__init__(self, parent)
                    
                    self.parent = parent
                    
                    self. pathToDeleteOffIcon = resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_TAG_DELETE + "-" + OFF + "." + CLASSIFICATION_ICON_EXTENSION))
                    self. pathToDeleteOnIcon = resource_filename(__name__, os.path.join(CLASSIFICATION_ICON_FOLDER, CLASSIFICATION_ICON_TAG_DELETE + "-" + ON + "." + CLASSIFICATION_ICON_EXTENSION))
                    
                    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

                    self.setPixmap(QIcon(self.pathToDeleteOffIcon).pixmap(QSize(parent.fm.height() - parent.iconBorder * 2, parent.fm.height() - parent.iconBorder * 2)))

#                    self.setFocusPolicy(Qt.NoFocus)
                def mousePressEvent(self, event):
                    self.clicked.emit()
                
                def enterEvent(self, event):
                    self.update()
                    self.setPixmap(QIcon(self.pathToDeleteOnIcon).pixmap(QSize(self.parent.fm.height() - self.parent.iconBorder * 2, self.parent.fm.height() - self.parent.iconBorder * 2)))

                    QApplication.setOverrideCursor(Qt.PointingHandCursor)        
                    event.ignore()
        
                def leaveEvent(self, event):
                    self.update()
                    self.setPixmap(QIcon(self.pathToDeleteOffIcon).pixmap(QSize(self.parent.fm.height() - self.parent.iconBorder * 2, self.parent.fm.height() - self.parent.iconBorder * 2)))

                    QApplication.restoreOverrideCursor()        
                    event.ignore()
#           └──────────────────── DeleteLabel ──────────────────────┘        
                
            def __init__(self, media, scale, translatedText, rawText, title_id):
            
                super().__init__(translatedText + "   ")
                self.media = media
                self.rawText = rawText
                self.title_id = title_id

                self.iconBorder = 2 * scale

                # Set size of button
                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold)) 
                self.fm = QFontMetrics(self.font())

                # Delete Icon                
                label_icon = self.DeleteLabel(self)


                layout = QHBoxLayout(self)
                layout.setContentsMargins(0, 0, self.iconBorder, 0)
                layout.addWidget(label_icon, alignment=QtCore.Qt.AlignRight)

                # calculate text width
                self.setFixedWidth(self.fm.width(self.text()) + 10)
                self.setFixedHeight(self.fm.height())

                label_icon.clicked.connect(self.on_delete)            
                self.clicked.connect(self.on_click)

            def on_delete(self):

                # remove the tag from the tag list
                tag_list.remove(self.rawText)
            
                # change the tag list in the Object
                media.classification.setTagList(tag_list)
            
                # change the status of the favorite in the card.ini
                updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_TAG, ','.join(tag_list))
        
                # change the value of the rate in the json
                medlib.input_output.saveJson(media.getRoot())

                # No need TAG FIELD anymore                    
                mainWidget.setNeededTagField(False)

                # Re-print the widgets
                mainWidget.regenerate()
            
            def on_click(self):
                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ShiftModifier:
                    withShift = True
                else:
                    withShift = False
                self.media.search( withShift, self.rawText, self.title_id)
#       └──────────────────── TagButtonForSearch ──────────────────────┘        

        #
        # TAG FIELD
        #
#       ┌──────────────────── TagField ──────────────────────┐
        class TagField(QLineEdit):
            """
            It represents the TAG field
            """
            def __init__(self, media, scale): #, translatedText, rawText, title_id):
            
                super().__init__()
                self.media = media

                # Set size of button
                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Bold)) 
                self.setStyleSheet( "color:black; background:'" + CLASSIFICATION_TAG_FIELD_BACKGROUND_COLOR + "'")
                fm = QFontMetrics(self.font())

                # calculate text width
                self.setFixedWidth(fm.width("WWWWWWW") + 10)
                self.setFixedHeight(fm.height())            
             
            def keyPressEvent(self, event):

                # press ESC on the TAG FIELD
                if event.key() == Qt.Key_Escape:
                    
                    # No need TAG FIELD anymore
                    mainWidget.setNeededTagField(False)
                    
                    # Re-paint the widget (without the TAG FIELD)
                    mainWidget.regenerate()
                    
                    # I do not want to propagate the ESC event to the parent
                    event.setAccepted(True)

#                    print("Tag field")

                # press ENTER on the TAG FIELD                    
                elif event.key() == Qt.Key_Return:
                    text = self.text().strip()
                
                    if text and text not in tag_list:

                        # add the tag to the tag list
                        tag_list.append(text)
            
                        # change the tag list in the Object
                        media.classification.setTagList(tag_list)
            
                        # change the status of the favorite in the card.ini
                        updateCardIni(media.getPathOfCard(), SECTION_CLASSIFICATION, KEY_CLASSIFICATION_TAG, ','.join(tag_list))
        
                        # change the value of the rate in the json
                        medlib.input_output.saveJson(media.getRoot())

                    # No need TAG FIELD anymore
                    mainWidget.setNeededTagField(False)

                    # Re-print the widgets
                    mainWidget.regenerate()
                    
                    # I do not want to propagate the ESC event to the parent
                    event.setAccepted(True)
                
                else:
                    super(TagField, self).keyPressEvent(event)
#       └──────────────────── TagField ──────────────────────┘
                    
#       ┌──────────────── TagListButtonsWidget ──────────────┐
        class TagListButtonsWidget(QWidget):
            def __init__(self, mainWidget, media, scale):
                QWidget.__init__(self)

                self.mainWidget = mainWidget
                self.media = media
                self.scale = scale
          
                self.layout = FlowLayout()
                self.layout.setAlignment(Qt.AlignLeft)        
                self.layout.setSpacing(1)        
                self.layout.setContentsMargins(0, 0, 0, 0)                
                self.setLayout( self.layout )

                self.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale, weight=QFont.Normal))
                
                self.fieldWidget = None      

            def addButtonWidget(self, buttonWidget):
                self.layout.addWidget(buttonWidget)
                
            def addFieldWidget(self, fieldWidget):
                self.fieldWidget = fieldWidget
                self.layout.addWidget(fieldWidget)
                
            def setFocusTagField(self, value):
                if self.fieldWidget:
                    self.fieldWidget.setFocus(value)
#       └──────────────── TagListButtonsWidget ──────────────┘
                
        widget_value = TagListButtonsWidget(mainWidget, media, scale)
        needWidget = False
        
        # Add TAG buttons
        for tag in tag_list:            
            label = TagButtonForSearch(media, scale, tag, tag, title_id)
            widget_value.addButtonWidget(label)
            needWidget = True
                
        # Add TAG field
        if mainWidget.isNeededTagField():
            field = TagField(media, scale)
            widget_value.addFieldWidget(field)
                
            needWidget = True
            
        # if there was TAGs and/or TAG FIELD    
        if needWidget:
            return widget_value
        else:
            return None
        
