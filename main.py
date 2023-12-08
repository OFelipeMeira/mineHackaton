from Database import connector
from datetime import datetime, timezone
import asyncio
#from User_Interface import Screen

# pip install tortoise-orm[asyncmy] -- install Tortoise ORM SQL

# to run needs to create User: 'MainUser' password: 'password'
#                 create database 'object_db'
# Note: this user must to have global privileges

async def create_data():

    await connector.init()

    # Adding Types
    # print(await connector.create_Type("Box w/ small blister", 30, 15))
    # print(await connector.create_Type("Box w/ big blister", 30, 15))
    # print(await connector.create_Type("Box w/ small hive", 30, 15))
    # print(await connector.create_Type("Box w/ big hive", 30, 15))
    # print(await connector.create_Type("Big box w/ vertical hive", 60, 30))
    # print(await connector.create_Type("Big box w/ horizontal hive", 60, 30))

    # Adding Boxes
    # print(await connector.create_box("C123", 1, datetime.now()))
    # print(await connector.create_box("C234", 2, datetime.now()))
    # print(await connector.create_box("C345", 3, datetime.now()))
    # print(await connector.create_box("C456", 4, datetime.now()))
    # print(await connector.create_box("C567", 5, datetime.now()))
    # print(await connector.create_box("C678", 6, datetime.now()))
    # print(await connector.create_box("C789", 1, datetime.now()))
    # print(await connector.create_box("C111", 2, datetime.now()))
    # print(await connector.create_box("C222", 3, datetime.now()))

    # Adding all part numbers
    for part_number in part_numbers_to_add:
        await connector.create_part_number(f"{part_number}")
        print(f"{part_number} Added")

    # Adding all Paternoster Positions
    for positions in paternoster_positions:
        await connector.create_paternoster_position(pos_name=positions)
        print(f"Position {positions} Added")


part_numbers_to_add = [
"281039240",
"281039009",
"281020472",
"281020780",
"0261S1094G",
"281039124",
"0261B006YV",
"0261S1000W",
"0261S1001L",
"0261S1002C",
"0261S1007U",
"0261S1009D",
"0261S100A0",
"0261S100AY",
"0261S101YD",
"0261S100AZ",
"0261S100B0",
"0261S100B1",
"0261S100B3",
"0261S100B4",
"0261S100B6",
"0261S100B7",
"0261S100B9",
"0261S100BE",
"0261S100BA",
"0261S100BB",
"0261S101BG",
"0261S101BH",
"0261S101U6",
"0261S101YB",
"0261S107D1",
"0261S105N0",
"0261S101YE",
"0261S101YH",
"0261S102SJ",
"0261S102TL",
"0261S102TM",
"0261S102V9",
"0261S102VA",
"0261S102X3",
"0261S102X4",
"0261S102X5",
"0261S104LH",
"0261S104UB",
"0261S1052N",
"0261S1059A",
"0261S1059B",
"0261S105H4",
"0261S105KR",
"0261S105YZ",
"0261S105YY",
"0261S105KS",
"0261S105WE",
"0261S105WF",
"0261S105XS",
"0261S105YE",
"0261S1061C",
"0261S1060B",
"0261S1062M",
"0261S106CK",
"0261S106CL",
"0261S106D7",
"0261S106D8",
"0261S106D6",
"0261S106DA",
"0261S106DT",
"0261S106DX",
"0261S106E0",
"0261S106E1",
"0261S106UX",
"0261S1061A",
"0261S106D9",
"0261S1061B",
"0261S106NZ",
"0261S106PN",
"0261S106R9",
"0261S106V0",
"0261S107MA",
"0261S107MB",
"0261S107MC",
"0261S107M5",
"0261S1060Z",
"0261S15021",
"0261S15161",
"0261S15314",
"0261S16429",
"0261S16430",
"0261S16464",
"0261S16518",
"0261S16519",
"0261S16520",
"0261S16521",
"0261S16522",
"0261S16523",
"0261S16525",
"0261S16526",
"0261S16527",
"0261S16528",
"0261S16529",
"0261S16530",
"0261S16531",
"0261S16609",
"0261S16610",
"0261S16947",
"0261S17441",
"0261S17655",
"0261S17842",
"0261S17853",
"0261S18067",
"0261S18068",
"0261S18069",
"0261S18073",
"0261S18097",
"0261S18099",
"0261S18101",
"0261S18112",
"0261S18126",
"0261S18211",
"0261S18387",
"0261S18446",
"0261S18447",
"0261S18448",
"0261S18556",
"0261S18557",
"0261S18558",
"0261S18570",
"0261S18572",
"0261S18630",
"0261S18632",
"0261S18634",
"0261S18636",
"0261S18638",
"0261S18640",
"0261S18642",
"YD0261S105YE",
"0261S18644",
"0261S18646",
"0261S18723",
"0261S18725",
"0261S18728",
"0261S18729",
"0261S18973",
"0261S18981",
"0261S19021",
"0261S19026",
"0261S19088",
"0261S19089",
"0261S19094",
"0261S19340",
"0261S19446",
"0261S19447",
"0261S19687",
"0261S19690",
"0261S19791",
"0261S19806",
"0261S20112",
"0261S20718",
"0261S20768",
"0261S20798",
"0261S20890",
"0261S20892",
"0261S20893",
"0261S20894",
"0261S21207",
"0261S21208",
"0261S21209",
"0261S21210",
"0261S21211",
"0261S21212",
"0261S21253",
"0261S21427",
"0261S21428",
"0261S21485",
"0261S21486",
"0261S21706",
"0261S21707",
"0261S21708",
"0261S21709",
"0261S21726",
"0261S21728",
"0261S21730",
"0261S21732",
"0261S21750",
"0261S21752",
"0261S21770",
"0261S21830",
"0261S21831",
"0261S21833",
"0261S21834",
"0261S21845",
"0261S21988",
"0261S22055",
"0261S22120",
"0261S22149",
"0261S22166",
"0261S22300",
"0261S22350",
"0261S22351",
"0261S22443",
"0261S22444",
"0261S22445",
"0261S22450",
"0261S13089 (24) Velho",
"0261S10645 (24) Velho",
"0261S10483 (24) Velho",
"0261S06893",
"0261S07892",
"0261S08073",
"0261S08526",
"0261S08640",
"0261S08641",
"0261S08849",
"0261S09196",
"0261S09748",
"0261S09897",
"0261S09898",
"0261S10004",
"0261S10005",
"0261S10433",
"0261S10435",
"0261S10437",
"0261S10439",
"0261S10455",
"0261S10483",
"0261S10645",
"0261S10746",
"0261S10760",
"0261S11061",
"0261S11891",
"0261S11892",
"0261S12143",
"0261S12144",
"0261S12145",
"0261S12653",
"0261S12813",
"0261S13060",
"0261S13087",
"0261S13088",
"0261S13089",
"0261S13702",
"0261S13703",
"0261S14241",
"Bloqueio",
"Caixas Vazias",
"0261B00008",
"0261B32617",
"0261B33209",
"0261B37524",
"0281B10B3N",
"0281039124",
"0261S22447"
]

paternoster_positions = [
"P01,1",
"P01,2",
"P01,3",
"P01,4",
"P01,5",
"P01,6",
"P01,7",
"P02,1",
"P02,2",
"P02,3",
"P02,4",
"P02,5",
"P02,6",
"P02,7",
"P03,1",
"P03,2",
"P03,3",
"P03,4",
"P03,5",
"P03,6",
"P03,7",
"P04,1",
"P04,2",
"P04,3",
"P04,4",
"P04,5",
"P04,6",
"P04,7",
"P05,1",
"P05,2",
"P05,3",
"P05,4",
"P05,5",
"P05,6",
"P05,7",
"P06,1",
"P06,2",
"P06,3",
"P06,4",
"P06,5",
"P06,6",
"P06,7",
"P07,1",
"P07,2",
"P07,3",
"P07,4",
"P07,5",
"P07,6",
"P07,7",
"P08,1",
"P08,2",
"P08,3",
"P08,4",
"P08,5",
"P08,6",
"P08,7",
"P09,1",
"P09,2",
"P09,3",
"P09,4",
"P09,5",
"P09,6",
"P09,7",
"P10,1",
"P10,2",
"P10,3",
"P10,4",
"P10,5",
"P10,6",
"P10,7",
"P11,1",
"P11,2",
"P11,3",
"P11,4",
"P11,5",
"P11,6",
"P11,7",
"P12,1",
"P12,2",
"P12,3",
"P12,4",
"P12,5",
"P12,6",
"P12,7",
"P13,1",
"P13,2",
"P13,3",
"P13,4",
"P13,5",
"P13,6",
"P13,7",
"P14,1",
"P14,2",
"P14,3",
"P14,4",
"P14,5",
"P14,6",
"P14,7",
"P15,1",
"P15,2",
"P15,3",
"P15,4",
"P15,5",
"P15,6",
"P15,7",
"P16,1",
"P16,2",
"P16,3",
"P16,4",
"P16,5",
"P16,6",
"P16,7",
"P17,1",
"P17,2",
"P17,3",
"P17,4",
"P17,5",
"P17,6",
"P17,7",
"P18,1",
"P18,2",
"P18,3",
"P18,4",
"P18,5",
"P18,6",
"P18,7",
"P19,1",
"P19,2",
"P19,3",
"P19,4",
"P19,5",
"P19,6",
"P19,7",
"P20,1",
"P20,2",
"P20,3",
"P20,4",
"P20,5",
"P20,6",
"P20,7",
"P21,1",
"P21,2",
"P21,3",
"P21,4",
"P21,5",
"P21,6",
"P21,7",
"P22,1",
"P22,2",
"P22,3",
"P22,4",
"P22,5",
"P22,6",
"P22,7",
"P23,1",
"P23,2",
"P23,3",
"P23,4",
"P23,5",
"P23,6",
"P23,7",
"P24,1",
"P24,2",
"P24,3",
"P24,4",
"P24,5",
"P24,6",
"P24,7",
"P25,1",
"P25,2",
"P25,3",
"P25,4",
"P25,5",
"P25,6",
"P25,7",
"P26,1",
"P26,2",
"P26,3",
"P26,4",
"P26,5",
"P26,6",
"P26,7",
"P27,1",
"P27,2",
"P27,3",
"P27,4",
"P27,5",
"P27,6",
"P27,7",
"P28,1",
"P28,2",
"P28,3",
"P28,4",
"P28,5",
"P28,6",
"P28,7"
]

async def drop():
    await connector.connect()
    await connector.drop_all()
    print("database Droppped")


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

async def import_data():
    await connector.connect()
    await connector.import_data()

async def create_box():
    await connector.connect()
    await connector.create_box("C987")

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
    # asyncio.run( create_box() )
    """
    NEED TO EXPORT DATA - pandas
    """