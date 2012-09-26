# -*- coding: UTF-8 -*-
#!/usr/bin/python

# Import modules for CGI handling 
import sys, cgi

#enable deugging
import cgitb; cgitb.enable()

# Import modules for HECA/CAI flightdata parser
from HECAlib import HECAParser


# Create instance of GET request
GET = cgi.FieldStorage()


### No Request render a html page.
if len(GET.keys()) == 0:
    with open( "templetes/hello.html" , 'r') as f:
        read_data = f.read()
    f.closed
    print "Content-type: text/html\r\n\r\n"
    print read_data
### Process Request 
else:
    returnType = None 
    flightData = None
    try:
        for ky in GET.keys():
        ### format=flight ################################################
            if ky == 'json':
                returnType = "json"
                if GET[ky].value == "arrival":
                    flightData = "arrival"; continue
                elif GET[ky].value == "departure":
                    flightData = "departure"; continue
                elif GET[ky].value == "both" or GET[ky].value == "all":
                    flightData = "both"; continue
            ################################################
            if ky == 'xml':
                returnType = "xml"
                if GET[ky].value == "arrival":
                    flightData = "arrival"; continue
                elif GET[ky].value == "departure":
                    flightData = "departure"; continue
                elif GET[ky].value == "both" or GET[ky].value == "all":
                    flightData = "both"; continue
        ### flight=format ################################################
            if ky == 'arrival':
                flightData = "arrival"
                if GET[ky].value == "json":
                    returnType = "json"; continue
                elif GET[ky].value == "xml":
                    returnType = "xml"; continue
            ################################################
            if ky == 'departure':
                flightData = "departure"
                if GET[ky].value == "json":
                    returnType = "json"; continue
                elif GET[ky].value == "xml":
                    returnType = "xml"; continue
        ################################################### GET request ###
    except Exception as inst:
        with open( "templaltes/head.html" , 'r') as f:
            read_data = f.read()
        f.closed
        print "Status: "+statusCode+"\r\nContent-Type: text/html\r\n\r\n"
        print read_data
        print '<h1 style="font-size: 50px;">'+statusCode+'</h1>'
        print '<h2 style="font-weight: bold;">An Error was Encountered,'
        print "<br/>Check your Requested Parameter and Authentication.</h2>"
        print type(inst)
        print inst.args
        print inst
        print '<h2> Contact <a href="mailto:apis@chehab.me">  apis@chehab.me  </a>  </h2>'
    except:
        with open( "templaltes/head.html" , 'r') as f:
            read_data = f.read()
        f.closed
        print "Status: "+statusCode+"\r\nContent-Type: text/html\r\n\r\n"
        print read_data
        print '<h1 style="font-size: 50px;">'+statusCode+'</h1>'
        print '<h2 style="font-weight: bold;">An Error was Encountered,'
        print "<br/>Check your Requested Parameter and Authentication."
        print '<br/><br/> Contact <a href="mailto:apis@chehab.me">  apis@chehab.me  </a>  </h2>'
    
    
    #######################################################################################
    ### Returing Request ##################################################################
    try:
        CAI = HECAParser()
        ### Returing JSON #################################################################
        if returnType == "json":
            print "Content-type: application/json"#; print
            print "Content-Encoding: UTF8"; print
            if flightData == "both":
                print CAI.HECAGetAsJSON()
            elif flightData == "arrival":
                print CAI.HECAGetArrivalAsJSON()
            elif flightData == "departure":
                print CAI.HECAGetDepartureAsJSON()
        ### Returing XML ##################################################################
        if returnType == "xml":
            print "Content-type: application/xml"
            print "Content-Encoding: UTF8"; print
            if flightData == "both":
                print CAI.HECAGetAsXML()
            elif flightData == "arrival":
                print CAI.HECAGetArrivalAsXML()
            elif flightData == "departure":
                print CAI.HECAGetDepartureAsXML()
    except:
        with open( "templaltes/head.html" , 'r') as f:
            read_data = f.read()
        f.closed
        print "Status: "+statusCode+"\r\nContent-Type: text/html\r\n\r\n"
        print read_data
        print '<h1 style="font-size: 50px;">'+statusCode+'</h1>'
        print '<h2 style="font-weight: bold;">An Error was Encountered,'
        print "<br/>Try Agian Later."
        print '<br/><br/> Contact <a href="mailto:apis@chehab.me">  apis@chehab.me  </a>  </h2>'
    