from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_astradb import AstraDBVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from recommendation_system.models.model import mistral_chat, BAAIembedding
from dotenv import load_dotenv
import os

load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')
APPLICATION_TOKEN = os.getenv('APPLICATION_TOKEN')
KEY_SPACE = os.getenv('KEY_SPACE')
embed_model_path = BAAIembedding(path=r'recommendation_system\models\embedding_model\models--BAAI--bge-base-en-v1.5\snapshots\a5beb1e3e68b9ab74eb54cfd186867f64f240e1a')

class MistralRAG:
    def __init__(self):
        self.context_prompt = self.contextualize_prompt()
        self.promptqa = self.qa_prompt()
        self.vectordb = self.retreiver(embed_model_path)
        
    def ragchain(self, model,chat_memory):
        # Correctly create the history-aware retriever
        history_aware = create_history_aware_retriever(
            llm=model, 
            retriever=self.vectordb, 
            prompt=self.context_prompt
        )
        
        qa_chain = create_stuff_documents_chain(llm=model, prompt=self.promptqa)
        rag_chain = create_retrieval_chain(history_aware, qa_chain)
        rag_chain_memory = RunnableWithMessageHistory(
            rag_chain,
            chat_memory,
            input_messages_key='input',
            output_messages_key='answer',
            history_messages_key='chat_history'
        )
        return rag_chain_memory
    
    def contextualize_prompt(self):
        retriever_Prompt = (
            "Given the chat history and the latest user question which might reference context in the chat history, "
            "formulate a standalone question which can be understood without the chat history. "
            "Do not answer the question, just reformulate it if needed and otherwise return it as it is."
        )

        contextualize_prompt = ChatPromptTemplate.from_messages(
            [
                ('system', retriever_Prompt),
                MessagesPlaceholder(variable_name='chat_history'),
                ('user', '{input}')
            ]
        )
        
        return contextualize_prompt

    def qa_prompt(self):
        prompt = """You are an ecommerce helpful AI assistant who helps in recommendation of products. Analyze the product titles and reviews to give accurate responses. Ensure your answers are relevant to the product context and refrain from staying off points. Reply with a friendly and calm tone. Be clear and concise. Don't use the text provided and don't use 'they'. Always be clear.
        context:{context}
        question:{input}
        answer:
        """
        
        qa_prompt_temp = ChatPromptTemplate.from_messages(
            [
                ('system', prompt),
                MessagesPlaceholder(variable_name='chat_history'),
                ('user', '{input}')
            ]
        )

        return qa_prompt_temp
    
    def retreiver(self, embed_model_path):
        vector_store = AstraDBVectorStore(
            collection_name='first_vs',
            embedding=embed_model_path,
            api_endpoint=API_ENDPOINT,
            token=APPLICATION_TOKEN,
            namespace=KEY_SPACE
        )
        return vector_store.as_retriever()
