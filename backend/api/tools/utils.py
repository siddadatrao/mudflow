from pinecone import Pinecone as PineconeClient
from openai import OpenAI
import os


def connections():
	openai_key = os.getenv("OPENAI_API_KEY")
	pinecone_key = os.getenv("PINECONE_API_KEY", "default_value_if_not_set")

	openai_connection = OpenAI(api_key=openai_key)
	pinecone_connection = PineconeClient(api_key=pinecone_key)
	return openai_connection, pinecone_connection, openai_key, pinecone_key