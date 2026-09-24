import requests
import time

# --- CONFIGURAÇÕES DO SEU BOT ---
TELEGRAM_TOKEN = "8778700968:AAG3OOxije6liThsI5J3sTn3IWOtHLCuA58" # Token oficial do seu bot
TELEGRAM_CHAT_ID = "8824895218"                                    # Seu ID pessoal (Igor Santos)

# Lista das loterias monitoradas
LOTERIAS = ["megasena", "lotofacil", "quina"]

def buscar_resultado(loteria):
    """Busca o último resultado da loteria na API pública"""
    url = f"https://herokuapp.com{loteria}/latest"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Erro ao buscar {loteria}: {e}")
    return None

def formatar_mensagem(dados, loteria):
    """Formata o texto com emojis para o Status do WhatsApp"""
    nome_loteria = dados['loteria'].upper()
    concurso = dados['concurso']
    data = dados['data']
    dezenas = " - ".join(dados['dezenas'])
    acumulou = "❌ NÃO" if dados['acumulou'] == False else "💰 ACUMULOU!"
    proximo_premio = dados.get('proximovalorEstimado', 0)
    
    # Emojis personalizados por jogo
    emoji = "🍀"
    if loteria == "megasena": emoji = "🟢"
    elif loteria == "lotofacil": emoji = "🟣"
    elif loteria == "quina": emoji = "🔵"

    texto = (
        f"{emoji} *{nome_loteria}* {emoji}\n"
        f"🏆 *Concurso:* {concurso} ({data})\n\n"
        f"🔢 *Números Sorteados:*\n"
        f"`{dezenas}`\n\n"
        f"📈 *Status:* {acumulou}\n"
        f"💸 *Estimativa Próximo Prêmio:* R\$ {proximo_premio:,.2f}\n\n"
        f"👉 _Siga Loterias Brasil para mais resultados!_"
    )
    return texto

def enviar_telegram(texto):
    """Envia a mensagem direto para o Telegram do Igor"""
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def executar_painel():
    print("Buscando resultados das loterias...")
    for loteria in LOTERIAS:
        dados = buscar_resultado(loteria)
        if dados:
            mensagem = formatar_mensagem(dados, loteria)
            enviar_telegram(mensagem)
            print(f"Resultado de {loteria} enviado para o Igor!")
            time.sleep(1)

if __name__ == "__main__":
    executar_painel()
