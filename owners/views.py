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
    
    # def get(self, request):
    #     owners = Owner.objects.all()
    #     results  = []
        
    #     for owner in owners:
    #         results.append(
    #             {
    #                 "name" : owner.name,
    #                 "email" : owner.email,
    #                 "age" : owner.age
    #             }
    #         )
       
    #     return JsonResponse({'resutls':results}, status=200) 
    
class DogsView(View):
    def post(self, request):
        data = json.loads(request.body)
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner_id = data["owner_id"]
        )
        return JsonResponse({'message':'SUCCESS'}, status=201)
    
    # def get(self, request):
    #     owners = Owner.objects.all()
    #     results  = []
        
    #     for owner in owners:
    #         results.append(
    #             {
    #                 "name" : owner.name,
    #                 "email" : owner.email,
    #                 "age" : owner.age
                    
    #             }
    #         )
       
    #     return JsonResponse({'resutls':results}, status=200)     