import my_functions
import datetime

# list holds options for regular users
FUNCTION_OPTIONS = ["Make a Rental Booking", "Review a Booking", "Manage Inventory", "Exit"]
# list hold options for administrators
ADMIN_FUNCTIONS_OPTIONS = ["Add New Equipment", "Remove An Equipment", "Update Equipment Price", "Generate Rental Report"]

def get_user_choice() -> int:
    """
    displays function options to user, and gets user's choice
    :return: user_choice
    """
    # Nice formatting for the options table
    print(f"\n{'='*48}\n")
    # Table header
    print(f"{'-'*30}\n|{'What would you like to do?':^28}|\n{'-'*30}")
    # lists the contents (options) of the table from a list
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
    # Table header
    print(f"{'-'*34}\n{'ID':<3}|{'Equipment':^15}|{'Daily rent':^12}|{'-'*34}")
    # Fills table with contents in text file
    with open("equipment_data.txt", "r") as file:
        index = 0
        # lists to hold their respective contents from the text file
        equip = []
        rent = []
        for raw_line in file:
            # gets individual information from each line
            line = raw_line.rstrip()
            line = line.split(",")
            # checks that the equipment has available inventory, skips those that are unavailable
            if int(line[2]) > 0:
                # adds content to their respective lists
                equip.append(line[0])
                rent.append(float(line[1]))
                # prints out the table contents
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
    # copies contents of text file into 1 list
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    # alters list content values as necessary
    for index, line in enumerate(lines):
        if chosen_equip in line:
            sline = line.rstrip()
            sline = sline.split(",")
            lines[index] = f"{sline[0]},{sline[1]},{int(sline[2])-1},{int(sline[3])+1}\n"
            break

    # overwrites text file with the new altered list
    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)


def print_receipt(fname: str, lname: str):
    """
    prints customer's latest receipt
    :param fname: customer's first name
    :param lname: customer's last name
    :return: NONE
    """
    # gets contents of last line in text file
    with open(f"{fname}_{lname}.txt", "r") as file:
        for raw_line in file:
            line = raw_line.rstrip()
            line = line.split(",")

    # prints receipt using the copied contents
    print(f"{'-' * 40}\n{line[0]}, here is your receipt for {line[3]}:\n{'-' * 40}")
    print(f"{'Equipment:':<16}{line[4]}\n{'Total Cost:':<16}${float(line[6]):,.2f}\n{'Rent Duration:':<16}{line[5]}")
    print(f"{'-' * 40}")


def make_a_booking():
    """
    makes a booking
    :return: NONE
    """
    # Shows option header
    print(FUNCTION_OPTIONS[0])
    print(f"{'-'*21}\n")

    # Gets customer information from user
    first_name = my_functions.get_valid_name(True).capitalize()
    last_name = my_functions.get_valid_name(False).capitalize()
    phone_number = my_functions.get_valid_phone()

    # displays the equipment table, and receives equipment and rent lists
    equipment, rent = display_booking_options()

    # gets user to choose equipment
    chosen_equip = my_functions.get_user_int_in_range(1, len(equipment)+1, "Enter index number to select equipment: ")-1
    # gets duration of rent from user
    rent_duration = my_functions.get_user_int_in_range(1, 8, f"How many days do you want to rent a \"{equipment[chosen_equip]}\" for?: ")
    # calculates total cost of rent
    total_cost = rent[chosen_equip] * rent_duration
    # takes current date as date of booking
    date_of_booking = datetime.date.today().strftime("%d/%m/%Y")

    # creates text file named after customer, contains booking details
    with open(f"{first_name}_{last_name}.txt", "a") as file:
        print(f"{first_name},{last_name},{phone_number},{date_of_booking},{equipment[chosen_equip]},{rent_duration},{total_cost}", file=file)

    # logs the name and date of booking into text file
    with open("bookings_2024.txt", "a") as file:
        print(f"{first_name},{last_name},{date_of_booking}", file=file)

    # updates inventory
    update_equipment(equipment[chosen_equip])
    # prints customer receipt
    print_receipt(first_name, last_name)


def review_booking():
    # Shows option header
    print(FUNCTION_OPTIONS[1])
    print(f"{'-'*16}\n")

    # list to store customers names
    names = []

    # gets contents from text file
    with open("bookings_2024.txt", "r") as file:
        for line in file:
            sline = line.rstrip()
            sline = sline.split(",")
            # stores customer names into list
            names.append(f"{sline[0]} {sline[1]}")

    # gets name to search for
    query_fname = my_functions.get_valid_name(True).capitalize()
    query_lname = my_functions.get_valid_name(False).capitalize()

    # checks if name is in list
    if f"{query_fname} {query_lname}" in names:
        # name was found, and their latest receipt is printed
        print(f"\nhere is \"{query_fname} {query_lname}\"'s latest receipt:\n")
        print_receipt(query_fname, query_lname)
    else:
        # name is not found and appropriate message is shown
        print(f"customer \"{query_fname} {query_lname}\" not found")


def admin_options():
    # Shows option header
    print(FUNCTION_OPTIONS[2])
    print(f"{'-'*16}\n")

    # redirects to login interface
    if verify_login() is True:
        # prints out options to user
        print(f"{'-'*30}\n|{'Administrator Options':^28}|\n{'-'*30}")
        for index, option in enumerate(ADMIN_FUNCTIONS_OPTIONS, 1):
            print(f"[{index}] {option:<25}|")
        print("-"*30)
        # gets user choice
        admin_choice = my_functions.get_user_int_in_range(1, 4, "Enter index number of your choice: ")

        # runs function based on user choice
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
    # bool represents whether admin user is found
    user_found = False
    user_index = 0
    # variable stores password attempts count
    attempts = 0

    # gets content from text file
    with open("admin_details.txt", "r") as file:
        # lists to hold usernames and passwords respectively
        usernames = []
        passwords = []

        for raw_line in file:
            line = raw_line.rstrip()
            line = line.split(" ")
            # stores usernames and passwords in their respective lists
            usernames.append(line[0])
            passwords.append(line[1])

    while not user_found:
        # gets username
        usrnm = my_functions.get_non_empty_string("Enter administrator username: ")
        for index, usr in enumerate(usernames):
            # checks that the username is valid
            if usrnm == usr:
                # updates bool so that outer loop ends
                user_found = True
                # stores index number of username, used to match with corresponding password
                user_index = index
                break

    # limits password attempts to a maximum of 3
    while attempts < 3:
        # gets password attempt
        pswrd = input("Enter password: ")
        # updates attempt count
        attempts += 1

        # checks if password is correct
        if pswrd == passwords[user_index]:
            # logs user in
            print("Logged in\n")
            return True
        else:
            # prints number of attempts left
            print(f"invalid password - {3-attempts} attempts left")

    # prints message if attempt count reaches 3
    print("Too many invalid attempts")
    return False


def add_new_equipment():
    # Shows option header
    print(ADMIN_FUNCTIONS_OPTIONS[0])
    print(f"{'-'*17}\n")

    # list to hold equipment names
    equipment = []

    # gets contents from text file
    with open("equipment_data.txt", "r") as file:
        for line in file:
            sline = line.rstrip()
            sline = sline.split(",")
            # stores equipment names into list in lower case
            equipment.append(sline[0].lower())

    while True:
        # gets name of new equipment to be added from user
        equip_name = my_functions.get_non_empty_string("Enter name of new equipment: ")

        # checks that equipment of the same name don't exist
        if equip_name.lower() not in equipment:
            break
        else:
            print("equipment already exists")

    # gets new equipment details from user
    equip_cost = my_functions.get_pos_num(f"Enter daily rental cost of \"{equip_name}\": ")
    equip_count = my_functions.get_pos_num(f"Enter current inventory amount of \"{equip_name}\"")

    # appends the new equipment to the end of text file
    with open("equipment_data.txt", "a") as file:
        print(f"{equip_name},{equip_cost},{equip_count},0", file=file)

    # prints success message
    print(f"\nSuccessfully added {equip_count} {equip_name} to inventory")


def remove_equipment():
    # shows option header
    print(ADMIN_FUNCTIONS_OPTIONS[1])
    print(f"{'-'*19}\n")

    # list holds equipment names
    equipment = []

    # copies contents of text file into list
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        sline = line.rstrip()
        sline = sline.split(",")
        # stores equipment names in list
        equipment.append(sline[0].lower())

    while True:
        # gets name of equipment to delete from user
        del_equip = my_functions.get_non_empty_string("Enter name of equipment to delete: ").lower()
        # checks that the equipment of that name exist
        if del_equip in equipment:
            break
        else:
            print(f"equipment \"{del_equip}\" not found")

    for index, equip in enumerate(equipment):
        if del_equip == equip.lower():
            # deletes the line containing the equipment to be removed
            lines.pop(index)

    # overwrites the text file with contents from list
    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)

    # prints success message
    print(f"\nSuccessfully removed {del_equip} from")


def change_equipment_rental():
    # shows option header
    print(ADMIN_FUNCTIONS_OPTIONS[2])
    print(F"{'-'*22}\n")

    # list to store equipment names
    equipment = []

    # copies contents of text file into list
    with open("equipment_data.txt", "r") as file:
        lines = file.readlines()

    for line in lines:
        sline = line.rstrip()
        sline = sline.split(",")
        # stores equipment names in list
        equipment.append(sline[0].lower())


    while True:
        # gets name of equipment to edit
        chosen_equip = my_functions.get_non_empty_string("Enter name of equipment to edit: ").lower()
        # checks that equipment exists
        if chosen_equip in equipment:
            break
        else:
            print(f"equipment \"{chosen_equip}\" not found")

    # gets new rental price for equipment from user
    new_rental = my_functions.get_pos_num("Enter new rental cost per day: ")

    # updates the equipment details in list with new rental price
    for index, line in enumerate(lines):
        if chosen_equip in line:
            sline = line.rstrip()
            sline = sline.split(",")
            lines[index] = f"{sline[0]},{new_rental},{sline[2]},{sline[3]}\n"
            break

    # overwrites text files with contents of list
    with open("equipment_data.txt", "w") as file:
        file.writelines(lines)

    #prints success message
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
