import my_functions

FUNCTION_OPTIONS = ["Make a Rental Booking", "Review a Booking", "Manage Inventory", "Exit"]


def get_user_choice() -> int:
    """
    displays function options to user, and gets user's choice
    :return: user_choice
    """
    print(f"\n{'='*48}\n")
    print("What would you like to do?")
    print("-"*27)
    for index, option in enumerate(FUNCTION_OPTIONS, 1):
        print(f"[{index}] {option:<22}|")
    print("-" * 27)
    user_choice = my_functions.get_user_int_in_range(1, 5, "Enter index number to select choice: ")
    print(f"\n{'='*48}\n")
    return user_choice


def display_booking_options() -> tuple[list, list]:
    """
    displays available booking options
    :return: equip, rent
    """
    print("-"*34)
    print(f"{'ID':<3}|{'Equipment':^15}|{'Daily rent':^12}|")
    print("-" * 34)
    with open("equipment_data.txt", "r") as file:
        index = 0
        equip = []
        rent = []
        for raw_line in file:
            line = raw_line.rstrip()
            line = line.split(",")
            if int(line[2]) > 0:
                equip.append(line[0])
                rent.append(float(line[1]))
                print(f"[{index+1}]  {equip[index]:<14}| ${rent[index]:>10,.2f}|")
                index += 1

    print("-" * 34)

    return equip, rent


def make_a_booking():
    print(FUNCTION_OPTIONS[0])

    first_name = my_functions.get_valid_name(True)
    last_name = my_functions.get_valid_name(False)
    phone_number = my_functions.get_valid_phone()

    equipment, rent = display_booking_options()

    chosen_equip = my_functions.get_user_int_in_range(1, len(equipment)+1, "Enter index number to select equipment: ")
    rent_duration = my_functions.get_user_int_in_range(1, 8, f"How many days would you to rent \"{equipment[chosen_equip-1]}\" for?: ")

    total_cost = rent[chosen_equip] * rent_duration

    with open(f"{first_name}_{last_name}.txt", "w") as file:
        print(f"{first_name},{last_name},{phone_number},{equipment},{rent_duration},{total_cost}", file=file)



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
