import pandas as pd,os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from recommendation_system.preprocessing import preprocess_data, save_preprocessed_data
from recommendation_system.EDA import summary_plot, distribution_of_rating
from recommendation_system.models.model import mistral_chat,BAAIembedding
from recommendation_system.rag import MistralRAG
from uuid import uuid1
#preprocessing
if not os.path.exists(os.path.join('data/preprocessed','review_data.csv')):
    df = pd.read_csv(r'data\raw\flipkart-data.csv')
    df['review'] = df['review'].apply(preprocess_data)
    save_preprocessed_data(df=df)

#Explorating Data Analysis
df = pd.read_csv(r'data\preprocessed\review_data.csv')
summary_plot(df=df)
distribution_of_rating(df=df)

#Mistral AI model and BAAI Embedding model
model = mistral_chat()
embedding_model = BAAIembedding(path=r'recommendation_system\models\embedding_model\models--BAAI--bge-base-en-v1.5\snapshots\a5beb1e3e68b9ab74eb54cfd186867f64f240e1a')

#RAG
def response_chat(user_input:str):
    store = {}
    def get_session_history(session_id:str)->BaseChatMessageHistory:
        if session_id not in store:
            store[session_id]=ChatMessageHistory()
        return store[session_id]
    mistralrag = MistralRAG()
    mistral_chat = mistralrag.ragchain(model=model,chat_memory=get_session_history)
    response = mistral_chat.invoke({'input':user_input},config={'configurable':{'session_id':'xyz'}})
    return {'store':store,'response':response}