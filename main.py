from telethon import TelegramClient, events
import asyncio
import telethon
from telethon.events import NewMessage, CallbackQuery, newmessage
from telethon.tl.custom import Message, Button, button, message
import os

str_pedido = """🟢Hola te escribo por el pedido que realizaste🟢
🗒Pediste:
**{}**

#️⃣Son **{}** capítulos

⚖️Peso Total:
🔰**{} MB**

🔰**{} GB**

💲Costo Total:
**{}**
🔰**{} CUP**

🎬Estos son los capítulos que nuestro equipo tiene para **📥DESCARGAR Y LUEGO 📤SUBIR MEDIANTE LA ☁️NUBE☁️** para que puedas descargarlos sin gasto de megas.

Puede comprobar el peso y precio, Es $1 CUP x cada 135 MB del PESO TOTAL ヽ(*￣▽￣*)ノ

📟PUEDES PAGAR POR 💳TRANSFERENCIA BANCARIA O  📲SALDO MÓVIL .-.-.-.-.

☑️Solo esperamos tú confirmación para comenzar,
        ¿Quieres el pedido por ese precio?"""


if __name__ == '__main__':
    try:
        api_id = os.environ['API_ID']
        api_hash = os.environ['API_HASH']
        bot_token = os.environ['BOT_TOKEN']
        users_allowed = os.environ['AUTH_USERS']
    except:
        api_id = "5095599"
        api_hash = "ac087d6bb97a885e4f64571cf7ead8a4"
        bot_token = "1906762390:AAH0bT5eB_mwBbNiaeHnrjDSbfa_XTt6l48"
        users_allowed = "1935578948"

    users_allowed = users_allowed.split(" ")

    print("iniciando..")
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    @bot.on(NewMessage())
    async def message_handler(event: message.Message):
        if not str(event.sender_id) in users_allowed:
            return

        if "/inicio" in event.raw_text.lower():
            pedido = event.message.message.replace("/inicio ", "")
            with open("inicio....suma", "w") as f:
                f.write(pedido)
        elif event.raw_text.lower() == "/fin":
            with open("inicio....suma", "r") as f:
                pedido = f.read()
            with open("pedido.txt", "r") as f:
                valores = f.read()
            valores = valores.split(" + ")
            datos = []
            for x in valores:
                if x != "":
                    datos.append(x)
            cantidad = len(datos)
            total = 0
            for dato in datos:
                total += float(dato)
            total_gb = ("{0:.1f}".format(((total / 1024))))
            precio_decimal = ("{0:.5f}".format(((total / 135))))
            precio = ("{0:.0f}".format(((total // 135))))

            suma_str = " + ".join(datos) + " = " + str("{0:.0f}".format(total))
            divicion_str = str("{0:.0f}".format(total)) + " ÷ 135 = " + str(precio_decimal)
            msg_pedido = str_pedido.format(pedido, cantidad, suma_str, total_gb, divicion_str, precio)
            await bot.send_message(event.chat_id, msg_pedido)
            if os.path.exists("pedido.txt"):
                os.unlink("pedido.txt")
            if os.path.exists("inicio....suma"):
                os.unlink("inicio....suma")

        elif os.path.exists("inicio....suma"):
            size = event.media.document.size
            with open("pedido.txt", "a") as f:
                data = str("{0:.0f}".format(((size) / 1024 ** 2))) + " + "
                f.write(data)

    loop = asyncio.get_event_loop()
    print(":::::::::::::::Online.")
    loop.run_forever()