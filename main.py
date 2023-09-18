from Database import connector
from datetime import datetime, timezone
import asyncio
from User_Interface import Screen

# pip install tortoise-orm[asyncmy] -- install Tortoise ORM SQL

async def create_data():

    await connector.init()

    # print(await connector.create_Type("Box w/ small blister", 30, 15))
    # print(await connector.create_Type("Box w/ big blister", 30, 15))
    # print(await connector.create_Type("Box w/ small hive", 30, 15))
    # print(await connector.create_Type("Box w/ big hive", 30, 15))
    # print(await connector.create_Type("Big box w/ vertical hive", 60, 30))
    # print(await connector.create_Type("Big box w/ horizontal hive", 60, 30))
# 
    # print(await connector.create_box(1, "C123", datetime.now()))
    # print(await connector.create_box(2, "C234", datetime.now()))
    # print(await connector.create_box(3, "C345", datetime.now()))
    # print(await connector.create_box(4, "C456", datetime.now()))
    # print(await connector.create_box(5, "C567", datetime.now()))
    # print(await connector.create_box(6, "C678", datetime.now()))
# 
    # print(await connector.create_paternoster_position("P1.1"))
    # print(await connector.create_paternoster_position("P1.2"))
    # print(await connector.create_paternoster_position("P1.3"))
    # print(await connector.create_paternoster_position("P1.4"))
    # print(await connector.create_paternoster_position("P1.5"))
    # print(await connector.create_paternoster_position("P2.1"))
    # print(await connector.create_paternoster_position("P2.2"))
    # print(await connector.create_paternoster_position("P2.3"))
    # print(await connector.create_paternoster_position("P2.4"))
    # print(await connector.create_paternoster_position("P2.5"))


    #print(await connector.alter_period("test2", 50))

    #box = await connector.get_box("C453")

    #print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # box = await connector.use_box(box.serial_number)

    # print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # box = await connector.clean_box(box.serial_number)

    # print(f"Name: {box.serial_number}, type: {box.box_type.name}, last_cleand: {box.last_cleand}, uses: {box.uses}")

    # print(await connector.get_types())


async def createPositon(pos):
    await connector.connect()
    await connector.create_paternoster_position(pos)

async def deletePosition(pos):
    await connector.connect()
    await connector.delete_paternoster_position(pos)

async def get_first_usable_pos():
    await connector.connect()
    a = await connector.get_first_usable_pos()
    print(a)

async def insert_paternoster(box_name):
    await connector.connect()
    if await connector.verify_box_paternoster(box_name):
        await connector.insert_paternoster(box_name)
    else:
        print("deu erro")

async def remove_paternoster(box_name):
    await connector.connect()
    await connector.remove_paternoster_box(box_name)

async def teste():
    await connector.connect()

    # now = datetime.now(tz=None)
    # await connector.insert_teste(date=now)

    a = await connector.get_inserted_date(2)
    # b = a.replace(tzinfo=None)
    # delta = timedelta(a, datetime.now())


    ###
    #
    #   SOLUÇÃO: ==== USAR timezone.utc)===
    #
    ####
    print(a.date1 - datetime.now(timezone.utc))
    # print(b)

if __name__ == '__main__':
    #asyncio.run(create_data())
    #asyncio.run(Screen.Screen())
    
#    print( asyncio.run(insert_paternoster("C123")) )
#    print( asyncio.run(remove_paternoster('C123')) )
    # print( asyncio.run(get_first_usable_pos()) )


    asyncio.run(teste())
    pass
