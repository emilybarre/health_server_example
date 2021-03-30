from pymodem import MongoModel, fields

class Patient(MongoModel):
    name = fields.CharField()
    id_no = fields.IntegerField()
    blood_type = fields.CharField()
    test = fields.ListField()