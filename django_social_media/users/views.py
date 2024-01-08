from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from users.forms import usersform
from django_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from PIL import Image, ImageOps

from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from werkzeug.utils import secure_filename
from django.contrib.auth.hashers import make_password
import hashlib
# from users.models import Users

class users():
    @api_view(['POST'])
    def user_login(request):
        try:
            cursor = connection.cursor()
            v_email = request.data['email']
            v_password = request.data['password']
            password = make_password(v_password)

            v_pass = hashlib.sha256()
            v_pass.update(v_password.encode('utf-8'))
            password = v_pass.hexdigest()
            print(password)

            cursor.callproc('user_login',((v_email,v_password)))
            result = cursor.fetchone()
            if result:
                user = result[0]
                user_name = result[1]
                return Response({'id':user,'status':'true','access_token':create_access_token(identity=user),'code':200},200)
            else:
                return Response({'message':'login failed','msg':'incorrect email or password','status':'false','code':400},400)
            
        except Exception as e:
            print(e)
            return Response({'msg':e})

        finally:
            cursor.close()
            connection.close()

    @jwt_required()
    @api_view(['POST'])
    def signup(request):
        try:
            cursor = connection.cursor()
            v_email = request.data['email']
            v_password = request.data['password']
            v_user_name = request.data['user_name']
            v_first_name = request.data['first_name']
            v_last_name = request.data['last_name']
            v_date_of_birth = request.data['date_of_birth']
            img = request.FILES.get('img')
       
            dt_strin = datetime.now().strftime("%Y-%m-%d%H-%M-%S")


            if img:
                filename = secure_filename(img.name)
                print(filename)
                img = Image.open(img)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img = ImageOps.exif_transpose(img) 

                # Convert Image to BytesIO
                img_byte_array = BytesIO()
                img.save(img_byte_array, format='JPEG')
                img_content = ContentFile(img_byte_array.getvalue())

                img_path = default_storage.save(f"image/{dt_strin}{filename}", img_content)

                url = default_storage.url(img_path)
                print('http://127.0.0.1:8000/'+url)


            created_by = get_jwt_identity(request)
            print((v_first_name,v_last_name,v_user_name,v_email,v_password,v_date_of_birth, created_by))
            
            created_by = 1
            cursor.callproc('add_users',((v_first_name,v_last_name,v_user_name,v_email,v_password,v_date_of_birth, created_by)))
            result = cursor.fetchone()
            print(result)
            if result:
                user = result[0]
                print(result[2])
                return Response({'id':user,'status':'true','code':200},200)
            else:
                return Response({'message':'signup failed','msg':'user registration unsuccessful','status':'false','code':400},400)
        
        except Exception as e:
            print(e)
            return Response({"msg":e})
        finally:
            cursor.close()
            connection.close()
