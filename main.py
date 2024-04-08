import my_functions
import datetime

FUNCTION_OPTIONS = ["Make a Rental Booking", "Review a Booking", "Manage Inventory", "Exit"]


def get_user_choice() -> int:
    """
    displays function options to user, and gets user's choice
    :return: user_choice
    """
    print(f"\n{'='*48}\n")
    print(f"{'-'*30}\n|{'What would you like to do?':^28}|\n{'-'*30}")
    for index, option in enumerate(FUNCTION_OPTIONS, 1):
        print(f"[{index}] {option:<25}|")
    print("-"*30)
    user_choice = my_functions.get_user_int_in_range(1, 5, "Enter index number to select choice: ")
    print(f"\n{'='*48}\n")
    return user_choice


def display_booking_options() -> tuple[list, list]:
    """
    displays available booking options
    :return: equip, rent
    """
    print(f"{'-'*34}\n{'ID':<3}|{'Equipment':^15}|{'Daily rent':^12}|{'-'*34}")
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


def update_equipment(chosen_equip: str):
    """
    updates equipment stock after a booking
    :param chosen_equip: equipment to be updated
    :return: NONE
    """
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        if chosen_equip in line:
            sline = line.rstrip()
            sline = sline.split(",")
            lines[index] = f"{sline[0]},{sline[1]},{int(sline[2])-1},{int(sline[3])+1}\n"
            break

    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)


def print_receipt(fname: str, lname: str):
    """
    prints customer's latest receipt
    :param fname: customer's first name
    :param lname: customer's last name
    :return: NONE
    """
    with open(f"{fname}_{lname}.txt", "r") as file:
        for raw_line in file:
            line = raw_line.rstrip()
            line = line.split(",")

    print(f"{'-' * 40}\n{line[0]}, here is your receipt for {line[3]}:\n{'-' * 40}")
    print(f"{'Equipment:':<16}{line[4]}\n{'Total Cost:':<16}${float(line[6]):,.2f}\n{'Rent Duration:':<16}{line[5]}")
    print(f"{'-' * 40}")


def make_a_booking():
    """
    makes a booking
    :return: NONE
    """
    print(FUNCTION_OPTIONS[0])

    first_name = my_functions.get_valid_name(True).capitalize()
    last_name = my_functions.get_valid_name(False).capitalize()
    phone_number = my_functions.get_valid_phone()

    equipment, rent = display_booking_options()

    chosen_equip = my_functions.get_user_int_in_range(1, len(equipment)+1, "Enter index number to select equipment: ")-1
    rent_duration = my_functions.get_user_int_in_range(1, 8, f"How many days do you want to rent a \"{equipment[chosen_equip]}\" for?: ")

    total_cost = rent[chosen_equip] * rent_duration
    date_of_booking = datetime.date.today().strftime("%d/%m/%Y")
    with open(f"{first_name}_{last_name}.txt", "a") as file:
        print(f"{first_name},{last_name},{phone_number},{date_of_booking},{equipment[chosen_equip]},{rent_duration},{total_cost}", file=file)

    with open("bookings_2024.txt", "a") as file:
        print(f"{first_name},{last_name},{date_of_booking}", file=file)

    update_equipment(equipment[chosen_equip])

    print_receipt(first_name, last_name)


def review_booking():
    names = []

    with open("bookings_2024.txt", "r") as file:
        for line in file:
            sline = line.rstrip()
            sline = sline.split(",")
            names.append(f"{sline[0]} {sline[1]}")
    query_fname = my_functions.get_valid_name(True).capitalize()
    query_lname = my_functions.get_valid_name(False).capitalize()

    if f"{query_fname} {query_lname}" in names:
        print(f"\nhere is \"{query_fname} {query_lname}\"'s latest receipt:\n")
        print_receipt(query_fname, query_lname)
    else:
        print(f"customer \"{query_fname} {query_lname}\" not found")


def admin_options():
    if verify_login() is True:
        admin_function_options = ["Add New Equipment", "Remove An Equipment", "Update Equipment Price"]

        print(f"{'-'*30}\n|{'Administrator Options':^28}|\n{'-'*30}")
        for index, option in enumerate(admin_function_options, 1):
            print(f"[{index}] {option:<25}|")
        print("-"*30)
        admin_choice = my_functions.get_user_int_in_range(1, 4, "Enter index number of your choice: ")

        if admin_choice == 1:
            add_new_equipment()
        elif admin_choice == 2:
            remove_equipment()
        else:
            change_equipment_rental()


def verify_login() -> bool:
    """
    login interface for administrators
    :return: bool
    """
    user_found = False
    user_index = 0
    attempts = 0
    with open("admin_details.txt", "r") as file:
        usernames = []
        passwords = []
        for raw_line in file:
            line = raw_line.rstrip()
            line = line.split(" ")
            usernames.append(line[0])
            passwords.append(line[1])

    while not user_found:
        usrnm = my_functions.get_non_empty_string("Enter administrator username: ")
        for index, usr in enumerate(usernames):
            if usrnm == usr:
                user_found = True
                user_index = index
                break

    while attempts < 3:
        pswrd = input("Enter password: ")
        attempts += 1

        if pswrd == passwords[user_index]:
            print("Logged in\n")
            return True
        else:
            print(f"invalid password - {3-attempts} attempts left")

    print("Too many invalid attempts")
    return False


def add_new_equipment():
    equipment = []
    with open("equipment_data.txt", "r") as file:
        for line in file:
            sline = line.rstrip()
            sline = sline.split(",")
            equipment.append(sline[0].lower())

    while True:
        equip_name = my_functions.get_non_empty_string("Enter name of new equipment: ")
        if equip_name.lower() not in equipment:
            break
        else:
            print("equipment already exists")

    equip_cost = my_functions.get_pos_num(f"Enter daily rental cost of \"{equip_name}\": ")
    equip_count = my_functions.get_pos_num(f"Enter current inventory amount of \"{equip_name}\"")

    with open("equipment_data.txt", "a") as file:
        print(f"{equip_name},{equip_cost},{equip_count},0", file=file)

    print(f"\nSuccessfully added {equip_count} {equip_name} to inventory")


def remove_equipment():
    equipment = []
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        sline = line.rstrip()
        sline = sline.split(",")
        equipment.append(sline[0].lower())

    while True:
        del_equip = my_functions.get_non_empty_string("Enter name of equipment to delete: ").lower()
        if del_equip in equipment:
            break
        else:
            print(f"equipment \"{del_equip}\" not found")

    for index, equip in enumerate(equipment):
        if del_equip == equip.lower():
            lines.pop(index)

    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)

    print(f"\nSuccessfully removed {del_equip} from")


def change_equipment_rental():
    equipment = []
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        sline = line.rstrip()
        sline = sline.split(",")
        equipment.append(sline[0].lower())

    while True:
        chosen_equip = my_functions.get_non_empty_string("Enter name of equipment to edit: ").lower()
        if chosen_equip in equipment:
            break
        else:
            print(f"equipment \"{chosen_equip}\" not found")

    new_rental = my_functions.get_pos_num("Enter new rental cost per day: ")

    for index, line in enumerate(lines):
        if chosen_equip in line:
            sline = line.rstrip()
            sline = sline.split(",")
            lines[index] = f"{sline[0]},{new_rental},{sline[2]},{sline[3]}\n"
            break

    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)

    print(f"\nSuccessfully updated \"{chosen_equip}\" with new rental cost: ${new_rental:,.2f}")


def main():
    while True:
        user_choice = get_user_choice()
        if user_choice == 1:
            make_a_booking()
        elif user_choice == 2:
            review_booking()
        elif user_choice == 3:
            admin_options()
        else:
            if my_functions.verify_user_choice("Are you sure you want to exit? [Y/N]"):
                break


main()
