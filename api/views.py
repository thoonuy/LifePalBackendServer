from rest_framework.views import APIView
from .models import FoodItem
from rest_framework import viewsets
from rest_framework import permissions # so only authenticated users can access api
from .serializer import FoodItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .lpscripts import food_recommend, water_intake_recommend, sleep_time_recommend
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

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
def foodrec(request):
    def getrec(mealtime, w, bf, aa, c):
        # 2.a. get FoodItem objects
        menu = list(FoodItem.objects.filter(mealtime=mealtime))
        if not menu: return [] # return [] if there's nothing

        # 2.b. convert to food_list
        food_list = []
        for i in menu:
            if i.calories == None: continue
            food = {
                'type': str(i.category),
                'name': str(i.name),
                'calories': float(i.calories)
            }
            food_list.append(food)

        # 2.c. create FoodRecommendation object
        fr = food_recommend.FoodRecommendation(food_list)

        # 2.d. recommend 
        recfoods = fr.recommend_foods(weight=w, fat=bf, avg_ae=aa, time=mealtime, c=c)
        return [t[1] for t in recfoods]

    def getFIObjects(meal, mealtime):
        fiobjs = [FoodItem.objects.get(name=fi, mealtime=mealtime) for fi in meal]
        return fiobjs

    if request.method == 'GET':
        # 1. get params from request
        weight = float(request.GET['weight'])
        bodyfat = float(request.GET['bodyfat'])
        avg_activity = float(request.GET['avg_activity'])
        cb = int(request.GET['cb'])
        cl = int(request.GET['cl'])
        cd = int(request.GET['cd'])

        # 2. for each meal time
        # 2.a. get recommendation
        breakfast = getrec("breakfast", weight, bodyfat, avg_activity, cb)
        lunch = getrec("lunch", weight, bodyfat, avg_activity, cl)
        dinner = getrec("dinner", weight, bodyfat, avg_activity, cd)

        # 2.b. reformat for response
        breakfast = getFIObjects(breakfast, "breakfast")
        lunch = getFIObjects(lunch, "lunch")
        dinner = getFIObjects(dinner, "dinner")

        
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
def waterrec(request):
    if request.method == 'GET':
        # 1. get params from request
        age = float(request.GET['age'])
        weight = float(request.GET['weight'])
        height = float(request.GET['height'])
        avg_activity = float(request.GET['avg_activity'])
        temperature = float(request.GET['temperature'])
        # 2. recommend
        path = os.path.join(BASE_DIR, "api/lpscripts/water_drinking_data.csv")
        wr = water_intake_recommend.WaterRecommendatio(path)
        model_path = os.path.join(BASE_DIR, "api/lpscripts/models/water_intake_model")
        scaler_path = os.path.join(BASE_DIR, "api/lpscripts/models/std_scaler.bin")
        result = wr.recommend_water_intake(age,weight,height,avg_activity,temperature, model_path, scaler_path)
        # 3. respond
        responsedict = {"recommended intake": result, "unit": "liters"}
        return Response(responsedict)

@api_view(['GET'])
def sleeprec(request):
    def time_to_output_dict(t,b):
        hh,mm = t.split(':')
        return {"sleep_time": hh+mm, "date": "after" if b else "before"}

    if request.method == 'GET':
        # 1. get params from request
        avg_asleep = float(request.GET['avg_asleep'])
        avg_inbed = float(request.GET['avg_inbed'])
        avg_activity = float(request.GET['avg_activity'])
        wake_time = str(request.GET['wake_time'])
        wake_time = str(int(wake_time[0:2])) + ':' + wake_time[2:]
        # 2. recommend
        sleep_rcm = sleep_time_recommend.SleepRecommendation()
        # [('01:05', 0.8817204301075268, True), ('23:32', 0.7655555555555555, False)]
        recs,x = sleep_rcm.recommend_sleep_times('dev2', 'pass2312', avg_inbed, avg_asleep, avg_activity, wake_time)
        # recs,x = sleep_rcm.recommend_sleep_times('dev2', 'pass2312', 9, 6.89, 654, "9:52")
        # 3. respond
        responsedict = [time_to_output_dict(r[0], r[2]) for r in recs]
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


