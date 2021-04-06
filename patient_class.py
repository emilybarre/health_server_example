from pymodm import MongoModel, fields

class Patient(MongoModel):
    name = fields.CharField()
    id_no = fields.IntegerField(primary_key=True)
    blood_type = fields.CharField()
    test = fields.ListField()