import sys

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card

from medlib.input_output import collectCards
from PyQt5 import QtCore
from cardholder.card_data_interface import CardDataInterface
import types

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card selector'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 300
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet('background: white')
 
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setSpacing(0)
        self.setLayout(self.scroll_layout)
        
        self.card_holder = CardHolder(            
            self, 
            self.getNewCard,
            self.collectCards,
            None,               #self.selectCard,
            None,               #self.goesHigher
        )
        
        self.card_holder.setBackgroundColor(QColor(Qt.yellow))
        self.card_holder.setBorderWidth(10)
        self.card_holder.set_max_overlapped_cards(5)
        self.card_holder.set_y_coordinate_by_reverse_index_method(self.get_y_coordinate_by_reverse_index)
        self.card_holder.set_x_offset_by_index_method(self.get_x_offset_by_index)
        self.scroll_layout.addWidget(self.card_holder)
        
        next_button = QPushButton("next",self)
        next_button.clicked.connect(self.card_holder.button_animated_move_to_next)        
        next_button.setFocusPolicy(Qt.NoFocus)
        
        previous_button = QPushButton("prev",self)
        previous_button.clicked.connect(self.card_holder.button_animated_move_to_previous)
        previous_button.setFocusPolicy(Qt.NoFocus)

        fill_up_button = QPushButton("fill up",self)
        fill_up_button.clicked.connect(self.fill_up)
        fill_up_button.setFocusPolicy(Qt.NoFocus)

        self.scroll_layout.addStretch(1)
        self.scroll_layout.addWidget(previous_button)
        self.scroll_layout.addWidget(next_button)
        self.scroll_layout.addWidget(fill_up_button)
        
        self.setFocusPolicy(Qt.NoFocus)

        self.show()

    def change_spinner(self):
        self.card_holder.set_spinner(self.spinner_file_name)
        
    def fill_up(self):
        self.card_holder.startCardCollection([])

    #
    # Input parameter for CardHolder
    #
    def collectCards(self, paths):
        collector = collectCards()
        collector.setNextLevelListener(self.goesDeeper)
     
        cdl = collector.getMediaCollectorList()
        
        return cdl

 
    
    #
    # Input parameter for CardHolder
    #
    def getNewCard(self, card_data, local_index, index):
        """        
        """
        card = Card(self.card_holder, card_data, local_index, index)
        
        card.setBorderFocusedColor(QColor(Qt.blue))
        #card.setBackgroundColor(QColor(Qt.white))
        #card.set_border_radius( 15 )
        #card.setBorderWidth(18)
        card.setMaximumHeight(300)
        card.setMinimumHeight(300)
 
        panel = card.getPanel()
        layout = panel.getLayout()
        
        myPanel = card.card_data.getWidget(1)

        layout.addWidget(myPanel)
        
        return card
        
    #
    # Input parameter for MediaCollector
    #
    def goesDeeper(self, mediaCollector):        
        mcl = mediaCollector.getMediaCollectorList()
        msl = mediaCollector.getMediaStorageList()
        sum_list = mcl + msl
        if sum_list:
            self.card_holder.refresh(sum_list)
  
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        """        
        """        
#        return reverse_index * reverse_index * 16
        return reverse_index * 50
    
    def get_x_offset_by_index(self, index):
        """
        """
        return index * 4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()

    sys.exit(app.exec_())
