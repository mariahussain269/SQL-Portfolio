
# importing urllib capabilities to enable requesting of http requests and parsing including handling any URL errors


import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import ssl


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# Prompting for a URL

counter = 0 

url = input('Enter - ')

# read the XML data from the previous URL using urllib


data = urlopen(url, context=ctx).read()
print('Retrieved', len(data), 'characters')
#print(data.decode())


#  parse and extract the comment counts from the XML data 

tree = ET.fromstring(data)


lst = tree.findall('comments/comment')
#print('User count:', len(lst))


for item in lst:
    sloo= float((item.find('count').text))
    counter += sloo


print('Total: ', counter)



