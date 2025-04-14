from atproto import Client
import pandas as pd
import os
from dotenv import load_dotenv

class BlueSkyAPI:

    def __init__(self):
        load_dotenv()
        self.client = Client()
        self.username = os.getenv("BSKY_USERNAME")
        self.password = os.getenv("BSKY_PASSWORD")
        self.login()

    def login(self):
        try:
            self.client.login(self.username, self.password)
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def get_terme(self, terme: str, limit: int = 100) -> pd.DataFrame:
        """
        Recherche des posts contenant un terme spécifique via l'API BlueSky et retourne un DataFrame.

        Args:
        - terme (str): Le mot-clé à rechercher.
        - limit (int): Nombre maximal de résultats.

        Returns:
        - pd.DataFrame: Contenant auteur, contenu, date et URI.
        """
        try:
            params = {'q': terme, 'limit': limit, 'lang': 'fr'}
            results = self.client.app.bsky.feed.search_posts(params=params)

            posts_data = [{
                'author': post.author.handle,
                'content': post.record.text,
                'timestamp': post.indexed_at,
                'uri': post.uri
            } for post in results.posts]

            df = pd.DataFrame(posts_data)
            df.to_csv("./bsky_posts.csv", index=False)
            return df

        except Exception as e:
            print(f"Erreur lors de la récupération des posts : {e}")
            return pd.DataFrame()
