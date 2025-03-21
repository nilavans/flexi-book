from dataclasses import dataclass, asdict
from database.connection import get_database_connection
from utils.utils import map_rows_to_dataclass


@dataclass
class Vendor:
    id: int
    service_id: int
    name: str
    location: str
    description: str

    @classmethod
    def create_vendor(cls, service_id: int, name: str, location: str, description: str):
        query = """ 
            INSERT 
            INTO vendors 
            (service_id, name, location, description) 
            VALUES(%s, %s, %s, %s) 
            RETURNING id
            """
        connection = get_database_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (service_id, name, location, description))
            vendor_id = cursor.fetchone()[0]
            connection.commit()
            return asdict(cls(vendor_id, service_id, name, location, description))
        except Exception as e:
            print(f"Error while creating vendor: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_vendors_service_id(cls, service_id: int):
        query = """
            SELECT id, service_id, name, location, description
            FROM vendors
            WHERE service_id = (%s)
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (service_id,))
            vendors = cursor.fetchall()
            if vendors:
                return map_rows_to_dataclass(cls, vendors)
            return None
        except Exception as e:
            print(f"Error while retrieving vendors: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_vendors(cls):
        query = """
            SELECT id, service_id, name, location, description
            FROM vendors
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            vendors = cursor.fetchall()
            if vendors:
                return map_rows_to_dataclass(cls, vendors)
            return None
        except Exception as e:
            print(f"Error while retrieving all vendors: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
