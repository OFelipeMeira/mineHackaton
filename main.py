from Database import connector
from datetime import datetime
import asyncio
from User_Interface import Screen

# pip install tortoise-orm[asyncmy] -- install Tortoise ORM SQL

async def create_data():

    await connector.init()

    print(await connector.create_Type("Box w/ small blister", 30, 15))
    print(await connector.create_Type("Box w/ big blister", 30, 15))
    print(await connector.create_Type("Box w/ small hive", 30, 15))
    print(await connector.create_Type("Box w/ big hive", 30, 15))
    print(await connector.create_Type("Big box w/ vertical hive", 60, 30))
    print(await connector.create_Type("Big box w/ horizontal hive", 60, 30))
    
    print(await connector.create_box(1, "C123", datetime.now()))
    print(await connector.create_box(2, "C234", datetime.now()))
    print(await connector.create_box(3, "C345", datetime.now()))
    print(await connector.create_box(4, "C456", datetime.now()))
    print(await connector.create_box(5, "C567", datetime.now()))
    print(await connector.create_box(6, "C678", datetime.now()))


    #print(await connector.alter_period("test2", 50))

    #box = await connector.get_box("C453")

    #print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # box = await connector.use_box(box.serial_number)

    # print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # box = await connector.clean_box(box.serial_number)

    # print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # print(await connector.get_types())

async def testes():
    await connector.connect()

    #-- inserindo caixas no paternoster:
#    await connector.insert_paternoster("C123",1)
    
#    #--pegando as caixas do paternoster:
#    boxes = await connector.get_all_paternoster_boxes()
#    print(boxes[0])

    await connector.remove_paternoster("C123")
    


if __name__ == '__main__':
    #asyncio.run(create_data())
    #asyncio.run(Screen.Screen())
    
    asyncio.run(testes())





