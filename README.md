# HECA FlightBoard API 
> Cairo Internatinal Airport FlightBoard API

### About the API
This API was initaly developed as simple parser to the
unfriendly [CAI Website](http://cairo-airport.com) flight information pages for a _demo/educational_ __iOS App__ which displays HECA/CAI Arrival, Departuers Flight Boards.

### The Evelution
For the sole perposer of spportin a __RESTfull URIs__, the simple script has eveluted into a simple API.

It's not totaly a __RESTfull API__ as it's sole role to supply flight information accepting as in __PUT, POST__ or even __DELETE__ have no point to support.

### Usage
1. Run `index.py` file as Pytohn CGI script, at _line #20_
```python
# line number #20
    with open( "hello.html" , 'r') as f: 
``` 
change the `hello.html` with an html file to be displaed as defualt page when no request are passed.

2. Create an instance of the parser 
```python
CAI = HECAParser()
```

3. execute these methods depending on requested flight board and the return format.

	for JSON format:
```python
#return both flight boards in JSON format 
    CAI.HECAGetAsJSON() # @line #76
#return the arrivals flight board in JSON format 
    CAI.HECAGetArrivalAsJSON() # @line #78
#return the departure flight board in JSON format 
    CAI.HECAGetDepartureAsJSON() # @line #80
```
	for XML format:
```python
#return both flight boards in XML format
    CAI.HECAGetAsXML() # @line #86
#return the arrivals flight board in XML format
    CAI.HECAGetArrivalAsXML() # @line #88
#return the departure flight board in XML format
    CAI.HECAGetDepartureAsXML() # @line #90
```


