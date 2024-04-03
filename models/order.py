from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

"""
By inheriting from Base, the User class inherits all the features 
provided by Base, such as metadata management, reflection, 
and other ORM-related functionalities. This approach makes 
it easier to manage and work with database models in SQLAlchemy.
"""

class Order(BaseModel, Base):

    __tablename__ = 'order'

    medicine_id = Column(String(60), ForeignKey('medicine.id'), nullable=False)
    customer_id = Column(String(60), ForeignKey('customer.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False, default='pending')

    # Define relationship to Customer (many-to-one)
    customer = relationship("Customer", back_populates="orders")

    # Define relationship to Medicine (many-to-one)
    medicine = relationship("Medicine", back_populates="orders")

    # Define a relationship to Payment (one-to-one)
    payment = relationship("Payment", back_populates="order", uselist=False)

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)

    def to_dict(self):
        """
        Returns a dictionary representation of the class instance
        """
        inventory_dict = super().to_dict()
        inventory_dict['medicine_name'] = self.medicine.name
        inventory_dict['customer_email'] = self.customer.email
        return inventory_dict