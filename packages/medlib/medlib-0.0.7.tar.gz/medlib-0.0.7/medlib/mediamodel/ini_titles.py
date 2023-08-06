import os

from medlib.handle_property import config_ini

from pkg_resources import resource_filename

from medlib.constants import PANEL_FONT_TYPE
from medlib.constants import PANEL_FONT_SIZE
from medlib.constants import TITLE_ICON_EXTENSION
from medlib.constants import TITLE_ICON_FOLDER
from medlib.constants import TITLE_ICON_HEIGHT
from medlib.constants import TITLE_ICON_PREFIX

from medlib.handle_property import _
from builtins import object

from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

class IniTitles(object):
    """
    This class represents the [titles] section in the card.ini file
    """
    
    def __init__(self, orig_title, title_list_by_language=None):
        """
        This is the constructor of the IniTitles class
        ___________________________________________
        input:
            orig_title                string        "The title in the original language"
            title_list_by_language    dictionary    {"hu":"Magyar cim", "en":"English title"}
        """
        self.orig_title = orig_title
        self.title_list_by_language = title_list_by_language if title_list_by_language else {}
    
    def __str__(self):
        return self.getTranslatedTitle()
        
    def getOrigTitle(self):
        return self.orig_title
        
    def getTranslatedTitle(self):
        """
        Returns back the raw title.
        If the title does not exists on the specific language, then the 'original' title will be returned
        _________________________________________________________________________________________________
        input:
        """
        title = self.title_list_by_language.get(config_ini['language'])
        if not title:
            title=self.getOrigTitle()
        return title
    
    def getOrderTitle(self, media):
        """
        Returns back the modified title with episodes and seasons if there is
        
        if no season no episode (simple movie)
            getTranslatedTitle()
        
        if episode + no season in the parent Collector (miniseries/saga)
            Parents_Collector.getTranslatedTitle() {episode} getTranslatedTitle()
            
        if episode + season in the parent Collector (series)
            Parent's_Parent's_Collector.getTranslatedTitle() (S{season}E{episode}) getTranslatedTitle()
        """
        formatted_title = self.getTranslatedTitle()
        parent_collector = media.getParentCollector()
        
        if parent_collector:
            episode = media.general.getEpisode()
            track = media.general.getTrack()

            parent_season = parent_collector.general.getSeason()
            parent_album = parent_collector.general.getAlbum().zfill(4) + parent_collector.getTranslatedTitle() if parent_collector.general.getAlbum() else None
            parent_parent_collector = parent_collector.getParentCollector()        
        
            from medlib.mediamodel.media_collector import MediaCollector
        
            # if media is Collector
            if issubclass(media.__class__, MediaCollector):
                season = media.general.getSeason()
                album = media.general.getAlbum()
        
                # Album
                if album:
                    formatted_title = album + "-" + formatted_title
                
                # Season (the season real title is omitted)
                elif season:      
                    formatted_title = _("title_season").format(season.zfill(4))          
        
            # The actual media is Storage - There is Episode but not in Season => Miniseries
            elif episode and not parent_season:
                
                parent_title = parent_collector.getTranslatedTitle()
                        
                formatted_title = parent_title + episode.zfill(4) + formatted_title                

            # The actual media is Storage and Episode in Season
            elif episode and parent_season:

                series_title = parent_parent_collector.getTranslatedTitle()
            
                formatted_title = series_title + parent_season.zfill(4) + episode.zfill(4) + formatted_title

            # The actual media is Storage - but not Album
            elif track and not parent_album:
                parent_title = parent_collector.getTranslatedTitle()
                        
                formatted_title = parent_title + track.zfill(4) + formatted_title                
            
            # The actual media is Storage and Track in Album
            elif track and parent_album:
                
                performer_title = parent_parent_collector.getTranslatedTitle()
                
                formatted_title = performer_title + parent_album + track.zfill(4) + formatted_title
                
        return formatted_title    
    
    def getFormattedTitle(self, media):
        """
        Returns back the modified title with episodes and seasons if there is
        
        if no season no episode (simple movie or collector)
            getTranslatedTitle()
        
        if episode + no season in the parent Collector (miniseries/saga)
            getTranslatedTitle()-{episode}.Part

        if track + no album in the parent Collector (music without album)
            getTranslatedTitle()
            
        if episode + season in the parent Collector (series)
            if keepHierarchy
                (S{season}E{episode}) getTranslatedTitle() -                 
            else
                Parent's_Parent's_Collector.getTranslatedTitle(): (S{season}E{episode}) getTranslatedTitle()

        if track + album in the parent Collector (music in album)
            if keepHierarchy
                ({track}. getTranslatedTitle() -                 
            else
                Parent's_Parent's_Collector.getTranslatedTitle(): {album(year)}-{album title} {track}. - getTranslatedTitle()
        """
        
        formatted_title = self.getTranslatedTitle()
        parent_collector = media.getParentCollector()
        
        if parent_collector:
            episode = media.general.getEpisode()
            track = media.general.getTrack()

            parent_season = parent_collector.general.getSeason()
            parent_album = parent_collector.general.getAlbum() + "-" + parent_collector.getTranslatedTitle() if parent_collector.general.getAlbum() else None
        
            from medlib.mediamodel.media_collector import MediaCollector
        
            # if media is Collector
            if issubclass(media.__class__, MediaCollector):
                season = media.general.getSeason()
                album = media.general.getAlbum()
        
                # Album
                if album:
                    formatted_title = album + "-" + formatted_title
                
                # Season
                elif season:                
                    formatted_title = _("title_season").format(season)
        
            # The actual media is Storage - There is Episode but not in Season => Miniseries
            elif episode and not parent_season:
                
                #TODO if MUSIC
                formatted_title = formatted_title + "-" + _("title_part").format(episode)

                parent_title = parent_collector.getTranslatedTitle()
                        
                # bulk list - The series title is not visible and 
                # the raw title of the episode is not the same as the row title of the Container's title - you have to attache it
                if config_ini["keep_hierarchy"] == "n" and parent_title != self.getTranslatedTitle():
                    formatted_title = parent_title + ": " + formatted_title

            # The actual media is Storage and Episode in Season
            elif episode and parent_season:
                formatted_title = formatted_title + " (S" + parent_season.zfill(2) + "E" + episode.zfill(2) + ")"

                parent_parent_collector = parent_collector.getParentCollector()
                series_title = parent_parent_collector.getTranslatedTitle()
            
                # bulk list - The series title is not visible - you have to attache it
                if config_ini["keep_hierarchy"] == "n":
                    formatted_title = series_title + ": " + formatted_title
            
            # The actual media is Storage - but not Album
            elif track and not parent_album:
                parent_title = parent_collector.getTranslatedTitle()

                formatted_title = formatted_title + " #" + track                
                        
                if config_ini["keep_hierarchy"] == "n":
                    formatted_title = parent_title + ": " + formatted_title #+ " " + track                
            
            # The actual media is Storage and Track in Album
            elif track and parent_album:
                
                formatted_title = track + ". " + formatted_title

                parent_parent_collector = parent_collector.getParentCollector()
                performer_title = parent_parent_collector.getTranslatedTitle()
                
                # bulk list - The Album title is not visible - you have to attache it
                if config_ini["keep_hierarchy"] == "n":
                    formatted_title = performer_title + ": (" + parent_album + ") " + formatted_title
                
        return formatted_title
    
    def getJson(self):
        json = {}
        json.update({} if self.orig_title is None or not self.orig_title else {"orig": self.orig_title})
        
        json.update(
            {key: value for key, value in self.title_list_by_language.items()} if self.title_list_by_language else {}
            )
       
        return json    
    
    def getWidget(self, media, scale):
        """  _________________________________________
            | Icon | Title                            |
            |______|__________________________________|
        """
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignLeft)
        
        # space between the three grids
        title_layout.setSpacing(10)
        
        # margin around the widget
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        widget = QWidget()
        widget.setLayout(title_layout)

        #
        # existing           showing
        # ____________________________________________________________________________
        #
        # icon.png           icon.png
        #
        # card.ini:
        #    iconkey + 
        #    media +
        #    categpry        media-{collector/storage}-{media}-{categry}-{iconkey}.png
        #
        # card.ini:
        #    iconkey         media-{collector/storage}-{iconkey}.png
        #
        # card.ini:
        #    media +
        #    categpry        media-{collector/storage}-{media}-{categry}.png
        #

        #
        # Icon
        #
        pixmap = None
        pathToFile = media.getPathOfIcon()
        if pathToFile:
            pixmap = QPixmap( pathToFile )
            
        if not pixmap:
        
            #media-(collector/storage)
            iconFileName = TITLE_ICON_PREFIX + "-" + media.getFolderType()
        
            # media-(collector/storage)-{iconKey}
            if media.control.getIconKey():
                iconFileName += "-" + media.control.getIconKey()  
            # media-(collector/storage)-{media}        
            elif media.control.getMedia() and not media.control.getCategory():
                iconFileName += "-" + media.control.getMedia()
            # media-(collector/storage)-{media}-{category}                
            elif media.control.getMedia() and media.control.getCategory():
                iconFileName += ( "-" + media.control.getMedia() if media.control.getMedia() else "" ) + ( "-" + media.control.getCategory() if media.control.getCategory() else "" )
        
            iconFileName += "." + TITLE_ICON_EXTENSION               
            pathToFile = resource_filename(__name__, os.path.join(TITLE_ICON_FOLDER, iconFileName))                   
            pixmap = QPixmap( pathToFile )

        if pixmap.isNull():            
            smaller_pixmap = QPixmap(TITLE_ICON_HEIGHT * scale, TITLE_ICON_HEIGHT * scale)
            smaller_pixmap.fill(QColor(media.getBackgroundColor()))
        else:
            
            if pixmap.width() >= pixmap.height():
                smaller_pixmap = pixmap.scaledToWidth(TITLE_ICON_HEIGHT * scale)
            else:
                smaller_pixmap = pixmap.scaledToHeight(TITLE_ICON_HEIGHT * scale)
   
        iconWidget = QLabel()
        iconWidget.setPixmap(smaller_pixmap)

        title_layout.addWidget(iconWidget)

        #
        # Title
        #
        titleWidget = QLabel(self.getFormattedTitle(media))
        titleWidget.setFont(QFont(PANEL_FONT_TYPE, PANEL_FONT_SIZE * scale * 1.8, weight=QFont.Bold))

        title_layout.addWidget(titleWidget)
        return widget
    
    
    
    
