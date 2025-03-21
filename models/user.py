from bcrypt import hashpw, gensalt, checkpw
from database.connection import get_database_connection
from dataclasses import dataclass, asdict


@dataclass
class User:
    user_id: int
    username: str
    password: str
    security_question: str
    security_answer: str

    # Hash password & security answer using bcrypt.
    @staticmethod
    def encrypt(value: str) -> str:
        hashed = hashpw(value.encode("utf8"), gensalt())
        return hashed.decode("utf-8")

    # Validate the providated data against the hashed value.
    @staticmethod
    def authorise(plaintext: str, hashed: str) -> bool:
        return checkpw(plaintext.encode("utf8"), hashed.encode("utf8"))

    # Register a new user in the db.
    @classmethod
    def create_user(cls, username: str, password: str, security_question: str, security_answer: str):
        hashed_pass = cls.encrypt(password)
        hashed_sa = cls.encrypt(security_answer)
        query = """ 
            INSERT 
            INTO users 
            (username, password, security_question, security_answer) 
            VALUES(%s, %s, %s, %s) 
            RETURNING user_id
            """
        values = (username, hashed_pass, security_question, hashed_sa)

        connection = get_database_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query, values)
            user_id = cursor.fetchone()[0]
            connection.commit()
            return cls(user_id, username, hashed_pass, security_question, security_answer)
        except Exception as e:
            print(f"Error while creating user: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_user_by_username(cls, username: str):
        query = """
            SELECT user_id, username, password, security_question, security_answer
            FROM users
            WHERE username = %s
        """

        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if user:
                return asdict(cls(*user))
            return None
        except Exception as e:
            print(f"Error while retrieving user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def get_user(cls, user_id: int):
        query = """
            SELECT user_id, username, password, security_question, security_answer
            FROM users
            WHERE user_id = %s
        """

        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                return asdict(cls(*user))
            return None
        
        except Exception as e:
            print(f"Error while retrieving user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def update_user(
        cls,
        user_id: int,
        username: str = None,
        password: str = None,
        security_question: str = None,
        security_password: str = None,
    ) -> bool:
        connection = get_database_connection()
        cursor = connection.cursor()

        try:
            updates = []
            values = []
            if username:
                updates.append("username = %s")
                values.append(username)
            if password:
                updates.append("password = %s")
                values.append(password)
            if security_question:
                updates.append("security_question = %s")
                values.append(security_question)
            if security_password:
                updates.append("security_answer = %s")
                values.append(security_password)

            if updates:
                values.append(user_id)
                query = f"""
                    UPDATE users 
                    SET {", ".join(updates)}
                    WHERE user_id = %s
                """
                print(query)
                cursor.execute(query, values)
                connection.commit()
                return True
            return False
        except Exception as e:
            print(f"Error while updating password: {e}")
            connection.rollback()
            return False
        finally:
            cursor.close()
            connection.close()
