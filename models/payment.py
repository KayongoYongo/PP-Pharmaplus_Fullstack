from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

"""
By inheriting from Base, the User class inherits all the features 
provided by Base, such as metadata management, reflection, 
and other ORM-related functionalities. This approach makes 
it easier to manage and work with database models in SQLAlchemy.
"""

class Payment(BaseModel, Base):

    __tablename__ = 'payment'

    order_id = Column(String(60), ForeignKey('order.id'), nullable=False)
    customer_id = Column(String(60), ForeignKey('customer.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False)
    delivery_trype = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False, default='pending')

    # Define a relationship to the Medicine table
    order = relationship("Order", back_populates="payment")
    customer = relationship("Customer", back_populates="payment")

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)