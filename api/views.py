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
        weight = float(request.GET['weight'])
        bodyfat = float(request.GET['bodyfat'])
        avg_activity = float(request.GET['avg_activity'])
        cb = int(request.GET['cb'])
        cl = int(request.GET['cl'])
        cd = int(request.GET['cd'])

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
        breakfast = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='breakfast', c=cb)
        lunch = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='lunch', c=cl)
        dinner = fr.recommend_foods(weight=weight, fat=bodyfat, avg_ae=avg_activity, time='dinner', c=cd)
        
        breakfast = [t[1] for t in breakfast]
        lunch = [t[1] for t in lunch]
        dinner = [t[1] for t in dinner]

        def getFIObjects(meal):
            fiobjs = [FoodItem.objects.get(name=fi) for fi in meal]
            return fiobjs

        breakfast = getFIObjects(breakfast)
        lunch = getFIObjects(lunch)
        dinner = getFIObjects(dinner)
        
        responsedict = [
            {"category": "Breakfast",
             "items": [x.reformatforios()[1] for x in breakfast]},
            {"category": "Lunch",
             "items": [x.reformatforios()[1] for x in lunch]},
            {"category": "Dinner",
             "items": [x.reformatforios()[1] for x in dinner]}
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


