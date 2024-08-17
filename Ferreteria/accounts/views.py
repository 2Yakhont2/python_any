from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth import get_user_model, login, logout, authenticate

# Crear usuario con la informacion recuperada del formulario
# get_user_model >> Recuperar un objeto que coincida con nuestro modelo de usuario (Shopper)
User = get_user_model()

def signup(request):
    if request.method == "POST":
        # Procesar el formulario
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe")
        else:
            # create_user >> permite obtener funcionalidades como cifrado de contraseña
            # A create_user le pasamos la informacion que recuperamos del form: username y password
            user = User.objects.create_user(username=username, password=password)

            # Para iniciar sesion usamos la funcion login. 
            # Login necesita un request y un usuario (variable user linea 21)
            login(request, user)
            return redirect('index')

    return render(request, 'accounts/signup.html')

# No necesitamos pasarle la info al request de que usuario esta conectado, porque ya lo tiene.
def logout_user(request):
    logout(request)
    return redirect('index')

def login_user(request):
    if request.method == "POST":
        # Recuperar la informacion del formulario
        username = request.POST.get("username")
        password = request.POST.get("password")

        # authenticate >> comprueba si la info enviada correspe a la almacenada en la bd
        # authenticate >> Permite almacenar en una var la info, si el user no ingresa la info
        # correcta la funcion le muestra un mensaje de error: contraseña/usuario incorrecto

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña incorrecto.")

    return render(request, 'accounts/login.html')

def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return redirect("index")

    return render(request, "accounts/profile.html")
