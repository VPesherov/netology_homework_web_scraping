import json


class JsonClass:
    def __init__(self, data, file_name):
        self.json_data = data
        self.file_name = file_name

    def write_in_json(self):
        with open(self.file_name, 'w', encoding='utf-8', newline="") as f:
            json.dump(self.json_data, f, ensure_ascii=False)
