from .query import *
from .utils import *

def get_post_call(request):
    openai_connection, pinecone_connection, openai_key, pinecone_key = connections()
    post = get_query(request, openai_connection, pinecone_connection, openai_key, "plant_based", "medrag", "You are a tool that generates linkedin posts when given a base idea from a user. The Linkedin post you provide should be unique and non general. We are trying to maintain a positive attitude while being specific to the external information." + "\n")
    print(post)
    return post

def get_post_call_with_podcast_db(request):
    openai_connection, pinecone_connection, openai_key, pinecone_key = connections()
    podcast_bit = get_similar("podcasts", "medrag", request, openai_connection, pinecone_connection)
    print("------------------")
    print(podcast_bit)
    print("------------------")
    post = get_query(request, openai_connection, pinecone_connection, openai_key, "plant_based", "medrag", "Given this section of my podcast and external data can you make a linkedin post? Podcast: + " + podcast_bit + "\n")
    print(post)
    return post

def get_post_with_provided_transcript(request, transcript):
    openai_connection, pinecone_connection, openai_key, pinecone_key = connections()

    post = get_query(request, openai_connection, pinecone_connection, openai_key, "plant_based", "medrag", "Given this transcript of my podcast and external data can you make a linkedin post? Podcast: + " + transcript + "\n")
    print(post)
    return post