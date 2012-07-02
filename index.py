#!/usr/bin/python

# Import modules for CGI handling 
import sys, cgi

#enable deugging
import cgitb; cgitb.enable()

# Import modules for HECA/CAI flightdata parser
from HECA import HECAParser


# Create instance of GET request
get = cgi.FieldStorage()