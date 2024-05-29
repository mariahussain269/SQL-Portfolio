
#Here, I've opened a URL and extracted the text from the webpage to be written to a text file. 
#I then used SQL to insert this into a table and analyse the most active organisations in the email chain by locating how many instances of each organisation email occured


#Importing necessary tools 
import urllib.request, urllib.parse, urllib.error
import sqlite3
import ssl


# Ignore SSL certificate errors for https
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# here we have to pass url and path where we want to save our text file

url = 'https://raw.githubusercontent.com/mariahussain269/SQL-Portfolio/main/mbox.txt'
fhand = urllib.request.urlopen(url, context=ctx)


conn = sqlite3.connect('webscrape.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')


for line in fhand:
    words =(line.decode().strip())
    if not words.startswith('From: '): continue
    words = words.split()
    email = (words[1])
    org = email.split('@')[1]
    
 #Connecting to SQL and inserting each organisation to a row in a table and counting instances of these

    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
        VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                (org,))
    conn.commit()

# finding the top ten organisations in email chain ( https://www.sqlite.org/lang_select.html )
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()