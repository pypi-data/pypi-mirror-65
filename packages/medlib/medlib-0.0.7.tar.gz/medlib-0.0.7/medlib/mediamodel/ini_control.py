from medlib.card_ini import JSON_KEY_CONTROL_MEDIA
from medlib.card_ini import JSON_KEY_CONTROL_ORDERBY
from medlib.card_ini import JSON_KEY_CONTROL_CATEGORY
from medlib.card_ini import JSON_KEY_CONTROL_ICONKEY

import json

class IniControl(object):
    """
    This class represents the [control] section in the card.ini file
        -orderby
        -media - (icon)
        -category
    """
    
    def __init__(self, orderby, media, category, iconkey):
        """
        This is the constructor of the IniControl class
        ___________________________________________
        input:
            orderby         string        "folder","title","episode"
            media           string        "video", "audio", "ebook", "picture", "doc"
            category        string        "movie", "music", "show", "presentation", "alternative", "miscellaneous", "radioplay"
            iconkey         string        "key" will be converted to "media-key.png"
        """
        self.orderby = orderby
        self.media = media
        self.category = category
        self.iconkey = iconkey        
    
    def __str__(self):
        return json.dumps(self.getJson(), indent=4, sort_keys=True)
#        return "\norderby:  " + self.getOrderBy() + "\n" + "media:    " + self.getMedia() + "\n" + "category: " + self.getCategory() + "\n"
        
    def getOrderBy(self):
        return self.orderby

    def getMedia(self):
        return self.media
    
    def getCategory(self):
        return self.category
    
    def getIconKey(self):
        return self.iconkey

    def getJson(self):        
        json = {}
        json.update({} if self.orderby is None or not self.orderby else {JSON_KEY_CONTROL_ORDERBY: self.orderby})
        json.update({} if self.media is None or not self.media else {JSON_KEY_CONTROL_MEDIA: self.media})
        json.update({} if self.category is None or not self.category else {JSON_KEY_CONTROL_CATEGORY:self.category})
        json.update({} if self.iconkey is None or not self.iconkey else {JSON_KEY_CONTROL_ICONKEY: self.iconkey})
        
        return json
    
    