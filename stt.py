import speech_recognition as sr
import ssl
import winsound  # Biblioteca nativa do Windows para sons do sistema

# Desativa a verificação rigorosa de SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def ouvir():
    """
    Ativa o microfone, toca um bipe, escuta o operador e retorna o texto.
    """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Ajustando ruído ambiente...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # --- Efeito sonoro de "Microfone Aberto" (Pode falar) ---
        # winsound.Beep(frequência em Hertz, duração em milissegundos)
        winsound.Beep(500, 150)  
        winsound.Beep(700, 200) 
        
        print("Pode falar...")
        try:
            # timeout: espera no máximo 5 segundos para você começar a falar
            # phrase_time_limit: grava no máximo 10 segundos de fala
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            # --- Efeito sonoro de "Erro/Cancelado" (Grave) ---
            winsound.Beep(400, 300)
            print("Erro: Demorou muito para falar.")
            return None
        
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Operador: {texto}")
        return texto.lower()
        
    except sr.UnknownValueError:
        winsound.Beep(350, 150)
        winsound.Beep(350, 150)
        print("Erro: O Google não conseguiu entender as palavras.")
        return None
    except sr.RequestError as e:
        winsound.Beep(350, 150)
        winsound.Beep(350, 150)
        print(f"Erro de conexão/SSL com o serviço do Google: {e}")
        return None

if __name__ == "__main__":
    resultado = ouvir()
    if resultado:
        print(f"Comando recebido: {resultado}")
