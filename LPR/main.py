# # Importando as bibliotecas necessárias
# import cv2  # OpenCV para manipulação de imagem e vídeo
# import torch  # type: ignore # PyTorch, um framework de aprendizado de máquina
# import easyocr  # type: ignore # Biblioteca de OCR para reconhecimento de caracteres

# #from LPR.sort.sort_ import Sort  # Importa o algoritmo SORT para rastreamento de objetos
# from sort.sort_ import Sort  # Importa o algoritmo SORT para rastreamento de objetos

# from collections import deque  # Importa deque, uma lista de alta performance
# import re  # Importa re para trabalhar com expressões regulares


# # Inicializações
# reader = easyocr.Reader(['en'])  # Inicializa o OCR com suporte a inglês
# mot_tracker = Sort()  # Inicializa o rastreador SORT
# yolov5_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Carrega o modelo YOLOv5
# #plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./plate.pt')  # Carrega um modelo personalizado para placas

# plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\ct67ca\\Desktop\\Easy_Park\\LPR\\yolov5s.pt')  # Carrega um modelo personalizado para placas

# cap = cv2.VideoCapture('./videos/placas.mp4')  # Abre o arquivo de vídeo
# recent_plates = deque(maxlen=10)  # Cria uma deque para armazenar as últimas 10 placas detectadas

# # Função para pré-processar imagens, facilitando o reconhecimento de texto
# def preprocess_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Converte a imagem para escala de cinza
#     _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Aplica limiarização binária
#     denoised = cv2.medianBlur(binary, 5)  # Aplica um filtro de mediana para reduzir ruído
#     return denoised  # Retorna a imagem processada

# # Função para padronizar placas de veículos
# def standardize_plate(text):
#     text = re.sub(r'[^A-Z0-9]', '', text.upper())  # Remove caracteres não alfanuméricos e converte para maiúsculas
#     if len(text) == 7:  # Verifica se o texto tem 7 caracteres
#         letters = text[0:3] + text[4]  # Separa as letras
#         numbers = text[3] + text[5:7]  # Separa os números
#         letters = letters.replace('0', 'O').replace('1', 'I').replace('5', 'S')  # Substitui caracteres semelhantes
#         numbers = numbers.replace('O', '0').replace('I', '1').replace('S', '5')  # Substitui caracteres semelhantes
#         text = letters[0:3] + numbers[0] + letters[3] + numbers[1:3]  # Reorganiza os caracteres
#         return text  # Retorna a placa padronizada
#     return ""  # Retorna string vazia se não tiver 7 caracteres


# # def LicensePlateRecognition():

# # Loop para processar cada frame do vídeo
# while cap.isOpened():
#     ret, frame = cap.read()  # Lê um frame do vídeo
#     if not ret:
#         break  # Se não conseguir ler, sai do loop
    
#     frame_resized = cv2.resize(frame, (960, 540))# Diminui a imagem para ser apresentada na inferencia
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB
#     detections = yolov5_model(frame_rgb)  # Realiza a detecção de objetos no frame
#     vehicle_boxes = detections.xyxy[0][:, :4].cpu().numpy().astype(int)  # Extrai as caixas delimitadoras dos veículos
#     track_ids = mot_tracker.update(torch.Tensor(vehicle_boxes))  # Atualiza o rastreador com as caixas delimitadoras

#     plate_outputs = plate_model(frame_rgb)  # Detecta placas no frame
#     plate_detections = plate_outputs.xyxy[0][:, :4].cpu().numpy().astype(int)  # Extrai as caixas delimitadoras das placas

#     for plate_box in plate_detections:  # Para cada placa detectada
#         x1, y1, x2, y2 = map(int, plate_box)
#         cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Converte as coordenadas da caixa para inteiros
#         plate_crop = frame_rgb[y1:y2, x1:x2]  # Extrai a imagem da placa
#         preprocessed_plate = preprocess_image(plate_crop)  # Pré-processa a imagem da placa
#         results = reader.readtext(preprocessed_plate)  # Lê o texto da placa
        
#         for (bbox, text, prob) in results:  # Para cada texto lido na placa
#             if prob > 0.5:  # Se a confiança do OCR for maior que 0.5
#                 standardized_text = standardize_plate(text)  # Padroniza o texto
#                 if standardized_text and standardized_text not in recent_plates:  # Se o texto for válido e não estiver nas placas recentes
#                     recent_plates.append(standardized_text)  # Adiciona à lista de placas recentes
#                     print("Detected plate:", standardized_text)  # Imprime a placa detectada
#                     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Desenha um retângulo ao redor da placa
#                     cv2.putText(frame, standardized_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # Escreve o texto da placa sobre o vídeo

#     cv2.imshow('Frame', frame_resized)  # Mostra o frame processado
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Se pressionar 'q', sai do loop
#         break

# cap.release()  # Libera o recurso de vídeo
# cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV


# # if __name__ == "__main__":
# #     LicensePlateRecognition()



import cv2  # OpenCV para manipulação de imagem e vídeo
import torch  # PyTorch, um framework de aprendizado de máquina
import easyocr  # Biblioteca de OCR para reconhecimento de caracteres
from sort.sort_ import Sort  # Importa o algoritmo SORT para rastreamento de objetos
from collections import deque  # Importa deque, uma lista de alta performance
import re  # Importa re para trabalhar com expressões regulares

class PlateRecognition:
    def __init__(self, video_path, yolov5_model_path='yolov5s', plate_model_path='./plate.pt', max_recent_plates=10):
        self.reader = easyocr.Reader(['en'])  # Inicializa o OCR com suporte a inglês
        self.mot_tracker = Sort()  # Inicializa o rastreador SORT
        self.yolov5_model = torch.hub.load('ultralytics/yolov5', yolov5_model_path)  # Carrega o modelo YOLOv5
        self.plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\ct67ca\\Desktop\\Easy_Park\\LPR\\plate.pt')  # Carrega um modelo personalizado para placas
        self.cap = cv2.VideoCapture(video_path)  # Abre o arquivo de vídeo
        self.recent_plates = deque(maxlen=max_recent_plates)  # Cria uma deque para armazenar as últimas placas detectadas
        self.total_cars = 0
        

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Converte a imagem para escala de cinza
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Aplica limiarização binária
        denoised = cv2.medianBlur(binary, 5)  # Aplica um filtro de mediana para reduzir ruído
        return denoised  # Retorna a imagem processada

    def standardize_plate(self, text):
        text = re.sub(r'[^A-Z0-9]', '', text.upper())  # Remove caracteres não alfanuméricos e converte para maiúsculas
        if len(text) == 7:  # Verifica se o texto tem 7 caracteres
            letters = text[0:3] + text[4]  # Separa as letras
            numbers = text[3] + text[5:7]  # Separa os números
            letters = letters.replace('0', 'O').replace('1', 'I').replace('5', 'S')  # Substitui caracteres semelhantes
            numbers = numbers.replace('O', '0').replace('I', '1').replace('S', '5')  # Substitui caracteres semelhantes
            text = letters[0:3] + numbers[0] + letters[3] + numbers[1:3]  # Reorganiza os caracteres
            return text  # Retorna a placa padronizada
        return ""  # Retorna string vazia se não tiver 7 caracteres

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()  # Lê um frame do vídeo
            if not ret:
                break  # Se não conseguir ler, sai do loop

            frame_resized = cv2.resize(frame, (960, 540))  # Diminui a imagem para ser apresentada na inferencia
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB
            detections = self.yolov5_model(frame_rgb)  # Realiza a detecção de objetos no frame
            vehicle_boxes = detections.xyxy[0][:, :4].cpu().numpy().astype(int)  # Extrai as caixas delimitadoras dos veículos
            track_ids = self.mot_tracker.update(torch.Tensor(vehicle_boxes))  # Atualiza o rastreador com as caixas delimitadoras

            self.total_cars += len(vehicle_boxes)

            plate_outputs = self.plate_model(frame_rgb)  # Detecta placas no frame
            plate_detections = plate_outputs.xyxy[0][:, :4].cpu().numpy().astype(int)  # Extrai as caixas delimitadoras das placas

            for plate_box in plate_detections:  # Para cada placa detectada
                x1, y1, x2, y2 = map(int, plate_box)
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Converte as coordenadas da caixa para inteiros
                plate_crop = frame_rgb[y1:y2, x1:x2]  # Extrai a imagem da placa
                preprocessed_plate = self.preprocess_image(plate_crop)  # Pré-processa a imagem da placa
                results = self.reader.readtext(preprocessed_plate)  # Lê o texto da placa

                for (bbox, text, prob) in results:  # Para cada texto lido na placa
                    if prob > 0.5:  # Se a confiança do OCR for maior que 0.5
                        standardized_text = self.standardize_plate(text)  # Padroniza o texto
                        if standardized_text and standardized_text not in self.recent_plates:  # Se o texto for válido e não estiver nas placas recentes
                            self.recent_plates.append(standardized_text)  # Adiciona à lista de placas recentes
                            print("Detected plate:", standardized_text)  # Imprime a placa detectada
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Desenha um retângulo ao redor da placa
                            cv2.putText(frame, standardized_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # Escreve o texto da placa sobre o vídeo

            cv2.imshow('Frame', frame_resized)  # Mostra o frame processado
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Se pressionar 'q', sai do loop
                break

        self.cap.release()  # Libera o recurso de vídeo
        cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV
        print("Total de carros detectados:", self.total_cars)



plate_recognition = PlateRecognition(video_path='C:\\Users\\ct67ca\\Desktop\\Easy_Park\\videos\\placas.mp4')
plate_recognition.process_video()