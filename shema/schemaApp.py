  
from flask_marshmallow import Marshmallow
ma = Marshmallow()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'description', 'reference', 'cant', 'fech_update')
