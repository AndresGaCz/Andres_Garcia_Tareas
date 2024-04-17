import logging
import re
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresiones regulares
saludo = re.compile(r"Hello|Hola", re.IGNORECASE)  # Saludos

estado = re.compile(r"Bien|Mal", re.IGNORECASE)  # Respuesta1

cumpleaños = re.compile(r"Pronto sera mi cumpleaños", re.IGNORECASE)  # Respuesta2

fecha = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")  # Respuesta3

despedida = re.compile(r"Adios|Bye", re.IGNORECASE)  # Despedida

# Comando start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help."""
    await update.message.reply_text("Help!")

# Respuestas

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    message_text = update.message.text
    if saludo.search(message_text):  # Si el usuario saluda
        await update.message.reply_text("Hola ¿Cómo te va?")
    elif estado.search(message_text):  # Si el usuario responde a "¿Cómo estás?"
        if "Bien" in message_text:
            await update.message.reply_text("Que bueno, me alegro")
        elif "Mal" in message_text:
            await update.message.reply_text("Oh, lamento escucharlo")
    elif cumpleaños.search(message_text):  # Si el usuario da las gracias
        await update.message.reply_text("Felicidadeees, ¿Cual es tu fecha de nacimiento?")
    elif fecha.search(message_text):  # Si el usuario proporciona un correo electrónico
        await update.message.reply_text("Oh, genial, espero te la pases de excelente en tu cumpleaños")
    elif despedida.search(message_text):
        await update.message.reply_text("Hasta luego señor Wayne")
    else:  # Si el bot no entiende el mensaje
        await update.message.reply_text("Khe")

def main() -> None:
    """Inicia el bot."""
    application = Application.builder().token("7149303311:AAHIZUcnAIAW0EBbUGrqzQz5I5EuHizwe38").build()

    # Manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Actualizaciones
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Ejecuta el bot 
if __name__ == "__main__":
    main()