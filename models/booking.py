from database.connection import get_database_connection
from dataclasses import dataclass, asdict
from datetime import datetime
from utils.utils import map_rows_to_dataclass


@dataclass
class Booking:
    booking_id: int
    user_id: int
    slot_id: int
    people_count: int
    slot_time: str
    status: str

    @staticmethod
    def combine_datetime(slot_date: str, slot_time: str) -> str:
        return datetime.combine(slot_date, slot_time)

    @classmethod
    def create_booking(cls, user_id: int, slot_id: int, people_count: int, slot_date: str, slot_time: str, Slot):
        slot_datetime = cls.combine_datetime(slot_date, slot_time)

        query = """ 
            INSERT 
            INTO bookings 
            (user_id, slot_id, people_count, slot_time, status)
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING booking_id
            """
        values = (user_id, slot_id, people_count, slot_datetime, "confirmed")

        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            connection.autocommit = False

            cursor.execute(query, values)
            booking_id = cursor.fetchone()[0]

            Slot.mark_unavailable(connection, slot_id)
            connection.commit()
            return asdict(cls(booking_id, user_id, slot_id, people_count, slot_time, "confirmed"))
        except Exception as e:
            print("Error creating booking:", e)
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_bookings(cls, user_id: int):
        query = """
           SELECT booking_id, user_id, slot_id, people_count, slot_time, status
           FROM bookings
           WHERE user_id = %s
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (user_id,))
            bookings = cursor.fetchall()
            if bookings:
                return map_rows_to_dataclass(cls, bookings)
            return None
        except Exception as e:
            print(f"Error while retrieving bookings: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
            
    @staticmethod
    def clear_bookings(user_id: int):
        query = """
           DELETE
           FROM bookings
           WHERE user_id = %s
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (user_id,))
            connection.commit()
            return True
        except Exception as e:
            connection.rollback()
            print(f"Error while deleting bookings history: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
