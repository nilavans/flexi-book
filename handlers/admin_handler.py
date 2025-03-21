import time
from services.admin_service import (
    verify_admin,
    is_valid_name,
    add_new_service,
    get_all_services,
    is_valid_service_id,
    is_valid_vendor_id,
    add_new_vendor,
    get_valid_input,
    get_all_vendors,
    add_new_slot,
)
from utils.utils import clear, print_table

MAX_ATTEMPTS = 3


def login():
    for attempts in range(MAX_ATTEMPTS, 0, -1):
        name = input("Enter your name admin: \n").strip()
        password = input("Enter you password admin: \n").strip()

        if verify_admin(name, password):
            return True

        print(f"Invalid admin name or password! {attempts - 1} attempts left")
        time.sleep(2)
        clear()

    print("Too many failed attempts. Redirecting...")
    return False


def add_service():
    print("Hey admin, before proceeding please login.")
    is_admin = login()

    if not is_admin:
        print("Your are not authorised to proceed!")
        return False

    for attempts in range(MAX_ATTEMPTS, 0, -1):
        name = input("Enter a new service name (Min 3 characters without special characters): \n").strip().capitalize()

        if not is_valid_name(name):
            print(
                f"Invalid name {attempts} attempt(s) left! (It should be at least 3 characters with only letters and numbers.)"
            )
            time.sleep(2)
            clear()
            continue

        service_data = add_new_service(name)
        if service_data:
            print(f"Added new service with an ID: {service_data['id']}")
            return True

        print("Failed to add new service!")
        return False

    print("Too many failed attempts. Redirecting...")
    return False


def add_vendor():
    print("Hey admin, before proceeding please login.")
    is_admin = login()

    if not is_admin:
        print("Your are not authorised to proceed!")
        return False

    services = get_all_services()
    if not services:
        print("No services available yet! Please add service first.")
        return False
    print_table(services)

    for attempts in range(MAX_ATTEMPTS, 0, -1):
        try:
            service_id = int(input("Select the service you would like to add vendor (or '0' to go back): \n"))
            break
        except ValueError:
            print("Please enter a valid number!")

        if not is_valid_service_id(service_id, services):
            print(f"Invalid choice {attempts} attempts left! Select a valid service id")
            time.sleep(2)
            clear()
    if service_id is None:
        print("Aborting vendor addition.")
        return False

    name = get_valid_input(
        "Enter new vendor name (Min 3 chars, letters/numbers only): \n",
        "Invalid name! Should be at least 3 characters (letters/numbers only).",
    )
    if name is None:
        print("Aborting vendor addition.")
        return False

    location = get_valid_input(
        "Enter location (Min 3 chars, letters/numbers only): \n",
        "Invalid location! Should be at least 3 characters (letters/numbers only).",
    )

    if location is None:
        print("Aborting vendor addition.")
        return False

    description = input("Enter description (optioal): \n")

    vendor_data = add_new_vendor(service_id, name, location, description)
    if vendor_data:
        print(f"Added new vendor with an ID: {vendor_data['id']}")
        return True

    print("Failed to add new vendor!")
    return False


def add_slot():
    print("Hey admin, before proceeding please login.")
    is_admin = login()

    if not is_admin:
        print("Your are not authorised to proceed!")
        return False

    vendors = get_all_vendors()
    if not vendors:
        print("No vendors available for this service! Please add vendors first.")
        return False
    print_table(vendors)

    for attempts in range(MAX_ATTEMPTS, 0, -1):
        try:
            vendor_id = int(input("Select the vendot you would like to add slot (or '0' to go back): \n"))
            break
        except ValueError:
            print("Please enter a valid number!")

        if not is_valid_vendor_id(vendor_id, vendors):
            print(f"Invalid choice {attempts} attempts left! Select a valid vendor id")
            time.sleep(2)
            clear()
    if vendor_id is None:
        print("Aborting slot addition.")
        return False
    
    slot_date = get_valid_input(
        "Enter the slot date (YYYY-MM-DD): \n", "Invalid date format! Please use YYYY-MM-DD.", False
    )

    if slot_date is None:
        print("Aborting slot addition.")
        return False

    start_time = get_valid_input(
        "Enter the slot time (HH:MM in 24hr format): \n", "Invalid time format! Please use HH:MM.", False
    )

    if start_time is None:
        print("Aborting slot addition.")
        return False

    for attempts in range(MAX_ATTEMPTS, 0, -1):
        try:
            max_people = int(input("Enter the maximum number of people allowed in this slot: \n"))
            break
        except ValueError:
            print(f"Please enter a valid number! {attempts - 1} attempts left")
    if max_people is None:
        print("Aborting slot addition.")
        return False
    
    for attempts in range(MAX_ATTEMPTS, 0, -1):
        try:
            price = float(input("Enter the price for this slot: \n"))
            break
        except ValueError:
            print(f"Please enter a valid number! {attempts - 1} attempts left")
    if price is None:
        print("Aborting slot addition.")
        return False
    
    slot_data = add_new_slot(vendor_id, slot_date, start_time, max_people, price)
    if slot_data:
        print(f"Added new vendor with an ID: {slot_data['id']}")
        return True
    
    print("Failed to add slot!")
    return False
