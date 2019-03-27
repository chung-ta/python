from datetime import datetime
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns as columns
from cassandra.cqlengine.models import Model
GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

# Create your models here.
class Account(DjangoCassandraModel):
    __table_name__ = 'account'
    username = columns.Text(max_length=20, primary_key=True)
    email = columns.Text(required =True, index=True)
    first_name = columns.Text(max_length=100)
    last_name = columns.Text(max_length=100)
    phone = columns.Text(max_length=20)
    gender = columns.Text(max_length=10)
    password = columns.Text(required=True, max_length=50)
    created_date = columns.DateTime(default=datetime.now, index=True)
    last_updated_date = columns.DateTime(default=datetime.now, index=True)

class AdminUser(DjangoCassandraModel):
    __table_name__ = 'admin_user'
    username = columns.Text(max_length=20, primary_key=True)
    email = columns.Text(required =True, index=True)
    first_name = columns.Text(max_length=100)
    last_name = columns.Text(max_length=100)
    password = columns.Text(required=True, max_length=50)
    created_date = columns.DateTime(default=datetime.now, index=True)
    is_active = columns.Boolean(default=True)

class UsLocation(DjangoCassandraModel):
    __table_name__ = 'us_cities'
    id = columns.UUID(primary_key=True)
    city_name = columns.Text
    latitude = columns.Float
    longitude = columns.Float
    state = columns.Text
    county = columns.Text
    zip_code = columns.Text

    def __str__(self):
        return '***' + str(self.id) + ' - ' + str(self.city_name)