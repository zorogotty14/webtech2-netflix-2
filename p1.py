import sqlite3

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(id, name, photo,genre,ratings,description):
    try:
        sqliteConnection = sqlite3.connect('netflix.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO 'movies'
                                  ('id', 'name', 'photo', 'location','genre','ratings','description') VALUES (?, ?, ?, ?,?,?,?)"""

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (id, name, empPhoto, photo,genre,ratings,description)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")





insertBLOB(41, "Grudge", "gr.jpg", "Horror",5,"After a young mother murders her family in her own house a single mother and detective tries to investigate and solve the case. Later she discovers the house is cursed by a vengeful ghost that dooms those who enter it with a violent death.")
