from module11_homework_final_classes import Name, Phone, AddressBook, Record, Birthday, InvalidBirthday, InvalidPhone

address_book = AddressBook()

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
    return address_book.add_record(record)


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

def exit_command(*args):
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
        
        cmd, data = parser(command)
        result = cmd(*data)
        print(result)
        if cmd == exit_command:
            break  
        

if __name__ == "__main__":
    main()

