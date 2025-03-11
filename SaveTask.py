import datetime
import json

class SaveTask: # TODO сделать методы асинхронными, которые позволили бы большому кол-ству пользователей вводить данные
    def __init__(self):
        self.tasks = {str: {}}
        del self.tasks[str]

    def update_dict(self, user_id: str, data: {}):

        if self.tasks.get(user_id):
            current_data = self.tasks.get(user_id)
            current_data.update(data)
            self.tasks[user_id] = current_data
        else:
            self.tasks.update({user_id: data})

    def delete_id(self, user_id: str):
        del self.tasks[user_id]

    def find_element_by_user_id(self, user_id):
        return self.tasks[user_id]

    def convert_to_json(self):
        return json.dumps(self.tasks, indent=4)

    def print(self): # выводит все задачи которые есть
        for item in self.tasks.items():
            print(item)