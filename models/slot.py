from dataclasses import dataclass, asdict
from database.connection import get_database_connection
from utils.utils import map_rows_to_dataclass


@dataclass
class Slot:
    id: int
    vendor_id: int
    slot_date: str
    start_time: str
    end_time: str
    max_people: int
    is_available: bool
    price: int

    @staticmethod
    def mark_unavailable(conn, slot_id: int):
        query = """
           UPDATE slots
           SET is_available = FALSE
           WHERE id = (%s)
        """
        with conn.cursor() as cursor:
            cursor.execute(query, (slot_id,))

    @classmethod
    def create_slot(cls, vendor_id: int, slot_date: str, start_time: str, end_time: str, max_people: int, price: float):
        query = """ 
            INSERT 
            INTO slots 
            (vendor_id, slot_date, start_time, end_time, max_people, price) 
            VALUES(%s, %s, %s, %s, %s, %s) 
            RETURNING id
            """
        connection = get_database_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (vendor_id, slot_date, start_time, end_time, max_people, price))
            slot_id = cursor.fetchone()[0]
            connection.commit()
            return asdict(cls(slot_id, vendor_id, slot_date, start_time, end_time, max_people, True, price))
        except Exception as e:
            print(f"Error while creating slot: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_slots(cls, vendor_id: int):
        query = """
            SELECT id, vendor_id, slot_date, start_time, end_time, max_people, is_available, price
            FROM slots
            WHERE vendor_id = (%s) AND is_available = (%s)
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (vendor_id, True))
            slots = cursor.fetchall()
            if slots:
                return map_rows_to_dataclass(cls, slots)
            return None
        except Exception as e:
            print(f"Error while retrieving user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
