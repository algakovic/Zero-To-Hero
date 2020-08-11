# Zero to Hero: An Overwatch Hero Recommendation System

Version: 1.0

## Executive summary:
Zero to Hero is a recommendation system that offers users who play the popular eSports title: Overwatch a way to choose a hero to play with. In Overwatch, two teams of 6 players go head to head in a heated contest. With a growing pool of 31 heroes to choose from in 3 different roles, new and veteran users can benefit from this hero recommender. 

Often players will be stuck single-mindedly on a hero unwilling to choose a new hero to play. This can put enormous pressure on the team. These users will be able to get a hero recommended to them using Zero to hero. Older players who have played a long time and want to diversify their hero pool can also benefit. 

The system falls in line with the game developers encouragement to players of choosing heroes that they enjoy playing or at the very least providing some variety in their hero choices.
You can try the app created by my partner and I [here](https://zerotohero.netlify.app/).
## Key Files:
1. [Link](https://docs.google.com/presentation/d/1Msojl3rMYKx6QoBoxKPLGWAH0FjbMUsbQF8YecpShV8/edit?usp=sharing) to google slides presentation file  
2. Zero_to_Hero_Presentation.pdf: PDF of presentation slides  
3. Zero_to_Hero.ipynb: Jupyter Notebook  
4. Recommender_utils.py: Local python functions source file for jupyter notebook   
5. 60k_Top5_heroes.csv: Raw CSV file with data  
6. app.py: Flask application file  
7. zero_to_hero.py: python code source for app.py  
8. Scrapy: All files related to Scraping user top heroes data  
9. Zero-to-hero-client: All files related to React Front-end client for application.

## Methodology:
1. **Data and Functions Import**  
2. **Cleaning and Reformating Data into Relevant Structure**  
3. **Role Category Implementation**  
4. **Implementing the Recommendation System**  
    4.1 Training the model  
5. **Making a Recommendation**  
    5.1 Interactive user_rating input  
    5.2 Making predictions with new user ratings

## Key Findings:
The system recommends well to users who exist in the database.
However it does not extend well to new users that have to overcome the cold start problem by choosing and rating the five randomly selected heroes.
The data that trained the KNN model is highly skewed towards top players and thus recommendations returned follow a set hierarchy of heroes.
In other words the model returns what most players at the top level are playing in the current meta state of the game. Based on this data 'Genji', 'Widowmaker', 'McCree', 'Hanzo' and 'Ana' are consistently at the top of the recommended list.


![Prediction function in action:](/Images/Prediction-function-in-action.png)
Prediction function for recommendation system returning sorted list of hero recommendations



## Conclusions:
The Main issue with the system is the skewedness of the training data towards highest ranking players. These players tend towards playing similar 'best choice' heroes and so the system is weighted towards recommending those heroes over others. 

## Recommendations:
Obtain data on the community at large rather than top ranked players and run model again.

Features to implement include: 
- Existing users will be able to provide their Battle_Tag id to obtain a recommendation.  

- Implementation of a role choice system, giving users the ability to key in on one of the three Roles (Tank, Support, Damage) getting a recommendation of their desired role.  

- Recommending heroes based on the synergy factor of the team.  



