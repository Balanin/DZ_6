from Class import *

USERS = AddressBook()

# +
#@ error_handler
def add_user(data):
    name, *phones = data
    if name  in USERS:
         raise ValueError('This contact already exist.')
    record = Record(name)
    for phone  in phones:
        record.add_phone(phone)
    USERS.add_record(record)
   

    return f'User {name} added with number: {phone}'
# +
#@ error_handler
def delete_contact(data):
    name, *phone = (data)
    if name not in USERS.data.keys():
        return f'Contact with name {name} not found!'
    else:
        USERS.remove_record(name)
        return f'Contact {name} has been deleted'

#+
#@ error_handler
def delete_phone(data):
    name, *phone = (data)
    if name not in USERS.data.keys():
        return f'Contact with name {name} not found!'
    else:
        contact = USERS[name]
        contact.del_phone(*phone)
        return f'Number {phone} has been deleted from {name}'
#+
#@ error_handler
def addd_phone(data):
    name, *phones = data
    if name  in USERS:
        record = Record(name)
        for phone  in phones:
            record.add_phone(phone)
        USERS.add_record(record)
        return f'User {name} changed the get new number: {phone}'

#+
#@ error_handler
def change_phone(data):
    name, *phone = data
    record = USERS[name]
    record.change_phones(phone)
    return f'User {name} changed the phone, his new number: {phone[1]}'

# +
#@ error_handler
def show_all(_) -> str:
    """Displays the entire phonebook."""

    result = ''

    phone_book = USERS.iterator()
    count = 0
    for contact in phone_book:  
        for i in contact:
            result +=  f'{i.name.value}:'
            for number in i.numbers:
                result += f' {number.value}\n'
                count += 1
                if count == 3:
                    result += '\n'
                    count = 0
    return result 

   

#@ error_handler
def show_phone(data):
    name = data[0]
    record = USERS[name]
    return f'{record.get_info()}'

def birthday(data):
    name, day = data
    record = USERS[name]
    record.add_birthday(day)
    return f'Birthday added on {day}'

def next_birthday(data):
    name, *args = data
    record = USERS[name]
    x = record.days_to_birthday()
    return f'Until the next birthday {x}'


def hello(_):
    return "How can I help you?"

def exit(_):
    return "Good bye!"

HANDLER = {
        
            "hello": hello,
            "good bye": exit,
            "close": exit,
            "exit": exit,
            "add contact": add_user,
            "add phone": addd_phone,   
            "delete": delete_contact,
            "del phone": delete_phone,
            "show all": show_all,
            "change": change_phone,   
            "phone": show_phone,
            "add birthday": birthday,
            "next birthday": next_birthday    
            
}

def parser(user_input):
    new_input = user_input
    data = ''
    for key in HANDLER:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            data = data.strip().split(' ')
            
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()


def reaction_func(reaction):
    return HANDLER.get(reaction, break_func)

def break_func():
    return 'Wrong enter.'


def main():
    while True:
        user_input = input('>>> ')
        result = parser(user_input)
        if  result == "good bye" or result =="close" or result == "exit":
            print("Good bye!")
            break
        print(result)

    
        
if __name__ == "__main__":
    
      main()
   