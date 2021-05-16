from pydash import invert

CELL_VALUES = {
    ' _ | ||_|': '0',
    '     |  |': '1',
    ' _  _||_ ': '2',
    ' _  _| _|': '3',
    '   |_|  |': '4',
    ' _ |_  _|': '5',
    ' _ |_ |_|': '6',
    ' _   |  |': '7',
    ' _ |_||_|': '8',
    ' _ |_| _|': '9'
}


def parse_account_number(num):
    # input has 9 3x3 "cells".
    # break it up into individual cells.

    cells = get_cells(num)
    cell_values = []
    for cell in cells:
        cell_values.append(get_cell_value(cell))

    return tuple(cell_values)


def get_cell_value(cell):
    return CELL_VALUES.get(cell, -1)


def get_cells(num):
    cells = []

    # copy into lines
    lines = get_lines(num)

    for offset in range(0, 26, 3):
        cell = lines[0][offset:offset + 3]
        cell += lines[1][offset:offset + 3]
        cell += lines[2][offset:offset + 3]

        cells.append(cell)

    return cells


def get_lines(num):
    lines = ["", "", ""]
    offset = 0

    for char in num:
        lines[offset] += char
        if len(lines[offset]) == 27:
            offset += 1

    return lines


def format_cell(cell):
    return "%s\n%s\n%s" % (cell[0:3], cell[3:6], cell[6:9])


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
    for inner_array in nested:
        if ''.join(inner_array) in CELL_VALUES:
            num += CELL_VALUES[''.join(inner_array)]
        else:
            num += '?'
    return num


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
            file.write(account_number + ' ILL\n')
        elif not is_valid_account_number(account_number):
            file.write(account_number + ' ERR\n')
        else:
            file.write(account_number + '\n')
    file.close()
