import cv2
import os
from datetime import datetime, timedelta

# Constantes de configuracao
PASTA_SAIDA = "outputs"  # Diretorio para armazenar os videos gravados
HORARIO_INICIO = "00:00"  # Horario de inicio da deteccao
HORARIO_FIM = "05:00"  # Horario de termino da deteccao
LIMIAR_MOVIMENTO = 80  # Limite de sensibilidade para a deteccao de movimento
AREA_MINIMA = 1500  # Area minima do movimento para ser considerada relevante
HISTORICO_FUNDO = 1000  # Quantidade de frames para o subtrator de fundo
VARIACAO_FUNDO = 100  # Sensibilidade do subtrator de fundo

# Funcao que verifica se o horario atual esta dentro do intervalo permitido para deteccao
def verificar_horario(inicio, fim):
    agora = datetime.now().strftime('%H:%M')
    return inicio <= agora <= fim

# Funcao que gera um nome unico para o arquivo de video com base no horario atual
def obter_nome_arquivo():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Funcao para escrever logs dentro da pasta do video
def escrever_log(mensagem, pasta_video):
    with open(os.path.join(pasta_video, "log.txt"), "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")

# Funcao principal de deteccao e gravacao de video
def detectar_movimento_webcam():
    captura = cv2.VideoCapture(0)  # Inicializa a captura de video pela webcam
    if not captura.isOpened():
        print("Erro ao acessar a webcam.")
        return

    # Configuracao inicial do video
    largura = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(captura.get(cv2.CAP_PROP_FPS)) or 30  # Default FPS caso nao seja identificado
    nome_arquivo = obter_nome_arquivo()

    # Diretorio e arquivo de saida
    pasta_video = os.path.join(PASTA_SAIDA, nome_arquivo)
    os.makedirs(pasta_video, exist_ok=True)  # Cria a pasta do video
    codec = cv2.VideoWriter_fourcc(*"MJPG")  # Codec MJPEG (compativel com a maioria dos sistemas)
    arquivo_video = os.path.join(pasta_video, f"{nome_arquivo}.avi")
    gravador = cv2.VideoWriter(arquivo_video, codec, fps, (largura, altura))

    # Inicializacao do subtrator de fundo com parametros ajustados
    subtrator_fundo = cv2.createBackgroundSubtractorMOG2(history=HISTORICO_FUNDO, varThreshold=VARIACAO_FUNDO)

    # Variaveis de controle
    pausado = False
    proxima_divisao = datetime.now().replace(hour=12 if datetime.now().hour < 12 else 0, minute=0, second=0, microsecond=0) + timedelta(hours=12)

    # Log inicial
    escrever_log(f"Inicio da gravacao: {arquivo_video}", pasta_video)

    try:
        while True:
            ret, frame = captura.read()
            if not ret:
                print("Erro ao ler o video da webcam.")
                break

            # Suaviza o frame para reduzir o impacto de ruidos de camera
            frame_suavizado = cv2.GaussianBlur(frame, (5, 5), 0)

            # Verifica se esta dentro do horario permitido para deteccao
            dentro_horario = verificar_horario(HORARIO_INICIO, HORARIO_FIM)

            if dentro_horario and not pausado:
                # Aplica o subtrator de fundo para detectar movimentos
                mascara_fundo = subtrator_fundo.apply(frame_suavizado)
                _, mascara_binaria = cv2.threshold(mascara_fundo, LIMIAR_MOVIMENTO, 255, cv2.THRESH_BINARY)

                # Detecta contornos dos movimentos
                contornos, _ = cv2.findContours(mascara_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                movimentos_detectados = len(contornos)

                for contorno in contornos:
                    if cv2.contourArea(contorno) > AREA_MINIMA:
                        (x, y, w, h) = cv2.boundingRect(contorno)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Log de movimento detectado
                if movimentos_detectados > 0:
                    escrever_log(f"Movimento detectado: {movimentos_detectados} movimentos", pasta_video)

            elif not dentro_horario:
                # Exibe no frame que a deteccao esta desativada
                cv2.putText(frame, "Deteccao desativada (fora do horario)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                escrever_log(f"Deteccao desativada - Fora do horario", pasta_video)

            # Grava o frame processado no arquivo
            gravador.write(frame)

            # Exibe o frame na tela
            cv2.imshow("Deteccao de Movimento - Webcam", frame)

            # Controle de pausa e play
            tecla = cv2.waitKey(30) & 0xFF
            if tecla == ord('q'):  # Sair do programa
                escrever_log(f"Gravacao interrompida", pasta_video)
                break
            elif tecla == ord('p'):  # Pausar e continuar a gravacao
                pausado = not pausado
                estado = "Pausado" if pausado else "Continuando"
                escrever_log(f"Gravacao {estado}", pasta_video)

            # Verifica se e hora de dividir o arquivo de video
            if datetime.now() >= proxima_divisao and (datetime.now().minute == 0 and datetime.now().second == 0):
                print("Dividindo o arquivo de video...")
                gravador.release()  # Fecha o arquivo de video atual
                nome_arquivo = obter_nome_arquivo()  # Gera um novo nome para o arquivo
                pasta_video = os.path.join(PASTA_SAIDA, nome_arquivo)
                os.makedirs(pasta_video, exist_ok=True)  # Cria nova pasta
                arquivo_video = os.path.join(pasta_video, f"{nome_arquivo}.avi")
                gravador = cv2.VideoWriter(arquivo_video, cv2.VideoWriter_fourcc(*"MJPG"), fps, (largura, altura))
                escrever_log(f"Arquivo de video dividido: {arquivo_video}", pasta_video)
                proxima_divisao = datetime.now().replace(hour=12 if datetime.now().hour < 12 else 0, minute=0, second=0, microsecond=0) + timedelta(hours=12)

    except KeyboardInterrupt:
        print("Gravacao interrompida.")
    finally:
        # Libera os recursos da captura e gravacao
        captura.release()
        gravador.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detectar_movimento_webcam()
