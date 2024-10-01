import openai
import pinecone

def get_embedding(text, open_ai_client, model="text-embedding-3-small"):
	return open_ai_client.embeddings.create(input = [text], model=model).data[0].embedding

def templatize(query, context):
	return "Use following external resource in creating the linkedin post:" + context + " Create the post based on this description: " + query

def get_similar(namespace, index, query, open_ai_client, pinecone):
	query_embedding = get_embedding(query, open_ai_client, model='text-embedding-3-small')
	print("Got embedding")
	print(query_embedding)
	query_results1 = pinecone.Index(index).query(
		namespace=namespace,
		vector=query_embedding,
		top_k=1,
		include_values=False,
		include_metadata=True,
	)
	print(query_result)
	query_result = query_results1['matches'][0]['metadata']['text']
	return query_result

def get_similar_create_post(namespace, index, query, open_ai_client, pinecone):
	query_embedding = get_embedding(query, open_ai_client, model='text-embedding-3-small')
	query_results1 = pinecone.Index(index).query(
		namespace=namespace,
		vector=query_embedding,
		top_k=1,
		include_values=False,
		include_metadata=True,
	)
	query_result = query_results1['matches'][0]['metadata']['text']
	return templatize(query, query_result)

def get_completion(prompt, key, role):
	openai.api_key = key

	response = openai.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
		{"role": "system", "content": role},
		{"role": "user", "content": prompt}
		],
		
	)

	return response.choices[0].message.content

def get_query(query, openai_connection, pinecone_connection, openai_key, namespace, index, role):
	prompt = get_similar_create_post(namespace, index, query, openai_connection, pinecone_connection)
	stream = get_completion(prompt, openai_key, role)
	return stream


