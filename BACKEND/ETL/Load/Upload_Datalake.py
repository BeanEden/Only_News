import boto3
import os

class UploadDataLake:
    """
    Class qui permet d'upload des fichier dans un dataLake. 
    Verifie si le bucket exist sinon le créé lui même.
    """
    def __init__(self, 
                 endpoint_url='http://minio:9000',
                 access_key=None, 
                 secret_key=None):
        
        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key or os.getenv("MINIO_USERNAME"),
            aws_secret_access_key=secret_key or os.getenv("MINIO_PASSWORD"),
        )

    def create_bucket(self, bucket_name):
        """
        Crée un bucket si il n'existe pas déjà.

        Args:
            bucket_name (str): Le nom du bucket que l'on souhaite créé.            

        Returns:
            Renvoi un string si le bucket exist ou à été créé.
        """
        existing_buckets = [bucket['Name'] for bucket in self.s3.list_buckets().get('Buckets', [])]
        if bucket_name in existing_buckets:
            print(f"✅ Bucket '{bucket_name}' existe déjà")
        else:
            self.s3.create_bucket(Bucket=bucket_name)
            print(f"🚀 Bucket '{bucket_name}' créé avec succès")

    def upload_file(self, file_path, bucket_name, object_name=None):
        """
        Upload un fichier local vers le bucket.

        Args:
            file_path (str): Le chemin du fichier à upload dans le datalake.
            bucket_name (str): Le nom du bucket.
            object_name (str): Le nom de l'objet.

        Returns:
            Renvoie une erreur si le fichier n'est pas toruvé.
            Renvoie un string si le fichier est bien upload dans la datalake.
        """

        self.create_bucket(bucket_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Fichier '{file_path}' introuvable")

        if object_name is None:
            object_name = os.path.basename(file_path)

        self.s3.upload_file(file_path, bucket_name, object_name)
        print(f"✅ Fichier '{file_path}' uploadé dans le bucket '{bucket_name}' en tant que '{object_name}'")

    def list_files(self, bucket_name):
        """
        Liste les fichiers d'un bucket

        Args:
            bucket_name (str): Le nom du bucket.

        Returns:
            Renvoie la liste des fichier contenus dans le bucket.
        """
        response = self.s3.list_objects_v2(Bucket=bucket_name)
        contents = response.get('Contents', [])
        if not contents:
            print(f"🫙 Le bucket '{bucket_name}' est vide")
            return []
        print(f"📝 Fichiers dans le bucket '{bucket_name}':")
        for obj in contents:
            print(f" - {obj['Key']}")
        return [obj['Key'] for obj in contents]