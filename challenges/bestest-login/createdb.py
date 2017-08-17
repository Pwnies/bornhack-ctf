import sqlite3
import os
import md5

if (not os.path.isfile("database.db")):
    try:
        con = sqlite3.connect("database.db")

        c = con.cursor()

        c.execute("""create table flags(
            flag TEXT PRIMARY KEY
        )""")
        c.execute("""create table users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )""")
        secure = md5.new("omgiamleethackzor").hexdigest()
        password = md5.new(secure).hexdigest()
        c = con.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ["admin", password])
        con.commit()
        con.close()
    except sqlite3.Error, e:
        print "Error: %s" % e
