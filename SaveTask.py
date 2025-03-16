import datetime
import json
from aiogram.filters import Filter

class SaveTask(Filter):
    '''
    Класс для сохранения и изменения списка задач для пользователей\n
    :param tasks (dict): список в котором хранится\n
    :param key (str): ID пользователя\n
    :param value (dict): остальные данные по типу: <b>user_id, task_name, task_description, start_date_task, end_date_task </b>и<b> priority</b>
    '''
    def __init__(self):
        self.tasks = {str: {}}
        del self.tasks[str]

    async def update_dict(self, user_id: str, data: {}):
        '''
        <i>Этот метод обновляет или добавляет новый список по 'user_id'</i>\n 
        :param user_id (str): ID пользователя
        :param data (dict): Данные для добавления/обновления
        '''
        try:
            if self.tasks.get(user_id):
                current_data = self.tasks.get(user_id)
                current_data.update(data)
                self.tasks[user_id] = current_data
            else:
                self.tasks.update({user_id: data})
        except Exception as e:
            print(f'Error occurred while updating dictionary: {str(e)}')

    async def delete_id(self, user_id: str):
        '''
        <i>Этот метод удаляет список по 'user_id', если его нету то он выикдывает ошибку</i>\n
        :param user_id (str): ID пользователя
        '''
        try:
            del self.tasks[user_id]
        except Exception as e:
            print(f'Error occurred while deleting ID: {str(e)}')

    async def find_element_by_user_id(self, user_id):
        '''
        <i>Этот метод возвращает список по 'user_id', если его нету то он выикдывает ошибку</i>\n
        :param user_id (str): ID пользователя
        :return: dict
        '''
        try:
            return self.tasks[user_id]
        except Exception as e:
            print(f'Error occurred while finding ID: {str(e)}')

    async def convert_to_json(self):
        '''
        <i>Этот метод возвращает список в формате JSON, если что-то пошло не так, он выкидывает ошибку но не завершает программу</i>\n
        :return: JSON
        '''
        try:
            return json.dumps(self.tasks, indent=4)
        except Exception as e:
            print(f'Error occurred while converting to JSON: {str(e)}')

    async def print(self):
        '''
        <i>Этот метод выводит список в консоль</i>\n
        '''
        try:
            for item in self.tasks.items():
                print(item)
        except Exception as e:
            print(f'Error occurred while printing: {str(e)}')
        
    
    # TODO до конца не уверен рабоатет это или нет, надо будет проверить, я не до конца понимаю как работает __call__
    async def __call__(self, user_id: str, key: str):
        ''' 
        <i>Этот метод возвращает True если по 'user_id' есть 'key' который имеет значение, иначе False</i>\n
        :param user_id (str): ID пользователя
        :param key (str): ключ
        :return: bool
        '''
        return self.tasks[user_id].get(key) is not None


'''Example usage:
a = SaveTask()
a.update_dict('1', {'user_id': '2'})
a.update_dict('1', {'name': 'made tests for API'})
a.update_dict('1', {'description': 'testing my API'})
a.update_dict('1', {'priority': 9})

a.update_dict('1', 
{'name': 'asd', 
'start_date': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")),
'finish_date': str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))})

a.update_dict('2', {'uwiyer': 12})
'''