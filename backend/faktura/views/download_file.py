import logging
import os

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view


@api_view(['GET'])
def download_file(request):
    logger = logging.getLogger("app")
    logger.info('Download file called')
    path = request.query_params['path']
    _, file_extension = os.path.splitext(path)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    logger.info(file_path)
    if os.path.exists(file_path):
        if file_extension == '.pdf' or file_extension == '':
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf', filename="testabcdefg.pdf")
        if file_extension == '.jpg':
            return FileResponse(open(file_path, 'rb'), content_type='image/jpg', filename="testabcdefg.jpg")
        if file_extension == '.png':
            return FileResponse(open(file_path, 'rb'), content_type='image/png', filename="testabcdefg.png")
        if file_extension == '.xlsx':
            return FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="testabcdefg.xlsx")
        if file_extension == '.xml':
            return FileResponse(open(file_path, 'rb'), filename="testabcdefg.xml")
    raise Http404
