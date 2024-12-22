from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY= os.getenv('GROQ_API_KEY')

def mistral_chat(temp=0.4,max_token=100):
    model = ChatGroq(
    model = 'mixtral-8x7b-32768',
    api_key = GROQ_API_KEY,
    temperature=temp,
    max_tokens = max_token 
)
    return model

def BAAIembedding(path:str):

    embed_model = HuggingFaceEmbeddings(model_name=os.path.join(path),
                                    #model_kwargs={'device':'cuda'},
                                    encode_kwargs={'normalize_embeddings':True})
    return embed_model