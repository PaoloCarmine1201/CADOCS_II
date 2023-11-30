import json
class customException(Exception):
    def __init__(self, input_list, list_name):
        super().__init__(f"ERROR: The list {list_name} is empty")
        self.list_name = list_name
        self.input_list = input_list

    def printError(self):
        if not self.input_list:
            raise self

    def to_json(self):
        error_message = str(self)
        if not self.input_list:
            error_message = "List is empty"

        return json.dumps({
            "error": error_message,
            "list_name": self.list_name
        })