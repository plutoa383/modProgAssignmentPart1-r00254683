import my_functions

FUNCTION_OPTIONS = ["Make a Rental Booking", "Review a Booking", "Manage Inventory", "Exit"]


def get_user_choice() -> int:
    """
    displays function options to user, and gets user's choice
    :return: user_choice
    """
    print(f"\n{'='*48}\n")
    print("What would you like to do?")
    print("-"*26)
    for index, option in enumerate(FUNCTION_OPTIONS, 1):
        print(f"[{index}] {option}")
    print("-" * 26)
    user_choice = my_functions.get_user_int_in_range(1, 5, "Enter index number to select choice: ")
    print(f"\n{'='*48}\n")
    return user_choice


def main():
    print(get_user_choice())


main()
