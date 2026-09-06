#RAG implementation

import ollama
import numpy as np
import os
import json

def parse_file(filename):
    with open(file=filename, encoding="utf-8-sig") as f: 
        paragraphs = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line: 
                buffer.append(line)
            elif len(buffer):
                paragraphs.append((" ").join(buffer))
                buffer = []
        if len(buffer):
            paragraphs.append((" ").join(buffer))
        return paragraphs  
    

print("Hello World")

    
def save_embeddings(filename, embeddings):
    if not os.path.exists("embeddings"):    
        os.makedirs("embeddings")
    with open(f"embeddings/{filename}.json", "w") as f:
        json.dump(embeddings, f)

def load_embeddings(filename):
    if not os.path.exists(f"embeddings/{filename}.json"):
        print("Error: File does not exist")
        return False
    with open(f"embeddings/{filename}.json", "r") as f:
        return json.load(f)
        

#implement chunking
    
def get_embeddings(filename, model_name, chunks):
    if (embeddings := load_embeddings(filename)):
        return embeddings 
    
    
    embeddings = [ollama.embed(model=model_name, input=chunk).embeddings[0]
            for chunk in chunks]
    
    save_embeddings(filename, embeddings)
    return embeddings
    
def get_most_similar(target, chunk_embeddings):
    target_norm = np.linalg.norm(target) 
    similarity_scores = [
        np.dot(target, item) / (target_norm * np.linalg.norm(item)) for item in chunk_embeddings
    ]
    return sorted(zip(similarity_scores, range(len(chunk_embeddings))), reverse = True)
    
def main():
    SYSTEM_PROMPT = """You are a helpful reading assistand who answers questions based on snippets of text provided
    in context. Answer using only the context provided being as concise as possible/ If you are unsure
    just say that you don't know. 
    Context: """
    
    
    filename = "peterpan.txt"
    paragraphs = parse_file(filename)
    
    #add chunking function
    
    embeddings = get_embeddings(filename, "nomic-embed-text:latest", paragraphs)
    
    prompt = input("Enter your question here -> ")
    prompt_embedding = ollama.embed(model = "nomic-embed-text:latest", input = prompt ).embeddings[0]

    most_similar_chunks = get_most_similar(prompt_embedding, embeddings) [:5]
    
    for item in most_similar_chunks:
        print(item[0], paragraphs[item[1]])
    
    response = ollama.chat(
        model = "qwen2.5:0.5b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT 
                + "\n".join(paragraphs[item[1]] for item in most_similar_chunks),
            },
            {"role": "user", "content": prompt},
        ],
    )
    print("\n\n")
    print(response["message"]["content"])
    

if __name__ == "__main__":
    main()