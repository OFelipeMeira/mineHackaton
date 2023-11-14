from Database import connector
from datetime import datetime, timezone
import asyncio
#from User_Interface import Screen

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
    print(await connector.create_box(1, "C789", datetime.now()))
    print(await connector.create_box(2, "C111", datetime.now()))
    print(await connector.create_box(3, "C222", datetime.now()))

    for i in range(1,3,1):
        for j in range(1,10,1):
            await connector.create_paternoster_position(f"P{i}.{j}")
            print(f"Position P{i}.{j} created")


async def drop():
    await connector.connect()
    await connector.drop_all()


async def deletePosition(pos):
    await connector.connect()
    await connector.delete_paternoster_position(pos)

async def insert_paternoster(box_name):
    await connector.connect()
    await connector.insert_paternoster(box_name)
    await connector.disconnect()

async def remove_paternoster(box_name):
    await connector.connect()
    await connector.remove_paternoster(box_name)
    await connector.disconnect()

async def export_paternoster():
    await connector.connect()
    await connector.export_paternoster()

# async def import_data():
#     await connector.connect()
#     await connector.import_data()

if __name__ == '__main__':
    # asyncio.run(drop())
    # asyncio.run(create_data())

    # print(asyncio.run( test() ))
    
    # print( asyncio.run(insert_paternoster("C123")) )
    # print( asyncio.run(insert_paternoster("C789")) )
    # try:
    #     asyncio.run(remove_paternoster("C123"))
    # except Exception as e:
    #     print(e)

    # asyncio.run( export_paternoster() )
    # asyncio.run( import_data() )
    """
    NEED TO EXPORT DATA - pandas
    """