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

# Login 
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

# Get all users
@csrf_exempt
def get_all_users(request):
    if request.method=='GET':
        get_all_users=UserDetails.objects.all() #queryset
        serialized_data=UserDetailsSerializer(get_all_users,many=True)
        return JsonResponse(serialized_data.data,safe=False)

# create user
@csrf_exempt
def create_user(request):
        if request.method=='POST':
            try:
                input_data = json.loads(request.body)
                serializer_data = UserDetailsSerializer(data=input_data) # deserializing the data
                if serializer_data.is_valid():
                    serializer_data.save()
                    return JsonResponse({
                        "success" : True,
                        "message" : "Data saved successfully"
                    },status=201)
            except Exception as e:
                return JsonResponse({
                        "success" : False,
                        "error" : str(e),
                        "message" : "Failed to save Data"
                    },status=400)

@csrf_exempt
def get_user_by_email(request,email):
    if request.method=='GET':
        try:
            user = UserDetails.objects.get(email=email)
            serializer_data = UserDetailsSerializer(user) # deserializing the data
            return JsonResponse({
                    "success" : True,
                    "message" : serializer_data.data
                },status=200)
        except Exception as e:
            return JsonResponse({
                    "success" : False,
                    "error" : str(e),     
                },status=400)

@csrf_exempt
def update_user_data(request,email):
    if request.method=='PATCH':
        try:
            user = UserDetails.objects.get(email=email)
            input_data = json.loads(request.body)
            serializer_data = UserDetailsSerializer(user,data = input_data,partial = True) # deserializing the data
            
            if serializer_data.is_valid():
                serializer_data.save()
            return JsonResponse({
                    "Success" : True,
                    "message" : "Data updated successfully",
                    "Updated_data" : serializer_data.data
                },status=200)
        except Exception as e:
            return JsonResponse({
                    "success" : False,
                    "Error" : str(e),     
                },status=400)

@csrf_exempt
def delete_user_data(request,email):
    if request.method=='DELETE':
        try:
          user = UserDetails.objects.get(email=email)
          user.delete()
          return JsonResponse({
                    "Success" : True,
                    "message" : "Data deleted successfully",
                    
                },status=200)
        except Exception as e:
            return JsonResponse({
                    "success" : False,
                    "Error" : str(e),     
                },status=400)



    

