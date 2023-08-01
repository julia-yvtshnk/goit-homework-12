from collections import UserDict
import re
from datetime import datetime


class InvalidPhone(Exception):
    ... 

class InvalidBirthday(Exception):
    ...              
    

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
        
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)
    

class Name(Field):
    ...


class Phone(Field):        
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, new_value):        
        if re.match(r'^0\d{9}$', new_value):
            self.__value = new_value
        else:
            raise InvalidPhone("Phone number should match the format 0*********")
        
               

class Birthday(Field):
    def __init__(self, value):
        self._value = None
        super().__init__(value)
        self.value = value
        

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value is None:
            try:
                self._value = datetime.strptime(new_value, '%d.%m.%Y')
            except ValueError:
                raise InvalidBirthday("Birthday date should match the format dd.mm.yyyy")        


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name        
        self.phones = []
        self.birthday = birthday
        if phone:
            self.phones.append(phone)
        
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"
        
        
    def remove_phone(self, phone: Phone):
        if phone.value in [p.value for p in self.phones]:
            self.phones.remove(phone)
            return f"phone {phone} was removed for contact {self.name}"
        return f"There is no {phone} for contact {self.name}"
        
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} was changed to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}" 
    
    def days_to_birthday(self):
        if self.birthday:
            today =  datetime.today().date()
            next_birthday = self.birthday.value.replace(year=today.year).date()
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_to_birthday = (next_birthday - today).days
            return days_to_birthday
           
    
    def __str__(self):
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"        

  
    

class AddressBook(UserDict):
    
    def add_record(self, record: Record):       
        self.data[record.name.value] = record
        return f"Contact {record} was added successfuly"
    
    def iterator(self, n=5):
        result = ''
        count = 0
        for r in self.values():
            result += str(r) + '\n'
            count += 1
            if count >= n:
                yield result
                count = 0
                result = ''
            if result:
                yield result
            
        
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())       

    


if __name__ == "__main__":
    username = Name('Alex')
    userphone = Phone('0661234567')
    userbirthday = Birthday('04.09.1988')
    # userbirthday.value='04.09.1988'
    # userphone1 = Phone('0123')
    # userphone3 = Phone('0123456789')

    
    # print(address_book)
    # days_until_birthday = user_record.days_to_birthday()
    # print(f"Days until next birthday: {days_until_birthday}")
    # rec1.add_phone(userphone1)
    # rec1.change_phone(userphone1, userphone3)


    username1_1 = Name('Boris')
    userphone1_1 = Phone('0071234567')
    # userphone1_2 = Phone('777')
    # userphone1_3 = Phone('066')
    rec1 = Record(username1_1)
    rec1.add_phone(userphone1_1)
    
    username1_2 = Name('Emma')
    userphone1_2 = Phone('0123456789')
    rec2 = Record(username1_2, userphone1_2)
    
    
    user_record = Record(username, userphone, userbirthday)
    address_book = AddressBook()
    address_book.add_record(user_record)
    address_book.add_record(rec1)
    address_book.add_record(rec2)

    #print(rec1, rec1_1)

    
    
    # print(ad_b)

    # for k, v in ad_b.data.items():
    #     print(k, v)
        
    for rec in address_book.iterator(2):
        print('page')
        print(rec)
    



   