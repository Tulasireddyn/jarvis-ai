
import os

class JarvisMemory:
    def __init__(self):
        self.use_pinecone = False
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        
        if self.api_key and self.index_name:
            try:
                # Placeholder for real Pinecone init
                # from pinecone import Pinecone
                # pc = Pinecone(api_key=self.api_key)
                # self.index = pc.Index(self.index_name)
                self.use_pinecone = True
            except Exception as e:
                print(f"Failed to init Pinecone: {e}")
                self.use_pinecone = False
        
        if not self.use_pinecone:
            print("Using Mock Memory (List)")
            self.memory = []

    def save_context(self, text):
        if self.use_pinecone:
            # Mocking the embedding and upsert execution for now to avoid dependency errors if lib not installed
            # In a real scenario, we would use sentence-transformers to embed `text`
            print(f"Simulating save to Pinecone: {text[:50]}...")
            pass
        else:
            self.memory.append(text)

    def retrieve_context(self, query):
        if self.use_pinecone:
             # Placeholder: Retrieve from Pinecone
             return "Retrieved context from Pinecone (Simulated)"
        else:
            # Simple keyword match or return last 3
            relevant = [m for m in self.memory if any(word in m.lower() for word in query.lower().split())]
            return "\n".join(relevant[-3:]) if relevant else "No context found."
