from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST'])
def testget(request):
    response = Response()
    if request.method == 'GET':
        response.status_code = 200
        response.content = 'get_succees'
        return response
    elif request.method == 'POST':
        if request.data['value'] == 'i':
            response.status_code = 200
            response.content = 'value is right'
        elif request.data['value'] == 'u':
            response.status_code = 200
            response.content = 'value is fault'
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return response
    response.status_code = status.HTTP_400_BAD_REQUEST
    return response


# def testpost(request):
#

