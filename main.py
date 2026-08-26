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
    

def get_embeddings(model_name, chunks):
    return [ollama.embed(model=model_name, input=chunk).embeddings[0]
            for chunk in chunks]
    pass
    
def save_embeddings():
    pass

def load_embeddings():
    pass   
             

def main():
    filename = "peterpan.txt"
    paragraphs = parse_file(filename)
    embeddings = get_embeddings("nomic-embed-text:latest", paragraphs[5:90])
    print(paragraphs[:10])
    pass

if __name__ == "__main__":
    main()