import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_dj.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser(
        username : str = 'admin',
        email : str = 'admin@admin.test',
        password : str = 'admin'
    ):
    # Criando superusuário
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superusuário: admin/admin criado - Sucesso!')     
    else:
        print('O superusuário existente - OK!')

if __name__ == '__main__':
    create_superuser()
