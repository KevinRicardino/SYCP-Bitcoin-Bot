import ssl
import json
from datetime import datetime, timedelta, timezone

import websocket

def comprar():
    pass


def vender():
    pass


def ao_abrir(ws):
    print()
    print(" REAL TIME BITCOIN BOT ".center(60, "="))
    print("\n>>> Abriu a conexão!")

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""

    ws.send(json_subscribe)


def ao_fechar(ws):
    print()
    print("-" * 60)
    print("\n>>> Fechou a conexão!")


def erro(ws, erro):
    print()
    print("-" * 60)
    print("\n>>> Deu erro!")


def ao_receber_mensagem(ws, mensagem):
    mensagem = json.loads(mensagem) # Parsing (pegar e mudar mensagem visualmente)
    if mensagem['event'] == 'trade': # Verifica se a mensagem é de um evento de trade antes de acessar o preço
        # Define o fuso horário de Brasília (UTC-3)
        fuso_brasilia = timezone(timedelta(hours=-3))

        # Pega a hora atual já com o fuso correto
        agora_br = datetime.now(fuso_brasilia)

        # Formata a exibição
        timestamp = agora_br.strftime('%H:%M:%S')

        price = mensagem['data']['price']

        if price > 64450:
            vender()
        elif price < 64450:
            comprar()
        else:
            print(">>> Ainda não há transações no valor desejado...")

        print(f"\tBTC/USD: [{price} - {timestamp}]")
    else:
        print(f">>> Evento de controle: {mensagem['event']}!!!\n")
        print("-" * 60)
        print()
        print("Último valor pedido para venda:\n")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=ao_abrir,
                                on_close=ao_fechar,
                                on_message=ao_receber_mensagem,
                                on_error=erro
                                )
    ws.run_forever(sslopt={"cert_regs": ssl.CERT_NONE})