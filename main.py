from scan_numbers import get_account_numbers_from_file, split_account_number_into_numbers, \
calculate_cell_values, is_valid_account_number, generate_account_validation_report


zero = '''
       _  
      |_|
       _|
'''


def print_hi():
    scanned = get_account_numbers_from_file('entries.txt')
    exploded = split_account_number_into_numbers(scanned)
    generate_account_validation_report(exploded)
    print(is_valid_account_number('457508000'))


if __name__ == '__main__':
    print_hi()

