import sqlite3
conn=sqlite3.connect("javis.db")
cursor=conn.cursor()

# query="CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY ,name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)
# query="CREATE TABLE IF NOT EXISTS web_command (id INTEGER PRIMARY KEY ,name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)
# query="CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY ,name VARCHAR(200),email VARCHAR(200),phone VARCHAR(20))"
# cursor.execute(query)

# query = "INSERT INTO sys_command (name, path) VALUES (?, ?)"
# values = (
#     "whatsapp",
#     'Start-Process "shell:appsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"'
# )
# cursor.execute(query, values)

query = "INSERT INTO sys_command (name,path) VALUES ('whatsapp','D:\\OneDrive\\Desktop\\WhatsApp.lnk')"
cursor.execute(query)

# query="INSERT INTO web_command (name,url) VALUES ('whatsapp','https://web.whatsapp.com/')"
# cursor.execute(query)
# query="delete from sys_command where name='whatsapp'"
# cursor.execute(query)

# values = [
#     (1,"Appa","tukaram@gmail.com",9980756589),
#     (2,"amma","suvarna@gmail.com",9731974591),
#     (3,"dayanand","dayanand@gmail.com",6360901414),
#     (4,"rajshekhar","rajashekharkakhandaki8@gmail.com",6360803162)
# ]

# # insert many
# cursor.executemany("INSERT INTO contacts VALUES (?, ?,?,?)", values)
conn.commit()

conn.close()