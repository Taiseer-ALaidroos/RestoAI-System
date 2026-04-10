import sqlite3

# إنشاء أو الاتصال بقاعدة البيانات
conn = sqlite3.connect("restaurant.db")
cursor = conn.cursor()

# إنشاء جدول الموظفين إذا لم يكن موجودًا
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    name TEXT NOT NULL,
    password INTEGER NOT NULL,
    phone TEXT NOT NULL           
)
""")
name="Aiham"
password="1234"
phone="773840302"

name1="Mohammed-sheply"
password1="1234"
phone1="775451608"

name2="Taiseer"
password2="1212"
phone2="775088208"

name3="Raed"
password3="1212"
phone3="781491119"

cursor.execute("INSERT INTO users (name, password , phone) VALUES (?, ? ,?)", 
                    (name, password,phone))
cursor.execute("INSERT INTO users (name, password , phone) VALUES (?, ? ,?)", 
                    (name1, password1,phone1))
cursor.execute("INSERT INTO users (name, password , phone) VALUES (?, ?,?)", 
                    (name2, password2,phone2))
cursor.execute("INSERT INTO users (name, password , phone) VALUES (?, ?,?)", 
                    (name3, password3,phone3))


conn.commit()
conn.close()
print("تم إنشاء قاعدة البيانات وجدول الموظفين بنجاح!")