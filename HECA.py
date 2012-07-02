from HTMLParser import HTMLParser
from urllib import urlopen
import json




class CAIhtmlParser(HTMLParser):
    
    row = {}
    allRows = []
    columnsIndex = 0
    columnsTitle = ['airline','flight#','date','sch','eta','actual','destination','via','terminal','hall','Status']
    
    
    def handle_starttag(self, tag, attrs):
        if len(attrs) and not self.openRow:
            if tag == "tr" and attrs[0] == ('align', 'center'):
                print "$> raw OPEN"
        if tag == "td" and self.openRow:
            print "$> td OPEN"
    
    def handle_endtag(self, tag):
        if tag == "tr" and self.openRow:
            self.openRow = False
            self.columnsIndex = 0
            self.allRows.append(self.row)
        if tag == "td" and self.openRow:
            self.insertCell = False
            if self.columnsIndex == 10:
                self.columnsIndex = 0
            else:
                self.columnsIndex += 1
    
    def handle_data(self, data):
        if self.insertCell:
            self.row[ self.columnsTitle[ self.columnsIndex ] ] = data
            
    def returnRows(self):
    for row in self.allRows:
        print "\n####################################\n"
        for col in self.columnsTitle:
            print col + ": " + row[col] + "\n"
    
    def expandRow(self,row):
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
    
if __name__ == '__main__':
    
    
    print "$>   Fetching"
    
    
    f = urlopen("http://www.cairo-airport.com/flight_departure_result.asp")
    CAIdeparture = f.read()
    f.close()
    
    
    print "$>   Parsing"
    
    
    parser = CAIhtmlParser()
    parser.feed(CAIdeparture)
    parser.jsonExport()
    
    
    print "$>   total listing: "+ str( len(parser.allRows) )
    print "$>   Done"