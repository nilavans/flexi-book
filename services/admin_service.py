import re
import time
from datetime import datetime, timedelta
from models.service import Service
from models.vendor import Vendor
from models.slot import Slot

MAX_ATTEMPTS = 3


def get_valid_input(prompt, error_message, validate = True, back=False):
    for attempts in range(MAX_ATTEMPTS, 0, -1):
        value = input(prompt).strip()
        if back and value == "0":
            return None
        if validate and is_valid_name(value):
            return value
        else:
          return value
        print(f"{error_message} ({attempts - 1} left!)")
        time.sleep(2)
    return None


def verify_admin(name: str, password: str) -> bool:
    if name == "admin" and password == "admin":
        return True
    return False


def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9]+( [a-zA-Z0-9]+)*$", name.strip()))


def is_valid_service_id(id: int, services: list[dict]) -> bool:
    ids = [service["id"] for service in services]
    return True if id in ids else False


def is_valid_vendor_id(id: int, vendors: list[dict]) -> bool:
    ids = [vendor["vendor_id"] for vendor in vendors]
    return True if id in ids else False


def add_new_service(name) -> dict:
    return Service.create_service(name)


def add_new_vendor(servie_id: int, name: str, location: str, description: str = None) -> dict:
    return Vendor.create_vendor(servie_id, name, location, description)


def add_new_slot(vendor_id: int, slot_date: str, start_time: str, max_people: int, price: float) -> dict:
    slot_date = datetime.strptime(slot_date, "%Y-%m-%d").date()
    start_time = datetime.strptime(start_time, "%H:%M").time()
    start_datetime = datetime.combine(datetime.today(), start_time)
    slot_end_datetime = start_datetime + timedelta(hours=1)
    slot_end = slot_end_datetime.time()

    Slot.create_slot(vendor_id, slot_date, start_time, slot_end, max_people, price)


def get_all_services() -> list[dict]:
    return Service.get_services()


def get_all_vendors() -> list[dict]:
    return Vendor.get_vendors()
