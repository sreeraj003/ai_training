def chunk_text (text:str,chunk_size:int=500,overlap:int=100):
    if(chunk_size<=0):
        raise ValueError("chunk size should be more than zero")
    
    if(overlap<0 or overlap >=chunk_size):
        raise ValueError("overlap should be between 0 and chunk size")
    
    words = text.split()
    chunks = []
    start= 0
    while start<len(words):
        end = start+chunk_size
        chunk =  " ".join(words[start:end])
        chunks.append(chunk)
        start = start+chunk_size-overlap
    return chunks
        