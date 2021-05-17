from src.bank_OCR import \
    get_account_numbers_from_file, split_account_number_into_numbers, \
    is_valid_account_number, generate_account_validation_report


def main():
    scanned_lines = get_account_numbers_from_file('../entries.txt')
    split_into_digits = split_account_number_into_numbers(scanned_lines)
    generate_account_validation_report(split_into_digits)
    print(is_valid_account_number('777777177'))


if __name__ == '__main__':
    main()

