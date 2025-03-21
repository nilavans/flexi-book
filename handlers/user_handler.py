import time

from services.user_service import (
    authorise_info,
    get_user_info,
    register_user,
    update_password,
    update_username,
    validate_password,
    validate_user,
    is_valid_username,
    validate_username,
    get_user_by_user_id,
)
from utils.status import UserStatus
from utils.utils import clear

SECURITY_QUESTIONS = {
    1: "What is your favorite book?",
    2: "What is your pet’s name?",
    3: "What is your mother's maiden name?",
}
MAX_ATTEMPTS = 3


# Incase user forgot his/her password, will use security question to set new password.
def set_security_info(user=None):
    for key, question in SECURITY_QUESTIONS.items():
        print(f"{key}: {question} \n")

    while True:
        try:
            choice = int(input("Select question (1-3): \n"))
            if choice in [1, 2, 3]:
                break
            print("Invalid choice. Please enter 1, 2 or 3")
        except ValueError:
            print("Please enter a valid number")

    security_question = SECURITY_QUESTIONS[choice]
    if user:
        while True:
            security_answer = input(f"Enter your answer for question {choice}: \n").lower()
            if authorise_info(security_answer, user["security_answer"]):
                print("Security answer can't be same as old answer")
                continue
            break
    else:
        security_answer = input(f"Enter your answer for question {choice}: \n").lower()
    return security_question, security_answer


def register():
    print("\n🔹 REGISTER NEW USER 🔹")
    # Username validation loop.
    while True:
        uname = input("Enter a username (Min 5 characters without special characters): \n").lower()

        if validate_username(uname):
            break

        print("Invalid username! It should be at least 5 characters with only letters and numbers.")
        time.sleep(2)
        clear()

    # Check if username already exists in db.
    if validate_user(uname):
        print("User already exists!")
        return UserStatus.USER_ALREADY_EXISTS

    # Password validation loop.
    while True:
        password = input("Enter a password: \n")
        cpassword = input("Confirm password: \n")

        if validate_password(password, cpassword):
            break

        print("password doesn't match! Try again.")
        time.sleep(2)
        clear()

    # Security info for password reset.
    print("Choose a Security Question: \n")
    security_question, security_answer = set_security_info()

    if register_user(uname, password, security_question, security_answer):
        print("\n🎉 Registration Successful! You can now log in.")
        return UserStatus.REGISTER_SUCCESS

    print("User not created successfully. Please try again!")
    return UserStatus.REGISTRATION_FAILED


# Handle password reset with security verifications.
def reset_password(user):
    while True:
        npass = input("Enter a new password: \n")

        if authorise_info(npass, user["password"]):
            print("New password can't be same as old password!")
            time.sleep(2)
            clear()
            continue

        cpass = input("Confirm new password: \n")
        if not validate_password(npass, cpass):
            print("Passwords do not match! Try again.")
            time.sleep(2)
            clear()
            continue

        print("Verify your identity to reset password:")
        sq, sa = user["security_question"], user["security_answer"]

        while True:
            print(f"Your security question: {sq} \n")
            new_sa = input("Enter your answer: \n").lower()

            if not authorise_info(new_sa, sa):
                print("Security verification failed! Password reset aborted.")

                retry = input("Do you want to try again? (Y/N): ").upper()
                if retry == "Y":
                    continue

                return UserStatus.SECURITY_VERIFICATION_FAILED
            break

        print("Select a new Security Question: \n")
        new_security_question, new_security_answer = set_security_info(user)

        if update_password(user["user_id"], npass, new_security_question, new_security_answer):
            print("New password updated successfully! 🎉")
            return UserStatus.PASSWORD_RESET_SUCCESS

        print("Couldn't update new password. Try again later! ☹️")
        return UserStatus.PASSWORD_RESET_FAILED


def login():
    print("\n🔹 LOGIN USER 🔹")
    while True:
        uname = input("Enter your username (Press 'C' to go back): \n").strip()

        if uname.upper() == "C":
            print("Redirecting to the main menu...")
            time.sleep(2)
            clear()
            return UserStatus.BACK_TO_MENU, None

        # Get user info from db and check if user exists.
        user_info = get_user_info(uname)
        if not user_info:
            print("User don't exists! Please check your username and try again.")
            time.sleep(2)
            clear()
            continue

        #  User will have certain attempts to enter correct password, if failed will be redirected.
        attempts = MAX_ATTEMPTS
        while attempts > 0:
            password = input("Enter your password (Press 'F' to reset password): \n")

            if password.upper() == "F":
                return reset_password(user_info), None

            if authorise_info(password, user_info["password"]):
                return UserStatus.LOGIN_SUCCESS, user_info["user_id"]

            attempts -= 1
            if attempts > 0:
                print(f"Incorrect password! {attempts} attempts left.")
                time.sleep(2)
            else:
                print("Too many failed attempts. Redirecting to login page...")
                time.sleep(2)
                clear()
                return UserStatus.LOGIN_FAILED, None


def logout():
    clear()
    print("🔒 Logging out...")
    time.sleep(2)
    exit()


def change_password(user_id):
    user = get_user_by_user_id(user_id)
    if not user:
        print("User data not found!")
        return
    return reset_password(user)


def change_username(user_id):
    user = get_user_by_user_id(user_id)
    if not user:
        print("User data not found!")
        return

    while True:
        uname = input("Enter a new username (Min 5 characters without special characters): \n").lower()

        if validate_username(uname, user["username"]):
            print("New username can't be same as old username.")
            time.sleep(2)
            clear()
            continue

        if is_valid_username(uname):
            break

        print("Invalid username! It should be at least 5 characters with only letters and numbers.")
        time.sleep(2)
        clear()

        # Check if username already exists in db.
        if validate_user(uname):
            print("Username already exists! Try with another name.")
            time.sleep(2)
            clear()
        break

    if not update_username(user_id, uname):
        print("Username update failed!")
        return UserStatus.USERNAME_RESET_FAILED

    print("Username successfully changed!")
    return UserStatus.USERNAME_RESET_SUCCESS

