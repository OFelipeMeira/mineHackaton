from tortoise.models import Model
from tortoise import Tortoise, fields
from datetime import datetime, timedelta


"""
    MODELS
        Boxes
        Types
        Paternoster
"""

class Boxes(Model):
    box_id = fields.IntField(pk=True)
    box_type = fields.ForeignKeyField('models.Types', related_name='types')
    serial_number = fields.CharField(64, unique=True)
    last_cleand = fields.DateField()
    uses = fields.IntField()

    def __str__(self):
        return self.serial_number

class Types(Model):
    type_id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    max_num_uses = fields.IntField()
    cleaning_period = fields.IntField()

    def __str__(self):
        return self.name
    
class Paternoster(Model):
    pat_id = fields.IntField(pk=True)
    pat_box = fields.ForeignKeyField('models.Boxes', related_name='boxes')
    pat_pos = fields.ForeignKeyField('models.PaternosterPositions', related_name="pat_positions")
    insert_date = fields.CharField(19)
    removed_date = fields.CharField(19, default="")
    
    def __str__(self):
        return self.pat_id

class PaternosterPositions(Model):
    pos_id = fields.IntField(pk=True)
    pos_name = fields.CharField(10)
    in_use = fields.BooleanField(default=False)


"""
    CONFIG
        init
        connect
"""
async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url="mysql://MainUser:password@127.0.0.1:3306/object_db",
        modules={'models' : ['Database.connector']},
    )
    # Generate the schema
    await Tortoise.generate_schemas()

async def connect():
    await Tortoise.init(
        db_url="mysql://MainUser:password@127.0.0.1:3306/object_db",
        modules={'models' : ['Database.connector']},
    )


"""
    Boxes
        create_box
        alter_box
        use_box
        clean_box
        get_box
"""

async def create_box(type_id: int, serial_number: str, last_cleand=datetime.now(), uses=0):
    box_type = await Types.get(type_id=type_id)
    await Boxes.create(box_type = box_type, serial_number = serial_number, last_cleand = last_cleand, uses = uses)

async def alter_box(box_type_name: str, box_type_name_new: str, new_period: int, new_uses = 0):
    new_uses = int(new_uses)
    new_period = int(new_period)
    box_type = await Types.get(name=box_type_name)
    if new_uses > 0:
        box_type.max_num_uses = new_uses
    box_type.cleaning_period = new_period
    if box_type_name != box_type_name_new:
        box_type.name = box_type_name_new
    await box_type.save()
    return box_type

async def use_box(box_serial_number: str):
    box = await Boxes.get(serial_number=box_serial_number)
    box.uses += 1
    await box.save()
    return await get_box(box_serial_number)

async def clean_box(box_serial_number: str):
    box = await Boxes.get(serial_number=box_serial_number)
    box.uses = 0
    box.last_cleand = datetime.now()
    await box.save()
    return await get_box(box_serial_number)

async def get_box(box_serial_number: str):
    box = await Boxes.get_or_none(serial_number=box_serial_number)
    if box:
        await box.fetch_related("box_type")
    return box


"""
    Types
        create_type
        get_type
        get_types
        alter_period
"""

async def create_Type(name: str, max_num_uses: int, cleaning_period: int):
    await Types.create(name = name, max_num_uses = max_num_uses , cleaning_period = cleaning_period)

async def get_type(type_name: str):
    return await Types.get(name=type_name)

async def get_types():
    return await Types.all().values()

async def alter_period(box_type_name: str, new_period: int, new_uses = 0):
    return await alter_box(box_type_name, box_type_name, new_period, new_uses)


"""
    Paternoster
        insert_paternoster
        remove_paternoster
"""

async def insert_paternoster(serial_number: str):
    insert_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    box = await Boxes.get(serial_number=serial_number)
    pos = await get_first_usable_pos()
    pos.in_use = True
    await pos.save()
    await Paternoster.create(pat_box_id=box.box_id, insert_date=insert_date, pat_pos=pos)

async def remove_paternoster_box(box_serial_number: str):
    """
    :param: code of the box
    :return: if the box can be removed, return False, else return none
    """
    box = await Boxes.get(serial_number=box_serial_number)

    box_pat = await Paternoster.get(pat_box_id=box.box_id, removed_date="")

    # getting the inserted date
    insert_data = box_pat.insert_date
    
    # Converting string from the DB to date object:
    insert_data = datetime.strptime(insert_data, '%Y-%m-%d %H:%M:%S')
    if (datetime.now()- insert_data) <= 1:
        pat_pos = await PaternosterPositions.get(pos_id=box_pat.pat_pos_id)

        pat_pos.in_use = False
        await pat_pos.save()

        box_pat.removed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await box_pat.save()
    
    else:
        return None
    
async def verify_box_paternoster(box_serial_number:str):
    """
    Method used to verify if a box is already is on Paternoster
    """

    box = await Boxes.get_or_none(serial_number=box_serial_number)
    pat = await Paternoster.get_or_none(pat_box_id=box.box_id)
    if pat:
        return False
    else:
        return True


"""
    PaternosterPosition
        create_paternoster_position
        delete_paternsoter_position
        get_first_usable_pos
"""

async def create_paternoster_position(pos_name):
    await PaternosterPositions.create(pos_name=pos_name)

async def delete_paternoster_position(pos_name):
    pos_object = await PaternosterPositions.get(pos_name=pos_name)
    await pos_object.delete()

async def get_first_usable_pos():
    pos = await PaternosterPositions.filter(in_use=False)
    return pos[0]

