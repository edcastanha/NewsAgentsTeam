from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny 

class GetTokenView(APIView):
    '''
    Views de autenticação para obter token de acesso

    Parâmetros aceitos:
    - POST
    - username: string
    - password: string

    Exemplo de requisição:
    
        curl -X POST \
        http://localhost:8000/api/get-token/ \
        -H 'Content-Type: application/json' \
        -d '{
            "username": "testuser", 
            "password": "testpassword"
        }'
    '''
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED) 
