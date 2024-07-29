import asyncio
import aiohttp
import cv2
import numpy as np
import json
# from LPR.main import PlateRecognition
from LPR.main import PlateRecognition

async def send_parking_status(parking_status):
    headers = {'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/receive-status/', data=json.dumps(parking_status), headers=headers) as response:
            if response.status == 200:
                print("Dados enviados com sucesso!")
            else:
                print("Erro ao enviar os dados:", await response.text())


async def send_plate(plate):
    headers = { 'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/receive-plate/', json=plate, headers=headers) as response:
            if response.status == 201:
                print('Placa enviada!')
            else:
                print('Erro ao enviar a placa: ', await response.text())


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

    parking_status = [{'spot_id': '1', 'status': 'Free'}, {'spot_id': '2', 'status': 'Free'}, {'spot_id': '3', 'status': 'Free'},
    {'spot_id': '4', 'status': 'Free'}, {'spot_id': '5', 'status': 'Free'}, {'spot_id': '6', 'status': 'Free'}, {'spot_id': '7', 'status': 'Free'}, 
    {'spot_id': '8', 'status': 'Free'}]


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
            # x1, y1, x2, y2 = coordinates # 439, 87, 135, 212
            cropped_image = img[y:y+h,x:x+w] # 87: 212, 439, 135
            cv2.imwrite(output_path, cropped_image)
        
        # desenhando quadradinhos verdes sobre a img 
        for i, (x, y, w, h) in enumerate(vagas):
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
            recorte = imgDil[y:y+h,x:x+w]
            qtPxBranco = cv2.countNonZero(recorte)
            cv2.putText(img,str(qtPxBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
            status = "Free"
            
            if qtPxBranco > 4500 and not capturado[i]:
                status="Occupied"
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
                name_frame = f"frame_vaga{i+1}.jpg"
                cv2.imwrite(name_frame, img)
                capturado[i] = True
                print (f"capturado com sucesso! {i+1}")      
                cropping_spaces(name_frame, vagas[i], f"crop_vaga{i+1}.jpg")       


                vaga = str(i + 1)
                status_spot = {"spot_id": str(vaga), "status": status}

                updated = False
                for i in range(len(parking_status)):
                    if parking_status[i]["spot_id"] == vaga:
                        parking_status[i]["status"] = status
                        crop_name = f'crop_vaga{vaga}.jpg'
                        # plateRecognition.process_image(crop_name)
                        #plate = str(plateRecognition.process_image(r'C:\Users\ct67ca\Desktop\Easy_Park\carre.jpg')
                        plate_spot = {"spot_id": str(vaga), "plate": 'RTZ9H06'}
                        updated = True
                        
                if not updated:
                    parking_status.append(status_spot)

                print(parking_status)
                await send_parking_status(parking_status)
                await send_plate(plate_spot)


            elif qtPxBranco < 4500:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                status = 'Free'

                vaga = str(i + 1)
                status_spot = {"spot_id": vaga, "status": status}

                for i in range(len(parking_status)):
                    if parking_status[i]["spot_id"] == vaga and parking_status[i]["status"] == 'Occupied':
                        parking_status[i]["status"] = 'Free'
                        print(parking_status)
                        print("atualizei\n")
                        await send_parking_status(parking_status)

        masked_img = cv2.bitwise_and(img, mask)
        cv2.imshow('video', masked_img)

        
        
        if cv2.waitKey(10) == 27: 
            break
                
    video.release()
    cv2.destroyAllWindows()


