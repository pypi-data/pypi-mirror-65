from . import fields
from . import models
from .database import Database

db = Database()

Model = db.Model

__all__ = ['fields', 'models']
