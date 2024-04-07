def get_pos_num(prompt: str) -> int:
    """
    gets and validates a positive integer from user
    :param prompt: string used as prompt to ask user
    :return: valid_num
    """
    while True:
        try:
            valid_num = int(input(prompt))
            if valid_num > 0:
                break
            else:
                print("enter a valid number")
        except:
            print("enter a valid number")

    return valid_num


if __name__ == '__main__':
    # get_pos_num() test
    get_pos_num("enter positive integer")
