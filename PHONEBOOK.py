import json
import datetime
import re
from string import ascii_letters

phonebook = {}

def phonebook_read_from_file(filename):
    global phonebook
    try:
        with open(filename, "r", encoding='utf-8-sig') as file:
            phonebook_as_string = file.read()
        phonebook = json.loads(phonebook_as_string)
        return
    except FileNotFoundError:
        with open(filename, "w+") as file:
            print('Phonebook file is not found. New phonebook.txt is created.')
            return 
    print('Can\'t create phonebook file. Please check user permissions.')
    return

def phonebook_write_to_file (filename):
    global phonebook
    phonebook_as_string = json.dumps(phonebook, indent=2)
    try:
        with open(filename, "w", encoding='utf-8-sig') as file:
            file.write(phonebook_as_string)
    except FileNotFoundError:
        with open(filename, "w+") as file:
            file.write(phonebook_as_string)
    return

def calculate_age(date_as_string):
    birth_date = datetime.datetime.strptime(date_as_string, '%Y-%m-%d').date()
    DAYS_IN_YEAR = 365.2425
    age = int((datetime.date.today() - birth_date).days / DAYS_IN_YEAR)
    return age

def input_name(label, empty):
    print(label)
    name = str(input())
    if empty and len(name) == 0:
        return ""
    words = name.split(" ")
    for word in words:
        for i in range(len(word)):
            if word[i] not in ascii_letters and not word[i].isdigit() and word[i] != ' ':
                print('Incorrect ' + label + '. Please enter again: ')
                name = input_name(label, empty)
    return name.title()

def input_date_of_birth(label, empty):
    print(label + '(as: YYYY-MM-DD)')
    date_as_string = str(input())
    if empty and len(date_as_string) == 0:
        return ""
    try:
        date_of_birth = datetime.datetime.strptime(date_as_string, '%Y-%m-%d').date()
    except ValueError:
        print('Incorrect date. Enter date again: ')
        date_as_string = input_date_of_birth(label, empty)
    return date_as_string

def input_phone_number(label, empty):
    print(label)
    phone_number = str(input())
    if empty and len(phone_number) == 0:
        return ""
    if len(phone_number) != 11 and len(phone_number) != 12:
        print('Incorrect phone number. Enter phone number again: ')
        phone_number = input_phone_number(label, empty)
    if phone_number[0:2] == '+7':
        phone_number = '8' + phone_number[2:]
    if re.match(r'[8]{1}[0-9]{10}', phone_number) != None:
        return phone_number
    else:
        print('Incorrect phone number. Enter phone number again: ')
        phone_number = input_phone_number(label, empty)
    return phone_number

def input_record_values():
    result = {
        "name": input_name("Name: ", False),
        "surname": input_name("Surname: ", False),
        "date_of_birth": input_date_of_birth('Date of birth: ', True),
        "phone_number": input_phone_number('Phone number: ', False)
    }
    return result

def phonebook_display_all():
    global phonebook
    return phonebook

def phonebook_output(phonebook):
    result = {}
    for name in phonebook.keys():
        for surname,value in phonebook[name].items():
            result.update([(name + " " + surname, value)])
    phonebook_as_string = json.dumps(result, indent=2)
    phonebook_as_string = phonebook_as_string.replace("{", "")
    phonebook_as_string = phonebook_as_string.replace("}", "")
    phonebook_as_string = phonebook_as_string.replace(",", "")
    print(phonebook_as_string)
    return

def phonebook_find_record():
    global phonebook
    result = {}
    print('Fill the field you need.Skip if you do not need.')
    name = input_name("Name: ", True)
    surname = input_name("Surname: ", True)
    telephone = input_phone_number("Phone number: ", True)

    if len(name) == 0 and len(surname) == 0:
        for name in phonebook:
            for surname in phonebook[name]:
                if phonebook[name][surname]["Phone"] == telephone:
                    result[name] = {surname: phonebook[name][surname]}
    elif len(name) == 0 and len(surname) != 0 and len(telephone) != 0:
        for key, value in phonebook.items():
            if surname in value:
                if telephone == phonebook[key][surname]["Phone"]:
                    obj = {surname: phonebook[key][surname]}
                    result.update([(key, obj)])

    elif len(surname) == 0 and len(name) != 0 and len(telephone) != 0:
        for key in phonebook:
            if name in phonebook:
                for key1 in phonebook[name]:
                    if telephone == phonebook[name][key1]["Phone"]:
                        obj = {surname: phonebook[key1][surname]}
                        result.update([(key1, obj)])

    elif len(telephone) == 0:
        if len(name) == 0 and len(surname) == 0:
            return result
        if name in phonebook:
            if surname in phonebook[name]:
                obj = {surname: phonebook[name][surname]}
                result.update([(name, obj)])
                return result
        if len(name) == 0:
            for key, value in phonebook.items():
                if surname in value:
                    obj = {surname: phonebook[key][surname]}
                    result.update([(key, obj)])
            return result
        if len(surname) == 0:
            if name in phonebook:
                result[name] = phonebook[name]

    elif len(name) != 0 and len(surname) != 0 and len(telephone) != 0:
        for key in phonebook:
            if key == name:
                for key1 in phonebook[name]:
                    if key1 == surname and phonebook[name][surname]["Phone"] == telephone:
                        result[name] = {surname: phonebook[name][surname]}
    return result

def phonebook_add_new_record():
    global phonebook
    result ={}
    record = input_record_values()
    name = record["name"]
    surname = record["surname"]
    if name in phonebook and surname in phonebook[name]:
        print('Record for ' + name + ' ' + surname + ' already exists')
        SUBMENU = {
            "1": {
                "MenuItem": "1. Change existing record",
                "Function": phonebook_change_record
            },
            "2": {
                "MenuItem": "2. Change name and surname of new record",
                "Function": phonebook_add_new_record
            },
            "3": {
                "MenuItem": "3. Change command",
                "Function": input
            }
        }
        print('Please choose the number of the desired operation:')
        for value in SUBMENU.values():
            print(value["MenuItem"])
        print("Print \'bye\' to quit the program")
        choice = str(input())
        print('You chose: ', choice)
        if choice == '3':
            return
        if choice in SUBMENU and choice != '3':
            # call corresponding procedure by command key
            result = SUBMENU[choice]["Function"]()
            return result
        else:
            print('Incorrect choice')
    value = {
        "BirthDate" : record["date_of_birth"],
        "Phone": record["phone_number"]
    }
    if name in phonebook:
        phonebook[name].update([(surname, value)])
    else:
        phonebook[name] = {surname: value}
    print('Record has been successfully added')
    result = {}
    result[name] = {surname: value}
    return result

def phonebook_delete_record():
    global phonebook
    name = input_name("Name: ", False)
    surname = input_name("Surname: ", False)
    if name in phonebook and surname in phonebook[name]:
        del phonebook[name][surname]
        if len(phonebook[name]) == 0:
                del phonebook[name]
        return 'Record has been deleted.'
    else:
        return 'There is no such contact'

def phonebook_delete_record_ALL_by_phone_number():
    global phonebook
    deleted = 0
    telephone = input_phone_number("Enter phone number again please: ", False)
    todelete = {}
    # find records to delete
    for name in phonebook:
        for surname in phonebook[name]:
            if phonebook[name][surname]["Phone"] == telephone:
                todelete[name] = surname
    # delete records from phonebook
    for key, value in todelete.items():
        del phonebook[key][value]
        if len(phonebook[key]) == 0:
            del phonebook[key]
            print(key + ' ' + value + ' record has been deleted.')
            deleted = deleted + 1
    if deleted == 0:
        return 'There is no such record.'
    else:
        return 'In total ' + str(deleted) + ' records have been deleted.'

def phonebook_delete_record_by_phone_number():
    global phonebook
    telephone = input_phone_number("Phone number: ", False)
    num = 0
    for name in phonebook:
        for surname in phonebook[name]:
            if phonebook[name][surname]["Phone"] == telephone:
                num = num + 1
                unique_name = name
                unique_surname = surname
    if num == 1:
        del phonebook[unique_name][unique_surname]
        if len(phonebook[unique_name]) == 0:
            del phonebook[unique_name]
        return 'Record has been deleted.'
    elif num == 0:
        return 'There is no such contact'
    elif num > 1:
        print('There are more than one contacts with number ' + telephone + '.')
        SUBMENU2 = {
            "1": {
                "MenuItem": "1. Delete specific record",
                "Function": phonebook_delete_record
            },
            "2": {
                "MenuItem": "2. Delete all these records",
                "Function": phonebook_delete_record_ALL_by_phone_number
            },
            "3": {
                "MenuItem": "3. Change command",
                "Function": input
            }
        }
        print('Please choose the number of the desired operation:')
        for value in SUBMENU2.values():
            print(value["MenuItem"])
        print("Print \'bye\' to quit the program")
        choice = str(input())
        print('You chose: ', choice)
        if choice == '3':
            return
        if choice in SUBMENU2 and choice != '3':
            # call corresponding procedure by command key
            result = SUBMENU2[choice]["Function"]()
            return result
        else:
            print('Incorrect choice')

def phonebook_change_record():
    global phonebook
    name = input_name("Name: ", False)
    surname = input_name("Surname: ", False)
    if name in phonebook and surname in phonebook[name]:
        new_date_of_birth = input_date_of_birth('New date of birth (click ENTER to skip): ', True)
        new_phone_number = input_phone_number('New phone number (click ENTER to skip): ', True)
        if len(new_date_of_birth) == 0:
            new_date_of_birth = phonebook[name][surname]["BirthDate"]
        if len(new_phone_number) == 0:
            new_phone_number = phonebook[name][surname]["Phone"]
        value = {
            "BirthDate": new_date_of_birth,
            "Phone": new_phone_number
        }
        phonebook[name][surname] = value
        print('Record has been successfully updated')
        result = {}
        result[name] = {surname: value}
        return result
    else:
        return 'There is no such contact'

def phonebook_display_person_age():
    name = input_name("Name ", False)
    surname = input_name("Surname ", False)
    if name in phonebook and surname in phonebook[name] and phonebook[name][surname]["BirthDate"] != '':
        age = str(calculate_age(phonebook[name][surname]["BirthDate"]))
        print(name + ' ' + surname + '\'s age is: ' + age)
        return
    elif name in phonebook and surname in phonebook[name] and phonebook[name][surname]["BirthDate"] == '':
        return 'This person has no birth date'
    else:
        return 'There is no such contact'

def main():
    global phonebook

    MENU = {
        "1" : {
            "MenuItem" : "1. Display all records",
            "Function" : phonebook_display_all
        },
        "2" : {
            "MenuItem" : "2. Find a record in phonebook",
            "Function" : phonebook_find_record
        },
        "3" : {
            "MenuItem" : "3. Add a new record to the phonebook",
            "Function" : phonebook_add_new_record
        },
        "4" : {
            "MenuItem" : "4. Delete a record by name and surname",
            "Function" : phonebook_delete_record
        },
        "5": {
            "MenuItem": "5. Delete a record by phone",
            "Function": phonebook_delete_record_by_phone_number
        },
        "6" : {
            "MenuItem" : "6. Introduce a change to the record",
            "Function" : phonebook_change_record
        },
        "7" : {
            "MenuItem" : "7. Display an age of the person",
            "Function" : phonebook_display_person_age
        },

    }
    FILENAME = "phonebook.txt"
    phonebook_read_from_file(FILENAME)

    while True:
        print('Please choose the number of the desired operation:')
        for value in MENU.values():
            print(value["MenuItem"])
        print("Print \'bye\' to quit the program")
        print('Please enter the number:')

        command = str(input())
        print ('You chose: ', command)
        if command == 'bye':
            phonebook_write_to_file(FILENAME)
            print('Was nice to see you! Bye, come again.')
            break

        if command in MENU:
            # call corresponding procedure by command key
            result = MENU[command]["Function"]()
            if isinstance(result, dict):
                # output dictionary nicely
                if not result:
                    print('There are no such records.')
                else:
                    phonebook_output(result)
            else:
                # there is no need to display None
                if result != None:
                    print(result)
        else:
            print('Command is not defined')
        phonebook_write_to_file(FILENAME)
        print('Press ENTER to continue ...')
        input()

if __name__== "__main__":
  main()