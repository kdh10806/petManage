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
    
class DogsView(View):
    def post(self, request):
        data = json.loads(request.body)
        owner = Owner.objects.all()
    
        Dog.objects.create(
            name = data['name'],
            age = data['age'],
            owner_id = owner.id
        )
        return JsonResponse({'message':'SUCCESS'}, status=201)