from atproto import Client
import os
from dotenv import load_dotenv

class BlueSkyAPI:
    def __init__(self):
        # Chargement des variables d'environnement
        load_dotenv()
        self.client = Client()
        self.username = os.getenv("BSKY_USERNAME")
        self.password = os.getenv("BSKY_PASSWORD")
        self.login()

    def login(self):
        """Tentative de connexion à l'API BlueSky avec le nom d'utilisateur et le mot de passe."""
        try:
            self.client.login(self.username, self.password)
        except Exception as e:
            print(f"Erreur de connexion : {e}")

    def get_timeline(self, cursor='', limit=50):
        try:
            data = self.client.get_timeline(cursor=cursor, limit=limit)
            posts_data = [{
                'author': post.author.handle,
                'content': post.record.text,
                'timestamp': post.indexed_at,
                'uri': post.uri
            } for post in data.feed]

            return posts_data, data.cursor
        except Exception as e:
            print(f"Erreur timeline : {e}")
            return [], None

    def get_feed_by_handle_and_slug(self, handle: str, slug: str, limit: int = 30, cursor: str = ''):
        """
        Récupère les posts d'un feed generator en utilisant simplement le handle et le slug.

        Args:
            handle (str): Le handle du créateur du feed (exemple: 'aendra.com').
            slug (str): Le slug du feed (exemple: 'verified-news').
            limit (int): Nombre de posts à récupérer.
            cursor (str): Pour la pagination.

        Returns:
            dict: Contient 'posts' (liste de posts) et 'next_cursor' (pour pagination).
        """
        try:
            # 1. On récupère le DID à partir du handle
            profile = self.client.app.bsky.actor.get_profile({'actor': handle})
            did = profile.did

            # 2. On construit l’URI
            feed_uri = f"at://{did}/app.bsky.feed.generator/{slug}"

            # 3. On récupère les posts
            params = {'feed': feed_uri, 'limit': limit, 'cursor': cursor}
            data = self.client.app.bsky.feed.get_feed(params)

            posts_data = [{
                'author': post.post.author.handle,
                'content': post.post.record.text,
                'timestamp': post.post.indexed_at,
                'uri': post.post.uri
            } for post in data.feed]

            return {
                'posts': posts_data,
                'next_cursor': data.cursor
            }

        except Exception as e:
            print(f"Erreur lors de la récupération du feed generator : {e}")
            return {'posts': [], 'next_cursor': None}

    def get_author_feed(self, actor: str, filter_type='posts_with_replies', cursor='', limit=50):
        try:
            data = self.client.get_author_feed(
                actor=actor,
                filter=filter_type,
                cursor=cursor,
                limit=limit,
            )

            posts_data = [{
                'author': post.post.author.handle,
                'content': post.post.record.text,
                'timestamp': post.post.indexed_at,
                'uri': post.post.uri
            } for post in data.feed]

            return posts_data, data.cursor
        except Exception as e:
            print(f"Erreur author feed : {e}")
            return [], None

