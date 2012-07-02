from HTMLParser import HTMLParser
from urllib import urlopen
import json

def enum(**enums):
    return type('Enum', (), enums)


class HECAParser(HTMLParser):
# '''
#     subclasing HTMLParser to customize HECA parsing results
#     and provide more custom methods HECA specific  
# '''    

    #Def enums 
    HECAHeading = enum(Arrival=0, Departure=1, Both=2)
    HECAFormat  = enum(JSON=0, XML=1, Plain=2)
    DebugMode   = enum(Off=False, On=True, Verbose=2, file=3)

    #####################
    flight        = {}
    # flightsList   = []
    arrivalList   = []
    departureList = []
    flightTemplet = {"airline":"","flightno":"","date":"","sch":"","eta":"","actual":"",
                     "airport":"","via":"","terminal":"","hall":"","status":""}

    #####################
    flightmode   = None
    insertIndex  = 0
    currentIndex = 0
    titles = ['airline','flightno','date','sch','eta','actual',"airport",'via','terminal','hall','status']

    #####################
    openRow     = False
    insertCell  = False
    debug       = DebugMode.Off


##########################################################################################
### Perant over-ride #####################################################################


    def handle_starttag(self, tag, attrs):
        #Open New Raw in case "<tr align=center>"
        if len(attrs) and not self.openRow:
            if tag == "tr" and attrs[0] == ('align', 'center'):
                self.openRow = True
                self.flight = {"airline":"","flightno":"","date":"","sch":"","eta":"","actual":"",
                                 "airport":"","via":"","terminal":"","hall":"","status":""}
        #New Cell if Raw Open add <td> tag found
        self.insertCell = True if tag == "td" and self.openRow else False


    def handle_endtag(self, tag):
        if tag == "tr" and self.openRow:
            self.openRow = False
            self.currentIndex = 0
            self.__debug_flight__()
            # if self.flightmode == None:
            #     self.flightsList.append(self.flight)
            if self.flightmode == self.HECAHeading.Arrival:
                self.arrivalList.append(self.flight)
            if self.flightmode == self.HECAHeading.Departure:
                self.departureList.append(self.flight)
        if tag == "td" and self.openRow:
            self.insertCell = False
            if self.currentIndex == 10:
                self.currentIndex = 0
            else:
                self.currentIndex += 1


    def handle_data(self, data):
        fieldData = ''
        for i in range(len(data)):
            if data[i] != '\n' and data[i] != '\r' and data[i] != '\t' and data[i] != '  ':
                fieldData += data[i]
        if self.insertCell:
            self.flight[ self.titles[ self.currentIndex ] ] = fieldData.strip()     


##########################################################################################
### Generate #############################################################################


    def HECARefreshFlightData(self):
        self.HECAGenerateFlightData()
    

    def HECAUpdateFlightData(self):
        self.HECAGenerateFlightData()
    

    def HECAGenerateFlightData(self):
        if self.debug:
            print " %>Parsing Flight Data"
        self.HECAGenerateArrival()
        self.HECAGenerateDeparture()
    

    def HECAGenerateArrival(self,):
        if self.debug:
            print " %>Parsing Arrival Data"
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        self.flightmode = self.HECAHeading.Arrival
        self.feed( f.read() )
        f.close()
        self.flightmode = None
        self.arrivalList.reverse()
    

    def HECAGenerateDeparture(self,):
        if self.debug:
            print " %>Parsing Departure Data"
        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        self.flightmode = self.HECAHeading.Departure
        self.feed( f.read() )
        f.close()
        self.flightmode = None
        self.departureList.reverse()
    

##########################################################################################
### Return JSON ##########################################################################


    def HECAGetAsJSON(self, _heading = HECAHeading.Both):
        if self.debug:
            print " %>Generating JSON"            
        if _heading == self.HECAHeading.Departure:
            if not self.departureList:
                self.HECAGenerateDeparture()
            return json.dumps( { "departure":self.departureList } )
        if _heading == self.HECAHeading.Arrival:
            if not self.arrivalList:
                self.HECAGenerateArrival()
            return json.dumps( { "arrival":self.arrivalList } )
        if _heading == self.HECAHeading.Both:
            if not self.arrivalList and not self.departureList:
                self.HECAGenerateFlightData()
            return json.dumps( { "arrival":self.arrivalList, "departure":self.departureList } )
    

    def HECAGetArrivalAsJSON(self):
        if self.debug:
            print " %>Generating Arrival JSON"
        if not self.arrivalList:
            self.HECAGenerateArrival()
        return json.dumps( {"Arrival":self.arrivalList} )
    

    def HECAGetDepartureAsJSON(self):
        if self.debug:
            print " %>Generating Departure JSON"
        if not self.departureList:
            self.HECAGenerateDeparture()
        return json.dumps( {"departure":self.departureList} )
    

##########################################################################################
### debug ################################################################################


    def __writeToFile__(self, filename, writedata):
        f = open( filename, 'w')
        f.write("")
        f.close()
        f = open( filename, 'w')
        f.write( writedata )
        f.close()


    def __debug_flightList__(self, force=False):
        if force or self.debug == self.DebugMode.Verbose:
            # for row in self.flightsList:
            for row in self.arrivalList:
                print "\n####################################\n"
                for cell in self.titles:
                    print "   "+ cell + ": " + row[cell] + "\n"


    def __debug_flight__(self, force=False):
        if force or self.debug == self.DebugMode.Verbose:
            print " %>openRow ###########################\n"
            for col in self.titles:
                print "   "+ col + ": " + self.flight[col] + "\n"
            print "######################################\n"
                        
    #                     
    #                     
    #     
    # def jsonExport(self, filename = 'JSON'):
    #     f = open( filename, 'w')
    #     f.write("")
    #     f.close()
    #     f = open( filename, 'a')
    #     f.write( json.dumps( self.allRows ) )
    #     f.close()
    #     
    # def CAIDepartureJSONExport(self):
    #     filename = "departure.json"
    #     f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     parser = CAIhtmlParser()
    #     parser.feed(CAI)    
    # 
    #     f = open( filename, 'w')
    #     f.write("")
    #     f.close()
    #     f = open( filename, 'a')
    #     f.write( json.dumps( parser.allRows ) )
    #     f.close()
    # 
    #     return "Departure Exported..."
    #     
    # def CAIArrivalJSONExport(self):
    #     filename = "arrival.json"
    #     f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     parser = CAIhtmlParser()
    #     parser.feed(CAI)    
    # 
    #     f = open( filename, 'w')
    #     f.write("")
    #     f.close()
    #     f = open( filename, 'a')
    #     f.write( json.dumps( parser.allRows ) )
    #     f.close()
    # 
    #     return "Arrival Exported..."
    # 
    # def CAIDepartureExport(self):
    #     f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     parser = CAIhtmlParser()
    #     parser.feed(CAI)    
    # 
    #     return json.dumps( parser.allRows )
    # 
    # def CAIArrivalExport(self):
    #     f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     parser = CAIhtmlParser()
    #     parser.feed(CAI)    
    # 
    #     return json.dumps( parser.allRows )
    # 
    # 
    # def CAIArrivalInstance(self):
    #     f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     arrival = CAIhtmlParser()
    #     arrival.feed(CAI)
    # 
    #     return arrival
    # 
    # def CAIDepartureInstance(self):
    #     f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     departure = CAIhtmlParser()
    #     departure.feed(CAI)
    # 
    #     return departure        
    # 
    # def CAIreturnJSON(self):
    #     f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     arrival = CAIhtmlParser()
    #     arrival.feed(CAI)    
    # 
    #     f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
    #     CAI = f.read()
    #     f.close()
    # 
    #     departure = CAIhtmlParser()
    #     departure.feed(CAI) 
    # 
    #     return json.dumps( { "arrival":arrival.allRows, "departure":departure.allRows } )
    # 
    # def CAIReturnArrivalXML(self):
    #     arrival = self.CAIArrivalInstance()
    # 
    #     xmlexport = "\n <arrival>\n"
    # 
    #     for fl in arrival.allRows:
    # 
    #         xmlexport += "\n  <flight>\n\n"
    # 
    #         for key in arrival.columnsTitle:
    #             #if len(fl[key]) != 0:
    #             xmlexport += "   <{}>{}</{}>\n".format(key, fl[key], key) 
    # 
    #         xmlexport += "\n  </flight>\n"
    # 
    #     xmlexport += "\n </arrival>\n"
    # 
    #     return xmlexport
    # 
    # def CAIReturnDepartureXML(self):
    #     departure = self.CAIDepartureInstance()
    # 
    #     xmlexport = "\n <departure>\n"
    # 
    #     for fl in departure.allRows:
    # 
    #         xmlexport += "\n  <flight>\n\n"
    # 
    #         for key in departure.columnsTitle:
    #             #if len(fl[key]) != 0:
    #             xmlexport += "   <{}>{}</{}>\n".format(key, fl[key], key)
    # 
    #         xmlexport += "  </flight>\n"
    # 
    #     xmlexport += "\n </departure>\n"
    # 
    #     return xmlexport
    # 
    # def CAIReturnXML(self):
    #     xmlexport = '<?xml version="1.0"?>\n'
    #     xmlexport += "<HECA>\n"
    #     xmlexport += "{}".format( self.CAIReturnArrivalXML() )
    #     xmlexport += "{}".format( self.CAIReturnDepartureXML() )
    #     xmlexport += "\n</HECA>"
    #     return xmlexport


    
if __name__ == '__main__':
    
    # CAI = CAIhtmlParser()
    # print CAI.CAIReturnDepartureXML()
    # 
    # print "$>   End"