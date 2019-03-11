import mysql.connector
import re

# Create my_db (object of class MySQLConnection), my connection to database
my_db = mysql.connector.connect(
    host='localhost',
    user='mv_app',
    passwd='1234567890.',
    database='my_vocabulary',
    autocommit=True
)

cursor = my_db.cursor()

counter = 0

# Open file en-cs.txt as dictionary
with open('en-cs.txt', encoding='utf-8') as dictionary:

    for line in dictionary:

        # Ignore lines which begin with #
        if re.search('^#', line):
            continue

        # Split line by tabs into variable items
        items = line.rstrip().split('\t')

        # When there are not at least two items, ignore this line
        if len(items) < 2:
            continue

        # First and second item is important (ignore everything else)
        # This two items are en and cz
        en, cz = items[0:2]

        # When there is some empty string in en or in cz, ignore the line
        if not en or not cz:
            continue

        if len(en) > 50 or len(cz) > 50:
            continue

        # Is the word in english?
        is_in_en = "SELECT id FROM english WHERE term = %s"
        cursor.execute(is_in_en, (en,))

        en_row = cursor.fetchone()

        # If not, insert the word into the table an remember id
        if en_row is None:
            en_insert = "INSERT INTO english (term) VALUES (%s)"
            cursor.execute(en_insert, (en,))
            id_en = cursor.lastrowid

        else:
            # When the word exists in the table, remember ID of this word
            id_en = en_row[0]

        is_in_cz = "SELECT id FROM czech WHERE term = %s"
        cursor.execute(is_in_cz, (cz,))

        cz_row = cursor.fetchone()

        if cz_row is None:
            cz_insert = "INSERT INTO czech (term) VALUES (%s)"
            cursor.execute(cz_insert, (cz,))
            id_cz = cursor.lastrowid

        else:
            id_cz = cz_row[0]

        is_in_trans = "SELECT id from translation " \
                      "WHERE czech_id = %s " \
                      "AND english_id = %s"
        cursor.execute(is_in_trans, (id_cz, id_en))

        duplicity = cursor.fetchone()

        if duplicity is None:
            translation = "INSERT INTO translation (czech_id, english_id) " \
                          "VALUES (%s, %s)"
            cursor.execute(translation, (id_cz, id_en))

            counter += 1
            if counter % 1000 == 0:
                print(f"Counter: {counter}")

cursor.close()
my_db.close()
