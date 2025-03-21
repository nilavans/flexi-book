import time
from utils.utils import clear, print_table, verify_card
from utils.status import BookingStatus
from services.slot_service import (
    get_all_services,
    get_service_by_choice,
    get_vendors_by_id,
    get_slots_by_vendor_id,
    get_slot_by_slot_id,
    confirm_booking,
    is_accommodation_available,
    get_all_bookings_by_user_id,
    clear_booking_by_user_id
    
)

MAX_ATTEMPTS = 3


def get_card_details():
    while True:
        cnum = input("Enter the Card number: \n")
        if not cnum.isdigit():
            print("❌ Invalid card number! Please enter digits only.")
            time.sleep(2)
            clear()
            continue
        cname = input("Enter card holder name: \n")
        if not cname.replace(" ", "").isalpha():
            print("❌ Invalid name! Enter a valid card holder name.")
            time.sleep(2)
            clear()
            continue
        try:
            expm, expy = input("Enter card expiry date (MM/YY): \n").split("/")
            if not (expm.isdigit() and expy.isdigit()):
                raise ValueError
        except ValueError:
            print("❌ Invalid expiry date! Enter in MM/YY format.")
            time.sleep(2)
            clear()
            continue
        cvv = input("Enter CVV: \n")
        if not (cvv.isdigit() and len(cvv) == 3):
            print("❌ Invalid CVV! Enter a 3-digit number.")
            time.sleep(2)
            clear()
            continue

        return cnum, cname, expm, expy, cvv


def payment():
    while True:
        pchoice = int(input("How would you like to make payment?: \n1.Debit Card\n2.Credit Card\n3.Back\n"))

        if pchoice == 3:
            return BookingStatus.BACK_TO_MENU

        if pchoice in (1, 2):
            for attempts in range(MAX_ATTEMPTS, 0, -1):
                cchoice = int(input("Which card would you like to use?: \n1.MasterCard\n2.Visa Card\n3.Back\n"))

                if cchoice == 3:
                    return BookingStatus.BACK_TO_MENU

                if cchoice in (1, 2):
                    cnum, cname, expm, expy, cvv = get_card_details()
                    if verify_card(cnum, cchoice):
                        print("✅ Payment successful!")
                        return BookingStatus.PAYMENT_SUCCESS
                    else:
                        print(f"Invalid card details {attempts - 1} attempts left.")
                        continue
                else:
                    print("❌ Invalid card choice! Please enter a valid option.")

            print("Too many failed attempts. Redirecting...")
            return BookingStatus.BOOKING_FAILED

        else:
            print("❌ Invalid input! Please enter a valid option.")
            time.sleep(2)
            clear()


def confirm_booking_process(user_id, slots, slot_id):
    slot = get_slot_by_slot_id(slots, slot_id)
    while True:
        try:
            req_people = int(input("Please specify how many people are you looking to book?: \n"))
        except ValueError:
            print("Please enter a valid number")

        if not is_accommodation_available(req_people, slot["max_people"]):
            return BookingStatus.CAN_NOT_ACCOMMADATE, None

        print_table([slot])

        cbook = input("Would you like to proceed with booking? (Y/N): \n").upper()
        if cbook != "Y":
            return BookingStatus.BACK_TO_MENU, None

        status = payment()
        if status == BookingStatus.PAYMENT_FAILED:
            print("❌ Payment failed! Try again later.")
            return BookingStatus.BOOKING_FAILED, None

        if status == BookingStatus.BACK_TO_MENU:
            return BookingStatus.BACK_TO_MENU, None

        booking_info = confirm_booking(user_id, slot, req_people)

        if not booking_info:
            print("Booking failed! Try again.")
            return BookingStatus.BOOKING_FAILED, None

        print("🎊 YOUR BOOKING DETAILS 🎊")
        print_table(booking_info)
        return BookingStatus.BOOKING_SUCCESS, booking_info


def slots(user_id, vendors, vendor_id):
    slots = get_slots_by_vendor_id(vendor_id)
    if not slots:
        print(f"No slots available for this vendor {vendor_id}")
        return BookingStatus.NOT_AVAILABLE, None

    print_table(slots)
    while True:
        try:
            slot_id = int(input("Select the Slot ID to book (or '0' to go back):\n"))
        except ValueError:
            print("Please enter a valid number")
        match slot_id:
            case 0:
                print("Going back to previous menu...")
                return BookingStatus.BACK_TO_MENU, None
            case _ if slot_id in [slot["id"] for slot in slots]:
                return confirm_booking_process(user_id, slots, slot_id)
            case _:
                print("Invalid choice! Please select a valid service number.")


def vendors(user_id, services, choice):
    service = get_service_by_choice(services, choice)

    vendors = get_vendors_by_id(service["id"])
    if not vendors:
        print(f"No vendors found for {service['name']}")
        return BookingStatus.NOT_AVAILABLE, None

    print_table(vendors)
    while True:
        try:
            vendor_id = int(input(f"Select the {service['name']} ID to book (or '0' to go back):\n"))
        except ValueError:
            print("Please enter a valid number.")

        match vendor_id:
            case 0:
                print("Going back to previous menu...")
                return BookingStatus.BACK_TO_MENU, None
            case _ if vendor_id in [vendor["id"] for vendor in vendors]:
                return slots(user_id, vendors, vendor_id)
            case _:
                print("Invalid choice! Please select a valid service number.")


def book(user_id):
    services = get_all_services()

    if not services:
        print("No services found!")
        return BookingStatus.NOT_AVAILABLE, None

    for service in services:
        print(f"{service['id']}.{service['name']}")

    while True:
        try:
            choice = int(input("Select the service would you like to book (or '0' to go back):\n"))
        except ValueError:
            print("Please enter a valid number.")

        match choice:
            case 0:
                print("Going back to previous menu...")
                return BookingStatus.BACK_TO_MENU, None
            case _ if choice in [service["id"] for service in services]:
                return vendors(user_id, services, choice)
            case _:
                print("Invalid choice! Please select a valid service number.")


def booking_history(user_id):
    booking_data = get_all_bookings_by_user_id(user_id)
    if not booking_data:
        print("📌 No bookings found!")
        return BookingStatus.NOT_AVAILABLE

    print("\n------ 📝 YOUR BOOKING HISTORY -------\n")
    print_table(booking_data)
    
def clear_booking_history(user_id):
    clear_booking = clear_booking_by_user_id(user_id)
    if not clear_booking:
        print('Something went wrong! Try again later.')
        return BookingStatus.CLEAR_BOOKING_FAILED
    
    print('All the booking history are deleted!')
    return BookingStatus.CLEAR_BOOKING_SUCCESS

