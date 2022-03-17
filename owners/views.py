import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from owners.models import Owner, Dog

class OwnersView(View):
    def post(self, request):
        try:
            # 1. request.body로 부터 필요한 정보를 꺼낸다.
            data = json.loads(request.body)
            name = data['name'],
            email = data['email']
            age =  data['age']
        
            # Owner.objects.create(
            # name = data['name'],
            # email = data['email'],
            # age = data['age'],
            # )
            
            # 2. 해당 정보를 가지고 INSERT 쿼리를 날린다.
            Owner.objects.create(name=name, email=email, age=age)
        
            # 3. Response를 보낸다.
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'Error' : 'KeyError'}, status=400)
        
        
    def get(self, request):
        # 1. owner list
        owners = Owner.objects.all() #쿼리셋 리스트 리턴
        results  = []
        
        # 2. 각 owner 마다 역참조해서 강아지 리스트 만들기   
        for owner in owners:
            dogs = owner.dog_set.all()
            dog_list = []
            for dog in dogs:
                dog_dict = {
                    'name' : dog.name,
                    'age'  : dog.age
                }
                dog_list.append(dog_dict)
            
            owner_dict = {
                'name'  : owner.name,
                'email' : owner.email,
                'age'   : owner.age,
                'dogs'  : dog_list
            }
            results.append(owner_dict)
            
        # #list comprehension
        # results = [{
        #     'name'     : owner.name,
        #     'email'    : owner.email,
        #     'age'      : owner.age,
        #     'dogs'     : [{
        #         'name' : dog.name,
        #         'age'  : dog.age   
        #     }for dog in owner.dog_set.all()]
        # }for owner in owners]
        
        # 3. 프론트엔드에서 처리 가능한 데이터 구조에 맞게 가공해서 response
        return JsonResponse({'results':results}, status=200) # 쿼리셋은 json으로 serialize가 불가능하다.
    
class DogsView(View):
    def post(self, request):
        try:
            # 1. request.body로 부터 필요한 정보를 꺼낸다.
            data = json.loads(request.body)
            name = data['name']
            age = data['age']
            owner_id = data['owner']

            # 1-2. owner 객체를 가져와서 직접 할당( owner_id를 받음, 검증 먼저 하자. )
            owner = Owner.objects.get(id = owner_id)
            
            # 2. 해당 정보를 가지고 INSERT 쿼리를 날린다.
            Dog.objects.create(name=name, age=age, owner=owner)
            # Dog.objects.create(
            #     name = data['name'],
            #     age = data['age'],
            #     owner_id = data["owner_id"]
            # )
        
            # 3. Response를 보낸다.
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'Error' : 'KeyError'}, status=400)
        except Owner.DoesNotExist:
            return JsonResponse({'Error' : 'Specified owner does not exist.'}, status=404)
        except Owner.MultipleObjectsReturned:
            return JsonResponse({'Error' : 'Multiple id'}, status=400)
        
    def get(self, request):
        dogs = Dog.objects.all()
        results  = []
        
        for dog in dogs:
            results.append(
                {
                    "name" : dog.name,
                    "age" : dog.age,
                    "owner_name" : dog.owner.name
                }
            )
       
        return JsonResponse({'results':results}, status=200)