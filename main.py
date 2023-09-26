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

    print(await connector.create_paternoster_position("P1.1"))
    print(await connector.create_paternoster_position("P1.2"))
    print(await connector.create_paternoster_position("P1.3"))
    print(await connector.create_paternoster_position("P1.4"))
    print(await connector.create_paternoster_position("P1.5"))
    print(await connector.create_paternoster_position("P2.1"))
    print(await connector.create_paternoster_position("P2.2"))
    print(await connector.create_paternoster_position("P2.3"))
    print(await connector.create_paternoster_position("P2.4"))
    print(await connector.create_paternoster_position("P2.5"))

async def drop():
    await connector.connect()
    await connector.drop_all()


async def createPositon(pos):
    await connector.connect()
    await connector.create_paternoster_position(pos)

async def deletePosition(pos):
    await connector.connect()
    await connector.delete_paternoster_position(pos)

async def test():
    await connector.connect()

async def insert_paternoster(box_name):
    await connector.connect()
    if await connector.verify_box_paternoster(box_name):
        await connector.insert_paternoster(box_name)
    else:
        print("deu erro")
    await connector.disconnect()

async def remove_paternoster(box_name):
    await connector.connect()
    await connector.remove_paternoster_box(box_name)
    await connector.disconnect()

if __name__ == '__main__':
    # asyncio.run(create_data())
    # asyncio.run(drop())

    print(asyncio.run( test() ))
    
    # print( asyncio.run(insert_paternoster("C123")) )
    # print( asyncio.run(insert_paternoster("C789")) )

# ========== Vai ter que mudar ainda 
    print( asyncio.run(remove_paternoster('C123')) )
    # print( asyncio.run(remove_paternoster('C234')) )