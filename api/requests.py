import asyncio
import aiohttp
import json

async def send_parking_status(parking_status):
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/receive-status/', data=json.dumps(parking_status), headers=headers) as response:
            if response.status == 200:
                print("Dados enviados com sucesso!")
            else:
                print("Erro ao enviar os dados:", await response.text())

async def get_parking_status():
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/api/status/', headers= headers) as response:
            if response.status == 200:
                try:
                    data = await response.json()
                    print("Dados recebidos com sucesso: ", data)
                    return(data)
                except aiohttp.ContentTypeError:
                    text_data = await response.text()
                    print("Dados recebidos como texto: ", text_data)
                    return(text_data)
            else: 
                print("Erro ao recuperar os dados: ", await response.text())

async def periodic_check(parking_status_func, interval, parking_status):
    while True:
        status_data = await parking_status_func()
        if status_data != periodic_check.previous_status:
            periodic_check.previous_status = status_data
            await send_parking_status(parking_status)
        await asyncio.sleep(interval)

periodic_check.previous_status = None

periodic_task = asyncio.create_task(periodic_check(get_parking_status, 2, parking_status))

# await periodic_task