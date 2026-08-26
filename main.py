#barebones RAG implementation 

#open the file(s) 
#parse the file(s)
#get embeddings for the file 
#save embeddings to a vector database
#load embeddings 
import ollama
import numpy

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
    

def get_embeddings():
    return ollama.embeddings
    pass
    
def save_embeddings():
    pass

def load_embeddings():
    pass   
             

def main():
    filename = "peterpan.txt"
    pass
