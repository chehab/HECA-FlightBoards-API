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
    
if __name__ == '__main__':
    
    CAI = CAIhtmlParser()
    print CAI.CAIArrivalJSONExport()
    
    print "$>   End"