import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

# Returns array of clumped num_groups sized texts
# Input: (some set of text, number of sentences in one clump)
# Output: List of clumps
def clump_text(text, num_groups):
    clump_list = []
    sentences = sent_tokenize(text)
    
    temp_list = []
    c = 0
    for s in sentences:
        temp_list.append(s)
        c += 1
        if (c == num_groups):
            clump_list.append(''.join(temp_list))
            temp_list = []
            c = 0
    if (len(temp_list) > 0):
        clump_list.append(''.join(temp_list))
    
    
    return clump_list

# Creating a df with all clumps in individual row with associated page number of clumps
# Input: (Base df of page number and text on that page, number of sentences per clump
# Output: df with row of associated page number and clumps
def create_grouped_df(text_per_page, num_groups):

    page_nums = []
    grouped_texts = []


    for index, row in text_per_page.iterrows():
        clumped_texts = clump_text(row['text'], num_groups)
        number_of_clumped_strings = len(clumped_texts)
        page_nums = page_nums + [row['page_number']] * number_of_clumped_strings
        grouped_texts.extend(clumped_texts)
    clumped_df = pd.DataFrame({'page_nums': page_nums, 'grouped_texts': grouped_texts}, columns=['page_nums', 'grouped_texts'])
    
    return clumped_df

def get_embedding(text, open_ai_client, model="text-embedding-3-small"):
    return open_ai_client.embeddings.create(input = [text], model=model).data[0].embedding

def send_data_to_pinecone(data, open_ai_client, pinecone, namespace, index):
    # Create a DataFrame
    df = pd.DataFrame({'text': data})
    df['ada_embedding'] = df.text.apply(lambda x: get_embedding(x, open_ai_client, model='text-embedding-3-small'))
    # Add an ID column (for simplicity, using index as ID)
    df['id'] = df.index.astype(str)

    
    # Convert DataFrame rows to the format required by upsert
    vectors = [
        {
            "id": row['id'],
            "values": row['ada_embedding'],
            "metadata": {"text": row['text']}
        } for index, row in df.iterrows()
    ]
    
    # Assuming `index` is your Pinecone index object
    pinecone.Index(index).upsert(
        vectors=vectors,
        namespace=namespace
    )
