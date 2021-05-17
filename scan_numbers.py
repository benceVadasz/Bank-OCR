from constants import CELL_VALUES
from constants import ALTERNATIVES
from constants import LETTER_PAIRS
from constants import LETTER_VALUES


def get_account_numbers_from_file(filename):
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
                if len(line) < 28 and len(line) != 0:
                    missing_spaces = ' ' * (28 - len(line))
                    number_line += line.rstrip('\n') + missing_spaces
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
    account_number_string_array = []
    ind = 0
    place = 0
    inner_array = []
    for account_number_string in arr:
        for character in account_number_string:
            inner_array.append(character)
            ind += 1
            if ind != 0 and ind % 3 == 0:
                for x in inner_array:
                    nested[place].append(x)
                inner_array = []
                if ind % 27 == 0:
                    place = 0
                else:
                    place += 1
        account_number_string_array.append(change_digits_into_nums(nested))
        nested = [[], [], [], [], [], [], [], [], []]
    return account_number_string_array


def change_digits_into_nums(nested):
    num = ''
    fixes = []
    for inner_array in nested:
        if ''.join(inner_array) in CELL_VALUES:
            if int(CELL_VALUES[''.join(inner_array)]) >= 10:
                num += LETTER_PAIRS[''.join(inner_array)]
            else:
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
    result = []
    for x in range(len(reversed_account_number_array)):
        if not reversed_account_number_array[x].isalpha():
            result.append(int(reversed_account_number_array[x]) * (x+1))
        else:
            result.append(LETTER_VALUES[reversed_account_number_array[x]])

    return sum(result) % 11 == 0


def generate_account_validation_report(account_numbers_array):
    file = open('report.txt', 'w')
    for account_number in account_numbers_array:
        if '?' in account_number:
            file.write(f'{account_number} ILL\n')
        elif not is_valid_account_number(account_number):
            if len(correct_account_number_is_invalid(account_number)) > 1:
                file.write(f'{account_number} AMB {str(correct_account_number_is_invalid(account_number))} \n')
            elif len(correct_account_number_is_invalid(account_number)) == 1:
                file.write(f'{correct_account_number_is_invalid(account_number)[0]}\n')
            else:
                file.write(f'{account_number} ILL\n')
        else:
            file.write(account_number + '\n')
    file.close()


def correct_account_number_is_invalid(num):
    valid_numbers = []
    for i in range(len(num)):
        for alternative in ALTERNATIVES[num[i]]:
            new_num = num[:i] + alternative + num[i + 1:]
            if is_valid_account_number(new_num):
                valid_numbers.append(new_num)
    return valid_numbers
