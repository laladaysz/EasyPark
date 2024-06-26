import cv2
import numpy as np

# from LPR.main import PlateRecognition

def ParkingSpace():
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

    def cropping_spaces(image, coordinates, output_path):
        img = cv2.imread(image)

        x1, y1, x2, y2 = coordinates # 439, 87, 135, 212
  

        # NAO PODE SER DO MAIOR PRO MENOR TEM QUE MUDAR ISSO
        cropped_image = img[y:y+h,x:x+w] # 87: 212, 439, 135
        # cropped_image = img[87:212, 135:439] # 87:212, 439:135

        cv2.imwrite(output_path, cropped_image)
        # cv2.imwrite(output_path, img)

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

        # desenhando quadradinhos verdes sobre a img 
        for i, (x, y, w, h) in enumerate(vagas):
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
            recorte = imgDil[y:y+h,x:x+w]
            qtPxBranco = cv2.countNonZero(recorte)
            cv2.putText(img,str(qtPxBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
            
            if qtPxBranco > 4500 and not capturado[i]:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
            

                name_frame = f"frame_vaga{i+1}.jpg"
                cv2.imwrite(name_frame, img)
                capturado[i] = True
                print (f"capturado com sucesso! {i+1}")      
                cropping_spaces(name_frame, vagas[i], f"crop_vaga{i+1}.jpg")   
                continue
    
            else:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
  

        masked_img = cv2.bitwise_and(img, mask)
        cv2.imshow('video', masked_img)
        
        if cv2.waitKey(10) == 27: 
            break

                
    video.release()
    cv2.destroyAllWindows()

cont = 0
if cont == 0:

    ParkingSpace()