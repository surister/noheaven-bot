import sqlite3
import string
import random
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''
CREATE TABLE todo 
(int DEFAULT primary unique id, message_text text, boolean default false finished)''')


s = "".join([random.choices(string.ascii_letters)[0] for s in range(0, 20)])
print(s)


for _ in range(0, 10):
    c.execute('''
    INSERT INTO todo (id, TEXT, finished) VALUES (DEFAULT, s, DEFAULT)

    ''')

