from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

"""
By inheriting from Base, the User class inherits all the features 
provided by Base, such as metadata management, reflection, 
and other ORM-related functionalities. This approach makes 
it easier to manage and work with database models in SQLAlchemy.
"""


class Medicine(BaseModel, Base):

    __tablename__ = 'medicine'

    name = Column(String(255), nullable=False)
    dosage = Column(String(255), nullable=False)
    cost = Column(Integer, nullable=False)
    storage_conditions = Column(String(255), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    description = Column(Text)

    # Define a relationship to the Inventory table
    inventory = relationship("Inventory", uselist=False, back_populates="medicine")

    # Define relationship to Order (one-to-many)
    orders = relationship("Order", back_populates="medicine")

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)