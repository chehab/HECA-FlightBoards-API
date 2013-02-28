# -*- coding: UTF-8 -*-
#!/usr/bin/python
import sys

class HECATheme:

    
    __sectionA  = None
    __sectionB  = None
    __alert     = None
    __page      = None

    __head_lst__ = []
    
    def echo(self):
        self.__cat_all__()
        if self.__alert:
            self.__page = self.__sectionA + self.__alert + self.__sectionB
        else:
            self.__page = self.__sectionA + self.__sectionB
        return self.__page
    
    def __cat_all__(self):
        #A
        self._genHead()
        self._genNavBar()
        #B
        self._genHeroUnit()
        self._genRows()
        self._genFooter()
        
    def _genHead(self):
        self.__sectionA = "Content-type: text/html\r\n"
        self.__sectionA += "Content-Encoding: UTF8\r\n\r\n"
        self.__sectionA += self.__loadfile("theme/0-head.html")
        
        for mt in __head_lst__:
            self.__sectionA += mt

        self.__sectionA += "  </head>"
    
    def _genNavBar(self):
        self.__sectionA += self.__loadfile("theme/1-navbar.html")
    
    def alert(self, type, title=None, msg=None):
        self.__alert = ""
        self.__alert += self.__loadfile("theme/2-alert.html").format( \
        type=type, title=title, msg=msg )
    
    def pageRefresh(seconds, url=None):
        url = ";url="+url if url else ""
        metatag = '<meta http-equiv="refresh" content="{}{}">'
        self.__head_lst__.append( metatag.format(seconds,url) )

    def addMetaTag(htmltag):
        self.__head_lst__.append( htmltag )

    def _genHeroUnit(self):
        self.__sectionB = ""
        self.__sectionB += self.__loadfile("theme/3-hero-unit.html")
    
    def _genRows(self):
        self.__sectionB += self.__loadfile("theme/4-rows.html")
    
    def _genFooter(self):
        self.__sectionB += self.__loadfile("theme/5-footer.html")
    
    def __loadfile(self,filepath):
        with open( filepath , 'r') as f:
            read_data = f.read()
        f.closed
        return read_data
        
    