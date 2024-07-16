import cv2  # OpenCV para manipulação de imagem e vídeo
import torch  # PyTorch, um framework de aprendizado de máquina
import easyocr  # Biblioteca de OCR para reconhecimento de caracteres
from LPR.sort.sort_ import Sort  # Importa o algoritmo SORT para rastreamento de objetos
from collections import deque  # Importa deque, uma lista de alta performance
import re  # Importa re para trabalhar com expressões regulares

class PlateRecognition:
    def __init__(self, yolov5_model_path='yolov5s', plate_model_path='./plate.pt', max_recent_plates=10):
        self.reader = easyocr.Reader(['en'])  # Inicializa o OCR com suporte a inglês
        self.mot_tracker = Sort()  # Inicializa o rastreador SORT
        self.yolov5_model = torch.hub.load('ultralytics/yolov5', yolov5_model_path)  # Carrega o modelo YOLOv5
        self.plate_model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\ct67ca\\Desktop\\Easy_Park\\LPR\\plate.pt')  # Carrega um modelo personalizado para placas
        self.recent_plates = deque(maxlen=max_recent_plates)  # Cria uma deque para armazenar as últimas placas detectadas
        self.total_cars = 0

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

    def process_image(self, image):
        image = cv2.imread(image)
        if image is None:
            raise ValueError("Erro ao carregar imagem")
        
        frame_resized = cv2.resize(image, (960, 540))  # Diminui a imagem para ser apresentada na inferencia
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB
        
        detections = self.yolov5_model(frame_rgb)  # Realiza a detecção de objetos no frame
        vehicle_boxes = detections.xyxy[0][:, :4].cpu().numpy().astype(int) 

        if len(detections.xyxy[0]) == 0:
            raise ValueError("Nenhum objeto detectado pelo modelp YOLOv5")

        self.total_cars = len(vehicle_boxes)

        plate_outputs = self.plate_model(frame_rgb)  # Detecta placas no frame
        plate_detections = plate_outputs.xyxy[0][:, :4].cpu().numpy().astype(int)  # Extrai as caixas delimitadoras das placas

        for plate_box in plate_detections: # Para cada placa detectada 
            x1, y1, x2, y2 = map(int, plate_box)
            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Converte as coordenadas da caixa para inteiros
            plate_crop = frame_rgb[y1:y2, x1:x2]  # Extrai a imagem da placa


            results = self.reader.readtext(plate_crop)  # Lê o texto da placa

            for (bbox, text, prob) in results:  # Para cada texto lido na placa
                if prob > 0.5:  # Se a confiança do OCR for maior que 0.5
                    standardized_text = self.standardize_plate(text)  # Padroniza o texto
                    if standardized_text and standardized_text not in self.recent_plates:  # Se o texto for válido e não estiver nas placas recentes
                        self.recent_plates.append(standardized_text)  # Adiciona à lista de placas recentes
                        print("Placa detectada:", standardized_text)  # Imprime a placa detectada

                        
        cv2.imshow('Frame', frame_resized)  # Mostra o frame processado
        cv2.waitKey(1) & 0xFF == ord('q')   
        cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV
        print("Total de carros detectados:", self.total_cars)
        return(standardized_text)



plate_recognition = PlateRecognition()
print(plate_recognition.process_image(r'C:\Users\ct67ca\Desktop\Easy_Park\carre.jpg'))