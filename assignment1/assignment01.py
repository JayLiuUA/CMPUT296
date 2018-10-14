from binascii import unhexlify

# Your name: Xiaohui Liu
# The date: Feb 2th, 2018
# The names of any students you consulted with: Yuan Wang

# ---------------------------------------------------------------------------
#    URL parser  Copyright (C) 2018  Xiaohui Liu
#    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#    This is free software, and you are welcome to redistribute it
#    under certain conditions; type `show c' for details.
# ---------------------------------------------------------------------------


# Instructions: write a URL parser library in Python 3. This file should contain
# function that when called with a URL will return a 6-tuple of information
# about that URL: the scheme (protocol), the host, the port (or None if there
# is no port specified), the path as a list,
# the query arguments as a dictionary of lists,
# and the fragment.

# For example, if the provided URL is 
# http://localhost:8080/cats/cute/index.html?tag=fuzzy&tag=little+pawsies&show=data%26statistics#Statistics
# then your function should return the following Pythong data structure:
# (
#   'http',
#   'localhost',
#    8080,
#    [
#        'cats',
#        'cute',
#        'index.html',
#        ],
#   {
#        'tag': [
#            'fuzzy',
#            'little pawsies',
#            ],
#        'show': [
#            'data&statistics',
#            ],
#        },
#    'Statistics'
#   )

# Your function must be named parse_url. I've given you some starter code
# below. There is an accompanying file with this assignment called
# free_tests.py which you should run to test your code. It will call your
# function with various URLs and tell you whether your function returns
# the correct information or not.

# When marking your assignment I will use another file, similar to
# free_tests.py that will test your function in the same way, but using
# different URLs. Your mark on this assignment will be the fraction of
# URLs your function parses correctly. 

# If you are not familiar with tuples, dictionaries and lists in Python please,
# familiarize yourself.

# Do not forget to CITE any code you use from the web or other resources.
# YOU ARE NOT ALLOWED TO USE ANY LIBRARIES CAPABLE OF PARSING URLS OR DECODING
# PERCENT-ENCODED DATA. DOING SO WILL RESULT IN A ZERO MARK FOR THIS
# ASSIGNMENT. IF YOU ARE UNSURE WHETHER YOU CAN USE A PARTICULAR LIBRARY
# PLEASE POST ON ECLASS AND ASK. IF YOU DID NOT ASK TO USE A LIBRARY
# AND USE IT ANYWAY YOU MAY RECIEVE A ZERO MARK FOR THIS ASSIGNMENT.

# Submission instructions: Upload your version of
# this file to eClass under Assignment 1.

# Here is some code to get you started:

def find_host_port(url):
    host_starts = url.index("/") + 2
    new_url = url[host_starts:]               # cut the scheme part
    host_port_ends = new_url.index("/")
    new_url = new_url[:host_port_ends]
    if ":" in new_url:
        host_ends = new_url.index(":")
        host = new_url[0:host_ends]
        port_starts = host_ends + 1
        port_ends = len(new_url)
        port = new_url[port_starts:port_ends]    
        return host, int(port), port_ends + host_starts
    else:
        host_ends = len(new_url)
        host = new_url[0:host_ends]
        port = None
        return host, port, host_ends + host_starts
    
def find_path(url, path_starts):
    if "?" in url:
        path_ends = url.index("?")
        return path_ends, url[path_starts:path_ends].split("/")
    elif "#" in url:
        path_ends = url.index("#")
        return path_ends, url[path_starts:path_ends].split("/")
    else:
        path_ends = len(url)
        return path_ends, url[path_starts:path_ends].split("/")
    
def change_special(url):
    for i in range(len(url)):
        try:
            if url[i] == '%' and url[i+3] =='%':
                string1=url[i+1:i+3]
                string2=url[i+4:i+6]

                t= unhexlify(string1+string2).decode('utf-8')

                url=url.replace(url[i:i+6],t)
        except:
            pass 
    return url

def change(url):  
    symbol=[]
    new=""
    previous=0
    position=[i for i, j in enumerate(url) if j == '%']
    
    for i in position:
        string=url[i+1:i+3]
        
        t = unhexlify(string).decode('utf-8')
        symbol.append(t)
        
    last=url[position[-1]+3:] 
    for i in range(len(symbol)):

        new=new+url[previous:position[i]]+symbol[i]
        previous=position[i]+3
        if i == (len(symbol)-1):
            new=new+last  
    return new
    
def find_query(url, query_starts):
    if "#" in url:
        query_ends = url.index("#")
        sliced_url = url[query_starts:query_ends]
    else:
        sliced_url = url[query_starts:]
        query_ends = len(url)
    if len(sliced_url) > 0:
        space_url = sliced_url.replace("+", " ")
        query = space_url.split("&")
        for i in range(len(query)):
            query[i] = query[i].split("=")
        
        keys = []
        values = []
        for pair in query:
            keys.append(pair[0])
            values.append(pair[1])
        dic = {keys.pop(0):[values.pop(0)]}
        for i in range(len(keys)):
            if keys[i] in dic:
                dic[keys[i]].append(values[i])
            else:
                dic[keys[i]] = []
                dic[keys[i]].append(values[i])   
                
        return query_ends, dic
    else:
        dic = {}
        return query_ends, dic

def find_fragment(url, fragment_starts):
    if "#" in url:
        sliced_url = url[fragment_starts:]
        space_url = sliced_url.replace("+", " ")
        return space_url
    else:
        return None
        
def if_http(url):       # check if url starts with http
    is_http = False
    if "http" in url:
        is_http = True
    return is_http

def parse_url(url):
    is_http = if_http(url)
    if is_http:
        scheme_ends = url.index(":")
        scheme = url[0:scheme_ends]
        
        host, port, host_ends = find_host_port(url)
        
        path_starts = host_ends + 1
        path_ends, path = find_path(url, path_starts)

        for i in range(len(path)):
            if '%' in path[i]:
                path[i]=change(path[i])
        
        query_starts = path_ends + 1
        query_ends, query = find_query(url, query_starts)
              
        copy=query
        for x in range(len(url)):
            if url[x] == '%' and url[x+3] == '%':
                
                for i in query.keys():
                    if type(query[i]) == list:
                        for x in range(len(query[i])):
                            if '%' in query[i][x]:
                                query[i][x]=change_special(query[i][x])
                    elif type(query[i]) == str and '%' in query[i]:
                        query[i]=change_special(query[i])  

        if query == copy:
            for i in query.keys():
                if type(query[i]) == list:
                    for x in range(len(query[i])):
                        if '%' in query[i][x]:
                            query[i][x]=change(query[i][x])
                elif type(query[i]) == str and '%' in query[i]:
                    query[i]=change(query[i])  
                    
        fragment_starts = query_ends + 1
        fragment = find_fragment(url, fragment_starts)
        if fragment != None and '%' in fragment:
            fragment=change(fragment)        
        
        return (
            scheme,
            host,
            port,
            path,
            query,
            fragment
        )        
        
    else:
        index = url.index(":")
        scheme = url[0:index]
        return (
            scheme,
            None,
            None,
            None,
            None,
            None
    )

    
    
