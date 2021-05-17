from constants import CELL_VALUES
from constants import ALTERNATIVES


def get_account_numbers_from_file(filename):
    """Returns all account numbers found in <filename>, as a list of tuples"""

    accounts = []
    final_accounts = []
    number_line = ''
    row = 0
    with open(filename, 'r') as file:
        for line in file:
            row += 1

            if row % 4 == 0:
                accounts.append(number_line)
                number_line = ''
            else:
                if len(line) < 28:
                    number_line += line.rstrip('\n') + ' '
                else:
                    number_line += line.rstrip('\n')
    for num in accounts:
        spaces = 26 * ' '
        if len(num) < 80:
            final_accounts.append(spaces + num)
        else:
            final_accounts.append(num)
    return final_accounts


def split_account_number_into_numbers(arr):
    nested = [[], [], [], [], [], [], [], [], []]
    nums = []
    ind = 0
    place = 0
    ap = ''
    inner_array = []
    for s in arr:
        for c in s:
            inner_array.append(c)
            ind += 1
            if ind != 0 and ind % 3 == 0:
                for x in inner_array:
                    nested[place].append(x)
                inner_array = []
                if ind % 27 == 0:
                    place = 0
                else:
                    place += 1
        nums.append(change_digits_into_nums(nested))
        nested = [[], [], [], [], [], [], [], [], []]
    return nums


def change_digits_into_nums(nested):
    num = ''
    fixes = []
    for inner_array in nested:
        if ''.join(inner_array) in CELL_VALUES:
            num += CELL_VALUES[''.join(inner_array)]
        else:
            fixes = correct_illegible_cell(''.join(inner_array))
            num += '?'

    if len(fixes) >= 1:
        if len(get_correct_account_number(num, fixes)) > 0:
            num = get_correct_account_number(num, fixes)

    return num


def get_correct_account_number(number_string, fixes):

    for s in number_string:
        for fix in fixes:
            if s == '?':
                if is_valid_account_number(number_string.replace('?', fix)):
                    return number_string.replace('?', fix)
    return ''


def correct_illegible_cell(digit_string):
    counter = 0
    possible_digits = []
    for digit in CELL_VALUES:
        if len([i for i in range(len(digit)) if digit[i] != digit_string[i]]) == 1:
            possible_digits.append(CELL_VALUES[digit])

    return possible_digits


def calculate_cell_values(arr):
    account_number = ''
    for inner_array in arr:
        account_number += CELL_VALUES[''.join(inner_array)]
    return account_number


def is_valid_account_number(account_number):
    reversed_account_number_array = list(account_number)[::-1]
    return sum(
        [(x + 1) * int(reversed_account_number_array[x]) for x in range(len(reversed_account_number_array))]) % 11 == 0


def generate_account_validation_report(account_numbers_array):
    file = open('report.txt', 'w')
    for account_number in account_numbers_array:
        if '?' in account_number:
            file.write(f'{account_number} ILL\n')
        elif not is_valid_account_number(account_number):
            if correct_scanning_mistake(account_number) != account_number:
                file.write(correct_scanning_mistake(account_number) + '\n')
            else:
                file.write(f'{account_number} ERR\n')
        else:
            file.write(account_number + '\n')
    file.close()


def correct_scanning_mistake(num):
    for i in range(len(num)):
        for alternative in ALTERNATIVES[num[i]]:
            new_num = num[:i] + alternative + num[i + 1:]
            if is_valid_account_number(new_num):
                return new_num
    return num
