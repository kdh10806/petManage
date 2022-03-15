import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from owners.models import Owner, Dog

class OwnersView(View):
    def post(self, request):
        data = json.loads(request.body)
        Owner.objects.create(
            name = data['name'],
            email = data['email'],
            age = data['age'],
        )
        return JsonResponse({'message':'SUCCESS'}, status=201)
    
    def get(self, request):
        owners = Owner.objects.all()
        results  = []
        
        for owner in owners:
            dogs = owner.dog_set.all()
            dog_list = []
            for dog in dogs:
                dog_info = {
                'dog_name' : dog.name,
                'dog_age' : dog.age
                }
                dog_list.append(dog_info)
            results.append(
                {
                    "name" : owner.name,
                    "email" : owner.email,
                    "age" : owner.age,     
                    "dog_list" : dog_list,
                }
            )
        return JsonResponse({'results':results}, status=200) 
    
class DogsView(View):
    def post(self, request):
        data = json.loads(request.body)
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner_id = data["owner_id"]
        )
        return JsonResponse({'message':'SUCCESS'}, status=201)
    
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