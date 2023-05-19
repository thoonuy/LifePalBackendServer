from django.db import models

# Create your models here.
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    isVegan = models.BooleanField()
    isVegetarian = models.BooleanField()
    servingSize = models.CharField(max_length=20, null=True)
    servingUnit = models.CharField(max_length=20, null=True)
    calories = models.CharField(max_length=20, null=True)
    caloriesFromFat = models.CharField(max_length=20, null=True)
    totalFat = models.CharField(max_length=20, null=True)
    transFat = models.CharField(max_length=20, null=True)
    cholesterol = models.CharField(max_length=20, null=True)
    sodium = models.CharField(max_length=20, null=True)
    totalCarbohydrates = models.CharField(max_length=20, null=True)
    dietaryFiber = models.CharField(max_length=20, null=True)
    sugars = models.CharField(max_length=20, null=True)
    protein = models.CharField(max_length=20, null=True)
    vitaminA = models.CharField(max_length=20, null=True)
    vitaminC = models.CharField(max_length=20, null=True)
    calcium = models.CharField(max_length=20, null=True)
    iron = models.CharField(max_length=20, null=True)
    saturatedFat = models.CharField(max_length=20, null=True)
    isEatWell = models.BooleanField()
    isPlantForward = models.BooleanField()
    isWholeGrain = models.BooleanField()

    def __str__(self):
        return self.name

    def reformatforios(self):
        itemdict = {
            'name': self.name,
            'description': self.description,
            'nutrition':  {
                'isVegan': self.isVegan,
                'isVegetarian': self.isVegetarian,
                'servingSize': self.servingSize,
                'servingUnit': self.servingUnit,
                'calories': self.calories,
                'caloriesFromFat': self.caloriesFromFat,
                'totalFat': self.totalFat,
                'transFat': self.transFat,
                'cholesterol': self.cholesterol,
                'sodium': self.sodium,
                'totalCarbohydrates': self.totalCarbohydrates,
                'dietaryFiber': self.dietaryFiber,
                'sugars': self.sugars,
                'protein': self.protein,
                'vitaminA': self.vitaminA,
                'vitaminC': self.vitaminC,
                'calcium': self.calcium,
                'iron': self.iron,
                'saturatedFat': self.saturatedFat,
                'isEatWell': self.isEatWell,
                'isPlantForward': self.isPlantForward,
                'isWholeGrain': self.isWholeGrain
            }
        }
        return (self.category, itemdict)

