from tortoise.models import Model
from tortoise import Tortoise, fields
from datetime import datetime


"""
    MODELS
        Boxes
        Types
        Paternoster
"""
class Boxes(Model):
    """ Table to register all the boxes """
    box_id = fields.IntField(pk=True)
    box_type = fields.ForeignKeyField('models.Types', related_name='types')
    serial_number = fields.CharField(64, unique=True)
    last_cleand = fields.DateField()
    uses = fields.IntField()

    def __str__(self):
        return self.serial_number

class Types(Model):
    """ Table to register al the Types of boxes """    
    type_id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    max_num_uses = fields.IntField()
    cleaning_period = fields.IntField()

    def __str__(self):
        return self.name
    
class Paternoster(Model):
    """ Table to keep a register from all the boxes inserted on paternoster,
      keeping note from the insert and remove date.
      Also manage to remove only boxes after 1 day
    """
    pat_id = fields.IntField(pk=True)
    pat_box = fields.ForeignKeyField('models.Boxes', related_name='boxes')
    pat_pos = fields.ForeignKeyField('models.PaternosterPositions', related_name="pat_positions")
    insert_date = fields.CharField(19)
    removed_date = fields.CharField(19, default="")
    
    def __str__(self):
        return self.pat_id

class PaternosterPositions(Model):
    """ Table to register all the positions of the Paternoster """
    pos_id = fields.IntField(pk=True)
    pos_name = fields.CharField(10)
    in_use = fields.BooleanField(default=False)

class Testes(Model):
    id = fields.IntField(pk=True)
    date1 = fields.DatetimeField()
    date2 = fields.DatetimeField(null=True)

"""
    SETUP
        init
        connect
"""
async def init():
    """ Method to create and setup the models from the mySql database and generate schemas"""
    await Tortoise.init(
        db_url="mysql://MainUser:password@127.0.0.1:3306/object_db",
        modules={'models' : ['Database.connector']},
    )
    # Generate the schema
    await Tortoise.generate_schemas()

async def connect():
    """ Default Tortoise method to connect the database """
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
    """ Method used to create a new box at Boxes table
    :param: type_id:int  - Id from the Type of the box
    :param: serial_number: str - Serial number wroted in the QRCode in the box
    :param: last_cleand: datetime.object - Now
    :param: uses:int  - How many times were used - default 0
    """
    box_type = await Types.get(type_id=type_id)
    await Boxes.create(box_type = box_type, serial_number = serial_number, last_cleand = last_cleand, uses = uses)

async def use_box(box_serial_number: str):
    """ Method used to use a single box
    It adds 1 in the usages of this box

    :param: box_serial_number:str - Name of the box to select
    :return: box:Boxes.object - Register with that serial number
    """

    box = await Boxes.get(serial_number=box_serial_number)
    box.uses += 1
    await box.save()
    return await get_box(box_serial_number)

async def clean_box(box_serial_number: str):
    """ Method used to clean a single box
    It turns uses of a box to 0.
    
    :param: box_serial_number:str - Name of the box to select
    :return: box:Boxes.object - Register with that serial number
    """
    box = await Boxes.get(serial_number=box_serial_number)
    box.uses = 0
    box.last_cleand = datetime.now()
    await box.save()
    return await get_box(box_serial_number)

async def get_box(box_serial_number: str):
    """ Method used to return a single box object

    :param: box_serial_number:str - Name of the box to select
    :return: box:Boxes.object - Register with that serial number
    """
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
        alter_box
"""
async def create_Type(name: str, max_num_uses: int, cleaning_period: int):
    """ Method used to create new Type into the table Types
    :param: name:str - Name of the new Type
    :param: max_num_uses:int - Maximum of usages per cleaning
    :param: cleaning_period:int - How long (in days) boxes from this types need to be cleaned
    """
    await Types.create(name = name, max_num_uses = max_num_uses , cleaning_period = cleaning_period)

async def get_type(type_name: str):
    """ Method to return a single Type
    :param: type_name:str - Name of a type 
    :return: TypesObject
    """
    return await Types.get(name=type_name)

async def get_types():
    """ Method used to return all Types registered 
    :return: list - all types registered
    """
    return await Types.all().values()

async def alter_period(box_type_name: str, new_period: int, new_uses = 0):
    """ Method used to update the period of cleaning from a Type """
    return await alter_box(box_type_name, box_type_name, new_period, new_uses)

async def alter_box(box_type_name: str, box_type_name_new: str, new_period: int, new_uses = 0):
    """
    :param: box_type_name:str - Name of the Type to update
    :param: box_type_name:str - New name of the Type
    :param: new_period:int - New cleaning period
    :param: new_uses:int  - New usages - default 0
    :retun: box_type: Types.object - 
    """
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

"""
    Paternoster
        insert_paternoster
        remove_paternoster
"""

async def insert_paternoster(serial_number: str):
    """ Method used to insert new Boxes into Paternoster

    :param: box_serial_number :str - Code readed from QRCode in the box
    :return: True - if nothing goes wrong
    """
    insert_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    box = await Boxes.get(serial_number=serial_number)
    pos = await get_first_usable_pos()
    pos.in_use = True
    await pos.save()
    await Paternoster.create(pat_box_id=box.box_id, insert_date=insert_date, pat_pos=pos)
    return True

async def remove_paternoster_box(box_serial_number: str):
    """ Method used to remove a box from the Paternoster

    The method checks if already been more than one day when the box was inserted.
    if so, removes.

    :param: box_serial_number :str - Code readed from QRCode in the box
    :return: if the box can be removed, return True, else return None
    """
    box = await Boxes.get(serial_number=box_serial_number)
    box_pat = await Paternoster.get(pat_box_id=box.box_id, removed_date="")

    # getting the inserted date
    insert_data = box_pat.insert_date
    
    # Converting string from the DB to date object:
    insert_data = datetime.strptime(insert_data, '%Y-%m-%d %H:%M:%S')

    delta_time = datetime.now() - insert_data

    if delta_time.days <= 1:
        pat_pos = await PaternosterPositions.get(pos_id=box_pat.pat_pos_id)
        pat_pos.in_use = False
        box_pat.removed_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        await pat_pos.save()
        await box_pat.save()
        return True
    else:
        return None
    
async def verify_box_paternoster(box_serial_number:str):
    """ Method used to verify if a box is already is on Paternoster

    If the box selected, is not in Paternoster, ou already had been taken off - retrun True
    If the box selected, is inside Paternoster and haven't been taken off     - return False

    :param: box_serial_number :str - Code readed from QRCode in the box

    :return: Boolean
    """

    box = await Boxes.get_or_none(serial_number=box_serial_number)
    pat = await Paternoster.get_or_none(pat_box_id=box.box_id, removed_date="")
    print(pat)
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
async def create_paternoster_position(pos_name:str):
    """ Method to create a new position on the PaternosterPositions table

    :param: pos_name: str - Name readed from QRCode from the paternoster position
    """
    await PaternosterPositions.create(pos_name=pos_name)

async def delete_paternoster_position(pos_name:str):
    """ Method to delete a position from PaternosterPositions table 

    :param: pos_name : str - Name readed from QRCode from the paternoster position
    """
    pos_object = await PaternosterPositions.get(pos_name=pos_name)
    await pos_object.delete()

async def get_first_usable_pos():
    """ Method used to return the first usable position from the Paternoster

    :return: pos : PaternosterPosition register - First usable position
    """
    pos = await PaternosterPositions.filter(in_use=False)
    return pos[0]

""" TESTES
"""
async def get_inserted_date(id):
    a = await Testes.get(id=id, date2=None)
    return a

async def insert_teste(date):
    await Testes.create(date1=date)

