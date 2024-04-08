def get_pos_num(prompt: str) -> int:
    """
    gets a positive integer from user
    :param prompt: string used to interact with the user
    :return: valid_num
    """
    while True:
        # try statement to deal with invalid types of input causing errors
        try:
            # converts string from user into to integer
            valid_num = int(input(prompt))
            if valid_num > 0:
                break
            else:
                print("enter a valid number")
        except:
            print("enter a valid number")

    return valid_num


def get_non_empty_string(prompt: str) -> str:
    """
    gets a non-empty string from the user
    :param prompt: string used to interact with the user
    :return: valid_str
    """
    while True:
        # gets string from user
        valid_str = input(prompt)
        # checks that user string has a length of at least 1
        if len(valid_str) > 0:
            break
        else:
            print("enter a valid input")

    return valid_str


def get_valid_name(first_or_last: bool) -> str:
    """
    gets valid first or last name from the user
    :param first_or_last: boolean used to ask for either first (True) or last (False) name
    :return: valid_name
    """
    while True:
        if first_or_last:
            # variable 'first_or_last' has True value, so first name prompt is shown
            valid_name = get_non_empty_string("Enter your first name: ")
        else:
            # variable 'first_or_last' has False value, so last name prompt is shown
            valid_name = get_non_empty_string("Enter your last name: ")

        # checks that the string length does not exceed 20 and that the string is alphabetical
        if len(valid_name) <= 20 and valid_name.isalpha():
            break
        else:
            print("enter a valid input")

    return valid_name


def get_valid_phone() -> int:
    """
    gets a valid phone number from the user
    :return: valid_phone
    """
    while True:
        # gets valid integer from user
        valid_phone = get_pos_num("Enter your phone number: ")
        # checks that the integer has 10 digits
        if len(f"{valid_phone}") == 10:
            break
        else:
            print("enter a valid 10 digit phone number")

    return valid_phone


def get_user_int_in_range(lower: int, upper: int, prompt: str) -> int:
    """
    gets an integer from the user that's within a custom range
    :param lower: lower limit of range
    :param upper: upper limit of range
    :param prompt: string used to interact with the user
    :return: valid_int
    """
    while True:
        # gets valid integer from user
        valid_int = get_pos_num(prompt)
        # checks that the integer is within the customized range
        if valid_int in range(lower, upper):
            break
        else:
            print("enter a valid number")

    return valid_int


def verify_user_choice(prompt: str) -> bool:
    """
    asks for user to verify their choice
    :param prompt:
    :return: bool
    """
    while True:
        # gets a string from the user
        verify = get_non_empty_string(prompt)
        # checks that the string (the user's response to the prompt) is within the acceptables params
        if verify.lower() in ["y", "yes"]:
            return True
        elif verify.lower() in ["n", "no"]:
            return False
        else:
            print("enter a valid choice")


if __name__ == '__main__':
    # quick tests to check the functionality of the functions

    # get_pos_num() test
    print(get_pos_num("Enter a positive integer"))

    # get_non_empty_string() test
    print(get_non_empty_string("Enter a string"))

    # get_valid_name() test
    print(get_valid_name(True))
    print(get_valid_name(False))

    # get_valid_phone() test
    print(get_valid_phone())

    # get_user_int_in_range() test
    print(get_user_int_in_range(1, 11, "Enter a number from 1 to 10"))

    # verify_user_choice() test
    print(verify_user_choice("(Test) Are you sure? (Y/N)"))
