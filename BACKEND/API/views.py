from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .externe.BlueSky import BlueSkyAPI
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BlueSkySearchView(APIView):
    """
    Rechercher des posts sur BlueSky.
    """

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('terme', openapi.IN_QUERY, description="Terme à rechercher", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('limit', openapi.IN_QUERY, description="Nombre de résultats (max 100)", type=openapi.TYPE_INTEGER)
    ])
    def get(self, request):
        terme = request.query_params.get('terme', '')
        limit = int(request.query_params.get('limit', 10))

        if not terme:
            return Response({'error': 'Le paramètre "terme" est requis.'}, status=status.HTTP_400_BAD_REQUEST)

        api = BlueSkyAPI()
        df = api.get_terme(terme, limit)
        data = df.to_dict(orient='records')

        return Response(data, status=status.HTTP_200_OK)