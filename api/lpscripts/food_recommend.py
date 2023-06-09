import sys
import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
from scipy.stats import skewnorm

class FoodRecommendation():
    def __init__(self, food_list):
        self._food_df = None
        self._init_food_df(food_list)
    

    def _init_food_df(self, food_list):
        
        self._food_df = pd.DataFrame(food_list)
        # convert food type into categorical values
        le = LabelEncoder()
        self._food_df['type'] = le.fit_transform(self._food_df['type'])
        

    def _calc_calneeds(self, weight, fat, avg_ae, time='lunch'):
        """
        This method calculate and init the calories need for the user.
        Recommend Cal Needs = BMR + Average Activity Level
        : fat -> body fat percentage
        : avg_ae -> average active energy
        : time -> breakfast, lunch, or dinner
        """
        activity_level = None
        # determine activity level (sedentary, lightly active, active, very active)
        if (avg_ae < 130):
            activity_level = 1.2
        elif (avg_ae >= 130 and avg_ae < 160):
            activity_level = 1.375
        elif (avg_ae >= 160 and avg_ae < 580):
            activity_level = 1.55
        else:
            activity_level = 1.725



        cal_splits = {'breakfast': 0.2, 'lunch': 0.4, 'dinner': 0.4, 'all': 1}
        bmr = 370 + 21.6 * (1-fat) * weight
        cal_needs = bmr * activity_level
        cal_needs = cal_needs * cal_splits[time]

        return cal_needs
    

    def find_foods(self, input_cal, c=1, debug=False):
        """
        Find k top food that have closest calories to the user calories
        : c - size of combinations of food items
        """

        # random split of input calories to get different combinations of food
        def _skewed_random(a, b, skewness=2, size=None):
            # usually one food of a meal should have larger weight (e.g. primary dish)
            # therefore we need to skew the splits
            loc = (a + b) / 2
            scale = (b - a) / 6
            a_param = skewness
            x = skewnorm.rvs(a_param, loc, scale, size)
            return x
        
        # TODO: line 94-103 is changed
        # generate c random calories splits (skewed)
        cal_seg = []
        total_cal = input_cal
        for _ in range(c-1):
            cal = _skewed_random(0, total_cal, skewness=-2)
            cal_seg.append(cal)
            total_cal -= cal
        cal_seg.append(total_cal)

        if debug == True:
            print(cal_seg)

        # find c foods closest to the c splits
        cdist = [(0, None)] * c
        cfoods = {}
        for idx, cal in enumerate(cal_seg):
            min_cal = sys.float_info.max
            for _, row in self._food_df[['name', 'calories']].iterrows():
                dist = np.abs(cal - row.values[1])
        
                if row.values[1] not in cfoods and dist < min_cal:
                    cdist[idx] = (row.values[1], row.values[0])
                    cfoods[row.values[1]] = True
                    min_cal = dist

        return cdist
    

    def recommend_foods(self, weight=70.0, fat=0.165, avg_ae=300.0, time='lunch', c=1):
        """
        Recommend c foods based on user's health data
        : c - size of combinations of food items
        """
        cal_needs = self._calc_calneeds(weight, fat, avg_ae, time)

        return self.find_foods(cal_needs, c)
    






