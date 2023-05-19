from .models import FoodItem
from rest_framework import serializers

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'description', 'isVegan', 'isVegetarian',
                  'servingSize', 'servingUnit', 'calories', 'caloriesFromFat',
                  'totalFat', 'transFat', 'cholesterol', 'sodium',
                  'totalCarbohydrates', 'dietaryFiber', 'sugars', 'protein',
                  'vitaminA', 'vitaminC', 'calcium', 'iron', 'saturatedFat',
                  'isEatWell', 'isPlantForward', 'isWholeGrain']
