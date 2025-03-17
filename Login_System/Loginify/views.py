from django.shortcuts import render,redirect  
from django.http import HttpResponse,JsonResponse
from .models import UserDetails
from .Serializers import UserDetailsSerializer
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def print_hello(request):
    return HttpResponse("Hello, world!")

def home_page(request):
    return render(request,'index.html')

# Signup View
@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]

            if UserDetails.objects.filter(email=email).exists():
                '''
                return JsonResponse({
                        "message" : "Email already exists!",
                    },status=200) 
                '''
                messages.error(request, "Email already exists!")
                return render(request, "signup.html")

            user = UserDetails(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Signup successful! Please login.")
            '''
            return JsonResponse({
                        "message" : "Signup successful! Please login.",
                        "redirect_url": "/loginSystem/login/"
                    },status=200)
            '''
            return redirect("/loginSystem/login/")
            
        except Exception as e:
            return messages.error(request, str(e))
            '''
            return JsonResponse({
                    "success" : False,
                    "error" : str(e),
                },status=400)
            '''
    return render(request, "signup.html")

@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            password = request.POST["password"]

            user = UserDetails.objects.filter(email=email, password=password).first()

            if user:
                messages.success(request, f"Welcome, {user.username}!")
                '''
                return JsonResponse({
                        "message" : f"Welcome, {user.username}!"
                    },status=200)
                '''
                return render(request, "success.html") # , {"user": user}
            else:
                messages.error(request, "Invalid credentials!")
                '''
                return JsonResponse({
                    "success" : False,
                    "message" : "Invalid credentials!Username or password incorrect"
                },status=401)
                '''
                return render(request, "login.html")
        except Exception as e:
            '''
            return JsonResponse({
                    "success" : False,
                    "error" : str(e)
                },status=400) 
            ''' 
            return messages.error(request, str(e))
    return render(request, "login.html")


    

