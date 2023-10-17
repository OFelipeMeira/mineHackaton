import pandas as pd
import asyncio
from Database import connector

async def get_data():
    await connector.connect()
    return await connector.get_paternoster_all()

def export_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('Paternoster.xlsx', index=False)



if __name__ == "__main__":
    data = asyncio.get_event_loop().run_until_complete(get_data())
    export_excel(data)