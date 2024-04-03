from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

"""
By inheriting from Base, the User class inherits all the features 
provided by Base, such as metadata management, reflection, 
and other ORM-related functionalities. This approach makes 
it easier to manage and work with database models in SQLAlchemy.
"""

class Inventory(BaseModel, Base):

    __tablename__ = 'inventory'

    medicine_id = Column(String(60), ForeignKey('medicine.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Define a relationship to the Inventory table
    medicine = relationship("Medicine", back_populates="inventory")

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the class instance
        """
        inventory_dict = super().to_dict()
        inventory_dict['medicine_name'] = self.medicine.name
        return inventory_dict