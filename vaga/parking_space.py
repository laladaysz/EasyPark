import asyncio
import aiohttp
import cv2
import numpy as np
import json
from LPR.main import PlateRecognition
from datetime import datetime

async def registrarStatus(id, status):
    headers = {'Content-Type': 'application/json'}
    url = f'http://localhost:8083/vagas?numVaga={id}'
    payload = {"statusVaga": status}


    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=payload, headers=headers) as response:
            if response.status == 200:
                print("Dados enviados com sucesso!")
            else:
                print("\n\n Erro ao enviar os dados:", await response.text())


async def registrarEntrada(plate, vaga):
    headers = { 'Content-Type': 'application/json'}
    url = 'http://localhost:8083/entradaSaida'
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
    url = f'http://localhost:8083/entradaSaida/{id_vaga}'
    playload = {
        "horaSaida": hora_saida,
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(url, json=playload, headers=headers) as response:
            if response.status == 200:
                print('Saída registrada com sucesso!')
            else:
                print('Erro ao registrar saída: ', await response.text())


async def ParkingSpace():
    vaga1 = [1, 89, 108, 213]
    vaga2 = [115, 87, 152, 211]
    vaga3 = [289, 89, 138, 212]
    vaga4 = [439, 87, 135, 212]
    vaga5 = [591, 90, 132, 206]
    vaga6 = [738, 93, 139, 204]
    vaga7 = [881, 93, 138, 201]
    vaga8 = [1027, 94, 147, 202]

    vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]

    video = cv2.VideoCapture(r'C:\Users\ct67ca\Desktop\Easy_Park\videos\vagas_reverse.mp4')
    check = True
    plateRecognition = PlateRecognition()

    capturado = [False] * len(vagas)

    while check == True:
        check,img = video.read() 
        
        
        if not check:
            break

        # img preta e branca contornada e borrada
        imgcinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgTh = cv2.adaptiveThreshold(imgcinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        imgBlur = cv2.medianBlur(imgTh, 5)
        kernel = np.ones((3,3),np.int8)
        imgDil = cv2.dilate(imgBlur, kernel)
        mask = np.zeros_like(img)

        def cropping_spaces(image, coordinates, output_path):
            img = cv2.imread(image)
            cropped_image = img[y:y+h,x:x+w] # 87: 212, 439, 135
            cv2.imwrite(output_path, cropped_image)
        
        # desenhando quadradinhos verdes sobre a img 
        for i, (x, y, w, h) in enumerate(vagas):
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
            recorte = imgDil[y:y+h,x:x+w]
            qtPxBranco = cv2.countNonZero(recorte)
            cv2.putText(img,str(qtPxBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

            vaga_id = str(i+1)
            
            if qtPxBranco > 4500 and not capturado[i]:

                capturado[i] = True
                print (f"capturado com sucesso! {i+1}")
                status = "STATUS_OCUPADO"

                await registrarStatus(vaga_id, status)

                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
                name_frame = f"frame_vaga{i+1}.jpg"
                cv2.imwrite(name_frame, img)
                cropping_spaces(name_frame, vagas[i], f"crop_vaga{i+1}.jpg")   

                crop_name = f'crop_vaga{vaga_id}.jpg'

                plate = 0

                if vaga_id == "4":
                    plate = plateRecognition.process_image(r'C:\Users\ct67ca\Desktop\EASYPARK - PIM\carre.jpg')
                    print(f"Placa detectada: {plate}")
                    await registrarEntrada(plate, vaga_id)

                elif vaga_id == "5":
                    plate = plateRecognition.process_image(r'C:\Users\ct67ca\Desktop\EASYPARK - PIM\carro 3.png')
                    print(f"Placa detectada: {plate}")

                    await registrarEntrada(plate, vaga_id)

                elif vaga_id == "6":
                    plate = plateRecognition.process_image(r'C:\Users\ct67ca\Desktop\EASYPARK - PIM\carros 1.jpg')
                    print(f"Placa detectada: {plate}")

                    await registrarEntrada(plate, vaga_id)
                
                


            elif qtPxBranco < 4500 and capturado[i]:

                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                capturado[i] = False
                print(f"Vaga {vaga_id} liberada!")
                # status = "STATUS_LIVRE"

                hora_saida = datetime.utcnow().isoformat() 
                # await registrarStatus(vaga_id, status)
                await registrarSaida(vaga_id, hora_saida)

        masked_img = cv2.bitwise_and(img, mask)
        cv2.imshow('video', masked_img)

        
        
        if cv2.waitKey(10) == 27: 
            break
                
    video.release()
    cv2.destroyAllWindows()


