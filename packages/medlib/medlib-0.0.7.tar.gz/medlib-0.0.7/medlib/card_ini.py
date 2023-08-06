import re

media_dict = {
    'video': {
        'ext': ('mkv', 'mp4', 'flv', 'divx', 'avi', 'webm'), 
        'category': ('movie', 'music', 'show', 'presentation', 'alternative', 'miscellaneous', 'elearning', 'family', 'appendix', 'recipe')},
    'audio': {
        'ext': ('mp3', 'ogg'), 
        'category': ('radioplay', 'music', 'show', 'presentation', 'audiobook', 'elearning', 'appendix', 'recipe')},
    'text': {
        'ext': ('doc', 'odt', 'pdf', 'epub', 'mobi', 'azw', 'azw3', 'iba', 'txt','rtf'), 
        'category': ('book', 'doc', 'presentation', 'quiz', 'elearning', 'appendix', 'recipe')},
    'image': {
        'ext': ('jpg', 'jpeg', 'png'), 
        'category': ('elearning', 'recipe')},
    'link' : {
        'ext': (), 
        'category': ('appendix','elearning')},
    '': {
        'ext': (), 
        'category': ()
        }
    }

section_dict = {
    'titles': {},
    'storyline': {},
    'topic': {},
    'lyrics': {},
    'ingredient': {},
    'method': {},
    'general': {
        'length': {},
        'year': {},
        'director': (),
        'maker': (),
        'writer': (),
        'author': (),
        'actor': (),
        'performer': (),
        'lecturer': (),
        'contributor': (),
        'voice': (),
        'genre': (),
        'theme': (),
        'recipetype': (),
        'sub': (),
        'sound': (),
        'country': (),
        'season': (),
        'episode': (),
        'album': (),
        'track': ()
        },
    'classification': {'rate', 'tag', 'new', 'favorite'}, 
    'control': {'orderby', 'media', 'category', 'iconkey'},
    'appendixes': {},
    'media': {'link', 'file'},
    'link': {}
    }

class CardIni(object):

    @staticmethod
    def getSectionList():
        return list(section_dict.keys()) 

    @staticmethod
    def getMediaList():
        return list(media_dict.keys())
    
    @staticmethod
    def getCategoryListByMedia(media):
        return media_dict[media]['category']

    @staticmethod
    def getExtensionListByMedia(media):
        return media_dict[media]['ext']

    @staticmethod
    def getMediaFilePatternByMedia(media):
        
        ptrn = '|'.join( media_dict[media]['ext'] )
        return re.compile( '^.+[.](' + ptrn + ')$' )

    @staticmethod
    def getOrderByList():
        return ('folder', 'title')

    @staticmethod
    def getKeyListBySection(section):        
        return section_dict[section]        
    
    @staticmethod
    def getSectionDict():
        return section_dict

# --------------------
# --- INI ELEMENTS ---
# --------------------

CARD_INI_FILE_NAME = 'card.ini'
CARD_LIST_JSON_FILE_NAME = 'card.list.json'

# Titles
SECTION_TITLES = 'titles'

# Storyline/Topic/Lyrics/Ingredient/Method
SECTION_STORYLINE = 'storyline'
SECTION_TOPIC = 'topic'
SECTION_LYRICS = 'lyrics'
SECTION_INGREDIENT = 'ingredient'
SECTION_METHOD = 'method'

# General
SECTION_GENERAL = 'general'
KEY_GENERAL_LENGTH = 'length'
KEY_GENERAL_YEAR = 'year'
KEY_GENERAL_DIRECTOR = 'director'
KEY_GENERAL_MAKER = 'maker'
KEY_GENERAL_WRITER = 'writer'
KEY_GENERAL_AUTHOR = 'author'
KEY_GENERAL_ACTOR = 'actor'
KEY_GENERAL_PERFORMER = 'performer'
KEY_GENERAL_LECTURER = 'lecturer'
KEY_GENERAL_CONTRIBUTOR = 'contributor'
KEY_GENERAL_VOICE = 'voice'
KEY_GENERAL_GENRE = 'genre'
KEY_GENERAL_THEME = 'theme'
KEY_GENERAL_RECIPETYPE = 'recipetype'
KEY_GENERAL_SUB = 'sub'
KEY_GENERAL_SOUND = 'sound'
KEY_GENERAL_COUNTRY = 'country'
KEY_GENERAL_SEASON = 'season'
KEY_GENERAL_EPISODE = 'episode'
KEY_GENERAL_ALBUM = 'album'
KEY_GENERAL_TRACK = 'track'
KEY_GENERAL_INDEX = 'index'

# Classification
SECTION_CLASSIFICATION = 'classification'
KEY_CLASSIFICATION_RATE = 'rate'
KEY_CLASSIFICATION_TAG = 'tag'
KEY_CLASSIFICATION_NEW = 'new'
KEY_CLASSIFICATION_FAVORITE = 'favorite'

# Control
SECTION_CONTROL = 'control'
KEY_CONTROL_ORDERBY = 'orderby'
KEY_CONTROL_MEDIA = 'media'
KEY_CONTROL_CATEGORY = 'category'
KEY_CONTROL_ICONKEY = 'iconkey'

# Media
SECTION_MEDIA = 'media'

# ---------------------
# --- JSON ELEMENTS ---
# ---------------------

# Titles
JSON_SECTION_TITLES = SECTION_TITLES 

# Storyline/Topic/Lyrics/Ingredient/Method
JSON_SECTION_STORYLINE = SECTION_STORYLINE 
JSON_SECTION_TOPIC = SECTION_TOPIC 
JSON_SECTION_LYRICS = SECTION_LYRICS
JSON_SECTION_INGREDIENT = SECTION_INGREDIENT
JSON_SECTION_METHOD = SECTION_METHOD

# General
JSON_SECTION_GENERAL = SECTION_GENERAL
JSON_KEY_GENERAL_LENGTH = KEY_GENERAL_LENGTH
JSON_KEY_GENERAL_YEAR = KEY_GENERAL_YEAR
JSON_KEY_GENERAL_DIRECTOR = KEY_GENERAL_DIRECTOR
JSON_KEY_GENERAL_MAKER = KEY_GENERAL_MAKER
JSON_KEY_GENERAL_WRITER = KEY_GENERAL_WRITER
JSON_KEY_GENERAL_AUTHOR = KEY_GENERAL_AUTHOR
JSON_KEY_GENERAL_ACTOR = KEY_GENERAL_ACTOR
JSON_KEY_GENERAL_PERFORMER = KEY_GENERAL_PERFORMER
JSON_KEY_GENERAL_LECTURER = KEY_GENERAL_LECTURER
JSON_KEY_GENERAL_CONTRIBUTOR = KEY_GENERAL_CONTRIBUTOR
JSON_KEY_GENERAL_VOICE = KEY_GENERAL_VOICE
JSON_KEY_GENERAL_GENRE = KEY_GENERAL_GENRE
JSON_KEY_GENERAL_THEME = KEY_GENERAL_THEME
JSON_KEY_GENERAL_RECIPETYPE = KEY_GENERAL_RECIPETYPE
JSON_KEY_GENERAL_SUB = KEY_GENERAL_SUB
JSON_KEY_GENERAL_SOUND = KEY_GENERAL_SOUND
JSON_KEY_GENERAL_COUNTRY = KEY_GENERAL_COUNTRY
JSON_KEY_GENERAL_SEASON = KEY_GENERAL_SEASON
JSON_KEY_GENERAL_EPISODE = KEY_GENERAL_EPISODE
JSON_KEY_GENERAL_ALBUM = KEY_GENERAL_ALBUM
JSON_KEY_GENERAL_TRACK = KEY_GENERAL_TRACK

# Classification
JSON_SECTION_CLASSIFICATION = SECTION_CLASSIFICATION
JSON_KEY_CLASSIFICATION_RATE = KEY_CLASSIFICATION_RATE
JSON_KEY_CLASSIFICATION_TAG = KEY_CLASSIFICATION_TAG
JSON_KEY_CLASSIFICATION_NEW = KEY_CLASSIFICATION_NEW
JSON_KEY_CLASSIFICATION_FAVORITE = KEY_CLASSIFICATION_FAVORITE

# Control
JSON_SECTION_CONTROL = SECTION_CONTROL
JSON_KEY_CONTROL_ORDERBY = KEY_CONTROL_ORDERBY
JSON_KEY_CONTROL_MEDIA = KEY_CONTROL_MEDIA
JSON_KEY_CONTROL_CATEGORY = KEY_CONTROL_CATEGORY
JSON_KEY_CONTROL_ICONKEY = KEY_CONTROL_ICONKEY

# Collectors
JSON_NODE_COLLECTORS = 'collectors'
JSON_KEY_COLLECTOR_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_COLLECTOR_PATH_OF_CARD = 'path-of-card'
JSON_KEY_COLLECTOR_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_COLLECTOR_PATH_OF_ICON = 'path-of-icon'

# Storage
JSON_NODE_STORAGES = 'storages'
JSON_KEY_STORAGE_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_STORAGE_PATH_OF_CARD = 'path-of-card'
JSON_KEY_STORAGE_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_STORAGE_PATH_OF_MEDIA = 'path-of-media'
JSON_KEY_STORAGE_PATH_OF_ICON = 'path-of-icon'
JSON_KEY_STORAGE_MEDIA_EXTENSION = 'media-extension'

# Appendix
JSON_NODE_APPENDIXES = 'appendixes'
JSON_KEY_APPENDIX_NAME_OF_FOLDER = 'name-of-folder'
JSON_KEY_APPENDIX_PATH_OF_CARD = 'path-of-card'
JSON_KEY_APPENDIX_PATH_OF_IMAGE = 'path-of-image'
JSON_KEY_APPENDIX_PATH_OF_MEDIA = 'path-of-media'
JSON_KEY_APPENDIX_MEDIA_EXTENSION = 'media-extension'

JSON_NODE_PATH_COLLECTOR = 'paths-collector'
JSON_NODE_PATH_STORAGE = 'paths-storage'
JSON_NODE_PATH_APPENDIX = 'paths-appendix'

