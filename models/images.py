import hashlib
import uuid

from pprint import pprint
from datetime import datetime

from pymysql.err import IntegrityError
from models import Model, Field

class Image(Model):

	table_name = "images"

	id = Field(int, modifiable=False)
	user_id = Field(int)
	image64 = Field(str)
	image_type = Field(str)

	