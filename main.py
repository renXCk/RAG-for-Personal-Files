#barebones RAG implementation 

#open the file(s) 
#parse the file(s)
#get embeddings for the file 
#save embeddings to a vector database
#load embeddings 
import ollama
import numpy
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
    


    
def save_embeddings(filename, embeddings):
    if not os.path.exists("embeddings"):    
        os.makedirs("embeddings")
    with open(f"embeddings/{filename}.json", "w") as f:
        json.dump(embeddings, f)

def load_embeddings(filename):
    if not os.path.exists("embeddings"):
        print("Error: File does not exist")
        return False
    with open(f"embeddings/{filename}.json", "r") as f:
        return json.load(f)
    
def get_embeddings(filename, model_name, chunks):
    if (embeddings == load_embeddings(filename)):
        return embeddings 
    
    
    embeddings = [ollama.embed(model=model_name, input=chunk).embeddings[0]
            for chunk in chunks]
    
    save_embeddings(filename, embeddings)
    return embeddings
    
             

def main():
    filename = "peterpan.txt"
    paragraphs = parse_file(filename)
    
    embeddings = get_embeddings("nomic-embed-text:latest", paragraphs[5:90])
    
    
    print(paragraphs[:10])
    pass

if __name__ == "__main__":
    main()