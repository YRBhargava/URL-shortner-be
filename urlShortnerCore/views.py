from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, redirect
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import LoginSerializer
import json,random,string
from django.utils import timezone
from .models import User,Url


#----------------------LOGIN VIEW--------------------
@csrf_exempt
def loginView(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body.decode('utf-8'))
            # serializer = LoginSerializer(data=data)
            # if serializer.is_valid():
            #     return JsonResponse(serializer.validated_data, status=200)
            # return JsonResponse(serializer.errors, status=401)
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            
            user=User.objects.filter(email=email).first()
            
            if user and check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                print('------LINE 29-----',access_token)
                
                return JsonResponse({
                    'message': 'Login successful',
                    'userId': user.userId,
                    'name': user.name,
                    'access_token': access_token,
                    'refresh_token': str(refresh)
                }, status=200)
                
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST method is allowed'}, status=405)
    
#---------------------SIGNUP VIEW-------------------    
@csrf_exempt
def signupView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            name = data.get('name')
            phone = data.get('phone')
            password = data.get('password')

            if not email or not name or not phone or not password:
                return JsonResponse({'message': 'All fields are required'}, status=400)

            if len(phone) != 10 or not phone.isdigit():
                return JsonResponse({'message': 'Phone number must be exactly 10 digits'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'Email is already taken'}, status=400)

            user = User.objects.create(name=name, email=email,phone=phone,password=make_password(password))

            return JsonResponse({'message': 'Signup successful'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST method is allowed'}, status=405)  
    
    

#--------------------URL SHORTNER VIEW----------------------
@csrf_exempt
@permission_classes([IsAuthenticated])
def urlShortnerView(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            originalUrl = data.get('originalUrl')
            userId = data.get('userId')
            
            auth_header = request.headers.get('Authorization')
            print(auth_header)
    
            if auth_header is None:
                return JsonResponse({'message': 'Authorization header missing'}, status=401)
    
            try:
                token = auth_header.split(' ')[1]
                
            except IndexError:
                return JsonResponse({'message': 'Token not provided'}, status=401)
            
            jwt_auth = JWTAuthentication()
    
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                
            except Exception as e:
                print('####E--X--C--E--P--T--I--O--N####',e)
                return JsonResponse({'message': 'Invalid token'}, status=401)
            

            if not originalUrl or not userId:
                return JsonResponse({'message': 'URL is required'}, status=400)
            
            try:
                user = User.objects.get(userId=userId)
            except User.DoesNotExist:
                return JsonResponse({'message': 'User not found'}, status=404)
            
            if Url.objects.filter(userId=user, originalUrl=originalUrl).exists():
                return JsonResponse({'message': 'URL already exists for this user'}, status=409)

            short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            while Url.objects.filter(shortUrl=short_url).exists():
                short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

            urlEntry = Url.objects.create(
                userId=user,
                originalUrl=originalUrl,
                shortUrl=short_url,
                creationDate=timezone.now()
            )

            return JsonResponse({'message': 'URL shortened successfully', 'shortUrl': 'http://localhost:8001/s/'+short_url}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        
        except Exception as e:
            return JsonResponse({'message': f'Unexpected error: {str(e)}'}, status=500)
    
    else:
        return JsonResponse({'message': 'Only POST method is allowed'}, status=405)
    
#-------------------------ShortToOriginal---------------    
@csrf_exempt
def shortToOriginalView(request,path):
    try:
        url=get_object_or_404(Url, shortUrl=path)
        return redirect(url.originalUrl)
    except Exception as e:
        return JsonResponse({'message': 'URL Not Found'}, status=404)
    
    
#-------------------------Urls History--------------
@csrf_exempt
def urlsHistoryView(request, userId):
    if request.method == 'GET':
        try:
            # Check if the user exists
            user = User.objects.get(userId=userId)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        urls = Url.objects.filter(userId=user).values_list('originalUrl', 'shortUrl')

        urlsList = list(urls)

        return JsonResponse({'message':'Urls fetched sucessfully','urlsHistory': urlsList}, status=200)
    
    else:
        return JsonResponse({'message': 'Only GET method is allowed'}, status=405)
            
        
    
    
    
    
