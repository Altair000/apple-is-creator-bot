import yaml
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from main import home, get_captcha, validate_info, verification, send_verify_code

# VARIABLES GLOBALES
chat_id = None
captcha_token = None
captcha_id = None
scnt = None
widgetKey = None
sessionId = None
captcha = None
email = None
password = None
first_name = None
last_name = None
birth = None

# CARGAR CREDENCIALES DESDE YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

TOKEN = config['bot']['token'] # BOT TOKEN
ADMIN = config['bot']['admin_id'] # ADMIN ID

# CONFIGURACIONES DEL BOT
bot = telebot.TeleBot(TOKEN)
# RUTA DE LA IMAGEN CAPTCHA
image_path = 'image.jpg'
# COMANDOS
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, "¡Hola! Soy un bot para crear cuentas de Apple ID. Pulse el botón para comenzar")
    # Crear un teclado inline
    markup = types.InlineKeyboardMarkup()
    # Agregar un botón
    btn = types.InlineKeyboardButton("Haz clic aquí para iniciar el proceso", callback_data="register")
    markup.add(btn)  # Agregar el botón al teclado
    bot.send_message(chat_id, "Seleccione una opción:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "register")
def handle_button_click(call):
    global scnt, widgetKey, sessionId, captcha_token, captcha_id
    scnt, widgetKey, sessionId = home()
    captcha_token, captcha_id = get_captcha(scnt, widgetKey, sessionId)
    bot.send_photo(chat_id, photo=open(image_path, 'rb'))
    bot.reply_to(call.message, "Por favor, resuelva el captcha: ")
    bot.register_next_step_handler(call.message, icaptcha)

def icaptcha(message):
    global captcha  # Usar variable global
    captcha = message.text
    bot.reply_to(message, "Ahora introduzca su email: ")
    bot.register_next_step_handler(message, correo)


def correo(message):
    global email  # Usar variable global
    email = message.text
    bot.reply_to(message, "Ingrese la contraseña. Debe de ser 8 caracteres [una mayuscula, numeros y signos]: ")
    bot.register_next_step_handler(message, primer_nombre)

def primer_nombre(message):
    global password  # Usar variable global
    password = message.text
    bot.reply_to(message, "Ingrese su primer nombre comenzando con mayuscula: ")
    bot.register_next_step_handler(message, apellido)

def apellido(message):
    global first_name  # Usar variable global
    first_name = message.text
    bot.reply_to(message, "Ingrese su apellido comenzando con mayuscula: ")
    bot.register_next_step_handler(message, cumple)

def cumple(message):
    global last_name  # Usar variable global
    last_name = message.text
    bot.reply_to(message, "Ingrese su fecha de nacimiento en el siguiente formato 'Año-Mes-Día': ")
    bot.register_next_step_handler(message, finish)

def finish(message):
    global birth  # Usar variable global
    birth = message.text
    bot.reply_to(message, "Por favor espere...")
    validate_info(scnt, widgetKey, sessionId, email, password, first_name, last_name, birth, captcha, captcha_token, captcha_id)
    Id = verification(scnt, widgetKey, sessionId, email, first_name, last_name)
    msg, status = send_verify_code(scnt, widgetKey, email, sessionId, Id)
    bot.send_message(chat_id, msg)
    bot.send_message(chat_id, status)

@bot.message_handler(commands=['log'])
def send_log(message):
    chat_id = message.chat.id
    bot.send_document(chat_id, 'app.log')

if __name__ == '__main__':
    print("Bot Ejecutando")
    bot.infinity_polling()
