#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import models


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        updated_set = flag_created_at = False
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at":
                    flag_created_at = True
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    updated_set = True
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        if not flag_created_at:
            self.created_at = datetime.now()
        if not updated_set:
            self.updated_at = datetime.now()
        self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        # from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Creates dictionary of the class.

        Returns:
            dict: key values in __dict__.
        """
        my_dict = {key: value for key, value in dict(
            self.__dict__).items() if key != "_sa_instance_state"}
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict

    def delete(self):
        """deletes the current instance from FileStorage.__objects
        """
        models.storage.delete(self)
