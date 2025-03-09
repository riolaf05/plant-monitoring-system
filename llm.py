from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# Model Selection
def initialize_llm(model_option, api_key, temperature=0):
    if model_option == 'OpenAI GPT-4o':
        return ChatOpenAI(openai_api_key=api_key, model='gpt-4o', temperature=temperature)
    elif model_option == 'OpenAI GPT-4o Mini':
        return ChatOpenAI(openai_api_key=api_key, model='gpt-4o-mini', temperature=temperature)
    elif model_option == 'Llama 3 8B':
        return ChatGroq(groq_api_key=api_key, model='llama3-8b-8192', temperature=temperature)
    elif model_option == 'Llama 3.1 70B':
        return ChatGroq(groq_api_key=api_key, model='llama-3.1-70b-versatile', temperature=temperature)
    elif model_option == 'Llama 3.1 8B':
        return ChatGroq(groq_api_key=api_key, model='llama-3.1-8b-instant', temperature=temperature)
    elif model_option == 'gpt-3.5-turbo-16k':
        return ChatOpenAI(openai_api_key=api_key, model='gpt-3.5-turbo-16k', temperature=temperature)
    else:
        raise ValueError("Invalid model option selected")