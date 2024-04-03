from models.engine.db import DB # Import the DB class
from models.medicine import Base as MedicineBase # Import the declarative base
from models.customer import Base as CustomerBase
from models.inventory import Base as InventoryBase
from models.order import Base as OrderBase
from models.payment import Base as PaymentBase
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Instantiate the DB object
db_instance = DB()

# Create medicine table using SQLAlchemy's create_all() method
MedicineBase.metadata.create_all(db_instance._DB__engine)

# Create customer table using SQLAlchemy's create_all() method
CustomerBase.metadata.create_all(db_instance._DB__engine)

# Create inventory table using SQLAlchemy's create_all() method
InventoryBase.metadata.create_all(db_instance._DB__engine)

# Create order table using SQLAlchemy's create_all() method
OrderBase.metadata.create_all(db_instance._DB__engine)

# Create payment table using SQLAlchemy's create_all() method
PaymentBase.metadata.create_all(db_instance._DB__engine)

print("Tables created successfully")

"""
NOTE:
SQLAlchemy doesn't handle database creation directly; 
it assumes that the database already exists. 
So, if you try to create tables without the database being present, 
it will result in an error.
"""