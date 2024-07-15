  # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar equalização do histograma para melhorar o contraste
        equalized = cv2.equalizeHist(gray)
        
        # Aplicar um leve desfoque gaussiano para suavizar a imagem
        blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
        
        # Usar limiarização simples em vez de adaptativa
        _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        
        return binary  # Retorna a imagem processada