import re                     # Importa expressões regulares para extrair IPs
from datetime import datetime # Importa data e hora para o relatório

# -------------------------------------------------------------------------
# CRIA UM ARQUIVO DE LOG FAKE PARA TESTAR
# -------------------------------------------------------------------------

# Abre o arquivo "server.log" para escrita e cria logs simulados
with open("server.log", "w") as file:
    file.write("Nov 12 14:33:01 server sshd[1201]: Failed password for root from 177.233.10.45 port 45821 ssh2\n")
    file.write("Nov 12 14:34:05 server sshd[1202]: Accepted password for user1 from 192.168.0.10 port 52345 ssh2\n")
    file.write("Nov 12 14:35:11 server sshd[1203]: Failed password for admin from 177.233.10.45 port 45822 ssh2\n")
    file.write("Nov 12 14:36:00 server sshd[1204]: Connection closed by 192.168.0.11\n")
    file.write("Nov 12 14:36:50 server sshd[1205]: Failed password for root from 10.0.0.5 port 50231 ssh2\n")

# -------------------------------------------------------------------------
# FUNÇÃO PARA LER O ARQUIVO DE LOG E CONTAR TENTATIVAS DE LOGIN FALHO
# -------------------------------------------------------------------------

def ler_logs(caminho):
    contador = {}  # Dicionário que guarda {ip: quantidade_de_tentativas}
    regex = r"from ([\d\.]+) port"  # Expressão regular para capturar IP

    # Abre o arquivo e pega todas as linhas
    with open(caminho, "r") as file:
        linhas = file.readlines()

    # Percorre cada linha do arquivo
    for linha in linhas:

        # Verifica se contém um erro de senha
        if "Failed password" in linha:        

            # Procura o IP na linha usando o regex
            match = re.search(regex, linha)
            if match:
                ip = match.group(1)  # Extrai apenas o IP encontrado

                # Incrementa o contador para o IP
                if ip in contador:
                    contador[ip] += 1
                else:
                    contador[ip] = 1

    return contador  # Retorna o dicionário com as tentativas por IP  

# -------------------------------------------------------------------------
# FUNÇÃO PARA COLORIR TEXTOS NO TERMINAL
# -------------------------------------------------------------------------

def colorir(texto, cor):
    cores = {
        "VERMELHO": "\033[31m",
        "VERDE": "\033[32m",
        "AMARELO": "\033[33m",
        "AZUL": "\033[34m",
        "CIANO": "\033[36m",
        "RESET": "\033[0m"
    }
    return cores.get(cor, cores["RESET"]) + texto + cores["RESET"]

# -------------------------------------------------------------------------
# MOSTRA ALERTAS COM BASE NA QUANTIDADE DE TENTATIVAS
# -------------------------------------------------------------------------

def mostrar_alertas(contador, limite=3):
    ataque_detectado = False  # Controle para saber se houve ataque

    # Percorre todos os IPs e suas tentativas
    for ip, total_tentativas in contador.items():
        
        # Caso grave: muitas tentativas
        if total_tentativas >= limite:
            msg = f"🚨 ATAQUE DETECTADO do IP: {ip} Tentativas: {total_tentativas}"
            print(colorir(msg, "VERMELHO"))
            ataque_detectado = True

        # Caso leve: poucas tentativas
        elif total_tentativas > 0 and total_tentativas <= 3:
            msg2 = f"🔔 ATAQUE SUSPEITO do IP: {ip} Tentativas: {total_tentativas}"
            print(colorir(msg2, "AMARELO"))
            ataque_detectado = True

    # Caso nenhum ataque tenha sido encontrado
    if not ataque_detectado:
        msg3 = f"🟢 Nenhum ataque detectado"
        print(colorir(msg3, "VERDE"))

# -------------------------------------------------------------------------
# GERA RELATÓRIO DIÁRIO EM ARQUIVO
# -------------------------------------------------------------------------

def gerar_relatorio(contador, limite=3):
    ataque_detectado = False
    now = datetime.now()                      # Data e hora atual
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")  # Formato bonito

    # Abre o arquivo para adicionar informações
    with open("relatorio_diario.log", "a", encoding="utf-8") as file:

        for ip, total_tentativas in contador.items():

            # Caso grave
            if total_tentativas >= limite:
                msg = f"🚨 ATAQUE DETECTADO do IP: {ip} Tentativas: {total_tentativas}"
                print(colorir(msg, "VERMELHO"))
                file.write(f"{timestamp} - {msg}\n")
                ataque_detectado = True

            # Caso leve
            elif total_tentativas > 0 and total_tentativas <= 3:
                msg2 = f"🔔 ATAQUE SUSPEITO do IP: {ip} Tentativas: {total_tentativas}"
                print(colorir(msg2, "AMARELO"))
                file.write(f"{timestamp} - {msg2}\n")
                ataque_detectado = True

        # Caso nenhum ataque
        if not ataque_detectado:
            msg3 = f"🟢 Nenhum ataque detectado"
            print(colorir(msg3, "VERDE"))
            file.write(f"{timestamp} - {msg3}\n")

# -------------------------------------------------------------------------
# ANÁLISE INTERATIVA MANUAL DE UM IP
# -------------------------------------------------------------------------

def analisar_ip_interativo(limite=3):
    ataque_detectado = False
    ip = input("Digite o IP que deseja analisar: ")
    score = 0  # Pontuação de risco

    # Pergunta sobre tentativas de login
    tentativas_altas = input("Houve muitas tentativas de login? (S/N): ").upper()
    if tentativas_altas == "S":
        score += 1

    # Pergunta quantidade de tentativas
    quantidade_tentativas = int(input("Houve quantas tentativas de login? "))

    # Classifica pelo número de tentativas
    if quantidade_tentativas >= limite:
        ataque_detectado = True
        msg = f"🚨 ATAQUE DETECTADO do IP: {ip} Tentativas: {quantidade_tentativas}"
        print(colorir(msg, "VERMELHO"))

    elif quantidade_tentativas > 0 and quantidade_tentativas <= 3:
        ataque_detectado = True
        msg2 = f"🔔 ATAQUE SUSPEITO do IP: {ip} Tentativas: {quantidade_tentativas}"
        print(colorir(msg2, "AMARELO"))

    if not ataque_detectado:
        msg3 = f"🟢 Nenhum ataque detectado"
        print(colorir(msg3, "VERDE"))

    # Perguntas adicionais para compor pontuação final
    porta_suspeita = input("O IP tentou acessar portas suspeitas? (S/N): ").upper()
    if porta_suspeita == "S":
        score += 1

    varias_horas = input("Atividade continua por várias horas? (S/N): ").upper()
    if varias_horas == "S":
        score += 1

    user_invalido = input("Tentou logar com usuários inválidos? (S/N): ").upper()
    if user_invalido == "S":
        score += 1

    # Classificação final com base no score
    if score >= 3:
        nivel = "VERMELHO"
        print(colorir(f"🔶 CLASSIFICAÇÃO FINAL DO IP {ip}: NÍVEL VERMELHO (ALTO RISCO)", "VERMELHO"))

    elif score == 1 or score == 2:
        nivel = "AMARELO"
        print(colorir(f"⚠️ CLASSIFICAÇÃO FINAL DO IP {ip}: NÍVEL AMARELO (MÉDIO RISCO)", "AMARELO"))

    else:
        nivel = "VERDE"
        print(colorir(f"🟢 CLASSIFICAÇÃO FINAL DO IP {ip}: NÍVEL VERDE (SEGURO)", "VERDE"))

    return ip, nivel, quantidade_tentativas

# -------------------------------------------------------------------------
# SALVA RESULTADO DA ANÁLISE INTERATIVA NO RELATÓRIO
# -------------------------------------------------------------------------

def salvar_ip_relatorio(ip, nivel, quantidade_tentativas):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    with open("relatorio_diario.log", "a", encoding="utf-8") as file:
        file.write(f"{timestamp} - 🔔 ATAQUE SUSPEITO do IP: {ip} Tentativas: {quantidade_tentativas} Cor: {nivel}\n")

# -------------------------------------------------------------------------
# EXECUÇÃO DO SISTEMA
# -------------------------------------------------------------------------

contador = ler_logs("server.log")       # Lê o log e conta ataques
mostrar_alertas(contador)               # Mostra os alertas na tela
gerar_relatorio(contador)               # Salva no relatório diário

print("\n=== MODO INTERATIVO ===")
ip, nivel, quantidade_tentativas = analisar_ip_interativo()  # Perguntas manuais
salvar_ip_relatorio(ip, nivel, quantidade_tentativas)        # Salva o resultado
