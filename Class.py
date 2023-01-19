from collections import UserDict
from datetime import datetime
# def error_handler(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyError:
#             return 'This contact doesnt exist, please try again.'
#         except ValueError as exception:
#             return exception.args[0]
#         except IndexError:
#             return 'This contact cannot be added, it exists already'
#         except TypeError:
#             return 'Unknown command or parametrs, please try again.'
#     return inner

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):

    pass

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        print(value)
        if  len(value) != 13 or  value[0] != '+' or not value[1:].isdigit():
            raise ValueError('Invalid phone number.')
        self._value = value

class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        if value.find('-'):
            value = value.replace("-", ".")
        list = value.split('.')
        value1 = datetime(year=int(list[-1]), month=int(list[-2]), day=int(list[0])).date()
        if value1 > datetime.now().date():
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value

class Record:
    def __init__(self,name):
        self.name = Name(name)
        self.numbers =[]
        self.birthday = None

    def add_phone(self,number):
        self.numbers.append(Phone(number))
       
    def add_birthday(self,day):
        self.birthday = Birthday(day)

    def phone_in_contact(self, number) -> bool:
        for num in self.numbers:
            if num.value == number:
                return True
        return False

    def del_phone(self, number):
        for num in self.numbers:
            if num.value == number:
                self.numbers.remove(num)
                
    def get_all_numbers(self) -> list:
        return [number.value for number in self.numbers]

    def change_phones(self, number):
         for i in self.numbers:
            if i.value == number[0]:
                self.numbers.remove(i)
            self.add_phone(number[1])
    
    def get_info(self):
        phones_info = ''
        for phone in self.numbers:
            phones_info += f'{phone.value}, '
        return f'{self.name.value} : {phones_info[:-2]}'
    
    def __repr__(self):
        return f'{self.name}'

    def days_to_birthday(self):
        self.birthday
        if self.birthday.value.find('-'):
            self.birthday = self.birthday.value.replace("-", ".")

        list = self.birthday.split('.')
        this_year = datetime.now().year
        birthday = datetime(year=int(this_year), month=int(list[-2]), day=int(list[0])).date()
        current_datetime = datetime.now().date()

        if birthday < current_datetime :
            birthday = datetime(year=int(this_year)+1, month=int(list[-2]), day=int(list[0])).date() 
        return f'{birthday - current_datetime}'


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name) -> Record:
        return self.data.get(name)
    


    def remove_record(self, name):
        del self.data[name]

    def get_all_contacts(self):
        result = []
        for name in self.data.keys():
            phones = self.data[name]
            phones = phones.get_all_numbers()
            result.append({name: phones})
        return result

    def search(self, value):
        if self.has_record(value):
            return self.get_record(value)

        for record in self.get_all_record().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

    def iterator(self, count=2):
        page = []
        i = 0
        for record in self.data.values():
            page.append(record) 
            i += 1
            if i == count:
                yield page
                page = []
                i = 0
        if page:
            yield page
     
  