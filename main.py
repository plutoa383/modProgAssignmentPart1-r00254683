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


def display_booking_options() -> list:
    availability = []

    print(FUNCTION_OPTIONS[0])
    print("-"*48)
    print(f"{'ID':<3}|{'Equipment':^15}|{'Daily rent':^12}|{'Note':^13}|")
    print("-" * 48)
    with open("equipment_data.txt", "r") as file:
        index = 0
        for raw_line in file:
            index += 1
            line = raw_line.rstrip()
            line = line.split(",")
            if int(line[2]) > 0:
                print(f"[{index}]|{line[0]:<15}| ${float(line[1]):>10,.2f}|{'':>13}|")
                availability.append(True)
            else:
                print(f"[{index}]|{line[0]:<15}| ${float(line[1]):>10,.2f}|{'unavailable':^13}|")
                availability.append(False)
    print("-" * 48)

    return availability


def make_a_booking():
    availability = display_booking_options()



def main():
    while True:
        user_choice = get_user_choice()
        if user_choice == 1:
            make_a_booking()
        elif user_choice == 2:
            print("under development")
        elif user_choice == 3:
            print("under development")
        else:
            if my_functions.verify_user_choice("Are you sure you want to exit? [Y/N]"):
                break


main()
