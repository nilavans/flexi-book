from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Status:
    code: int
    message: str


class UserStatus(Enum):
    BACK_TO_MENU = Status(307, "Redirecting to menu")
    REGISTER_SUCCESS = Status(200, "Registration successful")
    REGISTRATION_FAILED = Status(400, "Registration failed")
    USER_ALREADY_EXISTS = Status(409, "User already exists")
    LOGIN_SUCCESS = Status(200, "Login successful")
    LOGIN_FAILED = Status(400, "Invalid username or password")
    PASSWORD_RESET_SUCCESS = Status(200, "Password reset success")
    PASSWORD_RESET_FAILED = Status(200, "Password reset failed")
    USERNAME_RESET_SUCCESS = Status(200, "Username reset success")
    USERNAME_RESET_FAILED = Status(200, "Username reset failed")
    SECURITY_VERIFICATION_FAILED = Status(409, "Security verfication failed")


class BookingStatus(Enum):
    BACK_TO_MENU = Status(307, "Redirecting to menu")
    BOOKING_SUCCESS = Status(200, "Booking successful")
    BOOKING_FAILED = Status(400, "Booking failed")
    PAYMENT_FAILED = Status(400, "Payment failed")
    PAYMENT_SUCCESS = Status(200, "Payment successful")
    CAN_NOT_ACCOMMADATE = Status(301, "Can't accommadate this many people.")
    NOT_AVAILABLE = Status(404, "Not available! Please try again.")
    CLEAR_BOOKING_SUCCESS = Status(200, "All booking cleared.")
    CLEAR_BOOKING_FAILED = Status(400, "Wouldn't clear booking history")
