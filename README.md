# LifePalBackend

## Food Recommendation Endpoint

Access with `api/foodrec`. All parameters below are required.

__Use format__:  
```
http://3.15.22.210:8000/api/foodrec/?weight=XXX&bodyfat=XXX&avg_activity=XXX&cb=XXX&cl=XXX&cd=XXX
```

__Parameters__:  
`weight`: Weight of user in kg.  
`bodyfat`: Body fat percentage of user.  
`avg_activity`: Average daily active energy expenditure of user.  
`cb`: Number of food items you want returned for breakfast.  
`cl`: Number of food items you want returned for lunch.  
`cd`: Number of food items you want returned for dinner.

__Example__:  
<http://3.15.22.210:8000/api/foodrec/?weight=55&bodyfat=0.165&avg_activity=300&cb=2&cl=1&cd=1>

## Full Menu Endpoint

Access with `api/menu`. No parameters needed. Simply follow link below:  
<http://3.15.22.210:8000/api/menu/>

## Water Intake Recommendation Endpoint

Access with `api/waterrec`. All parameters below are required.

__Use format__:  
```
http://3.15.22.210:8000/api/waterrec/?age=XXX&weight=XXX&height=XXX&avg_activity=XXX&temperature=XXX
```

__Parameters__:  
`age`: User's age in years.  
`weight`: User's weight.  
`height`: User's height.  
`avg_activity`: Average daily active energy expenditure of user.  
`temperature`: Current temperature.

__Example__:  
<http://3.15.22.210:8000/api/waterrec/?age=21&weight=10&height=1.85&avg_activity=320&temperature=14>

## Sleep Time Recommendation Endpoint

Access with `api/sleeprec`. All parameters below are required.

__Use format__:  
```
http://3.15.22.210:8000/api/sleeprec/?user=XXX&avg_asleep=XXX&avg_inbed=XXX&avg_activity=XXX&wake_time=XXX
```

__Parameters__:  
`user`: The user's username  
`avg_alseep`: Average time user spends alseep.  
`avg_inbed`: Average time user spends in bed.  
`avg_activity`: Average daily active energy expenditure of user.  
`wake_time`: The user's desired wake up time.

__Example__:  
<http://3.15.22.210:8000/api/sleeprec/?user=anteater&avg_asleep=6.89&avg_inbed=9&avg_activity=654&wake_time=0632>

