from rest_framework.views import APIView
from .models import FoodItem
from rest_framework import viewsets
from rest_framework import permissions # so only authenticated users can access api
from .serializer import FoodItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .lpscripts.testscript import dosomething
from .lpscripts import food_recommend

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    permission_classes = []

# class TesterViewSet(APIView):
#     def get(self, request):
#         return Response({'some':'data'})

@api_view(['GET'])
def recommendfood(request):
    if request.method == 'GET':
        weight = int(request.GET['weight'])
        bodyfat = float(request.GET['bodyfat'])
        avg_activity = int(request.GET['avg_activity'])

        fullmenu = FoodItem.objects.all()
        fullmenu = list(fullmenu)
        food_list = []
        for i in fullmenu:
            if i.calories == None: continue
            food = {
                'type': str(i.category),
                'name': str(i.name),
                'calories': float(i.calories)
            }
            food_list.append(food)
        
        fr = food_recommend.FoodRecommendation(food_list)
        breakfast = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='breakfast', c=1)[0][1]
        lunch = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='lunch', c=1)[0][1]
        dinner = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='dinner', c=1)[0][1]
        
        breakfast = FoodItem.objects.get(name=breakfast)
        lunch = FoodItem.objects.get(name=lunch)
        dinner = FoodItem.objects.get(name=dinner)
        
        responsedict = [
            {"category": "Breakfast",
             "items": [breakfast.reformatforios()[1]]},
            {"category": "Lunch",
             "items": [lunch.reformatforios()[1]]},
            {"category": "Dinner",
             "items": [dinner.reformatforios()[1]]}
        ]
        
        return Response(responsedict)

@api_view(['GET'])
def menu(request):
    if request.method == 'GET':
        fullmenu = FoodItem.objects.all()
        fullmenu = list(fullmenu)
        categories = {}
        for i in fullmenu:
            r = i.reformatforios()
            if r[0] in categories:
                categories[r[0]].append(r[1])
            else:
                categories[r[0]] = [r[1]]

        responsedict = []
        for c in categories:
            responsedict.append({'category': c, 'items': categories[c]})

        return Response(responsedict)


