from .query import *
from .utils import *

def get_post_call(request):
    print("Getting post call")
    openai_connection, pinecone_connection, openai_key, pinecone_key = connections()
    print(openai_key)
    print(pinecone_key)
    print(openai_connection)
    print(pinecone_connection)
    podcast_bit = get_similar("podcasts", "medrag", request, openai_connection, pinecone_connection)
    print("------------------")
    print(podcast_bit)
    print("------------------")
    post = get_query(request, openai_connection, pinecone_connection, openai_key, "plant_based", "medrag", "Given this section of my podcast and external data can you make a linkedin post? Podcast: + " + podcast_bit + "\n")
    print(post)
    return post