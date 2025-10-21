import csv
import sqlite3

con = sqlite3.connect("friday.db")

cursor = con.cursor()


# FOR CREATING THE SYSTEM COMMANDS
# query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
# cursor.execute(query)

# FOR INSERTING
# query = "INSERT INTO sys_command VALUES (null,'wps office','C:\\Users\\KIIT\\Desktop\\WPS Office.lnk')"
# cursor.execute(query)
# con.commit()








# FOR CREATING THE WEB COMMANDS TABLE
# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# FOR INSERTING
# query = "INSERT INTO web_command VALUES (null,'youtube','https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()










# FOR CREATING CONTACTS TABLE
# cursor.execute("DROP TABLE IF EXISTS contacts_table")
# cursor.execute('''
#     CREATE TABLE contacts_table (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         mobile_no TEXT
#     )
# ''')

# Read and insert
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         try:
#             if len(row) > 20:
#                 first_name = row[0].strip()
#                 last_name = row[2].strip()
#                 mobile_no = row[20].strip()
                
#                 if not first_name and not last_name:
#                     continue
#                 if not mobile_no:
#                     continue

#                 full_name = f"{first_name} {last_name}".strip()

#                 cursor.execute('''
#                     INSERT INTO contacts_table (name, mobile_no)
#                     VALUES (?, ?)
#                 ''', (full_name, mobile_no))
#             else:
#                 print("Skipping incomplete row:", row)
#         except Exception as e:
#             print("Skipping row due to error:", e, "Row:", row)

# # Save and close
# con.commit()
# con.close()




#Search in query
# query = 'Raj Kiit'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts_table WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%' , query + '%'))
# results = cursor.fetchall()
# print(results[0][0])


query = "INSERT INTO contacts_table VALUES(null,'Robot','6289996186')"
cursor.execute(query)
con.commit()