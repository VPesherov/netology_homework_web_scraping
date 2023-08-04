from classes.JsonClass import JsonClass
from applications.functions import find_vacancy


def main():
    file_name = 'vacancy.json'
    data = find_vacancy()
    json_instance = JsonClass(data, file_name)
    json_instance.write_in_json()


if __name__ == '__main__':
    main()
