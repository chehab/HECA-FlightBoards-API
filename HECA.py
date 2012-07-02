from HTMLParser import HTMLParser
from urllib import urlopen
import json




class CAIhtmlParser(HTMLParser):
    
    allRows = []
    row = {}
    openRow = False
    insertCell = False
    PrintView = False
    insertCount = 0
    columnsIndex = 0
    airportTitle = "Airport" # 'destination/origin'
    columnsTitle = ['airline','flightno','date','sch','eta','actual',"airport",'via','terminal','hall','status']
    
    
    def handle_starttag(self, tag, attrs):
        if len(attrs) and not self.openRow:
            if tag == "tr" and attrs[0] == ('align', 'center'):
                self.openRow = True
                self.row = {'airline':"",'flightno':"",'date':"",'sch':"",'eta':"",'actual':"",
                            "airport":"",'via':"",'terminal':"",'hall':"",'status':""}
                if self.PrintView:
                    print "\n\n\nopenRow\n"
        if tag == "td" and self.openRow:
            self.insertCell = True
    
    def handle_endtag(self, tag):
        if tag == "tr" and self.openRow:
            self.openRow = False
            self.columnsIndex = 0
            if self.PrintView:
                print "Saving Row: "
                self.expandRow(self.row)
                print "Row closed"
            self.allRows.append(self.row)
        if tag == "td" and self.openRow:
            self.insertCell = False
            if self.columnsIndex == 10:
                self.columnsIndex = 0
            else:
                self.columnsIndex += 1
    
    def handle_data(self, data):
        fieldData = ''
        for i in range(len(data)):
            if data[i] != '\n' and data[i] != '\r' and data[i] != '\t' and data[i] != '  ':
                fieldData += data[i]
        if self.insertCell:
            self.row[ self.columnsTitle[ self.columnsIndex ] ] = fieldData.strip()
            
    def returnRows(self):
        if self.PrintView:
            for row in self.allRows:
                print "\n####################################\n"
                for col in self.columnsTitle:
                    print col + ": " + row[col] + "\n"
                    
    def expandRow(self,row):
        if self.PrintView:
            print "####################################\n"
            for col in self.columnsTitle:
                print col + ": " + row[col] + "\n"
            print "####################################"
        
    def jsonExport(self, filename = 'JSON'):
        f = open( filename, 'w')
        f.write("")
        f.close()
        f = open( filename, 'a')
        f.write( json.dumps( self.allRows ) )
        f.close()
        
    def CAIDepartureJSONExport(self):
        filename = "departure.json"
        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        CAI = f.read()
        f.close()

        parser = CAIhtmlParser()
        parser.feed(CAI)    

        f = open( filename, 'w')
        f.write("")
        f.close()
        f = open( filename, 'a')
        f.write( json.dumps( parser.allRows ) )
        f.close()

        return "Departure Exported..."
        
    def CAIArrivalJSONExport(self):
        filename = "arrival.json"
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        CAI = f.read()
        f.close()

        parser = CAIhtmlParser()
        parser.feed(CAI)    

        f = open( filename, 'w')
        f.write("")
        f.close()
        f = open( filename, 'a')
        f.write( json.dumps( parser.allRows ) )
        f.close()

        return "Arrival Exported..."
    
    def CAIDepartureExport(self):
        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        CAI = f.read()
        f.close()

        parser = CAIhtmlParser()
        parser.feed(CAI)    

        return json.dumps( parser.allRows )

    def CAIArrivalExport(self):
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        CAI = f.read()
        f.close()

        parser = CAIhtmlParser()
        parser.feed(CAI)    

        return json.dumps( parser.allRows )


    def CAIArrivalInstance(self):
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        CAI = f.read()
        f.close()

        arrival = CAIhtmlParser()
        arrival.feed(CAI)

        return arrival

    def CAIDepartureInstance(self):
        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        CAI = f.read()
        f.close()

        departure = CAIhtmlParser()
        departure.feed(CAI)

        return departure        

    def CAIreturnJSON(self):
        f = urlopen("http://www.cairo-airport.com/flight_arrival_result.asp")
        CAI = f.read()
        f.close()

        arrival = CAIhtmlParser()
        arrival.feed(CAI)    

        f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
        CAI = f.read()
        f.close()

        departure = CAIhtmlParser()
        departure.feed(CAI) 

        return json.dumps( { "arrival":arrival.allRows, "departure":departure.allRows } )

    def CAIReturnArrivalXML(self):
        arrival = self.CAIArrivalInstance()

        xmlexport = "\n <arrival>\n"

        for fl in arrival.allRows:

            xmlexport += "\n  <flight>\n\n"

            for key in arrival.columnsTitle:
                #if len(fl[key]) != 0:
                xmlexport += "   <{}>{}</{}>\n".format(key, fl[key], key) 

            xmlexport += "\n  </flight>\n"

        xmlexport += "\n </arrival>\n"

        return xmlexport

    def CAIReturnDepartureXML(self):
        departure = self.CAIDepartureInstance()

        xmlexport = "\n <departure>\n"

        for fl in departure.allRows:

            xmlexport += "\n  <flight>\n\n"

            for key in departure.columnsTitle:
                #if len(fl[key]) != 0:
                xmlexport += "   <{}>{}</{}>\n".format(key, fl[key], key)

            xmlexport += "  </flight>\n"

        xmlexport += "\n </departure>\n"

        return xmlexport

    def CAIReturnXML(self):
        xmlexport = '<?xml version="1.0"?>\n'
        xmlexport += "<HECA>\n"
        xmlexport += "{}".format( self.CAIReturnArrivalXML() )
        xmlexport += "{}".format( self.CAIReturnDepartureXML() )
        xmlexport += "\n</HECA>"
        return xmlexport


    
if __name__ == '__main__':
    
    CAI = CAIhtmlParser()
    print CAI.CAIReturnDepartureXML()
    
    print "$>   End"