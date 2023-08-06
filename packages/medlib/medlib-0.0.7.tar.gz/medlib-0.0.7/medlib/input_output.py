import os
import re
import json
import configparser

from medlib.constants import PATH_FOLDER_CONFIG

from medlib.mediamodel import ini_storylines
from medlib.mediamodel.media_collector import MediaCollector
from medlib.mediamodel.media_storage import MediaStorage
from medlib.mediamodel.media_appendix import MediaAppendix
from medlib.mediamodel.paths_collector import PathsCollector
from medlib.mediamodel.paths_storage import PathsStorage
from medlib.mediamodel.paths_appendix import PathsAppendix
from medlib.mediamodel.ini_titles import IniTitles 
from medlib.mediamodel.ini_control import IniControl
from medlib.mediamodel.ini_storylines import IniStorylines
from medlib.mediamodel.ini_general import IniGeneral
from medlib.mediamodel.ini_classification import IniClassification

from medlib.handle_property import config_ini 
from medlib.handle_property import Property 

from medlib.card_ini import JSON_KEY_CLASSIFICATION_NEW
from medlib.card_ini import JSON_KEY_CLASSIFICATION_FAVORITE
from medlib.card_ini import JSON_KEY_CLASSIFICATION_TAG
from medlib.card_ini import JSON_KEY_CLASSIFICATION_RATE

from medlib.card_ini import KEY_CLASSIFICATION_TAG
from medlib.card_ini import KEY_CLASSIFICATION_RATE
from medlib.card_ini import KEY_CLASSIFICATION_FAVORITE
from medlib.card_ini import KEY_CLASSIFICATION_NEW

from medlib.card_ini import CardIni

from medlib.card_ini import KEY_GENERAL_LENGTH
from medlib.card_ini import KEY_GENERAL_YEAR
from medlib.card_ini import KEY_GENERAL_DIRECTOR
from medlib.card_ini import KEY_GENERAL_MAKER
from medlib.card_ini import KEY_GENERAL_WRITER
from medlib.card_ini import KEY_GENERAL_AUTHOR
from medlib.card_ini import KEY_GENERAL_ACTOR
from medlib.card_ini import KEY_GENERAL_PERFORMER
from medlib.card_ini import KEY_GENERAL_LECTURER
from medlib.card_ini import KEY_GENERAL_CONTRIBUTOR
from medlib.card_ini import KEY_GENERAL_VOICE
from medlib.card_ini import KEY_GENERAL_GENRE
from medlib.card_ini import KEY_GENERAL_THEME
from medlib.card_ini import KEY_GENERAL_RECIPETYPE
from medlib.card_ini import KEY_GENERAL_SUB
from medlib.card_ini import KEY_GENERAL_SOUND
from medlib.card_ini import KEY_GENERAL_COUNTRY
from medlib.card_ini import KEY_GENERAL_SEASON
from medlib.card_ini import KEY_GENERAL_EPISODE
from medlib.card_ini import KEY_GENERAL_TRACK
from medlib.card_ini import KEY_GENERAL_ALBUM

from medlib.card_ini import JSON_KEY_GENERAL_YEAR
from medlib.card_ini import JSON_KEY_GENERAL_LENGTH
from medlib.card_ini import JSON_KEY_GENERAL_DIRECTOR
from medlib.card_ini import JSON_KEY_GENERAL_MAKER
from medlib.card_ini import JSON_KEY_GENERAL_AUTHOR
from medlib.card_ini import JSON_KEY_GENERAL_ACTOR
from medlib.card_ini import JSON_KEY_GENERAL_PERFORMER
from medlib.card_ini import JSON_KEY_GENERAL_LECTURER
from medlib.card_ini import JSON_KEY_GENERAL_CONTRIBUTOR
from medlib.card_ini import JSON_KEY_GENERAL_VOICE
from medlib.card_ini import JSON_KEY_GENERAL_GENRE
from medlib.card_ini import JSON_KEY_GENERAL_THEME
from medlib.card_ini import JSON_KEY_GENERAL_SUB
from medlib.card_ini import JSON_KEY_GENERAL_SOUND
from medlib.card_ini import JSON_KEY_GENERAL_COUNTRY
from medlib.card_ini import JSON_KEY_GENERAL_SEASON
from medlib.card_ini import JSON_KEY_GENERAL_EPISODE
from medlib.card_ini import JSON_KEY_GENERAL_ALBUM 
from medlib.card_ini import JSON_KEY_GENERAL_TRACK
from medlib.card_ini import JSON_KEY_GENERAL_RECIPETYPE

from medlib.card_ini import KEY_CONTROL_ORDERBY
from medlib.card_ini import KEY_CONTROL_MEDIA
from medlib.card_ini import KEY_CONTROL_CATEGORY
from medlib.card_ini import KEY_CONTROL_ICONKEY

from medlib.card_ini import JSON_SECTION_STORYLINE
from medlib.card_ini import JSON_SECTION_TITLES
from medlib.card_ini import JSON_SECTION_TOPIC
from medlib.card_ini import JSON_SECTION_LYRICS
from medlib.card_ini import JSON_SECTION_GENERAL
from medlib.card_ini import JSON_SECTION_CLASSIFICATION
from medlib.card_ini import JSON_SECTION_CONTROL

from medlib.card_ini import JSON_NODE_PATH_COLLECTOR
from medlib.card_ini import JSON_NODE_PATH_STORAGE
from medlib.card_ini import JSON_NODE_PATH_APPENDIX
from medlib.card_ini import JSON_NODE_APPENDIXES
from medlib.card_ini import JSON_NODE_STORAGES
from medlib.card_ini import JSON_NODE_COLLECTORS

from medlib.card_ini import JSON_KEY_COLLECTOR_NAME_OF_FOLDER
from medlib.card_ini import JSON_KEY_COLLECTOR_PATH_OF_CARD
from medlib.card_ini import JSON_KEY_COLLECTOR_PATH_OF_IMAGE
from medlib.card_ini import JSON_KEY_COLLECTOR_PATH_OF_ICON

from medlib.card_ini import JSON_KEY_STORAGE_PATH_OF_ICON
from medlib.card_ini import JSON_KEY_STORAGE_NAME_OF_FOLDER
from medlib.card_ini import JSON_KEY_STORAGE_PATH_OF_CARD
from medlib.card_ini import JSON_KEY_STORAGE_PATH_OF_IMAGE
from medlib.card_ini import JSON_KEY_STORAGE_PATH_OF_MEDIA
from medlib.card_ini import JSON_KEY_APPENDIX_NAME_OF_FOLDER
from medlib.card_ini import JSON_KEY_APPENDIX_PATH_OF_CARD
from medlib.card_ini import JSON_KEY_APPENDIX_PATH_OF_IMAGE
from medlib.card_ini import JSON_KEY_APPENDIX_PATH_OF_MEDIA

from medlib.card_ini import CARD_LIST_JSON_FILE_NAME
from medlib.card_ini import CARD_INI_FILE_NAME

from medlib.card_ini import SECTION_CONTROL
from medlib.card_ini import SECTION_TITLES
from medlib.card_ini import SECTION_STORYLINE
from medlib.card_ini import SECTION_TOPIC
from medlib.card_ini import SECTION_LYRICS
from medlib.card_ini import SECTION_INGREDIENT
from medlib.card_ini import SECTION_METHOD
from medlib.card_ini import SECTION_GENERAL
from medlib.card_ini import SECTION_MEDIA
from medlib.card_ini import SECTION_CLASSIFICATION

def getPatternImage():
    return re.compile( '^image[.](jp(eg|g)|png)$' )

def getPatternIcon():
    return re.compile( '^icon[.](png)$' )

def getPatternRate():
    return re.compile('^([1][0])|([0-9])$')

def getPatternYear():
    return re.compile('^((19|[2-9][0-9])\d{2})(-((19|[2-9][0-9])\d{2}))?$')

def getPatternNumber():
    return re.compile('^([0-9]+)$')

def getPatternLength():
    return re.compile('^\d{1,3}[:]\d{1,2}$')

def getCollectedCardsFromRoot():
    """
        Reads the Cards. First try to read from the json file.
        If there is no json file then it reads it from the file system and
        then save it to the json file 
    """    
    media_path = config_ini['media_path']
    
    jsonForm = CardListJson.getInstance().read()

    if not jsonForm:
        mainCollector = collectCardsFromFileSystem(media_path)
        saveJson(mainCollector)
    else: 
        mainCollector = collectCardsFromJson(jsonForm)

    return mainCollector

def saveJson(mediaCollector):
    jsonForm = mediaCollector.getJson()
    CardListJson.getInstance().write(jsonForm)

def collectCardsFromFileSystem(actualDir, parentMediaCollector = None):
    """
        Recursive analysis on the the file system for the mediaCollectors
        _________________________________________________________________
        input:
                actualDir             The actual directory where the analysis is in process
                parentMediaCollector  The actual parentMediaCollector
    """
    NoneType = type(None)
    assert issubclass(parentMediaCollector.__class__, (MediaCollector, MediaStorage, NoneType))

    recentMedia = parentMediaCollector
        
    # Collect files and and dirs in the current directory
    file_list = [f for f in os.listdir(actualDir) if os.path.isfile(os.path.join(actualDir, f))] if os.path.exists(actualDir) else []
    dir_list = [d for d in os.listdir(actualDir) if os.path.isdir(os.path.join(actualDir, d))] if os.path.exists(actualDir) else []
    
    card_path = None
    media_path = None
    image_path = None
    icon_path = None
    media_name = None
    
    # ####################################
    #
    # Go through all FILES in the folder
    # and collect the files which matters
    #
    # ####################################    
    for file_name in file_list:
        
        # find the Card
        if file_name == CARD_INI_FILE_NAME:
            card_path = os.path.join(actualDir, file_name)
            
        # find the Image
        if getPatternImage().match( file_name ):
            image_path = os.path.join(actualDir, file_name)

        # find the Icon
        if getPatternIcon().match(file_name):
            icon_path = os.path.join(actualDir, file_name)
            
#        # find the Media (video or audio or odt or pdf)
#        if getPatternAudio().match(file_name) or getPatternVideo().match(file_name) or getPatternOdt().match(file_name) or getPatternPdf().match(file_name):
#            media_path = os.path.join(actualDir, file_name)
#            media_name = file_name

    # If there is Card.ini (could be MediaCollector/MediaStorage
    if card_path:
        
        # Read the Card.ini file
        card_ini = Property(card_path, True)
#        card_ini.update(section, key, value)        
#        parser = configparser.RawConfigParser()
#        parser.read(card_path, encoding='utf-8')
        
        # --- CONTROL --- #
        try:
            con_orderby = card_ini.get(SECTION_CONTROL, KEY_CONTROL_ORDERBY, CardIni.getOrderByList()[0], False)
            #con_orderby = parser.get("control", "orderby")
            #con_orderby = con_orderby if con_orderby in CardIni.getOrderByList() else ""
            con_orderby = con_orderby if con_orderby in CardIni.getOrderByList() else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            #con_orderby = ""
            con_orderby = CardIni.getOrderByList()[0]

        try:
            con_media = card_ini.get(SECTION_CONTROL, KEY_CONTROL_MEDIA, CardIni.getMediaList()[0], False)
            #con_media = parser.get("control", "media")
            #con_media = con_media if con_media in CardIni.getMediaList() else ""
            con_media = con_media if con_media in CardIni.getMediaList() else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            #con_media = ""
            con_media = CardIni.getMediaList()[0]
        
        try:
#            con_category = card_ini.get(SECTION_CONTROL, KEY_CONTROL_CATEGORY, CardIni.getCategoryListByMedia(con_media)[0], False)
            con_category = card_ini.get(SECTION_CONTROL, KEY_CONTROL_CATEGORY, None, False)
            #con_category = parser.get("control", "category")            
            #con_category = con_category if con_category in CardIni.getCategoryListByMedia(con_media) else ""
            con_category = con_category if con_category in CardIni.getCategoryListByMedia(con_media) else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            #con_category = ""
            con_category = CardIni.getCategoryListByMedia(con_media)[0]

        try:
            con_iconkey = card_ini.get(SECTION_CONTROL, KEY_CONTROL_ICONKEY, None, False)
#           con_iconkey = con_iconkey if con_iconkey in CardIni.getCategoryListByMedia(con_media) else ""
        except (configparser.NoSectionError, configparser.NoOptionError):
            con_iconkey = ""
                    
        control = IniControl(con_orderby, con_media, con_category, con_iconkey) 
 
        #MediaStorage
        is_media_storage = True if con_media and con_category else False            
 
        for file_name in file_list:
             
            # find the Media - Enabled Media file depends on the "control.media" in the card.ini (ex. media=video => enabled files: *.mkv, *.mp4, *.webm, *.avi, *.flv)
            if CardIni.getMediaFilePatternByMedia(con_media).match(file_name):
                media_path = os.path.join(actualDir, file_name)
                media_name = file_name

        # --- TITLE --- #
        try:
            titles_dict = card_ini.getOptions(SECTION_TITLES)
            #titles_dict=dict(parser.items("titles"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            titles_dict = {"orig": ""}            
        
        try:
            title_orig = card_ini.get(SECTION_TITLES, "orig", "", False) 
            #title_orig = parser.get("titles", "orig")
        except (configparser.NoSectionError, configparser.NoOptionError):
            title_orig = ""        
        
        titles_lang_dict = {}
        for key, value in titles_dict.items():
            hit = re.compile( '^(.{2})$' ).match(key)
            if hit is not None:
                titles_lang_dict[hit.group(1)] = value
            
        titles = IniTitles(title_orig, titles_lang_dict)

        #--- STORYLINE --- #
        try:
            storyline_dict = card_ini.getOptions(SECTION_STORYLINE)
            #storyline_dict=dict(parser.items("storyline"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            storyline_dict = None       
      
        if storyline_dict:
            storyline_lang_dict = {}
            storyline_orig=""            
            for key, value in storyline_dict.items():
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    storyline_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    storyline_orig = value
                    
            storyline = IniStorylines(storyline_orig, storyline_lang_dict)
        else:
            storyline = None
                
        #--- TOPIC --- #
        try:
            topic_dict = card_ini.getOptions(SECTION_TOPIC)
            #topic_dict=dict(parser.items("topic"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            topic_dict=None       
        
        if topic_dict:
            topic_lang_dict = {}
            topic_orig=""            
            for key, value in topic_dict.items():
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    topic_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    topic_orig = value
            
            topic = IniStorylines(topic_orig, topic_lang_dict)
        else:
            topic = None

        #--- LYRICS --- #
        try:
            lyrics_dict = card_ini.getOptions(SECTION_LYRICS)
            #lyrics_dict=dict(parser.items("lyrics"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            lyrics_dict=None       
        
        if lyrics_dict:
            lyrics_lang_dict = {}
            lyrics_orig = ""            
            for key, value in lyrics_dict.items():
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    lyrics_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    lyrics_orig = value
            
            lyrics = IniStorylines(lyrics_orig, lyrics_lang_dict)
        else:
            lyrics = None        

        #--- INGREDIENT --- #
        try:
            ingredient_dict = card_ini.getOptions(SECTION_INGREDIENT)
        except (configparser.NoSectionError, configparser.NoOptionError):
            ingredient_dict = None       
      
        if ingredient_dict:
            ingredient_lang_dict = {}
            ingredient_orig=""            
            for key, value in ingredient_dict.items():
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    ingredient_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    ingredient_orig = value
                    
            ingredient = IniStorylines(ingredient_orig, ingredient_lang_dict)
        else:
            ingredient = None

        #--- METHOD --- #
        try:
            method_dict = card_ini.getOptions(SECTION_METHOD)
            #storyline_dict=dict(parser.items("storyline"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            method_dict = None       
      
        if method_dict:
            method_lang_dict = {}
            method_orig=""            
            for key, value in method_dict.items():
                hit_lang = re.compile( '^(.{2})$' ).match(key)                
                if hit_lang is not None:
                    method_lang_dict[hit_lang.group(1)] = value
                elif key == "orig":
                    method_orig = value
                    
            method = IniStorylines(method_orig, method_lang_dict)
        else:
            method = None

        #--- GENERAL --- #
        try:
            general_dict = card_ini.getOptions(SECTION_GENERAL)
            #general_dict=dict(parser.items("general"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            if lyrics or topic or storyline:
                general_dict = {}
            else:
                general_dict=None       
        
        general = None
        if general_dict is not None:
            general = IniGeneral()    
            for key, value in general_dict.items():
                 
                # - length - #
                if key == KEY_GENERAL_LENGTH and getPatternLength().match( value ):
                    general.setLength(value)

                # - year - #
                if key == KEY_GENERAL_YEAR and getPatternYear().match( value ):
                    general.setYear(value)

                # - director - #
                elif key == KEY_GENERAL_DIRECTOR and len(value) > 0:
                    directors = value.split(",")
                    director_list = []            
                    for director in directors:
                        director_list.append(director.strip())
                    general.setDirectors(director_list)
                
                # - maker - #
                elif key == KEY_GENERAL_MAKER and len(value) > 0:
                    makers = value.split(",")
                    maker_list = []            
                    for maker in makers:
                        maker_list.append(maker.strip())
                    general.setMakers(maker_list)

                # - writer - #
                elif key == KEY_GENERAL_WRITER and len(value) > 0:
                    writers = value.split(",")
                    writer_list = []            
                    for writer in writers:
                        writer_list.append(writer.strip())
                    general.setWriters(writer_list)
                
                # - author - #
                elif key == KEY_GENERAL_AUTHOR and len(value) > 0:
                    authors = value.split(",")
                    author_list = []            
                    for author in authors:
                        author_list.append(author.strip())
                    general.setAuthors(author_list)

                # - actor - #
                elif key == KEY_GENERAL_ACTOR and len(value) > 0:
                    actors = value.split(",")
                    actor_list = []            
                    for actor in actors:
                        actor_list.append(actor.strip())
                    general.setActors(actor_list)
                
                # - performer - #
                elif key == KEY_GENERAL_PERFORMER and len(value) > 0:
                    performers = value.split(",")
                    performer_list = []            
                    for performer in performers:
                        performer_list.append(performer.strip())
                    general.setPerformers(performer_list)
                
                # - lecturer - #
                elif key == KEY_GENERAL_LECTURER and len(value) > 0:
                    lecturers = value.split(",")
                    lecturer_list = []            
                    for lecturer in lecturers:
                        lecturer_list.append(lecturer.strip())
                    general.setLecturers(lecturer_list)
                
                # - contributor - #
                elif key == KEY_GENERAL_CONTRIBUTOR and len(value) > 0:
                    contributors = value.split(",")
                    contributor_list = []            
                    for contributor in contributors:
                        contributor_list.append(contributor.strip())
                    general.setContributors(contributor_list)
                
                # - voice - #
                elif key == KEY_GENERAL_VOICE and len(value) > 0:
                    voices = value.split(",")
                    voice_list = []            
                    for voice in voices:
                        voice_list.append(voice.strip())
                    general.setVoices(voice_list)
                
                # - genre - #
                elif key == KEY_GENERAL_GENRE and len(value) > 0:
                    genres = value.split(",")
                    genre_list = []            
                    for genre in genres:
                        genre_list.append(genre.strip())
                    general.setGenres(genre_list)
                
                # - theme - #
                elif key == KEY_GENERAL_THEME and len(value) > 0:
                    themes = value.split(",")
                    theme_list = []            
                    for theme in themes:
                        theme_list.append(theme.strip())
                    general.setThemes(theme_list)

                # - recipetype - #
                elif key == KEY_GENERAL_RECIPETYPE and len(value) > 0:
                    recipetypes = value.split(",")
                    recipetype_list = []            
                    for recipetype in recipetypes:
                        recipetype_list.append(recipetype.strip())
                    general.setRecipeTypes(recipetype_list)
                
                # - subtitle - #
                elif key == KEY_GENERAL_SUB and len(value) > 0:
                    subs = value.split(",")
                    sub_list = []            
                    for sub in subs:
                        sub_list.append(sub.strip())
                    general.setSubs(sub_list)

                # - sound - #
                elif key == KEY_GENERAL_SOUND and len(value) > 0:
                    sounds = value.split(",")
                    sound_list = []            
                    for sound in sounds:
                        sound_list.append(sound.strip())
                    general.setSounds(sound_list)

                # - country - #
                elif key == KEY_GENERAL_COUNTRY and len(value) > 0:
                    countrys = value.split(",")
                    country_list = []            
                    for country in countrys:
                        country_list.append(country.strip())
                    general.setCountries(country_list)
                    
                # - season - #
                elif key == KEY_GENERAL_SEASON and getPatternNumber().match( value ):
                    general.setSeason(value)
                
                # - episode - #
                elif key == KEY_GENERAL_EPISODE and getPatternNumber().match( value ):
                    general.setEpisode(value)

                # - album - #
                elif key == KEY_GENERAL_ALBUM and getPatternNumber().match( value ):
                    general.setAlbum(value)
                
                # - track - #
                elif key == KEY_GENERAL_TRACK and getPatternNumber().match( value ):
                    general.setTrack(value)
                    
            
            if storyline:
                general.setStoryline(storyline);
            elif topic:
                general.setTopic(topic)
            elif lyrics:
                general.setLyrics(lyrics)
            
            if method:
                general.setMethod(method)
            if ingredient:
                general.setIngredient(ingredient)
        
        #--- CLASSIFICATION --- #
        try:
            classification_dict = card_ini.getOptions(SECTION_CLASSIFICATION)
            #classification_dict=dict(parser.items("classification"))
        except (configparser.NoSectionError, configparser.NoOptionError):
            classification_dict=None       
        
        classification = None
        if classification_dict:
            rat_rate = 0
            tag_list = []
            rat_favorite = False
            rat_new = False
       
            for key, value in classification_dict.items():
                if key == KEY_CLASSIFICATION_RATE and getPatternRate().match(value):
                    rat_rate = int(value)
                elif key == KEY_CLASSIFICATION_FAVORITE and (value == 'y' or value == 'n'):
                    rat_favorite = True if value == 'y' else False
                elif key == KEY_CLASSIFICATION_NEW and (value == 'y' or value == 'n'):
                    rat_new = True if value == 'y' else False
                elif key == KEY_CLASSIFICATION_TAG and len(value) > 0:
                    tags = value.split(",")                                
                    for tag in tags:
                        tag_list.append(tag.strip())
                   
            classification = IniClassification(rat_rate, tag_list, rat_favorite, rat_new) 

#        parser = configparser.RawConfigParser()
#        parser.read(card_path, encoding='utf-8')
#
        # --- MEDIA --- #
        #
        # Mostly used in case of Appendix
        # it is needed when the media is not the file which is in the same folder as the card.ini
        # for example: link
        #
        try:
#            media_path = parser.get("media", "link")
            media_path = card_ini.get(SECTION_MEDIA, "link", media_path, False) 

        except (configparser.NoSectionError, configparser.NoOptionError):
            pass


        # -------------------- MediaCollector/MediaStorage/MediaAppendix construction ------------
        #                                                    V
        #  ┌────────────────┐                         ┌────────────────┐
        #  │     NONE       │                         │     FOLDER     │
        #  └───────┬────────┘                         └───────┬────────┘  
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤ MediaCollector |             ├───────────┤ MediaCollector |
        #          │           └────────────────┘             │           └────────────────┘
        #          │                                          │
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          └───────────┤    FOLDER      |             ├───────────┤ MediaAppendix  | 
        #                      └────────────────┘             |           └────────────────┘
        #                                                     │
        #                                                     │           ┌────────────────┐ 
        #                                                     └───────────┤    FOLDER      |   
        #                                                                 └────────────────┘
        #         
        #  ┌────────────────┐                         ┌────────────────┐
        #  │ MediaCollector │                         │  MediaStorage  │
        #  └───────┬────────┘                         └───────┬────────┘  
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤ MediaCollector |             ├───────────┤ MediaAppendix  |
        #          │           └────────────────┘             │           └────────────────┘
        #          │                                          │
        #          │           ┌────────────────┐             │           ┌────────────────┐
        #          ├───────────┤  MediaStorage  |             └───────────┤     FOLDER     | 
        #          │           └────────────────┘                         └────────────────┘
        #          │
        #          │           ┌────────────────┐ 
        #          └───────────┤    FOLDER      |   
        #                      └────────────────┘ 
        #        

        continue_to_go_down = False
        
        #
        # If MediaAppendix - Under MediaStorage
        #
        if media_path and issubclass(parentMediaCollector.__class__, MediaStorage) and con_category == 'appendix':
            pathAppendix = PathsAppendix(os.path.dirname(card_path), card_path, image_path, media_path)
            recentMedia = MediaAppendix(pathAppendix, titles, control)
            parentMediaCollector.addMediaAppendix(recentMedia)
            continue_to_go_down = False

        #
        # If MediaStorage - Under MediaCollector
        #
        elif is_media_storage and issubclass(parentMediaCollector.__class__, MediaCollector):
#        elif card_path and media_path and issubclass(parentMediaCollector.__class__, MediaCollector):
            pathStorage = PathsStorage(os.path.dirname(card_path), card_path, image_path, icon_path, media_path)            
            recentMedia = MediaStorage(pathStorage, titles, control, general, classification)
            parentMediaCollector.addMediaStorage(recentMedia)
            continue_to_go_down = True

        #        
        # If MediaCollector - Under MediaCollector or Root
        #      
        elif not media_path and dir_list and issubclass(parentMediaCollector.__class__, (MediaCollector, NoneType)):
            pathCollector = PathsCollector(os.path.dirname(card_path), card_path, image_path, icon_path)            
            recentMedia = MediaCollector(pathCollector, titles, control, general, classification)
            
            # If it has parent -> add it to parent, otherwise it will be the parent
            if parentMediaCollector:
                parentMediaCollector.addMediaCollector(recentMedia)
            else:
                parentMediaCollector = recentMedia

            continue_to_go_down = True

#        else:
            
#            return parentMediaCollector
    else:
        continue_to_go_down = True
                
    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #
    ret = []    
    for name in dir_list:
        subfolder_path_os = os.path.join(actualDir, name)
        val = collectCardsFromFileSystem( subfolder_path_os, recentMedia )
        ret.append(val)

    if parentMediaCollector is None and ret:
        parentMediaCollector = ret[0]
    
    elif parentMediaCollector is None:
        parentMediaCollector = MediaCollector(PathsCollector("", "", "", ""), IniTitles("", {'orig':''}), IniControl("", "", "", ""), None, None)
        
    # and finaly returns
    return parentMediaCollector
  
  
def collectCardsFromJson(jsonForm, parentMediaCollector = None):
    """
        Recursively go through the jsonForm and fill up the MediaCollector
        _________________________________________________________________
        @param {dic} jsonForm:    media cards collected in json form to make MediaCollector
        @return MediaCollector:   The root MediaCollector 
    """
    NoneType = type(None)
    assert issubclass(parentMediaCollector.__class__, (MediaCollector, MediaStorage, NoneType))

    nextParent = parentMediaCollector
    
    # --- TITLE --- #
    titles = jsonForm.get(JSON_SECTION_TITLES)
    ini_titles = None
    if titles:        
        titles_dict = {}
        titles_orig = None
        for key, value in titles.items():
            hit = re.compile( '^(.{2})$' ).match(key)
            if hit is not None:
                titles_dict[key] = value
            elif key == 'orig':
                titles_orig = value
        ini_titles = IniTitles(titles_orig, titles_dict)
        
    #--- STORYLINE --- #
    storyline = jsonForm.get(JSON_SECTION_STORYLINE)
    ini_storyline = None
    if storyline:
        storyline_dict = {}
        storyline_orig = None
        for key, value in storyline.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                storyline_dict[key] = value
            elif key == 'orig':
                storyline_orig = value
        ini_storyline = IniStorylines(storyline_orig, storyline_dict)                
                
    #--- TOPIC --- #
    topic = jsonForm.get(JSON_SECTION_TOPIC)
    ini_topic = None
    if topic:
        topic_dict = {}
        topic_orig = None
        for key, value in topic.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                topic_dict[key] = value
            elif key == 'orig':
                topic_orig = value
        ini_topic = IniStorylines(topic_orig, topic_dict)                
            
    #--- LYRICS --- #
    lyrics = jsonForm.get(JSON_SECTION_LYRICS)
    ini_lyrics = None
    if lyrics:
        lyrics_dict = {}
        lyrics_orig = None
        for key, value in lyrics.items():
            hit = re.compile( '^(.{2})$' ).match(key)                
            if hit is not None:
                lyrics_dict[key] = value
            elif key == 'orig':
                lyrics_orig = value
        ini_lyrics = IniStorylines(lyrics_orig, lyrics_dict)

    ini_general = IniGeneral()            
    if ini_lyrics or ini_storylines or ini_topic:
        if ini_storyline:
            ini_general.setStoryline(ini_storyline);
        if ini_topic:
            ini_general.setTopic(ini_topic)
        if ini_lyrics:
            ini_general.setLyrics(ini_lyrics)
#    else:
#        ini_general = None
        
    #--- GENERAL --- #
    general = jsonForm.get(JSON_SECTION_GENERAL)
    if general:
        year = general.get(JSON_KEY_GENERAL_YEAR)
        length = general.get(JSON_KEY_GENERAL_LENGTH)
        director = general.get(JSON_KEY_GENERAL_DIRECTOR)
        maker = general.get(JSON_KEY_GENERAL_MAKER)
        author = general.get(JSON_KEY_GENERAL_AUTHOR)
        actor = general.get(JSON_KEY_GENERAL_ACTOR)
        performer = general.get(JSON_KEY_GENERAL_PERFORMER)
        lecturer = general.get(JSON_KEY_GENERAL_LECTURER)
        contributor = general.get(JSON_KEY_GENERAL_CONTRIBUTOR)
        voice = general.get(JSON_KEY_GENERAL_VOICE)
        genre = general.get(JSON_KEY_GENERAL_GENRE)
        theme = general.get(JSON_KEY_GENERAL_THEME)
        recipetype = general.get(JSON_KEY_GENERAL_RECIPETYPE)
        sub = general.get(JSON_KEY_GENERAL_SUB)
        sound = general.get(JSON_KEY_GENERAL_SOUND)
        country = general.get(JSON_KEY_GENERAL_COUNTRY)
        season = general.get(JSON_KEY_GENERAL_SEASON)
        episode = general.get(JSON_KEY_GENERAL_EPISODE)
        album = general.get(JSON_KEY_GENERAL_ALBUM)
        track = general.get(JSON_KEY_GENERAL_TRACK)
            
        if year:
            ini_general.setYear(year)
        if length:
            ini_general.setLength(length)
        if director:
            ini_general.setDirectors(director)
        if maker:
            ini_general.setMakers(maker)
        if author:
            ini_general.setAuthors(author)
        if actor:
            ini_general.setActors(actor)
        if performer:
            ini_general.setPerformers(performer)
        if lecturer:
            ini_general.setLecturers(lecturer)
        if contributor:
            ini_general.setContributors(contributor)
        if voice:
            ini_general.setVoices(voice)
        if genre:
            ini_general.setGenres(genre)
        if theme:
            ini_general.setThemes(theme)
        if recipetype:
            ini_general.setRecipeTypes(recipetype)
        if sub:
            ini_general.setSubs(sub)
        if sound:
            ini_general.setSounds(sound)
        if country:
            ini_general.setCountries(country)
        if season:
            ini_general.setSeason(season)
        if episode:
            ini_general.setEpisode(episode)
        if album:
            ini_general.setAlbum(album)
        if track:
            ini_general.setTrack(track)

    #--- CLASSIFICATION --- #
    classification = jsonForm.get(JSON_SECTION_CLASSIFICATION)
    ini_classification = None
    if classification:

        rat_rate = classification.get(JSON_KEY_CLASSIFICATION_RATE)
        rat_tags = classification.get(JSON_KEY_CLASSIFICATION_TAG)
        rat_favorite = classification.get(JSON_KEY_CLASSIFICATION_FAVORITE)
        rat_new = classification.get(JSON_KEY_CLASSIFICATION_NEW)
        
        rat_rate = rat_rate if getPatternRate().match(str(rat_rate)) else 0            
        rat_favorite = True if rat_favorite == 'y' else False        
        rat_new = True if rat_new == 'y' else False      
                   
        ini_classification = IniClassification(rat_rate, rat_tags, rat_favorite, rat_new) 

    # --- CONTROL --- #
    control = jsonForm.get(JSON_SECTION_CONTROL)
    #ini_control = None
    con_orderby = ""
    con_media = ""
    con_category = ""
    con_iconkey = ""
    if control:
        con_orderby = control.get(KEY_CONTROL_ORDERBY)
        con_media = control.get(KEY_CONTROL_MEDIA)
        con_category = control.get(KEY_CONTROL_CATEGORY)
        con_iconkey = control.get(KEY_CONTROL_ICONKEY)
    ini_control = IniControl(con_orderby, con_media, con_category, con_iconkey) 
 
    # --- MEDIA --- #
    
        
    # --- MEDIA-COLLECTOR --- #        
    path_collector = jsonForm.get(JSON_NODE_PATH_COLLECTOR)
    
    # --- MEDIA-STORAGE --- #        
    path_storage = jsonForm.get(JSON_NODE_PATH_STORAGE)
    
    # --- MEDIA-APPENDIX --- #
    path_appendix = jsonForm.get(JSON_NODE_PATH_APPENDIX)
    
    #
    # If MediaCollector - under MediaCollector or Root
    #
    if path_collector:
        name_of_folder = path_collector.get(JSON_KEY_COLLECTOR_NAME_OF_FOLDER)
        path_of_card = path_collector.get(JSON_KEY_COLLECTOR_PATH_OF_CARD)
        path_of_image = path_collector.get(JSON_KEY_COLLECTOR_PATH_OF_IMAGE)
        path_of_icon = path_collector.get(JSON_KEY_COLLECTOR_PATH_OF_ICON)
        
        ini_path_collector = PathsCollector(name_of_folder, path_of_card, path_of_image, path_of_icon)
        nextParent = MediaCollector(ini_path_collector, ini_titles, ini_control, ini_general, ini_classification)
    
        if parentMediaCollector:
            parentMediaCollector.addMediaCollector(nextParent)
        else:
            parentMediaCollector = nextParent
            
    #
    # If MediaStorage - Under MediaCollector
    #
    elif path_storage:
        name_of_folder = path_storage.get(JSON_KEY_STORAGE_NAME_OF_FOLDER)
        path_of_card = path_storage.get(JSON_KEY_STORAGE_PATH_OF_CARD)
        path_of_image = path_storage.get(JSON_KEY_STORAGE_PATH_OF_IMAGE)
        path_of_media = path_storage.get(JSON_KEY_STORAGE_PATH_OF_MEDIA)
        path_of_icon = path_storage.get(JSON_KEY_STORAGE_PATH_OF_ICON)
    
        ini_path_storage = PathsStorage(name_of_folder, path_of_card, path_of_image, path_of_icon, path_of_media)
        nextParent = MediaStorage(ini_path_storage, ini_titles, ini_control, ini_general, ini_classification)
        
        parentMediaCollector.addMediaStorage(nextParent)
        
    #
    # If MediaAppendix - MediaStorage
    #
    elif path_appendix:
        name_of_folder = path_appendix.get(JSON_KEY_APPENDIX_NAME_OF_FOLDER)
        path_of_card = path_appendix.get(JSON_KEY_APPENDIX_PATH_OF_CARD)
        path_of_image = path_appendix.get(JSON_KEY_APPENDIX_PATH_OF_IMAGE)
        path_of_media = path_appendix.get(JSON_KEY_APPENDIX_PATH_OF_MEDIA)
        
        ini_path_appendix = PathsAppendix(name_of_folder, path_of_card, path_of_image, path_of_media)
        nextParent = MediaAppendix(ini_path_appendix, ini_titles, ini_control)
        parentMediaCollector.addMediaAppendix(nextParent)

    # ################################## #
    #                                    #
    # Go through all SUB-FOLDERS in the  #
    # folder and collect the files which #
    # matters                            #
    #                                    #
    # ################################## #    
    
    # --- COLLECTORS --- #        
    collectors_list = jsonForm.get(JSON_NODE_COLLECTORS)    
    for childJson in collectors_list if collectors_list else {}:
        collectCardsFromJson( childJson, nextParent )        
 
    # --- STORAGES --- #        
    storages_list = jsonForm.get(JSON_NODE_STORAGES)
    for childJson in storages_list if storages_list else {}:
        collectCardsFromJson( childJson, nextParent )
        
    # --- APPENDIXES --- #        
    appendixes_list = jsonForm.get(JSON_NODE_APPENDIXES)
    for childJson in appendixes_list if appendixes_list else []:
        collectCardsFromJson( childJson, nextParent )    

    return parentMediaCollector






# =====================
#
# Handle card.list.json
#
# =====================
class CardListJson():
    FILE_NAME = CARD_LIST_JSON_FILE_NAME

    __instance = None    

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)
        return inst
        
    def __init__(self):        
        self.file = os.path.join(PATH_FOLDER_CONFIG, CardListJson.FILE_NAME)
        
    def write(self, jsonContent):
        with open(self.file, 'w') as outfile:
            json.dump(jsonContent, outfile)

    def read(self):
        content = self.inner_read()
        return content
        
    def inner_read(self):
        try:
            with open(self.file) as infile:
                data = json.load(infile)
        except:
            data = {}
        return data
      

