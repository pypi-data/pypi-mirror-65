import sys

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QColor

from PyQt5.QtCore import Qt

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card selector'
        self.left = 10
        self.top = 10
        self.width = 420
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
            self.collectCards
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
        
        self.card_holder.setFocus()

        self.show()

    def change_spinner(self):
        self.card_holder.set_spinner(self.spinner_file_name)

        
    def fill_up(self):
        self.card_holder.startCardCollection([])
        
    def collectCards(self, paths):
        """
        """
        cdl = []        
        cdl.append("Elso")
        cdl.append("Masodik")
        cdl.append("Harmadik")
        cdl.append("Negyedik")
        cdl.append("Otodik")
        cdl.append("Hatodik")
        cdl.append("Hetedik")
        cdl.append("Nyolcadik")
        cdl.append("Kilencedik")
        cdl.append("Tizedik")        
        return cdl
        
    def getNewCard(self, card_data, local_index, index):
        """
        
        """
        card = Card(self.card_holder, card_data, local_index, index)
        
        card.setBorderFocusedColor(QColor(Qt.blue))
        #card.setBackgroundColor(QColor(Qt.white))
        #card.set_border_radius( 15 )
        #card.setBorderWidth(18)
 
 
        panel = card.getPanel()
        layout = panel.getLayout()
        
        # Construct the Card
#        label=QLabel(card_data + "\n\n\n\n\n\n\n\n\n\nHello")
#        layout.addWidget(label)
        #layout.addWidget(QPushButton("hello"))

        myPanel = MyPanel(card)
        layout.addWidget(myPanel)
        
        return card
    
    def get_y_coordinate_by_reverse_index(self, reverse_index):
        """
        
        """        
        return reverse_index * reverse_index * 16
    
    def get_x_offset_by_index(self, index):
        """
        """
        return index * 4

class MyPanel(QWidget):
    
    def __init__(self, card):
        QWidget.__init__(self, card)
        
        self.card = card
        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: red' )
        
        self.self_layout = QVBoxLayout()
        self.self_layout.setSpacing(1)
        self.setLayout(self.self_layout)
                
        label=QLabel(card.card_data + "\n\n\n\n\n\n\n\n\n\nHello")
        self.self_layout.addWidget(label)
        
        
    def mousePressEvent(self, event):
        #if event.button() == Qt.LeftButton:
        #    print(self.card.card_data, self.card.local_index, self.card.status)
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()
        
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()
    sys.exit(app.exec_())
