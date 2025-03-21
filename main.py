import time
from handlers.user_handler import register, login, change_username, change_password, logout
from handlers.slot_handler import book, booking_history, clear_booking_history
from handlers.admin_handler import add_service, add_vendor, add_slot
from utils.utils import clear, print_table
from utils.status import UserStatus, BookingStatus
from database.connection import initialise_database


def settings(user_id):
    print("🔹 🔹 🔹 SETTINGS MENU 🔹 🔹 🔹")
    while True:
        choice = int(
            input("What do you like to do? \n1.Clear booking history\n2.Change Username\n3.Change Password\n4.Back\n")
        )
        print("---------------------------------")
        match choice:
            case 1:
                status = clear_booking_history(user_id)
                if status == BookingStatus.CLEAR_BOOKING_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                if status == BookingStatus.CLEAR_BOOKING_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
            case 2:
                status = change_username(user_id)
                if status == UserStatus.USERNAME_RESET_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                if status == UserStatus.USERNAME_RESET_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
            case 3:
                status = change_password(user_id)
                if status == UserStatus.PASSWORD_RESET_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                if status == UserStatus.PASSWORD_RESET_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
            case 4:
                print("Redirecting...")
                return
            case _:
                print("Invalid Input!")
                time.sleep(2)
                clear()


def user_menu(user_id):
    print("🔹 🔹 🔹 USER MENU 🔹 🔹 🔹")
    while True:
        choice = int(
            input("What do you like to do today? \n1.Book a slot\n2.View booking History\n3.Settings\n4.Logout\n")
        )
        print("-----------------------------------------")
        match choice:
            case 1:
                status, booking_info = book(user_id)
                if status == BookingStatus.BACK_TO_MENU:
                    continue
                if status == BookingStatus.BOOKING_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                    print("\n ------ 📝 YOUR BOOKING DETAIL 👇 -----")
                    print_table([booking_info])
                if status == BookingStatus.BOOKING_FAILED:
                    print(f"{status.value.code} - {status.value.message} 🎉")
            case 2:
                booking_history(user_id)
            case 3:
                settings(user_id)
            case 4:
                logout()
            case _:
                print("Invalid Input!")
                time.sleep(2)
                clear()


def menu():
    print("🔹 🔹 🔹 WELCOME TO FLEXI BOOK 🔹 🔹 🔹")
    while True:
        choice = int(input("\n1.Login\n2.Register\n3.Admin\n4.Exit\n"))
        print("---------------------------------")
        match choice:
            case 1:
                status, user_id = login()
                if status == UserStatus.LOGIN_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                    user_menu(user_id)
                elif status == UserStatus.PASSWORD_RESET_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                elif status == UserStatus.PASSWORD_RESET_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
                    continue
                elif status == UserStatus.LOGIN_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
            case 2:
                status = register()
                if status == UserStatus.REGISTER_SUCCESS:
                    print(f"{status.value.code} - {status.value.message} 🎉")
                    login()
                elif status == UserStatus.USER_ALREADY_EXISTS:
                    print(f"{status.value.code} - {status.value.message} ❌")
                elif status == UserStatus.REGISTRATION_FAILED:
                    print(f"{status.value.code} - {status.value.message} ❌")
                    time.sleep(2)
                    clear()
            case 3:
                admin()
            case 4:
                print("Goodbye! See you soon..👋")
                break

            # remove later for dev purpose.
            case 4:
                user_menu(2)
            case _:
                print("Invalid Input!")
                time.sleep(2)
                clear()

def admin():
    print("🔹 🔹 🔹 ADMIN MENU 🔹 🔹 🔹")
    while True:
        try: 
          choice = int(input('What would to like to handle? \n1.Add Service\n2.Add Vendor\n3.Add Slot\n4.Exit\n'))
        except ValueError:
          print("Please enter a valid number! ❌")
          continue
        
        match choice:
            case 1:
                add_service()
            case 2:
                add_vendor()
            case 3:
                add_slot()
            case 4:
                print(print("Goodbye! See you soon..👋"))
                time.sleep(2)
                exit()

def run():
    # Initialise DB and Create tables if not exists.
    initialise_database()
    print("⎯⎯-----------------------------------")
    menu()


if __name__ == "__main__":
    run()
