from enum import Enum
class TypeMessage(Enum):
    WriteTextFound = 1
    TaskAdded = 2
    TaskDeleted = 3
    NeedLetters = 4
    TaskExist = 5
    Nonexistent = 6
    TaskUpdated = 7
    ShowTasks = 8
    TaskUpdate = 9
    TaskDelete = 10
    TaskAdd = 11
    ModifyLanguage = 12
    LanguageModified = 13
    WelcomeBack = 14
    ThisBotStarted = 15


class MessageInfo:
    CountSendGetMessage = 0
    Num = 0
    count = 0

    RusMessage = {
        TypeMessage.WriteTextFound: "Не правильный ввод данных, попробуйте ввести данные еще раз!",
        TypeMessage.TaskExist: "Такая задача уже существует",
        TypeMessage.NeedLetters: "Введите буквы!",
        TypeMessage.LanguageModified: "Язык изменен!",
        TypeMessage.TaskAdded: "Задача добавлена!",
        TypeMessage.TaskDeleted: "Задача удалена!",
        TypeMessage.Nonexistent: "Такой задачи не существует!",
        TypeMessage.TaskUpdated: "Задача обновлена!",
        TypeMessage.ShowTasks: "Показать все задачи!",
        TypeMessage.TaskUpdate: "Обновить задачу!",
        TypeMessage.TaskDelete: "Удалить задачу!",
        TypeMessage.TaskAdd: "Добавить задачу!",
        TypeMessage.ModifyLanguage: "Изменить на Английский",
        TypeMessage.WelcomeBack: "С возвращением!",
        TypeMessage.ThisBotStarted: "Вы уже запустили бота!",
    }

    EnMessage = {
        TypeMessage.WriteTextFound: "Incorrect data entry, try entering the data again!",
        TypeMessage.TaskExist: "That task exist!",
        TypeMessage.NeedLetters: "Enter letters!",
        TypeMessage.LanguageModified: "Language Modified!",
        TypeMessage.TaskAdded: "Task added!",
        TypeMessage.TaskDeleted: "Task deleted!",
        TypeMessage.Nonexistent: "That task Non Existent!",
        TypeMessage.TaskUpdated: "Task updated!",
        TypeMessage.ShowTasks: "Show all tasks",
        TypeMessage.TaskUpdate: "Update task",
        TypeMessage.TaskDelete: "Delete task",
        TypeMessage.TaskAdd: "Add task",
        TypeMessage.ModifyLanguage: "Modify to Russian",
        TypeMessage.WelcomeBack: "Welcome back!",
        TypeMessage.ThisBotStarted: "You've already started the bot!"
    }

    @classmethod
    def GetDictionary(cls):
        """
        Returns the appropriate dictionary with translations based on indexing
        :return: Dictionary with translations
        """
        return cls.RusMessage if cls.Num == 0 else cls.EnMessage

    @classmethod
    def GetMessage(cls, message):
        cls.CountSendGetMessage += 1
        return cls.GetDictionary().get(message, "")

