import sqlite3

#Creating the SQLite file
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
# count = 0
for line in fh:

    #Creating the list of all the files starting from 'From: '
    if not line.startswith('From: '): continue
    email = line.split('@')


    #for checking the values
    # count = count + 1
    # print(count)
    # print(email[1])

    #Condition
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (email[1],))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (email[1],))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (email[1],))
    conn.commit()

# Printing the values
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
