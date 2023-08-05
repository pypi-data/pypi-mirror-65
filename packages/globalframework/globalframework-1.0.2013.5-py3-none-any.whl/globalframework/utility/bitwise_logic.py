import itertools as it
from globalframework.enumeration import PermissionBitwise



# Initialize a dictionary for the functions.
def function_dict():
    access = {}
    bit_list = list(PermissionBitwise)
    for item in bit_list:
        access[item] = 0
    return access

# Simulates Database source whereby input is a number between 0 - 15.
def database_input(db_input):
    invalid_input = 0
    if type(db_input) != int:
        db_num = 0
        invalid_input = 1
    else:
        db_num = db_input
    if invalid_input == 0:
        if db_num < 0 or db_num > 15:
            print(f'{db_num} is out of range. Only a number between 0 - 15 is accepted.')
            db_num = 0
        else:
            print(f'Database input is {db_num}.')
    return db_num

# Method to process hierarchical level of permission. The higher the value, the higher the number of permission access available.
def permission_logic(db_input):
    access = function_dict()
    ls1 = []
    for item in access:
        ls1.append(item.value)

    # Generate all possible number combinations.
    all_combinations = []
    for n in range(1, 4):
        for combination in it.combinations(ls1, n):
            if len(list(combination)) > 1:
                all_combinations.append(list(combination))

    # Identify the correct combination based on input and total combinations.
    combination = []
    level_matched = 0

    # First layer logic. If input is the same as the initial value, then only one function access is given.
    if db_input == 0 or db_input == 1 or db_input == 2 or db_input == 4 or db_input == 8 or db_input == 15:
        combination.append(db_input)
        level_matched = 1

    # Second layer logic. Iterate through the combinations to find a total that equates the input number.
    if level_matched == 0:
        for each_combination in all_combinations:
            if len(each_combination) > 1:
                total = 0
                for number in each_combination:
                    total = total + number
                if total == db_input:
                    combination = each_combination
    return combination

def permission_output(combination_list):
    access = function_dict()
    for each in combination_list:
        for function in list(PermissionBitwise):
            if each == function.value or each == 15:
                access[function] = 1
    return access

# Prints the result.
def get_access(result):
    print(result)

    for permission in result:
        print(f"{permission} {permission.value}")
