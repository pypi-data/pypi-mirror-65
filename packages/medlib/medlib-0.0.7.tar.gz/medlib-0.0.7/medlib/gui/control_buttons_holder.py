import sys
import os
import signal
import importlib
import psutil

#from threading import Thread
from pkg_resources import resource_string, resource_filename
from functools import cmp_to_key
import locale

from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import QWidget, QComboBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton

from medlib.constants import ON
from medlib.constants import OFF
from medlib.constants import CONTROL_IMG_FOLDER
from medlib.constants import CONTROL_IMG_PLAY_BUTTON
from medlib.constants import CONTROL_IMG_STOP_BUTTON
from medlib.constants import CONTROL_IMG_BACK_BUTTON
from medlib.constants import CONTROL_IMG_HIERARCHY_BUTTON
from medlib.constants import CONTROL_IMG_EXTENTION
from medlib.constants import CONTROL_IMG_SIZE
from medlib.gui.player import PlayerThread

# ================================
#
# Control Buttons Holder
#
# Contains:
#           Back Button
#           Play Sequentially
#           Fast Search Button
#           Advanced Search Button
#           Hierarchy on/off
# ================================
class ControlButtonsHolder(QWidget):
    """
        +---- Control ButtonsHolder (QWidget) -----------------+
        | +---- self_layout (QHBoxLayout) -------------------+ |
        | | +----+       +----++--------------+       +----+ | |
        | | |Back|       |Play||     List     |       |Hier| | |
        | | +----+       +----++--------------+       +----+ | |
        | +--------------------------------------------------+ |
        +------------------------------------------------------+
    
    """
    def __init__(self, control_panel):
        super().__init__()
       
        self.control_panel = control_panel
        
        self_layout = QHBoxLayout(self)
        self.setLayout(self_layout)
        
        self_layout.setContentsMargins(0, 0, 0, 0)
        self_layout.setSpacing(5)
        
    
        # -------------
        #
        # Back Button
        #
        # -------------     
        self.back_button_method = None
        
        back_button = QPushButton()
        back_button.setFocusPolicy(Qt.NoFocus)
        back_button.clicked.connect(self.back_button_on_click)
        
        back_icon = QIcon()
        back_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_BACK_BUTTON + "-" + ON + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Active)
        back_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_BACK_BUTTON + "-" + OFF + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Disabled)
        back_button.setIcon(back_icon )
        back_button.setIconSize(QSize(CONTROL_IMG_SIZE, CONTROL_IMG_SIZE))
        back_button.setCursor(QCursor(Qt.PointingHandCursor))
        back_button.setStyleSheet("background:transparent; border:none") 

        # Back button on the left
        self_layout.addWidget( back_button )

        self_layout.addStretch(1) 
        
        
        # ================================================
        # ================================================        
        
        # -------------------
        #
        # Play Sequentially Button
        #
        # -------------------

        self.play_continously_button = QPushButton()
        self.play_continously_button.setFocusPolicy(Qt.NoFocus)
        self.play_continously_button.clicked.connect(self.play_continously_button_on_click)
        
        play_continously_icon = QIcon()
        play_continously_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_PLAY_BUTTON + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.On)
#        play_continously_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_PLAY_BUTTON + "-" + ON + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.On)
        self.play_continously_button.setIcon( play_continously_icon )
        self.play_continously_button.setIconSize(QSize(25,25))
        self.play_continously_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.play_continously_button.setStyleSheet("background:transparent; border:none") 
        
        # Play button on the middle
        self_layout.addWidget( self.play_continously_button )

        # -------------------
        #
        # Stop Button
        #
        # -------------------
        self.stop_continously_button = QPushButton()
        self.stop_continously_button.setFocusPolicy(Qt.NoFocus)
        self.stop_continously_button.clicked.connect(self.stop_continously_button_on_click)
        
        stop_continously_icon = QIcon()
        stop_continously_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_STOP_BUTTON + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.On)
#        stop_continously_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_STOP_BUTTON + "-" + OFF + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.Off)
        self.stop_continously_button.setIcon( stop_continously_icon )
        self.stop_continously_button.setIconSize(QSize(25,25))
        self.stop_continously_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.stop_continously_button.setStyleSheet("background:transparent; border:none")

        # Stop button on the middle
        self_layout.addWidget( self.stop_continously_button )
        
        # ----------------------------------
        #
        # Playing Continously list drop-down
        #
        # ----------------------------------

        self.dropdown_play_continously = QComboBox(self)
        self.dropdown_play_continously.setFocusPolicy(Qt.NoFocus)
        self.dropdown_play_continously.setEditable(False)
        
        # listener for selection changed
        #self.dropdown_play_continously.currentIndexChanged.connect(self.play_continously_selection_changed_listener)
       
        style_box = '''
           QComboBox { 
               max-width: 500px; min-width: 300px; border: 1px solid gray; border-radius: 5px;
           }
        '''
        style_drop_down ='''
           QComboBox QAbstractItemView::item { 
               color: red;
               max-height: 15px;
           }
        '''            
     
        self.dropdown_play_continously.setStyleSheet(style_box)
        #self.dropdown_play_continously.addItem("")
        self_layout.addWidget( self.dropdown_play_continously )
        
        self.disablePlayStopContinously()
               
        self_layout.addStretch(1) 
        
        # ================================================
        # ================================================        
                
        # ----------------
        #
        # Hierarchy Button
        #
        # ----------------                  
        self.hierarchy_button_method = None
        
        self.hierarchy_button = QPushButton()
        self.hierarchy_button.setFocusPolicy(Qt.NoFocus)
        self.hierarchy_button.setCheckable(True)
        self.hierarchy_button.toggled.connect(self.hierarchy_button_on_toggle)
        
        hierarchy_icon = QIcon()
        hierarchy_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_HIERARCHY_BUTTON + "-" + ON + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.On)
        hierarchy_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join(CONTROL_IMG_FOLDER, CONTROL_IMG_HIERARCHY_BUTTON + "-" + OFF + "." + CONTROL_IMG_EXTENTION)) ), QIcon.Normal, QIcon.Off)
        self.hierarchy_button.setIcon(hierarchy_icon )
        self.hierarchy_button.setIconSize(QSize(CONTROL_IMG_SIZE, CONTROL_IMG_SIZE))
        self.hierarchy_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.hierarchy_button.setStyleSheet("background:transparent; border:none") 

        # Hierarchy button on the right
        self_layout.addWidget(self.hierarchy_button)

#        # ================================================
#        # ================================================

        # Initiate the PlayerThread
        ins = PlayerThread.getInstance()
        ins.startNextPlaying.connect(self.start_next_playing_emmitted)
        ins.stopPlayingAll.connect(self.stop_playing_all_emmitted)





        # -------------------
        #
        # Fast Search Button
        #
        # -------------------
#        self.fast_search_button = QPushButton()
#        self.fast_search_button.setFocusPolicy(Qt.NoFocus)
#        self.fast_search_button.setCheckable(True)
#        self.fast_search_button.setAutoExclusive(False)
#        self.fast_search_button.toggled.connect(self.fast_search_button_on_click)
#        
#        fast_search_icon = QIcon()
#        fast_search_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join("img", IMG_FAST_SEARCH_BUTTON_ON)) ), QIcon.Normal, QIcon.On)
#        fast_search_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join("img", IMG_FAST_SEARCH_BUTTON_OFF)) ), QIcon.Normal, QIcon.Off)
#        self.fast_search_button.setIcon( fast_search_icon )
#        self.fast_search_button.setIconSize(QSize(25,25))
#        self.fast_search_button.setCursor(QCursor(Qt.PointingHandCursor))
#        self.fast_search_button.setStyleSheet("background:transparent; border:none") 
#        self_layout.addWidget( self.fast_search_button )
#        
#        # -------------------
#        #
#        # Advanced Search Button
#        #
#        # -------------------
#        self.advanced_search_button = QPushButton()
#        self.advanced_search_button.setFocusPolicy(Qt.NoFocus)
#        self.advanced_search_button.setCheckable(True)
#        self.advanced_search_button.setAutoExclusive(False)
#        self.advanced_search_button.toggled.connect(self.advanced_search_button_on_click)
#        
#        advanced_search_icon = QIcon()
#        advanced_search_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join("img", IMG_ADVANCED_SEARCH_BUTTON_ON)) ), QIcon.Normal, QIcon.On)
#        advanced_search_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join("img", IMG_ADVANCED_SEARCH_BUTTON_OFF)) ), QIcon.Normal, QIcon.Off)
#        self.advanced_search_button.setIcon( advanced_search_icon )
#        self.advanced_search_button.setIconSize(QSize(25,25))
#        self.advanced_search_button.setCursor(QCursor(Qt.PointingHandCursor))
#        self.advanced_search_button.setStyleSheet("background:transparent; border:none") 
#        self_layout.addWidget( self.advanced_search_button )
#        
#        # ================================================
#        # ================================================
#                        
#        # -------------------
#        #
#        # Config Button
#        #
#        # -------------------
#        self.config_button = QPushButton()
#        self.config_button.setFocusPolicy(Qt.NoFocus)
#        self.config_button.setCheckable(False)
#        self.config_button.clicked.connect(self.config_button_on_click)
#        
#        config_icon = QIcon()
#        config_icon.addPixmap(QPixmap( resource_filename(__name__,os.path.join("img", IMG_CONFIG_BUTTON)) ), QIcon.Normal, QIcon.On)
#        self.config_button.setIcon( config_icon )
#        self.config_button.setIconSize(QSize(25,25))
#        self.config_button.setCursor(QCursor(Qt.PointingHandCursor))
#        self.config_button.setStyleSheet("background:transparent; border:none") 
#        self_layout.addWidget( self.config_button )   
#        
#        self.enableSearchIcons(False)
#        self.disablePlayStopContinously()
#        
#    # ======================================================
#    
    def clear_play_continously_elements(self):
        self.dropdown_play_continously.clear()
        
    def add_play_continously_separator(self):
        self.dropdown_play_continously.insertSeparator(self.dropdown_play_continously.__len__())        
        
    def add_play_continously_element(self, title, media_path, media_type):
        self.dropdown_play_continously.addItem(title, (media_path, media_type))        
        
    def get_play_continously_selected_path(self):
        return self.dropdown_play_continously.itemData( self.dropdown_play_continously.currentIndex() )

    def get_play_continously_media_path_by_index(self, index):
        return self.dropdown_play_continously.itemData( index )[0]

    def get_play_continously_media_type_by_index(self, index):
        return self.dropdown_play_continously.itemData( index )[1]

    def get_play_continously_data_list(self):
        items = []
        for index in range(self.dropdown_play_continously.count()):
            items.append( (self.dropdown_play_continously.itemText(index),) + self.dropdown_play_continously.itemData(index) )
        return items

    def get_play_continously_selected_title(self):
        return self.dropdown_play_continously.itemText( self.dropdown_play_continously.currentIndex() )    
    
    def get_play_continously_title_by_index(self, index):
        return self.dropdown_play_continously.itemText( index )
    
    def get_play_continously_selected_index(self):
        return self.dropdown_play_continously.currentIndex()

    def get_play_continously_last_index(self):
        return self.dropdown_play_continously.count() - 1
    
    def select_play_continously_element_by_index(self, index):
        self.dropdown_play_continously.setCurrentIndex(index)
        
    # ======================================================
            
    def disablePlayStopContinously(self):
        self.play_continously_button.setEnabled(False)
        self.stop_continously_button.setEnabled(False)
        self.dropdown_play_continously.setEnabled(False)
        
    def enablePlayContinously(self, enabled):
        self.play_continously_button.setEnabled(enabled)
        self.stop_continously_button.setEnabled(not enabled)
        self.dropdown_play_continously.setEnabled(enabled)
    
    # =====================================================


    # =================================================
    #
    # Image/Appendix CLICK button
    #
    # =================================================
    def image_or_appendix_on_click(self, list_to_play):
        
#        self.control_panel.gui.refreshPlayContinouslyListBeforeStartPlaying(index)
#        print("Disabled Play, Enabled Stop and selected Index:", index)
        
        PlayerThread.play(list_to_play)       
        

    # =================================================
    #
    # Play Contionusly STOP button
    #
    # =================================================
    def stop_continously_button_on_click(self):
        """
        Stops the continous play
        This method is called when the Play continously Stop button is pushed
        
        It stops the actually playing media, 
        It breaks Play Continouisly list

        in the PlayerThread.stop() method it sets the __run=False and emit the stopPlaying event
        the stopPlaying is connected to the stop_playing_listener() method
        """
        
        PlayerThread.stop()

    # =========================================
    #
    # Play Continously PLAY button
    #
    # =========================================
    def play_continously_button_on_click(self):
        """
        Select the list from the actual media till the end and starts to play it        
        This method is called when the Play Continously Play button is pushed
            
        """
        start_index = self.get_play_continously_selected_index()
        last_index = self.get_play_continously_last_index()
        list_to_play = []
        for actual_index in range(start_index, last_index + 1):
            list_to_play.append({
                'media-index': actual_index,
                'media-path': self.get_play_continously_media_path_by_index(actual_index), 
                'media-type': self.get_play_continously_media_type_by_index(actual_index)})
        
        PlayerThread.play(list_to_play)
#        ins.startNextPlaying.connect(self.select_in_playlist_by_index_listener)
#        ins.stopPlaying.connect(self.stop_playing_listener)

#
#        # Start to play the media collection
#        inst = PlayContinouslyThread.play(self)
#       
#        # connect the "selected" event to a method which will select the media in the drop-down list
#        inst.selected.connect(self.select_play_continously_element_by_index)
#


    # ---------------------------------------------
    #
    # startNextPlaying Emmitted in PlayThread
    #
    # ---------------------------------------------
    def start_next_playing_emmitted(self, index):
        """
        Disable the Play button, Enable the Stop button and select the next value
        in the Play list according to the index. 
        This method is called from the PlayerThread object when the next media is started
        """
        self.select_play_continously_element_by_index(index)  
        self.control_panel.gui.refreshPlayContinouslyListBeforeStartPlaying(index)


    # ---------------------------------------------
    #
    # startNextPlaying Emmitted in PlayThread
    #
    # ---------------------------------------------
    def stop_playing_all_emmitted(self):
        """
        This method is called from the PlayedThread object when the Stop button is pushed

        Enables the the Play button and disable the Stop button
        Refreshes the Play Continously List
        """
        #self.enablePlayContinously(True)
        
        self.control_panel.gui.refreshPlayContinouslyListAfterStopPlaying()        





        
        
    def play_continously_selection_changed_listener(self, index):
        """
        Focus the card according to the selected value in the Play list
        This method is called when the selected element changed in the Play list
        """
        if index >= 0:
            self.control_panel.gui.card_holder.focus_index(index)
        
#    # --------------------------
#    #
#    # Fast Search Button Clicked
#    #
#    # --------------------------
#    def fast_search_button_on_click(self, checked):
#        if checked:
#            self.advanced_search_button.setChecked(False)
#        # hide/show fast filter
#        self.control_panel.fast_filter_holder.setHidden(not checked)
#        # filter the list
#        self.control_panel.fast_filter_on_change()
#    
#    # ------------------------------
#    #
#    # Advanced Search Button Clicked
#    #
#    # ------------------------------
#    def advanced_search_button_on_click(self, checked):
#        if checked:
#            self.fast_search_button.setChecked(False)
#        # hide/show advanced filter
#        self.control_panel.advanced_filter_holder.setHidden(not checked)
#        # filter the list
#        self.control_panel.advanced_filter_filter_on_click()
        
        
    def setBackButtonMethod(self, back_button_method):
        self.back_button_method = back_button_method
        
    def setHierarchyButtonMethod(self, hierarchy_button_method):
        self.hierarchy_button_method = hierarchy_button_method
    
    def setHierarchy(self, show):
        self.hierarchy_button.setChecked(show)
        
    # -------------------
    #
    # Back Button Clicked
    #
    # -------------------
    def back_button_on_click(self):
        if self.back_button_method:            
            self.back_button_method()
            
            
    # -------------------
    #
    # Back Button Clicked
    #
    # -------------------
    def hierarchy_button_on_toggle(self, checked):
        if self.hierarchy_button_method:
            self.hierarchy_button_method(checked)
            

    # -----------------------
    #
    # Config Button Clicked
    #
    # -----------------------
#    def config_button_on_click(self):
#
#        config_ini_function = get_config_ini()        
#        orig_mp = config_ini_function.get_media_path()
#        orig_sdt = config_ini_function.get_show_original_title() 
#        orig_l = config_ini_function.get_language()
#        orig_vp = config_ini_function.get_media_player_video()
#        orig_vpp = config_ini_function.get_media_player_video_param()
#        orig_ap = config_ini_function.get_media_player_audio()
#        orig_app = config_ini_function.get_media_player_audio_param()
#
#        dialog = ConfigurationDialog()
#
#        # if OK was clicked
#        if dialog.exec_() == QDialog.Accepted:        
#
#            # get the values from the DIALOG
#            l = dialog.get_language()
#            sdt = dialog.get_show_original_title()            
#            mp = dialog.get_media_path()
#            vp = dialog.get_media_player_video()
#            vpp = dialog.get_media_player_video_param()
#            ap = dialog.get_media_player_audio()
#            app = dialog.get_media_player_audio_param()
#
#            # Update the config.ini file            
#            config_ini_function = get_config_ini()
#            need_to_recollect = False
#            if mp != orig_mp:
#                need_to_recollect = True
#                config_ini_function.set_media_path(mp)
#            if l != orig_l:
#                need_to_recollect = True
#                config_ini_function.set_language(l)
#            if sdt != orig_sdt:
#                need_to_recollect = True
#                config_ini_function.set_show_original_title(sdt)
#            if vp != orig_vp:
#                config_ini_function.set_media_player_video(vp)
#            if vpp != orig_vpp:
#                config_ini_function.set_media_player_video_param(vpp)
#            if ap != orig_ap:
#                config_ini_function.set_media_player_audio(ap)
#            if app != orig_app:
#                config_ini_function.set_media_player_audio_param(app)
#
#
##!!!!!!!!!!!!
#            # Re-read the config.ini file
#            re_read_config_ini()
#
#            # Re-import card_holder_pane
#            mod = importlib.import_module("medlib.gui.card_panel")
#            importlib.reload(mod)
##!!!!!!!!!!!!
#
#            if need_to_recollect:
#
#                # remove history
#                for card_holder in self.control_panel.gui.card_holder_history:
#                    card_holder.setHidden(True)
#                    self.control_panel.gui.card_holder_panel_layout.removeWidget(card_holder)
#                    #self.gui.scroll_layout.removeWidget(card_holder)
#                self.control_panel.gui.card_holder_history.clear()
#                
#                # Remove recent CardHolder as well
#                self.control_panel.gui.actual_card_holder.setHidden(True)
#                self.control_panel.gui.card_holder_panel_layout.removeWidget(self.control_panel.gui.actual_card_holder)
#                self.control_panel.gui.actual_card_holder = None
#            
#                # reload the cards
#                self.control_panel.gui.startCardHolder()
#            
#                # refresh the Control Panel
#                self.control_panel.refresh_label()
#            
#        dialog.deleteLater()
        



#class PlayContinouslyThread(QThread):
#    
#    selected = pyqtSignal(int)
#    
#    __instance = None
#    __run = False
#    __wait_for_stop = False
#    
#    @classmethod
#    def play(cls, parent):
#        
#        if cls.__instance is None:
#            cls.__new__(cls)
#        
#        cls.__init__(cls.__instance, parent)
#            
#        if not cls.__run:
#            cls.__instance.start()
#            
#        return cls.__instance
#
#    @classmethod
#    def stop(cls):
#        PlayContinouslyThread.__wait_for_stop = True
#        
#    def __new__(cls):
#        if cls.__instance is None:
#            cls.__instance = super().__new__(cls)
#        return cls.__instance    
#
#    def __init__(self, parent):
#        QThread.__init__(self)        
#        self.parent = parent
#         
#    def run(self):
#
#        PlayContinouslyThread.__run = True
#        PlayContinouslyThread.__wait_for_stop = False
#        self.parent.enablePlayContinously(False)
#
#        start_index = self.parent.get_play_continously_selected_index()
#        end_index = self.parent.get_play_continously_last_index()
#
#        stop_all = False
#        for index in range(start_index, end_index + 1):
#            
#            pid = None
#            media = self.parent.get_play_continously_path_by_index(index)
#            if media is not None:
#            
#                # play the next media
#                pid = play_media(media)               
#            
#                # emit an media selection event
#                self.selected.emit(index)                
#
#            # checking if it stopped
#            while pid is not None:
#
#                # if the Play Continously is stopped
#                if PlayContinouslyThread.__wait_for_stop:
#                    
#                    # then kill the process
#                    stop_all = True
#                    os.kill(pid, signal.SIGKILL)
#                    break
#                    
#                    # --- Id does not work. root needed ---
#                    #p = psutil.Process(pid)
#                    #p.terminate()
#
#                # I suppose the pid does not exist anymore
#                still_exist_pid = False
#                
#                # I check the running processes
#                for p in psutil.process_iter():
#                    if p.pid == pid:
#                        still_exist_pid = True
#                        break
#                    
#                if not still_exist_pid:
#                    break
#                
#                # at this point the pid is still exists so the media is playing
#                # I wait a second
#                QThread.sleep(1)
#
#            # If the Play Continously is stopped
#            if stop_all:
#                
#                # Break the loop on the files
#                break
#
#        # Indicates that the Thread is ready to start again
#        self.parent.enablePlayContinously(True)
#        PlayContinouslyThread.__run = False
#
#    def __del__(self):
#        self.exiting = True
#        self.wait()
