import os
import configparser
from pathlib import Path
from medlib import card_ini

#from medlib.logger import logger

class Property(object):
 
    def __init__(self, file, writable=False, folder=None):
        self.writable = writable
        self.file = file
        self.folder = folder
        self.parser = configparser.RawConfigParser()

        # !!! make it CASE SENSITIVE !!! otherwise it duplicates the hit if there was a key with upper and lower cases. Now it throws an exception
        self.parser.optionxform = str

    def __write_file(self):

        if self.folder:
            Path(self.folder).mkdir(parents=True, exist_ok=True)

        with open(self.file, 'w', encoding='utf-8') as configfile:
            self.parser.write(configfile)


    def get(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: get")

            self.parser[section]={key: default_value}
            self.__write_file()
        self.parser.read(self.file, encoding='utf-8')

        # try to read the key
        try:
            result=self.parser.get(section,key)

            # if it is EMPTY
            if not result:
                result = default_value

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: get")

            # if it should be write
            if self.should_write(writable):
                self.update(section, key, default_value)
                result=self.parser.get(section,key)
            else:
                result = default_value

        return result

    def getBoolean(self, section, key, default_value, writable=None):

        # if not existing file and we want to create it
        if not os.path.exists(self.file) and self.should_write(writable) :
            self.parser[section]={key: default_value}
            self.__write_file()

        # read the file
        self.parser.read(self.file, encoding='utf-8')

        # try to read the key
        try:
            result=self.parser.getboolean(section, key)

        # if does not exist the key
        except (configparser.NoSectionError, configparser.NoOptionError):

            # if it should be write
            if self.should_write(writable):

                self.update(section, key, default_value)
                # It is strange how it works with get/getboolean
                # Sometimes it reads boolean sometimes it reads string
                # I could not find out what is the problem
                #result=self.parser.get(section,key)
            result=default_value

        return result

    def update(self, section, key, value, source=None):

        # if not existing file        
        if not os.path.exists(self.file):
            #self.log_msg("MESSAGE: No file found FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source if source else "")
            self.parser[section]={key: value}

        # if the file exists
        else:

            # read the file
            self.parser.read(self.file, encoding='utf-8')

            # try to set the value
            try:
                # if no section -> NoSectionError | if no key -> Create it
                self.parser.set(section, key, value)

            # if there is no such section
            except configparser.NoSectionError as e:
                #self.log_msg("MESSAGE: " + str(e) + " FILE NAME: " + self.file + " OPERATION: update SOURCE: " + source)
                self.parser[section]={key: value}

        # update
        self.__write_file()
        
    def removeSection(self, section):
        self.parser.remove_section(section)
        self.__write_file()

    def removeOption(self, section, option):
        self.parser.read(self.file, encoding='utf-8')
        self.parser.remove_option(section, option)
        self.__write_file()
        
    def getOptions(self, section):
        try:
            return dict(self.parser.items(section))
        except configparser.NoSectionError as e:
            return dict()
    
    def should_write(self, writable):
        return ((writable is None and self.writable) or (writable))

# ====================
#
# Handle dictionary
#
# Singleton
#
# ====================
class Dict( Property ):
    
    DICT_FILE_PRE = "resources"
    DICT_FILE_EXT = "properties"
    DICT_FOLDER = "dict"
    DICT_SECTION = "dict"

    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls, lng):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance, lng)     
        return inst
        
    def __init__(self, lng):
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.__class__.DICT_FOLDER, self.__class__.DICT_FILE_PRE + "_" + lng + "." + self.__class__.DICT_FILE_EXT)
        super().__init__( file )
    
    def _(self, key):
        return self.get(self.__class__.DICT_SECTION, key,  "[" + key + "]")

class Config:
    HOME = str(Path.home())
    CONFIG_FOLDER = '.medlib'
    
    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(Config.HOME, Config.CONFIG_FOLDER)


# =====================
#
# Handle config.ini
#
# =====================
class ConfigIni( Property ):
    INI_FILE_NAME="config.ini"

    # (section, key, default)
    DEFAULT_LANGUAGE = ("general", "language", "hu")
    DEFAULT_SCALE_LEVEL = ("general", "scale-level", 1)
    DEFAULT_SCALE_FACTOR = ("general", "scale-factor", 0.1)
    DEFAULT_SHOW_ORIGINAL_TITLE = ("general", "show-original-title", "n")
    DEFAULT_KEEP_HIERARCHY = ("general", "keep-hierarchy", "y")
    DEFAULT_USE_XDG = ("general", "use-xdg", "y")
    DEFAULT_MEDIA_PATH = ("media", "media-path", ".")    

    DEFAULT_PLAYERS = {
        "link":      ("player", ("link-player",      "chrome"),      ("link-param",      "")),
        "video":     ("player", ("video-player",     "mplayer"),     ("video-param",     "-zoom -fs -framedrop -really-quiet")),
        "audio":     ("player", ("audio-player",     "rhythmbox"),   ("audio-param",     "")),
        "text-odt":  ("player", ("text-odt-player",  "libreoffice"), ("text-odt-param",  "--writer --quickstart --nofirststartwizard --view")),
        "text-doc":  ("player", ("text-doc-player",  "libreoffice"), ("text-doc-param",  "--writer --quickstart --nofirststartwizard --view")),
        "text-rtf":  ("player", ("text-rtf-player",  "libreoffice"), ("text-rtf-param",  "--writer --quickstart --nofirststartwizard --view")),
        "text-txt":  ("player", ("text-txt-player",  "kate"),        ("text-txt-param",  "")),
        "text-pdf":  ("player", ("text-pdf-player",  "okular"),      ("text-pdf-param",  "--presentation --page 1 --unique")),
        "text-epub": ("player", ("text-epub-player", "fbreader"),    ("text-epub-param", ""))
    }
    
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
        folder = os.path.join(Config.HOME, Config.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigIni.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getLanguage(self):
        return self.get(self.DEFAULT_LANGUAGE[0], self.DEFAULT_LANGUAGE[1], self.DEFAULT_LANGUAGE[2])

    def getScaleFactor(self):
        return self.get(self.DEFAULT_SCALE_FACTOR[0], self.DEFAULT_SCALE_FACTOR[1], self.DEFAULT_SCALE_FACTOR[2])

    def getScaleLevel(self):
        return self.get(self.DEFAULT_SCALE_LEVEL[0], self.DEFAULT_SCALE_LEVEL[1], self.DEFAULT_SCALE_LEVEL[2])

    def getShowOriginalTitle(self):
        return self.get(self.DEFAULT_SHOW_ORIGINAL_TITLE[0], self.DEFAULT_SHOW_ORIGINAL_TITLE[1], self.DEFAULT_SHOW_ORIGINAL_TITLE[2])

    def getKeepHierarchy(self):
        return self.get(self.DEFAULT_KEEP_HIERARCHY[0], self.DEFAULT_KEEP_HIERARCHY[1], self.DEFAULT_KEEP_HIERARCHY[2])

    def getUseXdg(self):
        return self.get(self.DEFAULT_USE_XDG[0], self.DEFAULT_USE_XDG[1], self.DEFAULT_USE_XDG[2])

    def getMediaPath(self):
        return self.get(self.DEFAULT_MEDIA_PATH[0], self.DEFAULT_MEDIA_PATH[1], self.DEFAULT_MEDIA_PATH[2])

    def getPlayerOptions(self):
        return self.DEFAULT_PLAYERS.keys()

    def getPlayerValue(self, key):
        valueList = self.DEFAULT_PLAYERS.get(key)
        return self.get(valueList[0], valueList[1][0], valueList[1][1])

    def getParamValue(self, key):
        valueList = self.DEFAULT_PLAYERS.get(key)
        return self.get(valueList[0], valueList[2][0], valueList[2][1])

# ---

    def setLanguage(self, lang):
        self.update(self.DEFAULT_LANGUAGE[0], self.DEFAULT_LANGUAGE[1], lang)

    def setScaleLevel(self, scale_level):
        if (int(scale_level) * float(self.getScaleFactor())) > -1.0:
            self.update(self.DEFAULT_SCALE_LEVEL[0], self.DEFAULT_SCALE_LEVEL[1], scale_level)

    def setScaleFactor(self, scale_factor):
        self.update(self.DEFAULT_SCALE_FACTOR[0], self.DEFAULT_SCALE_FACTOR[1], scale_factor)

    def setShowOriginal_title(self, show):
        self.update(self.DEFAULT_SHOW_ORIGINAL_TITLE[0], self.DEFAULT_SHOW_ORIGINAL_TITLE[1], show)

    def setKeepHierarchy(self, keep):
        self.update(self.DEFAULT_KEEP_HIERARCHY[0], self.DEFAULT_KEEP_HIERARCHY[1], keep)

    def setMediaPath(self, path):
        self.update(self.DEFAULT_MEDIA_PATH[0], self.DEFAULT_MEDIA_PATH[1], path)

    def setUseXdg(self, use_xdg):
        self.update(self.DEFAULT_USE_XDG[0], self.DEFAULT_USE_XDG[1], use_xdg)





def updateCardIni(card_ini_path, section, key, value):
    card_ini = Property(card_ini_path, True)
    card_ini.update(section, key, value)

def getConfigIni():
    return ConfigIni.getInstance()

def reReadConfigIni():
    global config_ini
    global dic
    
    ci = getConfigIni()
    
    # Read config.ini    
    config_ini['language'] = ci.getLanguage()
    config_ini['scale_factor'] = ci.getScaleFactor()
    config_ini['scale_level'] = ci.getScaleLevel()
    config_ini['show_original_title'] = ci.getShowOriginalTitle()
    config_ini['keep_hierarchy'] = ci.getKeepHierarchy()
    config_ini['use_xdg'] = ci.getUseXdg()
    config_ini['media_path'] = ci.getMediaPath()
    
    options = ci.getPlayerOptions()
    for key in options:
        config_ini[ 'player_' + key.replace("-","_") + '_player'] = ci.getPlayerValue(key)
        config_ini[ 'player_' + key.replace("-","_") + '_param'] = ci.getParamValue(key)

    # Get the dictionary
    dic = Dict.getInstance( config_ini['language'] )

# --------------------------------------------------------
# --------------------------------------------------------
#
# Gives back the translation of the word
#
# word      word which should be translated
#
# --------------------------------------------------------
# --------------------------------------------------------
def _(word):
    return dic._(word)

# ----------------------------------------------------------------------------------------------------
#
# Below code runs when it imported or forced to re-run
#
# How to use dic:
#            - in the beginning of your code define: "from medlib.handle_property import _"
#            - define the translations in the "medlib.dict.resources_<lang>.properties file
#            - in the code where you need the translated word use: "_('word_to_translate')"
#
# How to use config_ini:
#            - your "config.ini" file is in "HOME/.medlib" folder
#            - there are key-value pairs defined in the file
#            - in the beginning of your code: "from medlib.handle_property import config_ini"
#            - you can refer to the contents like: "config_ini('language')"
#
# -----------------------------------------------------------------------------------------------------
config_ini = {}
reReadConfigIni()



