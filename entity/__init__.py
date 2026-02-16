import os
from functools import lru_cache,cached_property

from dotenv import load_dotenv

from entity.mongo_core import MongoDB

load_dotenv()

class UserDB:
    @cached_property
    def db(self):
        return MongoDB(db_name=os.getenv("MONGO_DB_NAME"),collection_name="users")

class VehicleDB:
    @cached_property
    def db(self):
        return MongoDB(db_name=os.getenv("MONGO_DB_NAME"),collection_name="vehicles")

@lru_cache(maxsize=100)
def transaction_db(collection_name: str) -> MongoDB:
    return MongoDB(db_name=os.getenv("MONGO_DB_TRANSACTIONS_DB_NAME"), collection_name=collection_name)

user_db = UserDB().db
vehicle_db = VehicleDB().db




