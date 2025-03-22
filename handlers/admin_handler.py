import time
from services.admin_service import (
    verify_admin,
    add_new_service,
    get_all_services,
    is_valid_service_id,
    is_valid_vendor_id,
    add_new_vendor,
    get_all_vendors,
    add_new_slot,
)
from utils.utils import clear, print_table, get_valid_input, validate_name, validate_date, validate_time
from utils.status import AdminStatus

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
        return AdminStatus.PROCESS_ABORTED

    name = get_valid_input(
        "Enter a new service name (Min 3 characters without special characters): \n",
        "Invalid name! Should be at least 3 characters (letters/numbers only).",
        validate_name,
    ).capitalize()

    if name is None:
        print("Aborting service addition.")
        return AdminStatus.PROCESS_ABORTED

    service_data = add_new_service(name)
    if service_data:
        print(f"Added new service with an ID: {service_data['id']}")
        return AdminStatus.ADDED_SUCCESSFULLY
    print("Failed to add new service!")
    return AdminStatus.ADD_FAILED


def add_vendor():
    print("Hey admin, before proceeding please login.")
    is_admin = login()

    if not is_admin:
        print("Your are not authorised to proceed!")
        return AdminStatus.PROCESS_ABORTED

    services = get_all_services()
    if not services:
        print("No services available yet! Please add service first.")
        return AdminStatus.PROCESS_ABORTED
    print_table(services)

    service_id = get_valid_input(
        "Select the service ID to add vendor (or '0' to go back): \n",
        "Invalid service ID!",
        lambda x: x.isdigit() and is_valid_service_id(int(x), services),
        True,
    )
    if service_id is None:
        print("Aborting vendor addition.")
        return AdminStatus.PROCESS_ABORTED
    service_id = int(service_id)

    name = get_valid_input(
        "Enter new vendor name (Min 3 chars, letters/numbers only): \n",
        "Invalid name! Should be at least 3 characters (letters/numbers only).",
        validate_name,
    )
    if name is None:
        print("Aborting vendor addition.")
        return AdminStatus.PROCESS_ABORTED

    location = get_valid_input(
        "Enter location (Min 3 chars, letters/numbers only): \n",
        "Invalid location! Should be at least 3 characters (letters/numbers only).",
        validate_name,
    )
    if location is None:
        print("Aborting vendor addition.")
        return AdminStatus.PROCESS_ABORTED

    description = input("Enter description (optioal): \n")

    vendor_data = add_new_vendor(service_id, name, location, description)
    if vendor_data:
        print(f"Added new vendor with an ID: {vendor_data['id']}")
        return AdminStatus.ADDED_SUCCESSFULLY

    print("Failed to add new vendor!")
    return AdminStatus.ADD_FAILED


def add_slot():
    print("Hey admin, before proceeding please login.")
    is_admin = login()

    if not is_admin:
        print("Your are not authorised to proceed!")
        return AdminStatus.PROCESS_ABORTED

    vendors = get_all_vendors()
    if not vendors:
        print("No vendors available for this service! Please add vendors first.")
        return AdminStatus.PROCESS_ABORTED
    print_table(vendors)

    vendor_id = get_valid_input(
        "Select the vendor ID to add slot (or '0' to go back): \n",
        "Invalid vendor ID!",
        lambda x: x.isdigit() and is_valid_vendor_id(int(x), vendors),
        True,
    )
    if vendor_id is None:
        print("Aborting slot addition.")
        return AdminStatus.PROCESS_ABORTED
    vendor_id = int(vendor_id)

    slot_date = get_valid_input(
        "Enter the slot date (YYYY-MM-DD): \n", "Invalid date format! Please use YYYY-MM-DD.", validate_date
    )
    if slot_date is None:
        print("Aborting slot addition.")
        return AdminStatus.PROCESS_ABORTED

    start_time = get_valid_input(
        "Enter the slot time (HH:MM in 24hr format): \n", "Invalid time format! Please use HH:MM.", validate_time
    )
    if start_time is None:
        print("Aborting slot addition.")
        return AdminStatus.PROCESS_ABORTED

    max_people = get_valid_input(
        "Enter the maximum number of people allowed in this slot: \n",
        "Please enter a valid number!",
        lambda x: x.isdigit()
    )
    if max_people is None:
        print("Aborting slot addition.")
        return AdminStatus.PROCESS_ABORTED
    max_people = int(max_people)

    price = get_valid_input("Enter the price for this slot: \n", "Please enter a valid number!", lambda x: x.isdigit())
    if price is None:
        print("Aborting slot addition.")
        return AdminStatus.PROCESS_ABORTED
    price = int(price)

    slot_data = add_new_slot(vendor_id, slot_date, start_time, max_people, price)
    if slot_data:
        print(f"Added new vendor with an ID: {slot_data['id']}")
        return AdminStatus.ADDED_SUCCESSFULLY

    print("Failed to add slot!")
    return AdminStatus.ADD_FAILED
