import csv

file_name = "friends.csv"


class Row:

    def __init__(self, classmate_id, classmate_name, friend_id, friend_name, friend_of_friend_id,
                 friend_of_friend_name):
        self.classmate_id = classmate_id
        self.classmate_name = classmate_name
        self.friend_id = friend_id
        self.friend_name = friend_name
        self.friend_of_friend_id = friend_of_friend_id
        self.friend_of_friend_name = friend_of_friend_name

    pass


def export(rows):
    print('start export to file')
    file = open(file_name, 'w', newline='', encoding="utf-8")

    writer = csv.writer(file, delimiter=';')

    for row in rows:
        try:
            writer.writerow(
                [row.classmate_id,
                 row.classmate_name,
                 row.friend_id,
                 row.friend_name,
                 row.friend_of_friend_id,
                 row.friend_of_friend_name])
        except Exception as e:
            print(e)


def import_file():
    print('start import from file')
    rows = []
    try:
        #открываем файл на чтение
        with open(file_name, 'r', newline='', encoding="utf-8") as file:
            csvreader = csv.reader(file, delimiter=';')
            for row in csvreader:
                if len(row) < 5:
                    continue
                rows.append(Row(row[0], row[1], row[2], row[3], row[4], row[5]))
    except Exception as e:
        print(f"File {file_name} is not exist")
        print(e)

    return rows
