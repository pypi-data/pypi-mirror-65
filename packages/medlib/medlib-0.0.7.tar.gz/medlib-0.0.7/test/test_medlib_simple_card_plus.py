from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout

import sys

from medlib.handle_property import config_ini 

from medlib.input_output import collectCards

from medlib.mediamodel.ini_titles import IniTitles
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_classification import IniClassification
from medlib.mediamodel.ini_general import IniGeneral

from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage
from medlib.mediamodel.media_appendix import MediaAppendix

from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage
from medlib.mediamodel.paths_appendix import PathsAppendix
from medlib.constants import PANEL_HEIGHT

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card test'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = PANEL_HEIGHT
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet('background: white')
                
        self.setLayout(self.layout)        
        
        #global dic
#        path_collector_A = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
#        titles_A = IniTitles("Eredeti cim", {"hu":"Magyar cim", "en":"English title", "se":" "})
#        control_A =IniControl("title", "video", "movie")
#        storylines_A = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})
#        general_A = IniGeneral()
#        general_A.setStoryline(storylines_A)    
#        collector_A = MediaCollector(path_collector_A, titles_A, control_A, general_A)

#        path_collector_B = PathsCollector('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg")
#        titles_B = IniTitles("B Eredeti cim", {"hu":"Magyar cim", "en":"D English title", "se":"B"})
#        control_B =IniControl("title", "video", "movie")
#        storylines_B = IniStorylines("A tortenet ...", {"en":"the story is\nreally interesting\nbut now I will not tell more details", "hu":"a történet \n tobb soros\n leiras a filmrol\n hogy lehessen tesztelnei milyen hosszu uzeneteket\n tud kezelni"})    
#        general_B = IniGeneral()
#        general_B.setStoryline(storylines_B)
#        general_B.setSeries("3")
#        general_B.setEpisode("2")
#        rating_B = IniClassification(None, True, True) 
#        collector_B = MediaCollector(path_collector_B, titles_B, control_B, general_B, rating_B)

#        path_collector_C = PathsCollector('D_folder_name', "/path/to/ini", "/path/to/jpeg")
#        titles_C =  IniTitles("C Eredeti cim", {"hu":"ö Magyar cim", "en":"A English title", "se":"C"})
#        control_C =IniControl("title", "video", "movie")
#        storylines_C = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})    
#        general_C = IniGeneral()
#        general_C.setStoryline(storylines_C)    
#        collector_C = MediaCollector(path_collector_C, titles_C, control_C, general_C)

#        path_collector_D = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
#        titles_D =  IniTitles("D Eredeti cim", {"hu":"á Magyar cim", "en":"B English title", "se":"D"})
#        control_D =IniControl("title", "video", "movie")
#        storylines_D = IniStorylines("A tortenet ...", {"en":"the story is ..", "hu":"a történet ..."})
#        general_D = IniGeneral()
#        general_D.setStoryline(storylines_D)    
#        collector_D = MediaCollector(path_collector_D, titles_D, control_D, general_D)

#        path_collector_BA = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
#        titles_BA =  IniTitles("A Konténer", {"hu":"A Konténer", "en":"A Container", "se":"D"})
#        control_BA =IniControl("title", "video", "movie")
#        storylines_BA = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
#        general_BA = IniGeneral()
#        general_BA.setStoryline(storylines_BA)    
#        collector_BA = MediaCollector(path_collector_BA, titles_BA, control_BA, general_BA)
#        collector_B.addMediaCollector(collector_BA)

#        path_collector_BB = PathsCollector('A_folder_name', "/path/to/ini", "/path/to/jpeg")
#        titles_BB =  IniTitles("K Konténer", {"hu":"K Konténer", "en":"K Container", "se":"D"})
#        control_BB = IniControl("title", "video", "movie")
#        storylines_BB = IniStorylines("A gyujtő ...", {"en":"the container is ..", "hu":"A Gyüjtő ..."})
#        collector_BB = MediaCollector(path_collector_BB, titles_BB, control_BB, None)
#        collector_B.addMediaCollector(collector_BB)

# ---

#        path_appendix_A = PathsAppendix('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/media/akoel/Movies/Films/Red.Planet.2000.720p.mkv")
#        path_appendix_B = PathsAppendix('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/media/akoel/Movies/Films/Red.Planet.2000.720p.mkv")
#        media_appendix_titles_A = IniTitles("Appendix orig cim A", {"hu":"Magyar Appendix cim A", "en":"English Appendix title A"})
#        media_appendix_titles_B = IniTitles("Appendix orig cim B", {"hu":"Magyar Appendix cim B", "en":"English Appendix title B"})
#        media_appendix_A = MediaAppendix(path_appendix_A, media_appendix_titles_A)
#        media_appendix_B = MediaAppendix(path_appendix_B, media_appendix_titles_B)

#        path_storage_BC = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
#        titles_BC = IniTitles("B Mozi cime", {"hu":"B Mozi cim", "en":"D Movie title", "hu":"Magyar cim"})
#        control_BC = IniControl("title", "video", "movie")
#        storylines_BC = IniStorylines("Ez a \ndefault tortenet", {"en": "English story\nSecond line\nThird line\nFourth line", "hu": "Magyar tortenet\nmasodik sor\nharmadik sor" })
#        general_BC = IniGeneral()
#        general_BC.setYear( "2012-2013")
#        general_BC.setDirectors(["Director 1", "Director 2", "Director 3", "Director 4", "Director 5", "Director 6", "Director 7", "Director 8"])
#        #general_BC.setMakers(["Maker 1", "Maker 2", "Maker 3"])
#        general_BC.setWriters(["Writ 1", "Writ 2"])
#        #general_BC.setAuthors(["Author 1", "Author 2"]) 
#        general_BC.setActors(["Actor 1", "Actor 2", "Actor 3", "Actor 4", "Actor 5", "Actor 6", "Actor 7", "Actor 8", "Actor 9", "Actor 10", "Actor 11", "Actor 12", "Actor 13", "Actor 14", "Actor 15", "Actor 16", "Actor 17", "Actor 18", "Actor 19", "Actor 20"])
#        #general_BC.setPerformers(["Performer 1", "Performer 2"])
#        #general_BC.setLecturers(["Lecturer 1", "Lecturer 2"])
#        #general_BC.setContributors(["Contributor 1", "Contributor 2"])
#        #general_BC.setVoices(["Voice 1", "Voice 2"])
#        general_BC.setLength( "2:12" )
#        general_BC.setSounds(["en", "hu", "sv"])
#        general_BC.setSubs(["en", "hu", "de", "it", "pl"])
#        general_BC.setGenres(["action", "crime"])
#        general_BC.setThemes(["money", "greed"])
#        general_BC.setStoryline(storylines_BC)
#        general_BC.setSeries("9")
#        general_BC.setEpisode("5")

#        rating_BC = IniClassification(10, True, True) 
#        storage_BC = MediaStorage(path_storage_BC, titles_BC, control_BC, general_BC, rating_BC)
#        storage_BC.addMediaAppendix(media_appendix_A)
#        storage_BC.addMediaAppendix(media_appendix_B)
#        collector_B.addMediaStorage(storage_BC)

# ---

#        path_storage_BD = PathsStorage('C_folder_name', "/path/to/ini", "/media/akoel/Movies/Final/01.Video/01.Movie/01.Films/01.Uncategorized/A.Profi-1981/image.jpeg", "/path/to/media")
#        titles_BD = IniTitles("C Default Mozi cime", {"en":"A Movie title", "se":"B"})
#        control_BD = IniControl("title", "video", "movie")
#        storylines_BD = IniStorylines("Ez a \ndefault: \nA Mozi \ntorte\nnet ...\n Ez egy tobb soros\nUzenet\n Mert po\nnt ezt a\nkarom \n tesztelni", {"en":"the movie's story is .." })
       
#        general_BD = IniGeneral()
#        general_BD.setYear( "2012-2013")
#        general_BD.setDirectors(["Dir 1", "Dir 2"])
#        #general_BD.setMakers(["Maker 1", "Maker 2", "Maker 3"])
#        general_BD.setWriters(["Writ 1", "Writ 2"])
#        #general_BD.setAuthors(["Author 1", "Author 2"])
#        general_BD.setActors(["Actor 1", "Actor 2", "Actor 3", "Actor 4", "Actor 5", "Actor 6", "Actor 7", "Actor 8", "Actor 9", "Actor 10", "Actor 11", "Actor 12", "Actor 13", "Actor 14", "Actor 15", "Actor 16", "Actor 17", "Actor 18", "Actor 19", "Actor 20"])
#        #general_BD.setPerformers(["Performer 1", "Performer 2"])
#        #general_BD.setLecturers(["Lecturer 1", "Lecturer 2"])
#        #general_BD.setContributors(["Contributor 1", "Contributor 2"])
#        #general_BD.setVoices(["Voice 1", "Voice 2"])
#        #general_BD.setLength( "2:12" )
#        #general_BD.setSounds(["en", "hu", "sv"])
#        general_BD.setSubs(["en", "hu", "de", "it", "pl"])
#        general_BD.setGenres(["action", "crime"])
#        general_BD.setThemes(["money", "greed"])
#        general_BD.setStoryline(storylines_BD)
#        rating_BD = IniClassification(10, True, True) 
#        storage_BD = MediaStorage(path_storage_BD, titles_BD, control_BD, general_BD, rating_BD)
#        collector_B.addMediaStorage(storage_BD)

# ---

#        collector_A.addMediaCollector(collector_D)
#        collector_A.addMediaCollector(collector_B)
#        collector_A.addMediaCollector(collector_C)
 
        # --- Manually created Storages --- #
#        widget = storage_BC.getWidget(1)
#        widget = collector_B.getWidget(1)
 
        # --- Generated by the filesystem --- #
        
        mainCollector = collectCards()
        
        mediaToShow = mainCollector
        
#        media_list = mainCollector.getMediaCollectorList()    #Video
#        media_list = media_list[0].getMediaCollectorList()    #Video
#        media_list = media_list[0].getMediaCollectorList()    #Movie
#        media_list = media_list[0].getMediaStorageList()
#        mediaToShow = media_list[0]
        self.scale = float(config_ini['scale'])
        self.setGeometry(self.left, self.top, self.width, self.height * self.scale)
        
        mediaToShow.setNextLevelListener(self.goesDeeper)
        self.widget = mediaToShow.getWidget(self.scale)
        
        print(mediaToShow.getJson())

        self.layout.addWidget(self.widget)
        self.show()
      
        
        
#        from medlib import handle_property 
#        ci = handle_property.get_config_ini()
#        par = ci.getMediaPlayerWithParameters('text', 'epub')
#        print(par)

    def goesDeeper(self, mediaCollector):        
        mcl = mediaCollector.getMediaCollectorList()
        msl = mediaCollector.getMediaStorageList()
        
        if mcl:
            self.layout.removeWidget(self.widget);
            mts = mcl[0]
            mts.setNextLevelListener(self.goesDeeper)
            self.widget = mts.getWidget(self.scale)
            self.layout.addWidget(self.widget)
        elif msl:
            self.layout.removeWidget(self.widget);
            msl = msl[0]
            self.widget = msl.getWidget(self.scale)
            self.layout.addWidget(self.widget)
            
        
        
#    collector_A.setLanguage("hu")

#Collector_A
#├── Collector_D
#├── Collector_C
#└── Collector_B
#            ├── Collector_BA
#            ├── Collector_BB
#            ├── Storage_BC
#            └── Storage_BD

#for mc in collector_A.getMediaContainerList():
#    print(mc.getTitle())
#    print(collector_A.getHierarchyTitle(""))

    #print(BB_content.getHtml())
#    print(storage_BC.getHtml())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()
    sys.exit(app.exec_())

