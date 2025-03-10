import datetime
import json

class SaveTask:
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

    def print(self):
        for item in self.tasks.items():
            print(item)

a = SaveTask()
a.update_dict('1', {'user_id': '2'})
a.update_dict('1', {'name': 'made tests for API'})
a.update_dict('1', {'description': 'testing my API'})
a.update_dict('1', {'priority': 9})

a.update_dict('1', {'name': 'asd', 'start_date': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
                    'finish_date': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))})

a.update_dict('2', {'uwiyer': 12})


Tasks: SaveTask()