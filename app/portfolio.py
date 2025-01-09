import pandas as pd
import chromadb
import uuid



class Portfolio:
    def __init__(self):
        self.file_path = "app/resource/my_portfolio.csv"
        self.df = pd.read_csv(self.file_path)
        self.client = chromadb.PersistentClient("vector_store")
        self.collection = self.client.get_or_create_collection(name = "portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _,row in self.df.iterrows():
                self.collection.add(documents = row['Techstack'],metadatas = {"link_list" : row["Links"]},
                                    ids = [str(uuid.uuid4())])

    def links_list(self,job):
        return self.collection.query(query_texts = str(job["skills"]),n_results=2).get('metadatas',[])

