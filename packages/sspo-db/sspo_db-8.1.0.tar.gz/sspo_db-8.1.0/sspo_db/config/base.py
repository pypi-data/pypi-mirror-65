from .config import Base
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from sqlalchemy_serializer import SerializerMixin
import uuid

class Entity(Base, SerializerMixin):

    __abstract__  = True
    serialize_rules =('-id', "-uuid")
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(binary=False), unique=True, nullable=False, default=uuid.uuid4)
    date_created  = Column(DateTime,  default=datetime.datetime.utcnow)
    date_modified = Column(DateTime,  default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)    

    name = Column(String(200), nullable=True)
    description = Column(Text(), nullable=True)
    is_instance_of = ""

    def entity_name(self):
        return self.is_instance_of
    
    def __repr__(self):
        return super().__repr__()

    def to_dict(self):
        dict = super().to_dict()
        dict['uuid'] = str(self.uuid)
        return dict
    