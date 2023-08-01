'''
Напишите консольного бота помощника, который будет распознавать команды, вводимые с клавиатуры, и отвечать согласно введенной команде.

Бот помощник должен стать для нас прототипом приложения-ассистента. Приложение-ассистент в первом приближении должен уметь работать с книгой контактов и календарем. В этой домашней работе сосредоточимся на интерфейсе самого бота. Наиболее простой и удобный на начальном этапе разработки интерфейс - это консольное приложение CLI (Command Line Interface). CLI достаточно просто реализовать. Любой CLI состоит из трех основных элементов:

Парсер команд. Часть, которая отвечает за разбор введенных пользователем строк, выделение из строки ключевых слов и модификаторов команд.
Функции обработчики команд — набор функций, которые ещё называют handler, они отвечают за непосредственное выполнение команд.
Цикл запрос-ответ. Эта часть приложения отвечает за получение от пользователя данных и возврат пользователю ответа от функции-handlerа.
На первом этапе наш бот-ассистент должен уметь сохранять имя и номер телефона, находить номер телефона по имени, изменять записанный номер телефона, выводить в консоль все записи, которые сохранил. Чтобы реализовать такую несложную логику, воспользуемся словарем. В словаре будем хранить имя пользователя как ключ и номер телефона как значение.

Условия
Бот должен находиться в бесконечном цикле, ожидая команды пользователя.
Бот завершает свою работу, если встречает слова: .
Бот не чувствительный к регистру вводимых команд.
Бот принимает команды:
"hello", отвечает в консоль "How can I help you?"
"add ...". По этой команде бот сохраняет в памяти (в словаре например) новый контакт. Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
"change ..." По этой команде бот сохраняет в памяти новый номер телефона для существующего контакта. Вместо ... пользователь вводит имя и номер телефона, обязательно через пробел.
"phone ...." По этой команде бот выводит в консоль номер телефона для указанного контакта. Вместо ... пользователь вводит имя контакта, чей номер нужно показать.
"show all". По этой команде бот выводит все сохраненные контакты с номерами телефонов в консоль.
"good bye", "close", "exit" по любой из этих команд бот завершает свою роботу после того, как выведет в консоль "Good bye!".
Все ошибки пользовательского ввода должны обрабатываться при помощи декоратора input_error. Этот декоратор отвечает за возврат пользователю сообщений вида "Enter user name", "Give me name and phone please" и т.п. Декоратор input_error должен обрабатывать исключения, которые возникают в функциях-handler (KeyError, ValueError, IndexError) и возвращать соответствующий ответ пользователю.
Логика команд реализована в отдельных функциях и эти функции принимают на вход одну или несколько строк и возвращают строку.
Вся логика взаимодействия с пользователем реализована в функции main, все print и input происходят только там.
'''


from module11_homework_final_classes import Name, Phone, AddressBook, Record, Birthday, InvalidBirthday, InvalidPhone
import pickle



# помилки при введені даних
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "There is no such contact in the phone book"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name, phone in format 0********* (optional), birthday in format dd.mm.yyyy (optional)"
        except InvalidPhone as e:
            print(e)
        except InvalidBirthday as e:
            print(e)
    return inner


try:
    with open('contact_book.bin', 'rb') as f:
        address_book = pickle.load(f)
except FileNotFoundError:
        # Обробка ситуації, коли файл не знайдено
        address_book = AddressBook()


def hello_command():
    return "How can I help you?"

@input_error
def add_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday(args[2])
    record = address_book.get(str(name))
    if record:
        return record.add_phone(phone)
    record = Record(name, phone, birthday)
    address_book.add_record(record)
    return f"Contact {name} was added successfully"


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])    
    record = address_book.get(str(name))
    if record:        
        return record.change_phone(old_phone, new_phone)
    return f"There is no {name} in address book"

@input_error
def get_phone_command(name):
    return address_book.get(str(name))

def show_all_command(*args):    
    for rec in address_book.iterator(2):
        print('page')
        print(rec)
    
        
@input_error
def search(search_query):
    search_results = []
    for k, v in address_book.items():
        if (str(k).lower().find(search_query.lower()) != -1) or (str(v).lower().find(search_query.lower()) != -1):
            search_results.append(address_book.get(str(k)))
    for i in search_results:
        print(i)
    

def exit_command(*args):
    with open('contact_book.bin', 'wb') as f:
        pickle.dump(address_book, f)
    return 'Bye'

def unknown_command(*args):
    pass

COMMANDS = {
    hello_command: ('hello', 'hi'),
    add_command: ('add',),
    change_command: ('change', 'edit'),
    get_phone_command: ('phone',),
    show_all_command: ('show all',),
    exit_command: ('bye', 'exit', 'end')
}

def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):                
                data = text[len(kwd):].strip().split()                
                return cmd, data 
    return unknown_command, []

def main():   
    while True:        
        command = input("Enter command: ")
        # command = command.lower()
        
        cmd, data = parser(command)
        result = cmd(*data)
        print(result)
        
        if command.startswith("search"):
            try:
                search_query = input('>>> ')                
                search(search_query)                                   
            except:
                print("Enter search query")
        
        if cmd == exit_command:
            break
        
        '''if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:                
                name, phone = input("Give me name and phone (in format 0*********) please: ").split()                                   
                print(add_contact(name, phone))                
            except InvalidPhone as e:
                print(e)                                            
        elif command.startswith("change"):
            try:
                name, old_phone, new_phone = input("Give me name, old phone and new phone please: ").split()
                print(change_phone(name, old_phone, new_phone))
            except:
                print("Give me name and phone please")
        elif command.startswith("phone"):
            try:
                _, name = command.split()
                print(get_phone(name))
            except:
                print("Enter contact name")        
        elif command == "show all":
            print(show_all())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        elif command == ".":
            break
        else:
            print("Unknown command")'''

if __name__ == "__main__":
    main()

