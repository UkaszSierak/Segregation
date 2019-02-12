import sqlite3



def CreateTable():
    conn = sqlite3.connect('objects.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ratioValues(object TXT, img_path TXT, view TXT, ratio REAL)')

def DataEntry():
    conn = sqlite3.connect('objects.db')
    c = conn.cursor()
    c.execute("INSERT INTO ratioValues VALUES('klocek', 'klocek_side_view.jpg', 1, 0.56  )")
    conn.commit()


def DynamicDataEntry(obj, path, view, ratio):
    conn = sqlite3.connect('objects.db')
    c = conn.cursor()

    c.execute("INSERT INTO ratioValues (object, img_path, view, ratio) VALUES(?,?,?,?)",
              (obj, path, view, ratio))
    conn.commit()

def ReadFromDB():
    conn = sqlite3.connect('objects.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ratioValues')
    data = c.fetchall()
    c.close()
    conn.close()

    return data
def Close():
    conn = sqlite3.connect('objects.db')
    c = conn.cursor()
    c.close()
    conn.close()

#CreateTable()
#DataEntry()
#DynamicDataEntry()
#ReadFromDB()
