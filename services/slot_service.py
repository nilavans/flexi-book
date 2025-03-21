from models.booking import Booking
from models.service import Service
from models.slot import Slot
from models.vendor import Vendor


def confirm_booking(user_id: int, slot: dict, people_count: int) -> dict:
    return Booking.create_booking(user_id, slot["id"], people_count, slot["slot_date"], slot["start_time"], Slot)


def get_slots_by_vendor_id(vendor_id: int) -> dict:
    return Slot.get_slots(vendor_id)


def get_vendors_by_id(id: int) -> dict:
    return Vendor.get_vendors_service_id(id)


def get_service_by_choice(services, choice) -> dict:
    return next((service for service in services if service["id"] == choice), None)


def get_all_services() -> list[dict]:
    return Service.get_services()


def get_slot_by_slot_id(slots, slot_id) -> dict:
    return next((slot for slot in slots if slot["id"] == slot_id), None)


def is_accommodation_available(reqested_people, available_seats) -> bool:
    return True if reqested_people <= available_seats else False


def get_all_bookings_by_user_id(user_id: int) -> list[dict]:
    return Booking.get_bookings(user_id)


def clear_booking_by_user_id(user_id: int):
    return Booking.clear_bookings(user_id)
