from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from API.services.BlueSky_service import BlueSkyAPI
from API.serializers.bluesky_serializers import BlueSkyPostSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlueSkyTimelineView(APIView):
    """
    Récupérer la timeline de l'utilisateur authentifié.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('cursor', openapi.IN_QUERY, description="Curseur de pagination", type=openapi.TYPE_STRING),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de posts à retourner", type=openapi.TYPE_INTEGER)
        ],
        tags=['BlueSky']
    )
    def get(self, request):
        cursor = request.query_params.get('cursor', '')
        limit = int(request.query_params.get('limit', 50))

        api = BlueSkyAPI()
        posts_data, next_cursor = api.get_timeline(cursor, limit)

        if not posts_data:
            return Response({'error': 'Aucun post trouvé dans la timeline.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlueSkyPostSerializer(posts_data, many=True)
        return Response({'posts': serializer.data, 'next_cursor': next_cursor}, status=status.HTTP_200_OK)


class BlueSkyFeedGeneratorView(APIView):
    """
    Récupérer un feed personnalisé via son URI.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('feed_uri', openapi.IN_QUERY, description="URI du feed generator", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('cursor', openapi.IN_QUERY, description="Curseur de pagination", type=openapi.TYPE_STRING),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de posts à retourner", type=openapi.TYPE_INTEGER)
        ],
        tags=['BlueSky']
    )
    def get(self, request):
        feed_uri = request.query_params.get('feed_uri', None)
        cursor = request.query_params.get('cursor', '')
        limit = int(request.query_params.get('limit', 50))

        if not feed_uri:
            return Response({'error': "Le paramètre 'feed_uri' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        api = BlueSkyAPI()
        posts_data, next_cursor = api.get_feed_generator(feed_uri, cursor, limit)

        if not posts_data:
            return Response({'error': 'Aucun post trouvé dans ce feed generator.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlueSkyPostSerializer(posts_data, many=True)
        return Response({'posts': serializer.data, 'next_cursor': next_cursor}, status=status.HTTP_200_OK)


class BlueSkyAuthorFeedView(APIView):
    """
    Récupérer les posts d'un auteur via son DID.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('actor', openapi.IN_QUERY, description="DID de l'auteur", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('filter', openapi.IN_QUERY, description="Type de posts", type=openapi.TYPE_STRING, enum=['posts_with_replies', 'posts_no_replies', 'posts_with_media', 'posts_and_author_threads']),
            openapi.Parameter('cursor', openapi.IN_QUERY, description="Curseur de pagination", type=openapi.TYPE_STRING),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de posts à retourner", type=openapi.TYPE_INTEGER)
        ],
        tags=['BlueSky']
    )
    def get(self, request):
        actor = request.query_params.get('actor', None)
        filter_type = request.query_params.get('filter', 'posts_with_replies')
        cursor = request.query_params.get('cursor', '')
        limit = int(request.query_params.get('limit', 50))

        if not actor:
            return Response({'error': "Le paramètre 'actor' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        api = BlueSkyAPI()
        posts_data, next_cursor = api.get_author_feed(actor, filter_type, cursor, limit)

        if not posts_data:
            return Response({'error': "Aucun post trouvé pour cet auteur."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlueSkyPostSerializer(posts_data, many=True)
        return Response({'posts': serializer.data, 'next_cursor': next_cursor}, status=status.HTTP_200_OK)

class BlueSkyFeedGeneratorView(APIView):
    """
    Récupérer les posts d'un feed generator par handle et slug.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('handle', openapi.IN_QUERY, description="Handle du créateur du feed (ex: 'aendra.com')", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('slug', openapi.IN_QUERY, description="Slug du feed generator (ex: 'verified-news')", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de résultats (max 100)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('cursor', openapi.IN_QUERY, description="Cursor pour la pagination", type=openapi.TYPE_STRING),
        ],
        tags=['BlueSky']  # Tag Swagger
    )
    def get(self, request):
        handle = request.query_params.get('handle', None)
        slug = request.query_params.get('slug', None)
        limit = int(request.query_params.get('limit', 10))
        cursor = request.query_params.get('cursor', '')

        if not handle or not slug:
            return Response({'error': "Les paramètres 'handle' et 'slug' sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        api = BlueSkyAPI()
        result = api.get_feed_by_handle_and_slug(handle, slug, limit=limit, cursor=cursor)

        posts_data = result['posts']
        next_cursor = result['next_cursor']

        if not posts_data:
            return Response({'error': 'Aucun post trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlueSkyPostSerializer(posts_data, many=True)
        return Response({
            'posts': serializer.data,
            'next_cursor': next_cursor
        }, status=status.HTTP_200_OK)
