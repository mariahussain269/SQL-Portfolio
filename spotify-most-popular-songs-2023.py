#For this project, I used python to connect to SQL and create tables and insert data from a Spotify dataset downloaded from Kaggle. I then analyzed the data using SQL


import sqlite3
import csv

conn = sqlite3.connect('spotdb.sqlite')
cur = conn.cursor()

# Creating some fresh SQL tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Year;
DROP TABLE IF EXISTS Streams;
DROP TABLE IF EXISTS Track;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);


CREATE TABLE Year (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    yearname   INTEGER 
);

CREATE TABLE Streams (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    number  INTEGER UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT,
    year_id  INTEGER,
    streams_id  INTEGER,
    artist_id INTEGER
);

''')


handle = open('spotify-2023.csv')


#Parsing and inserting select data from Spotify csv file into the table using python 

with open('spotify-2023.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row if it exists
    for row in csvreader:
        if len(row) < 17: continue
        name = row[0]
        artist = row[1]
        releaseyear = row[3]
        numberofstreams = row[8]     
        #print(name, artist, releaseyear, spotifyplaylists, numberofstreams)

        
        cur.execute('''INSERT OR IGNORE INTO Artist (name) 
            VALUES ( ? )''', ( artist, ) )
        cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
        artist_id = cur.fetchone()[0]
    
        cur.execute('''INSERT OR IGNORE INTO Year (yearname) 
            VALUES ( ? )''', ( releaseyear, ) )
        cur.execute('SELECT id FROM Year WHERE yearname = ? ', (releaseyear, ))
        year_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Streams (number, artist_id) 
            VALUES ( ?, ? )''', ( numberofstreams, artist_id ) )
        cur.execute('SELECT id FROM Streams WHERE number = ? ', (numberofstreams, ))
        streams_id = cur.fetchone()[0]

        cur.execute('''INSERT OR REPLACE INTO Track
            (title, year_id, streams_id, artist_id) 
            VALUES ( ?, ?, ?, ? )''', 
            ( name, year_id, streams_id, artist_id ) )
    

conn.commit()

# Analyzing and exploring the data using the following SQL to determine the most streamed Spotify tracks as of 2023

SELECT name, title, number, yearname
FROM Track
JOIN Artist on Track.artist_id = Artist.id
JOIN Streams on Track.streams_id = Streams.id
JOIN Year on Track.year_id = Year.id
GROUP BY title, name
ORDER BY number desc







