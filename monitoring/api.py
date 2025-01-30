import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

async def registrarStatus(id, status):
    headers = {'Content-Type': 'application/json'}
    url = f'{API_BASE_URL}/vagas?numVaga={id}'
    payload = {"statusVaga": status}


    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=payload, headers=headers) as response:
            if response.status == 200:
                print("Dados enviados com sucesso!")
            else:
                print("\n\n Erro ao enviar os dados:", await response.text())


async def registrarEntrada(plate, vaga):
    headers = { 'Content-Type': 'application/json'}
    url = f'{API_BASE_URL}/entradaSaida'
    payload = {
        "placa": plate,
        "numeroVaga": int(vaga)
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                print('Placa enviada!')
            else:
                print('Erro ao enviar a placa: ', await response.text())


async def registrarSaida(id_vaga, hora_saida):
    headers = { 'Content-Type': 'application/json'}
    url = f'{API_BASE_URL}/entradaSaida/{id_vaga}'
    playload = {
        "horaSaida": hora_saida,
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=playload, headers=headers) as response:
            if response.status == 200:
                print('Saída registrada com sucesso!')
            else:
                print('Erro ao registrar saída: ', await response.text())