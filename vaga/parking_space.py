import asyncio
import aiohttp
import cv2
import numpy as np
import requests
import json
# import time

# from LPR.main import PlateRecognition

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

async def periodic_check(parking_status_func, interval, parking_space):
    while True:
        status_data = await parking_status_func()
        if status_data != periodic_check.previous_status:
            periodic_check.previous_status = status_data
            await send_parking_status(parking_space)
        await asyncio.sleep(interval)

periodic_check.previous_status = None

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

    video = cv2.VideoCapture(r'C:\Users\ct67ca\Desktop\Easy_Park\videos\vagas.mp4')
    check = True
    # qPLR = PlateRecognition(r'C:\Users\ct67ca\Desktop\Easy_Park\videos\placas.mp4')

    capturado = [False] * len(vagas)

    parking_status = []

    await periodic_check(get_parking_status, 2, parking_status)


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
                continue
    
            else:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

            vaga = str(i + 1)
            parking_status.append({"spot_id": vaga, "status": status})  
             # print (parking_status)

        # time.sleep(4)
        # status_data = await get_parking_status()
        # if status_data != parking_status:
        #     await send_parking_status(parking_status)

        masked_img = cv2.bitwise_and(img, mask)
        cv2.imshow('video', masked_img)
        
        if cv2.waitKey(10) == 27: 
            break

                
    video.release()
    cv2.destroyAllWindows()


# cont = 0
# if cont == 0:
#     import asyncio
#     asyncio.run(ParkingSpace())

async def main():
    video_task = asyncio.create_task(ParkingSpace())
    await video_task


asyncio.run(main())