import os

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view


@api_view(['GET'])
def download_file(request):
    path = request.query_params['path']
    _, file_extension = os.path.splitext(path)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        if file_extension == '.pdf' or file_extension == '':
            return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        if file_extension == '.jpg':
            return FileResponse(open(file_path, 'rb'), content_type='image/jpg')
        if file_extension == '.png':
            return FileResponse(open(file_path, 'rb'), content_type='image/png')
        if file_extension == '.xlsx':
            return FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    raise Http404
