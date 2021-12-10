from telethon import TelegramClient, events
import asyncio
import telethon
from telethon.events import NewMessage, CallbackQuery, newmessage
from telethon.tl.custom import Message, Button, button, message
import os
from urllib.parse import unquote
import random
import time

def oe(lista_enlaces):
    lista = []
    for i in lista_enlaces:
        if i != "":
            if i not in lista:
                lista.append(i)
    dicc = {}
    for l in lista:
        if not l in dicc:
            dicc[l.split("/")[-1]] = l
    d = sorted(dicc.items())
    text = []
    for i in d:
        v = (str(i).replace("(","").replace(")","").replace("'","").split(", ")[1])
        text.append(v)
    a = "\n".join(text)
    lista = []
    t = str(a).split("\n")
    for i in t:
        if i != "":
            lista.append(i)
    res = []
    for i in lista:
        nombre = unquote(unquote(i.split("/")[-1]))
        texto = i + "?  " + nombre + "\n"
        res.append(texto)
    a = "".join(res)
    return a


str_pedido = """🟢Hola esta es la __información__ de tu pedido🟢
🎬__Estos capítulos__ que te enviamos son los que nuestro equipo tiene para **📥DESCARGAR Y LUEGO 📤SUBIR __MEDIANTE LA ☁️NUBE☁️__** y asi puedas descargarlos __**sin gasto de megas**__.

**🗒Pediste:**
__{}__

#️⃣**Son __{}__ capítulos**

⚖️**Peso Total:**
🔰__{} **MB**__

🔰__{} **GB**__

💲**Costo Total:**
__{}__
🔰__{} **CUP**__

Verifica que ese sea el pedido que deseas, puedes comprobar el peso, y precio
Precio actual: __$**1 CUP** x cada **135 MB** del PESO TOTAL__ ヽ(*￣▽￣*)ノ

📟PUEDES PAGAR POR __💳TRANSFERENCIA BANCARIA__ O  __📲SALDO MÓVIL__ .-.-.-.-.

☑️Solo esperamos __tú confirmación__ para comenzar,
        **¿Quieres el pedido por ese precio?**"""


if __name__ == '__main__':
    try:
        if not os.path.exists("dev"):
            api_id = os.environ['API_ID']
            api_hash = os.environ['API_HASH']
            bot_token = os.environ['BOT_TOKEN']
            #users_allowed = os.environ['AUTH_USERS']
        else:
            api_id = "8805372"
            api_hash = "708f6bdf31d8c698f628a68ac2d92c09"
            bot_token = "1906762390:AAH0bT5eB_mwBbNiaeHnrjDSbfa_XTt6l48"
            #users_allowed = "1935578948 1449646326"
    except:
        print("error en la configuracion")

    #users_allowed = users_allowed.split(" ")

    print("iniciando..")
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    @bot.on(NewMessage())
    async def message_handler(event: message.Message):


        if event.raw_text.lower() == "/start":
            await bot.send_message(event.sender_id, "**Todo ok puedes __usarme__**")

        ########################## Inicio#####################################
        #######################################################################
        ###################### Ordenar enlaces ################################
        elif "/p " in event.raw_text.lower():
            if os.path.exists(str(event.sender_id) + "pedido.txt"):
                    os.unlink(str(event.sender_id) + "pedido.txt")
            if os.path.exists(str(event.sender_id) + "inicio....suma"):
                    os.unlink(str(event.sender_id) + "inicio....suma")
            nombre = event.message.message.replace("/p ", "")
            with open(str(event.sender_id) + "inicio....orden", "w") as f:
                f.write(nombre)

        ######################################################################
        ############### Inicio Sumar Pedidos #################################
        elif "/s " in event.raw_text.lower():
            if os.path.exists(str(event.sender_id) + "inicio....orden"):
                os.unlink(str(event.sender_id) + "inicio....orden")
            if os.path.exists(str(event.sender_id) + "..enlaces"):
                os.unlink(str(event.sender_id) + "..enlaces")
            pedido = event.message.message.replace("/s ", "")
            with open(str(event.sender_id) + "inicio....suma", "w") as f:
                f.write(pedido)

        ########################## Procesar Archivos ######################
        ###################################################################
        elif event.file:
            ######################## Archivos Ordenar Pedidos ######################
            if os.path.exists(str(event.sender_id) + "inicio....orden"):
                try:
                            nombre = str(event.message.media.document.attributes[0].file_name)
                except:
                            nombre = "None"
                if nombre.split(".")[-1] == "txt":
                            if os.path.exists(nombre):
                                nombre = nombre.replace(nombre.split(".")[-1], "") + str(random.randint(0, 500)) + nombre.split(".")[-1]
                            file = await event.message.download_media(file="./" + nombre)
                            with open(nombre, "r") as f:
                                enlaces = f.read()
                            with open(str(event.sender_id) + "..enlaces", "a") as f:
                                f.write(enlaces)
                            try:
                                os.unlink(nombre)
                            except:
                                pass
        ##########################################################################
        ####################### Archivos Sumar Pedidos ####################################
            elif os.path.exists(str(event.sender_id) + "inicio....suma"):
                size = event.media.document.size
                with open(str(event.sender_id) + "..pedido.txt", "a") as f:
                    data = str("{0:.0f}".format(((size) / 1024 ** 2))) + " + "
                    f.write(data)


        ################### FIN ##################
        elif event.raw_text.lower() == "/f":
            #### Ordenar enlaces
            if os.path.exists(str(event.sender_id) + "..enlaces"):
                with open(str(event.sender_id) + "..enlaces", "r") as f:
                    enlaces = f.read().split("\n")
                orden = oe(enlaces)
                with open(str(event.sender_id) + "inicio....orden") as f:
                    nombre = f.read()
                with open(nombre + ".txt","w")as f:
                    f.write(orden)

                await bot.send_file(event.sender_id, nombre + ".txt")
                dirs = [
                        nombre + ".txt", str(event.sender_id) + "..enlaces",
                        str(event.sender_id) + "inicio....orden",
                        str(event.sender_id) + "inicio....suma",
                        str(event.sender_id) + "..pedido.txt"
                        ]
                for d in dirs:
                    try:
                        if os.path.exists(d):
                            os.unlink(d)
                    except:
                        pass

            #### Sumar pedidos
            elif os.path.exists(str(event.sender_id) + "inicio....suma"):
                if os.path.exists(str(event.sender_id) + "..pedido.txt"):
                    with open(str(event.sender_id) + "inicio....suma", "r") as f:
                        pedido = f.read()
                    with open(str(event.sender_id) + "..pedido.txt", "r") as f:
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
                    dirs = [
                        str(event.sender_id) + "inicio....orden",
                        str(event.sender_id) + "inicio....suma",
                        str(event.sender_id) + "..pedido.txt"
                        ]
                    for d in dirs:
                        try:
                            if os.path.exists(d):
                                os.unlink(d)
                        except:
                            pass
        else:
                await event.reply("**Al parecer __no has comenzado__ ninguna tarea**")


    loop = asyncio.get_event_loop()
    print(":::::::::::::::Online.")
    loop.run_forever()