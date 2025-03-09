import os
import telebot
import time
from dotenv import load_dotenv
import base64
import openai
# Load environment variables
load_dotenv('.env')
load_dotenv(".env.orion", override=True)
from tools.image import image
from tools.temperature import temperature
from tools.moisture import moisture
from tools.watering import watering
# from utils.composio import composio_tools
from utils.llm import initialize_llm
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langgraph.prebuilt import create_react_agent
import logging
import logging_loki  # !pip install python-logging-loki
from utils.telegram import send_telegram_message

# Configuration
LOKI_URL = os.getenv('LOKI_URL')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_GROUP_ID = os.getenv('TELEGRAM_GROUP_ID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_OPTION = "OpenAI GPT-4o"

# Logging setup
logging_loki.emitter.LokiEmitter.level_tag = "level"
handler = logging_loki.LokiHandler(url=f"http://{LOKI_URL}/loki/api/v1/push", version="1")
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# Tools setup
tools = [image, temperature, moisture]
# tools += composio_tools

# Initialize ChatGroq model for language understanding
llm = initialize_llm(MODEL_OPTION, OPENAI_API_KEY, 0.2)

# Create ReAct agent
agent_executor = create_react_agent(llm, tools)

# Initialize bot
bot = telebot.TeleBot(TELEGRAM_CHAT_ID)

# Command Handlers
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to YourBot! Type /info to get more information.")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "This is a simple Telegram bot implemented in Python.")

# Message Handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    content_type = message.content_type

    # get data from tools #FIXME PASS DIRECTLY THE TOOL TO THE AGENT

    if content_type == 'text':
        try:

            # response = agent_executor.invoke(
            #     {"messages": [
            #         SystemMessage(content="""
            #                       You are an AI assistant responsible for detecting the condition of plants.

            #                       To carry out your tasks, you can use the tools provided to you.

            #                       When asked for information about the state of a plant, follow these steps:

            #                        1. Use the image tool to request a photo of the plant and save it in a folder.
            #                        2. Use the temperature tool to request the plant's temperature.
            #                        3. Use the moisture tool to request the plant's moisture level.
            #                        4. Send the collected data to the agent.
                                    
            #                        Try to respond to requests in the best possible way, with a polite yet slightly playful tone.
            #                        Use the available tools only when necessary to fulfill requests.
            #                        If you don't know the answer, do not make anything up. Instead, ask for help.
            #                        If you encounter any problems, report them to the group.
            #                       """),
            #         HumanMessage(content=message.text)
            #     ]}
            # )

            prompt = """

            You are an AI assistant responsible for detecting the condition of plants.
            
            Execute the following steps to carry out your tasks:

            1. Use the image tool to request a photo of the plant and save it in a folder.
            2. Use the temperature tool to request the plant's temperature.
            3. Use the moisture tool to request the plant's moisture level.
            4. Analyze the data and the image to provide a response on the plant's condition. If the plant needs to be watered, suggest it and ask the user if they would like to do it.
            5. If the user agrees use the watering tool to water the plant.

            Try to respond to requests in the best possible way, with a polite yet slightly playful tone.
            Use the available tools only when necessary to fulfill requests.

            """

            # get data from tools
            image_path=image.invoke()
            temperature=temperature.invoke()
            moisture=moisture.invoke()

            response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{img_base64}",
                        },
                        },
                    ],
                    }
                ],
                max_tokens=150,
            )
            content = response.choices[0].message.content

            # bot.send_message(TELEGRAM_GROUP_ID, response['output'])
            bot.reply_to(message, content)
        except Exception as e:
            logger.error(e, extra={"tags": {"service": "orion"}})
            send_telegram_message("Malfunzionamento su: Orion", "telegram_exchange", "telegram.key")
            bot.reply_to(message, "Ho avuto un problema!")
            bot.reply_to(message, str(e))
    else:
        bot.reply_to(message, "Non ho capito!")
        
# Start the bot
bot.polling()
