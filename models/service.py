from dataclasses import dataclass, asdict
from database.connection import get_database_connection
from utils.utils import map_rows_to_dataclass


@dataclass
class Service:
    id: int
    name: str

    @classmethod
    def create_service(cls, name: str):
        query = """ 
            INSERT 
            INTO services 
            (name) 
            VALUES(%s) 
            RETURNING id
            """
        connection = get_database_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, (name,))
            id = cursor.fetchone()[0]
            connection.commit()
            return asdict(cls(id, name))
        except Exception as e:
            print(f"Error while creating service: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_services(cls):
        query = """
            SELECT id, name
            FROM services
        """
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            services = cursor.fetchall()
            if services:
                return map_rows_to_dataclass(cls, services)
            return None
        except Exception as e:
            print(f"Error while retrieving user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
