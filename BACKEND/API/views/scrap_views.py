from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os
import importlib.util
from only_news.utils import get_available_sites

@api_view(['GET'])
def get_spider_categories(request):
    spider = request.GET.get('spider')
    if not spider:
        return Response({"error": "Paramètre 'spider' manquant"}, status=status.HTTP_400_BAD_REQUEST)

    sites = get_available_sites()

    if spider not in sites:
        return Response({"error": f"Spider inconnu : {spider}"}, status=status.HTTP_404_NOT_FOUND)

    try:
        project_path = sites[spider]
        scraper_path = os.path.join(project_path, f"{spider}_scraper/spiders/{spider}_spider.py")

        spec = importlib.util.spec_from_file_location(f"{spider}_module", scraper_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, f'get_{spider}_categories'):            
            func = getattr(module, f'get_{spider}_categories')
            categories = func()

            return Response({"categories": categories}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"La fonction f'get_{spider}_categories' est absente pour {spider}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
