# Detecção de Movimento com Webcam 🎥

Este é o **projeto final** para a cadeira de **Inteligência Artificial**, desenvolvido pelo aluno: **Felipe Anderloni Soares**. O sistema desenvolvido realiza **detecção de movimento** utilizando a webcam do computador e grava vídeos automaticamente quando movimento é detectado, dentro de um período de tempo configurável. 

A aplicação também mantém registros de logs com informações sobre a gravação e os eventos de detecção de movimento.

## Funcionalidades ⚙️

- **Detecção de Movimento**: O sistema identifica variações no cenário, como objetos em movimento, usando a técnica de subtração de fundo do OpenCV.
- **Gravação Automática**: O vídeo é gravado automaticamente ao detectar movimento.
- **Logs de Atividade**: Logs detalham os eventos da gravação, como o início da captura e a detecção de movimento.
- **Controle de Horário**: A detecção de movimento é configurada para funcionar apenas em um intervalo específico (por padrão, entre 00:00 e 05:00).
- **Pausa/Continuação**: A gravação pode ser pausada e retomada pressionando a tecla `p`.
- **Divisão de Arquivos**: O arquivo de vídeo é dividido a cada 12 horas, organizando melhor os arquivos gerados.

## Requisitos 🔧

- **Python 3.10** ou superior
- **Bibliotecas**:
  - `opencv-python`: Para captura de vídeo e processamento de imagens.
  - `os`: Para manipulação de arquivos e diretórios.
  - `datetime`: Para controle de datas e horas.

Estrutura de Pastas 📁
A estrutura de diretórios do projeto deve ser a seguinte:

/projetoVisaoComputacional
│
├── outputs/            # Pasta onde os vídeos gravados serão armazenados
│
├── main.py             # Código principal de detecção de movimento
│
└── README.md           # Documentação do projeto

Como Executar ▶️
1. **Clone o Repositório:** Você pode clonar este repositório ou baixar o arquivo main.py para sua máquina local.

2. **Instale as Dependências:** Instale a biblioteca necessária (OpenCV) com o seguinte comando:
pip install opencv-python

3. **Execute o Script:** Após instalar as dependências, execute o script main.py para iniciar a detecção de movimento:
python main.py

4. **Monitoramento:** O sistema começará a capturar vídeo da sua webcam. Caso haja movimento detectado durante o período configurado (00:00 - 05:00), o vídeo será gravado na pasta outputs e um log será gerado na mesma pasta.
