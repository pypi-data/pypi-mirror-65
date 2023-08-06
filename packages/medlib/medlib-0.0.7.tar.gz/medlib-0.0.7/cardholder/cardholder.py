
import math
import time 
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QMovie

from PyQt5 import QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QByteArray

from medlib.handle_property import getConfigIni
from pkg_resources import resource_filename
from math import copysign
from cardholder.card_data_interface import CardDataInterface
from medlib.mediamodel.media_collector import MediaCollector
 
# =========================
#
# Card Holder
#
# =========================
class CardHolder( QWidget ):
    
    resized = QtCore.pyqtSignal(int,int)
    moved_to_front = QtCore.pyqtSignal(int)
    
    DEFAULT_SPINNER_NAME = 'spinner.gif'

    DEFAULT_MAX_OVERLAPPED_CARDS = 4    
    DEFAULT_BORDER_WIDTH = 5
    DEFAULT_BACKGROUND_COLOR = QColor(Qt.red)
    DEFAULT_BORDER_RADIUS = 10
    
    DEFAULT_RATE_OF_CARD_WIDTH_DECLINE = 10
    DEFAULT_RATE_OF_CARD_Y_MULTIPLICATOR = 6
    
    CARD_TRESHOLD = 6  
    MAX_CARD_ROLLING_RATE = 10
    
    FAST_FORWARD_NUMBER = 5
    
    def __init__(self, 
                 parent, 
                 get_new_card_method, 
                 get_collected_cards_method,
                 refresh_list_listener = None,
                 select_card_method = None,
                 goes_higher_method = None          
                 ):
        """
        Represents a CardHolder widget
        Input:
            parent:                        The widget which contains this CardHolder
            get_new_card_method:           Method to create the appearing Card
            get_collected_cards_method:    Method to collect the contents of the Cards
            
            refresh_list_listener
            select_card_method
            goes_higher_method:            Method to go to the previous level           
        """
        #super(CardHolder, self).__init__(parent)
        QWidget.__init__(self, parent)

        self.parent = parent
        self.get_new_card_method = get_new_card_method
        self.get_collected_cards_method = get_collected_cards_method
        
        self.refresh_list_listener = refresh_list_listener
        self.select_card_method = select_card_method        
        self.goes_higher_method = goes_higher_method
        
        self.shown_card_list = []
        self.card_data_list = []

        self.set_max_overlapped_cards(CardHolder.DEFAULT_MAX_OVERLAPPED_CARDS, False)        
        self.setBorderWidth(CardHolder.DEFAULT_BORDER_WIDTH, False)
        self.setBorderRadius(CardHolder.DEFAULT_BORDER_RADIUS, False)
        self.setBackgroundColor(CardHolder.DEFAULT_BACKGROUND_COLOR, False)
        
        self.self_layout = QVBoxLayout(self)
        self.setLayout(self.self_layout)

        self.rate_of_movement = 0
        self.delta_rate = 0
        
        self.countDown = CountDown()
        self.countDown.timeOver.connect(self.animated_move_to_closest_descreet_position)
        
        self.collecting_spinner = None
        spinner_file_name = resource_filename(__name__,os.path.join("img", CardHolder.DEFAULT_SPINNER_NAME))
        self.set_spinner(spinner_file_name)

        self.set_y_coordinate_by_reverse_index_method(self.get_y_coordinate_by_reverse_index)
        self.set_x_offset_by_index_method(self.get_x_offset_by_index)

        # it hides the CardHolder until it is filled up with cards
        self.focus_index(0)
        
        self.setAttribute(Qt.WA_StyledBackground, True)

        # The CardHolder will accept Focus by Tabbing and Clicking
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()      
    
#    def setSelectedRootCardIndex(self, selected_root_card_index):
#        self.selected_root_card_index = selected_root_card_index
#        
#    def getSelectedRootCardIndex(self):
#        return self.selected_root_card_index        
    
    def set_y_coordinate_by_reverse_index_method(self, method):
        self.get_y_coordinate_by_reverse_index_method = method
        
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        return reverse_index * reverse_index * CardHolder.DEFAULT_RATE_OF_CARD_Y_MULTIPLICATOR

    def set_x_offset_by_index_method(self, method):
        self.get_x_offset_by_index_method = method

    def get_x_offset_by_index(self, index):
        return index * CardHolder.DEFAULT_RATE_OF_CARD_WIDTH_DECLINE

    # ----------------
    #
    # set spinner
    #
    # ----------------
    def set_spinner(self, file_name):

        # remove the old spinner
        if self.collecting_spinner != None:
            self.spinner_movie.stop()            
            self.collecting_spinner.setParent(None)
            self.collecting_spinner = None
            
        self.spinner_movie = QMovie(file_name, QByteArray(), self)
        self.collecting_spinner = QLabel(self.parent)
        self.collecting_spinner.setMovie(self.spinner_movie)
        self.collecting_spinner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.spinner_movie.setCacheMode(QMovie.CacheAll)
        self.spinner_movie.setSpeed(100)
        self.spinner_movie.start()          # if I do not start it, it stays hidden
        self.spinner_movie.stop()
        self.collecting_spinner.move(0,0)
        self.collecting_spinner.show()
        self.collecting_spinner.setHidden(True)

        img_size = self.spinner_movie.currentPixmap().size()
        self.collecting_spinner.resize(img_size.width(), img_size.height())      
        
    # --------------------------------------
    # Shows the spinner + removes all Cards
    # --------------------------------------
    def start_spinner(self):

        # remove all cards
        self.refresh()
        self.alignSpinner(self.parent.geometry().width(), self.parent.geometry().height())
        self.spinner_movie.start()
        self.collecting_spinner.setHidden(False)        

    def alignSpinner(self, windowWidth, windowHeight):
        self.collecting_spinner.move(
            (windowWidth-self.collecting_spinner.width()) / 2,
            (windowHeight-self.collecting_spinner.width()) / 2
        )
        
        
    # ------------------------------
    # Hides the spinner
    # ------------------------------
    def stop_spinner(self):
        self.collecting_spinner.setHidden(True)
        self.spinner_movie.stop()
        
    # ---------------------------------------------------------------------
    #
    # start card collection
    #
    # this method should be called when you want a new collection of cards
    #
    # ---------------------------------------------------------------------
    def startCardCollection(self):        

        self.start_spinner()

#        self.cc = CollectCardsThread.getInstance( self, self.get_collected_cards_method, parameters )
        self.cc = CollectCardsThread.getInstance( self, self.get_collected_cards_method )        
        if self.cc:
            self.cc.cards_collected.connect(self.refresh)
            self.cc.start()   

    # ------------------------------------------------------
    # fill up card descriptor - used by the refresh() method
    # ------------------------------------------------------
    def fill_up_card_descriptor_list(self, filtered_card_list = []):             
        self.card_data_list = []
        for card_data in filtered_card_list:
            self.card_data_list.append(card_data)

    def setBorderWidth(self, width, update=True):
        self.border_width = width
        if update:
            self.update()
        
    def get_border_width(self):
        return self.border_width

    def setBackgroundColor(self, color, update=True):
        self.background_color = color
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: ' + self.background_color.name())
        if update:
            self.update()
        
    def set_max_overlapped_cards(self, number, update=True):
        self.max_overlapped_cards = number
        if update:
            #self.focus_index(self.actual_card_index)
            self.focus_index(0)
        
    def setBorderRadius(self, radius, update=True):
        self.border_radius = radius
        if update:
            self.update()
        
    def get_max_overlapped_cards(self):
        return self.max_overlapped_cards
  
    def resizeEvent(self, event):
        self.resized.emit(event.size().width(),event.size().height())
        return super(CardHolder, self).resizeEvent(event)
 
    def remove_all_cards(self):
        for card in self.shown_card_list:
            card.setParent(None)
            card = None

    def remove_card(self, card):
        card.setParent(None)
        card = None

    def get_rate_of_movement(self):
        return self.rate_of_movement
    
    def get_delta_rate(self):
        return self.delta_rate

            
        
        





    
    # --------------------------------------------------------------------------
    #
    # Focus Index
    #
    # It builds up from scratch the shown_card_list from the card_data_list
    # In the 0. position (on front) will be the Card identified by the "index" parameter
    # The card in the 0. position will be indicated as the "focused"
    #
    # --------------------------------------------------------------------------
    def focus_index(self, index):
        index_corr = self.get_corrected_card_data_index(index)
        self.remove_all_cards()
        position = None
        self.shown_card_list = [None for i in range(index_corr + min(self.max_overlapped_cards, len(self.card_data_list)-1), index_corr - 1, -1) ]
        
        for i in range( index_corr + min(self.max_overlapped_cards, len(self.card_data_list)-1), index_corr - 1, -1):
            
            i_corr = self.get_corrected_card_data_index(i)
            
            if( i_corr < len(self.card_data_list)):

                local_index = i-index_corr
                card = self.get_new_card_method(self.card_data_list[i_corr], local_index, i_corr )                                
                position = card.place(local_index)
                
                self.shown_card_list[local_index] = card

        # if there is at least one Card
        if self.shown_card_list:

            # Control the Height of the CardHolder
            self.setMinimumHeight(position[0].y() + position[1].y() + self.border_width )
            self.setMaximumHeight(position[0].y() + position[1].y() + self.border_width )
        
            # for indicating the focused (0) Card
            self.rolling(0)
            
        # if there is NO Card at all
        else:
            # hides the CardHolder
            self.setMinimumHeight(0)
            self.setMaximumHeight(0)

    # for some reason the 2nd parameter is False from connect
    # that is why I cant connect it to directly
    def button_animated_move_to_next(self):
        self.animated_move_to_next()

    def button_animated_move_to_previous(self):
        self.animated_move_to_previous()


    # ---------------------------------
    #
    # Animated shows the next card
    #
    # ---------------------------------
    def animated_move_to_next(self, sleep=0.01):
        rate = self.get_rate_of_movement()
        
        if rate > 0:
            loop = self.MAX_CARD_ROLLING_RATE - rate
        elif rate < 0:
            loop = -rate
        else:
            loop = self.MAX_CARD_ROLLING_RATE
            
        self.animate = AnimateRolling.getInstance(int(loop), 1, sleep)
        if self.animate:
            self.animate.positionChanged.connect(self.rolling)
            self.animate.start()
       
    # ---------------------------------
    #
    # Animated shows the previous card
    #
    # ---------------------------------
    def animated_move_to_previous(self, sleep=0.01):
        rate = self.get_rate_of_movement()
        
        if rate > 0:
            loop = rate
        elif rate < 0:
            loop = self.MAX_CARD_ROLLING_RATE + rate
        else:
            loop = self.MAX_CARD_ROLLING_RATE
            
        self.animate = AnimateRolling.getInstance(int(loop), -1, sleep)
        if self.animate:
            self.animate.positionChanged.connect(self.rolling)
            self.animate.start()
    
    # ------------------------------------------------
    #
    # Animated moves to the closest descreet position
    #
    # ------------------------------------------------
    def animated_move_to_closest_descreet_position(self):
        rate = self.get_rate_of_movement()
        delta_rate = self.get_delta_rate()
        
        if rate != 0:
            
            if rate > 0:
                
                if delta_rate < 0:
                    value = -1
                    loop = rate
                else:
                    value = 1
                    loop = self.MAX_CARD_ROLLING_RATE - rate                    
                
                #if rate >= self.CARD_TRESHOLD:
                #    value = 1
                #    loop = self.MAX_CARD_ROLLING_RATE - rate                    
                #else:
                #    value = -1
                #    loop = rate
        
            elif rate < 0:
                
                if delta_rate < 0:
                    value = -1
                    loop = self.MAX_CARD_ROLLING_RATE + rate
                else:
                    value = 1
                    loop = -rate
                
                #if rate <= -self.CARD_TRESHOLD:
                #    value = -1
                #    loop = self.MAX_CARD_ROLLING_RATE + rate
                #else:
                #    value = 1
                #    loop = -rate
                
            self.animate = AnimateRolling.getInstance(int(loop), value, 0.02)
            if self.animate:
                self.animate.positionChanged.connect(self.rolling)
                self.animate.start()

    # ------------------------------------------------
    #
    # Animated moves to the set relative position Card
    #
    # ------------------------------------------------
    def animated_move_to(self, relative_position, sleep=0.01):
        self.animate = AnimateRolling.getInstance(relative_position * self.MAX_CARD_ROLLING_RATE, 1, sleep)
        if self.animate:
            self.animate.positionChanged.connect(self.rolling)
            self.animate.start()        

    # ---------------------------------------------------------------------
    #
    # Rolling Wheel
    #
    # Rolls the cards according to the self.rate_of_movement + delta_rate
    # Plus it starts a Timer. If the timer expires, the cards will be 
    # moved to the first next discreet position
    #
    # --------------------------------------------------------------------
    def rolling_wheel(self, delta_rate):
        self.rolling(delta_rate)
        
        if self.rate_of_movement != 0:
            self.countDown.start()

    # --------------------------------------------------------------------
    #
    # ROLLING
    #
    # Rolls the cards according to the self.rate_of_movement + delta_rate
    #
    # delta_rate:   In normal case it is +1 or -1
    #               Adding this value to the self.rate_of_movement, it
    #               shows that how far the cards moved negativ (up) or
    #               positive (down) direction compared to the default
    #               (local_index) value
    #               -10 means (-100%) it moved to the next position, 
    #               +10 means (+100%) it moved to the previous position
    #
    # -------------------------------------------------------------------
    def rolling(self, delta_rate):
        
        self.delta_rate = delta_rate
        
        if self.rate_of_movement >= self.MAX_CARD_ROLLING_RATE or self.rate_of_movement <= -self.MAX_CARD_ROLLING_RATE:
            self.rate_of_movement = 0

        self.rate_of_movement = self.rate_of_movement + delta_rate

        # Did not start to roll
        # if number of the shown cards are != min(max overlapped cards +1, len(self.card_data_list))
        #if len(self.shown_card_list) <= self.get_max_overlapped_cards() + 1:
        if len(self.shown_card_list) == min(self.max_overlapped_cards + 1, len(self.card_data_list)):
            
            # indicates that the first card is not the focused anymore
            card = self.shown_card_list[0]
            card.setNotFocused()
            
            # add new card to the beginning
            first_card = self.shown_card_list[0]                
            first_card_index = self.get_corrected_card_data_index(first_card.getIndexInDataList() - 1)
            card = self.get_new_card_method(self.card_data_list[first_card_index], -1, first_card_index ) 
            self.shown_card_list.insert(0, card)
            
            # add a new card to the end
            last_card = self.shown_card_list[len(self.shown_card_list)-1]                
            last_card_index = self.get_corrected_card_data_index(last_card.getIndexInDataList() + 1)
            #card = self.get_new_card_method(self.card_data_list[last_card_index], self.get_max_overlapped_cards() + 1, last_card_index ) 
            card = self.get_new_card_method(self.card_data_list[last_card_index], min(self.max_overlapped_cards + 1, len(self.card_data_list)), last_card_index ) 
            
            self.shown_card_list.append(card)
            
            # Re-print to avoid the wrong-overlapping
            for card in self.shown_card_list[::-1]:
                card.setParent(None)
                card.setParent(self)
                card.show()        

        # adjust
        rate = self.rate_of_movement / self.MAX_CARD_ROLLING_RATE
        if self.rate_of_movement >= 0:
            self.rolling_adjust_forward(rate)
        else:
            self.rolling_adjust_backward(rate)

        # indicates that the first card is the focus            
        if self.rate_of_movement == 0:
            card = self.shown_card_list[0]
            
            card.setFocused()

        # show the cards in the right position
        rate = self.rate_of_movement / self.MAX_CARD_ROLLING_RATE
        for i, card in enumerate(self.shown_card_list):
            virtual_index = card.local_index - rate
            card.place(virtual_index, True)

    def rolling_adjust_forward(self,rate):
        
        if rate >= 1.0:
            self.rate_of_movement = 0
            
            # remove the first 2 cards from the list and from CardHolder
            for i in range(2):
                card_to_remove = self.shown_card_list.pop(0)
                card_to_remove.setParent(None)

            # re-index
            for i, card in enumerate(self.shown_card_list):
                card.local_index = i
                
        elif rate == 0:
            # remove the first card from the list and from CardHolder
            card_to_remove = self.shown_card_list.pop(0)
            card_to_remove.setParent(None)
            
            # remove the last card from the list and from CardHolder
            card_to_remove = self.shown_card_list.pop(len(self.shown_card_list) - 1)
            card_to_remove.setParent(None)

    def rolling_adjust_backward(self,rate):
        
        if rate <= -1.0:
            self.rate_of_movement = 0
        
            # remove the 2 last cards from the list and from CardHolder
            for i in range(2):
                card_to_remove = self.shown_card_list.pop(len(self.shown_card_list) - 1)
                card_to_remove.setParent(None)
            
            # re-index
            for i, card in enumerate(self.shown_card_list):
                card.local_index = i

    # -----------------------------------------------------------
    #
    # INDEX CORRECTION
    #
    # if the index > numbers of the cards then it gives back 0
    #    as the next index
    # if the index < 0 then it gives back the index of the last
    #    card as the previous index
    #
    # that is how it actually accomplishes an endless loop
    #
    # -----------------------------------------------------------
    def get_corrected_card_data_index(self, index):
        if self.card_data_list:
            return (len(self.card_data_list) - abs(index) if index < 0 else index) % len(self.card_data_list)
        else:
            return index

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.background_color )

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()  

    def getFocusedCard(self):
        if self.shown_card_list:
            first_card = self.shown_card_list[0]
            return first_card
        else:
            return None

    def wheelEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        value = event.angleDelta().y()/8/15   # in normal case it is +1 or -1

        if modifiers == Qt.ControlModifier:
            
            # Change SCALE_LEVEL
            config_ini_function = getConfigIni()
            scale_level = int(config_ini_function.getScaleLevel())
            scale_level = scale_level + (1 if value > 0 else - 1)
            config_ini_function.setScaleLevel(str(scale_level))
            
            index_of_focused_card = self.getFocusedCard().getIndexInDataList()
            self.focus_index(index_of_focused_card)
            
        else:
            self.rolling_wheel(-value)
  
    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Up and event.modifiers() == Qt.ControlModifier:
            
            # Change SCALE_LEVEL
            config_ini_function = getConfigIni()
            scale_level = int(config_ini_function.getScaleLevel())
            scale_level = scale_level + 1
            config_ini_function.setScaleLevel(str(scale_level))

            parent_collector = self.getParentCollector()
            index_of_focused_card = self.getFocusedCard().getIndexInDataList()
            self.focus_index(index_of_focused_card)
            
        elif event.key() == QtCore.Qt.Key_Down and event.modifiers() == Qt.ControlModifier:
            
            # Change SCALE_LEVEL
            config_ini_function = getConfigIni()
            scale_level = int(config_ini_function.getScaleLevel())
            scale_level = scale_level - 1
            config_ini_function.setScaleLevel(str(scale_level))
            
            parent_collector = self.getParentCollector()
            index_of_focused_card = self.getFocusedCard().getIndexInDataList()
            self.focus_index(index_of_focused_card)            
        
        elif event.key() == QtCore.Qt.Key_Up:
            self.animated_move_to_next(sleep=0.04)
            
        elif event.key() == QtCore.Qt.Key_Down:
            self.animated_move_to_previous(sleep=0.04)

        elif event.key() == QtCore.Qt.Key_PageUp:
            self.animated_move_to(self.FAST_FORWARD_NUMBER, 0.04)
            
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.animated_move_to(-self.FAST_FORWARD_NUMBER, 0.04)
          
        #  
        # Goes Up in the hierarchy
        #
        elif event.key() == QtCore.Qt.Key_Escape:
            
            if self.goesHigher():
                
                # I do not want to propagate the ESC event to the parent
                event.setAccepted(True)
     
        #
        # Select a Card
        #
        elif event.key() == QtCore.Qt.Key_Space or event.key() == QtCore.Qt.Key_Return:
            
            # Comes from the MouseClick -> It could be any Card on the screen
            if event.text().isdigit():
                card_index = int(event.text())

                # Move the Card to the front
                self.focus_index(card_index)
                
            # Comes from SPACE/ENTER -> Only 
            else:
                pass

            # Fetch the Card in the focus (in front)
            selected_card = self.getFocusedCard()

            if self.select_card_method:
                self.select_card_method(selected_card)
            
            else:
        
                # Depending of the Media (Storage/Collector) needs to do different things
                panel = selected_card.getPanel()
                layout = panel.getLayout()
            
                # the 0th item in the layout is the Image
                widget = layout.itemAt(0).widget()
                widget.image_widget.toDoSelection()

            event.setAccepted(True)
                    
        else:
           
            event.setAccepted(False)  
    
    def collectMediaStorageWithoutHierarchy(self, sum_list, parent_collector):
        mcl = parent_collector.getMediaCollectorList()
        sum_list += parent_collector.getMediaStorageList()
        for media_collector in mcl:
            self.collectMediaStorageWithoutHierarchy(sum_list, media_collector)
        return sum_list
    
    def getParentCollector(self):
        return self.getFocusedCard().card_data.getParentCollector()
    
    # TODO build in the refresh()
    def getSortedMediaStorageList(self, parent_collector):
        
        # Without hierarchy
        if not self.parent.isSwitchKeepHierarchy():
            msl = self.collectMediaStorageWithoutHierarchy([], parent_collector)
            msl.sort(key=lambda arg: MediaCollector.sort_key(arg))
                
        # With hierarchy
        else:        
            msl = parent_collector.getMediaStorageList()
        
        return msl
             
    def refresh(self, parent_collector=None, index=0):
        """
        Fills up the CardHolder with Cards and pulls the <index>th Card to front
        
        
        """
       
        if parent_collector:

            # Without hierarchy
            if not self.parent.isSwitchKeepHierarchy():
                sum_list = self.collectMediaStorageWithoutHierarchy([], parent_collector)
                sum_list.sort(key=lambda arg: MediaCollector.sort_key(arg))

                # Listener of the refresh list
                # Here you refresh the self.mediaCollector object in the medlib_gui
                self.refresh_list_listener(parent_collector, sum_list)            
                
            # With hierarchy
            else:        
                mcl = parent_collector.getMediaCollectorList()
                msl = parent_collector.getMediaStorageList()
                sum_list = mcl + msl

                # Listener of the refresh list
                # 1. set self.mediaCollector
                # 2. fill up the "play continously" list if there is NO ongoing play
                # 3. save the "play continously" list if there IS ongoing play
                self.refresh_list_listener(parent_collector, msl)            

            self.fill_up_card_descriptor_list(sum_list)                
            self.focus_index(index)

        self.stop_spinner()


    def goesHigher(self):
        if self.goes_higher_method:
            #self.goes_higher_method(self.getFocusedCard())
            self.goes_higher_method()
         
            return True
        else:

            collector, index = self.parent.getHierarchyTitle().getOneLevelHigher()
            if collector and index >= 0:
                self.refresh(collector, index)
            return False
 
    def goesDeeper(self, mediaCollector):               
        self.refresh(mediaCollector)
           
    # --------------
    # MOUSE handling
    # --------------        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
        event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:

            # Rolling Cards
            delta_y = event.pos().y() - self.drag_start_position.y()
            self.drag_start_position = event.pos()

            if delta_y > 0:
                self.rolling_wheel(1)
            elif delta_y < 0:
                self.rolling_wheel(-1)
        event.ignore()
  
# ==========================================================
#
# Panel
#
# This Panel is inside the Card and contains all widget
# what the user what to show on a Card.
# This Panel has rounded corner which is calculated by the
# radius of the Card and the widht of the border.
#
# ==========================================================
class Panel(QWidget):
    DEFAULT_BORDER_WIDTH = 5
    DEFAULT_BACKGROUND_COLOR = QColor(Qt.lightGray)
    
    def __init__(self, parent):
        #super().__init__()
        QWidget.__init__(self, parent)
        
        self.self_layout = QVBoxLayout()
        self.self_layout.setContentsMargins(0, 0, 0, 0)
        self.self_layout.setSpacing(1)
        self.setLayout(self.self_layout)

        self.setBackgroundColor(Panel.DEFAULT_BACKGROUND_COLOR, False)        
        self.setBorderWidth(Panel.DEFAULT_BORDER_WIDTH, False)
        #self.setBorderRadius(border_radius, False)

        self.setAttribute(Qt.WA_StyledBackground, True)

    def getLayout(self):
        return self.self_layout
    
    def setBorderRadius(self, radius, update=True):
        self.border_radius = radius
        if update:
            self.update()
        
    def setBorderWidth(self, width, update=True):
        self.border_width = width
        self.self_layout.setContentsMargins( self.border_width, self.border_width, self.border_width, self.border_width )
        if update:
            self.update()

    def setBackgroundColor(self, color, update=True):
        self.background_color = color
        
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: ' + self.background_color.name())
        
        if update:            
            self.update()
    
    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.background_color )
        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()    

# ==================
#
# Card
#
# ==================
class Card(QWidget):

    STATUS_NORMAL = 0
    STATUS_FOCUSED = 1
    DTATUS_DISABLED = 2
    
#    DEFAULT_RATE_OF_WIDTH_DECLINE = 10
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_BORDER_RADIUS = 10
    
    DEFAULT_BORDER_NORMAL_COLOR = QColor(Qt.green)
    DEFAULT_BORDER_FOCUSED_COLOR = QColor(Qt.red)
    DEFAULT_BORDER_DISABLED_COLOR = QColor(Qt.lightGray)
    
    DEFAULT_STATUS = STATUS_NORMAL
    
    onMouseClicked = pyqtSignal(int)
    #onMouseDragged = pyqtSignal(int)
    
    def __init__(self, card_holder, card_data, local_index, index):
        #super().__init__(card_holder)
        QWidget.__init__(self, card_holder)

        assert issubclass(card_data.__class__, CardDataInterface)

        self.card_data = card_data
        self.card_data.setIndex(index)

#        self.card_data.setCard(self)

        self.index = index
        self.local_index = local_index
        self.card_holder = card_holder
        self.actual_position = 0
        
        self.self_layout = QVBoxLayout(self)
        self.setLayout(self.self_layout)
        #self.self_layout.setContentsMargins(self.border_width,self.border_width,self.border_width,self.border_width)
        self.self_layout.setContentsMargins(0, 0, 0, 0)
        self.self_layout.setSpacing(0)
        
        self.setBorderNormalColor(Card.DEFAULT_BORDER_NORMAL_COLOR)
        self.setBorderFocusedColor(Card.DEFAULT_BORDER_FOCUSED_COLOR)
        self.setBorderDisabledColor(Card.DEFAULT_BORDER_DISABLED_COLOR)
        
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: ' + "yellow")  

        # Panel where the content could be placed
        self.panel = Panel(self)
        self.panel_layout = self.panel.getLayout()
        self.self_layout.addWidget(self.panel)
        
        self.border_radius = Card.DEFAULT_BORDER_RADIUS
        self.setBorderWidth(Card.DEFAULT_BORDER_WIDTH, False)
        self.setBorderRadius(Card.DEFAULT_BORDER_RADIUS, False)        
        #self.set_rate_of_width_decline(Card.DEFAULT_RATE_OF_WIDTH_DECLINE, False)
        
        self.set_status(Card.STATUS_NORMAL)
        
        # Connect the widget to the Container's Resize-Event
        self.card_holder.resized.connect(self.resized)
        
        self.drag_start_position = None
        #self.setDragEnabled(True)
        #self.setAcceptDrops(True)
        
        self.onMouseClicked.connect(self.card_holder.animated_move_to)
        #self.onMouseDragged.connect(self.card_holder.rolling_wheel)
 
        self.already_mouse_pressed = False
        
        self.setAttribute(Qt.WA_StyledBackground, True)        

    def setIndexInDataList(self, index):
        self.index = index
        
    def getIndexInDataList(self):
        return self.index
        
    def setFocused(self):
        self.set_status(Card.STATUS_FOCUSED, True)
        
    def setNotFocused(self):
        self.set_status(Card.STATUS_NORMAL, True)
        
    def set_status(self, status, update=False):
        self.status = status

        if status == Card.STATUS_NORMAL:        
            self.set_border_color(self.get_border_normal_color(), update)
        elif status == Card.STATUS_FOCUSED:
            self.set_border_color(self.get_border_focused_color(), update)
        elif status == Card.STATUS_DISABLED:
            self.set_border_color(self.get_border_disabled_color(), update)

    def refresh_color(self):
        self.update()

    def set_border_color(self, color, update):
        self.border_color = color
        if update:
            self.update()

    def get_border_normal_color(self):
        return self.border_normal_color
    
    def get_border_focused_color(self):
        return self.border_focused_color
    
    def get_border_disabled_color(self):
        return self.border_disabled_color
    
    def setBorderNormalColor(self, color):
        self.border_normal_color = color
        
    def setBorderFocusedColor(self, color):
        self.border_focused_color = color
        
    def setBorderDisabledColor(self, color):
        self.border_disabled_color = color
 
    def setBackgroundColor(self, color):
        self.panel.setBackgroundColor(color)

    def setBorderWidth(self, width, update=True):
        self.border_width = width
        self.self_layout.setContentsMargins(self.border_width,self.border_width,self.border_width,self.border_width)
        self.panel.setBorderRadius(self.border_radius - self.border_width, update)
        if update:
            self.update()

    def setBorderRadius(self, radius, update=True):
        self.border_radius = radius
        self.panel.setBorderRadius(self.border_radius - self.border_width, update)
        if update:
            self.update()
   
    def getPanel(self):
        return self.panel
 
    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush(self.border_color)

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end() 
 
    # --------------
    # MOUSE handling
    # --------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            
            # indicates that the mouse button was pressed
            self.already_mouse_pressed = True
            
            self.drag_start_position = event.pos()
            
        event.ignore()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.already_mouse_pressed = False
        event.ignore()       

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.already_mouse_pressed and self.local_index > 0:                
                self.onMouseClicked.emit(self.local_index)
        event.ignore()






 
 
 
 
 
 

    # ----------------------------------------
    #
    # Resize the width of the Card
    #
    # It is called when:
    # 1. CardHolder emits a resize event
    # 2. The Card is created and Placed
    #
    # ----------------------------------------
    def resized(self, width, height, local_index=None):
        """
        Input:
            width:    CardHolder width
            height:   CardHolder height
        """
        # The farther the card is the narrower it is
        if local_index==None:
            local_index = self.local_index
        standard_width = width - 2*self.card_holder.get_border_width() - 2*self.card_holder.get_x_offset_by_index_method(local_index)
        self.resize( standard_width, self.sizeHint().height() )

    # ---------------------------------------
    #
    # Place the Card into the given position
    #
    # 0. position means the card is in front
    # 1. position is behind the 0. position
    # and so on
    # ---------------------------------------
    def place(self, local_index, front_remove=False):
        
        # Need to resize and reposition the Card as 'The farther the card is the narrower it is'
        self.resized(self.card_holder.width(), self.card_holder.height(), local_index)
        x_coordinate = self.card_holder.get_border_width() + self.card_holder.get_x_offset_by_index_method(local_index)
        y_coordinate = self.card_holder.get_border_width() + self.get_y_coordinate(local_index)
        
        if front_remove:
            y_coordinate = y_coordinate - local_index * (math.exp(5 - 5 * local_index) / 2000) * self.height()
            
        self.move( x_coordinate, y_coordinate )
        
        self.show()
        
        return(QPoint(x_coordinate, y_coordinate), QPoint(self.width(),self.height()))

    # ----------------------------------
    #
    # Get Y coordinate by the local_index
    #
    # ----------------------------------
    def get_y_coordinate(self, local_index):
        max_card = min(self.card_holder.max_overlapped_cards, len(self.card_holder.card_data_list) - 1)
        reverse_index = max_card - min(local_index, max_card)  #0->most farther
        return self.card_holder.get_y_coordinate_by_reverse_index_method(reverse_index)

    
    













# =========================
#
# Collect Cards
#
# ========================= 
class CollectCardsThread(QtCore.QThread):
    cards_collected = pyqtSignal(MediaCollector)
    __instance = None
    __run = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance    

    @classmethod
#    def getInstance(cls, parent, collect_cards_method, paths=None):
    def getInstance(cls, parent, collect_cards_method):        
        if not cls.__run:
            inst = cls.__new__(cls)
#            cls.__init__(cls.__instance, parent, collect_cards_method, paths)
            cls.__init__(cls.__instance, parent, collect_cards_method)
            return inst
        else:
            return None

#    def __init__(self, parent, collect_cards_method, paths):
    def __init__(self, parent, collect_cards_method):
        QThread.__init__(self)
        
        self.parent = parent
        self.collect_cards_method = collect_cards_method
#        self.paths = paths
        
    def run(self):
        CollectCardsThread.__run = True
        ####
        #time.sleep(5)
        ####
        
#        card_list = self.collect_cards_method( self.paths)
        card_list = self.collect_cards_method()
        
        self.cards_collected.emit(card_list)
        CollectCardsThread.__run = False

    def __del__(self):
        self.exiting = True
        self.wait()
 
# =========================
#
# Rolling Animation
#
# ========================= 
class AnimateRolling(QThread):
    
    positionChanged = pyqtSignal(int)
    __instance = None
    __run = False
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance    
    
    @classmethod
    def getInstance(cls, loop, value, sleep=0.01):
        if not cls.__run:
            inst = cls.__new__(cls)
            cls.__init__(cls.__instance, loop, value, sleep) 
            return inst
        else:
            return None
    
    def __init__(self, loop, value, sleep):
        QThread.__init__(self)
        self.loop = loop
        self.value = value
        self.sleep = sleep
            
    def __del__(self):
        self.wait()
    
    def run(self): 
        
        # blocks to call again
        AnimateRolling.__run = True
        for i in range(abs(self.loop)):
            time.sleep(self.sleep)
            self.positionChanged.emit(copysign(1, self.loop) * self.value)
        
        # release blocking
        AnimateRolling.__run = False


# =========================
#
# CountDown Timer
#
# =========================
class CountDown(QThread):
    
    timeOver = pyqtSignal()
    __timer = 0    
    
    def __init__(self):
        QThread.__init__(self)
            
    def __del__(self):
        self.wait()
    
    def run(self): 

        # Ha meg mukodik
        if CountDown.__timer > 0:
            CountDown.__timer = 10

        # Ha mar nem mukodik
        else:
            CountDown.__timer = 10
        
            while CountDown.__timer > 0:
                time.sleep(0.04)
                CountDown.__timer = CountDown.__timer - 1
               
            self.timeOver.emit()
