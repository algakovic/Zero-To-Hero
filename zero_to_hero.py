#!/usr/bin/env python
# coding: utf-8

# # Zero to Hero : An Overwatch Hero Recommender
import pandas as pd
import numpy as np
import matplotlib as plt
import time



# get_ipython().run_line_magic('matplotlib', 'inline')
Top5 = pd.read_csv('60k_Top5_heroes.csv')


#Define the rating function:
def rating(x, rating_new):
    if x==1:
        return rating_new
    else:
        return 0
#Rating Implementation function:
def apply_curation(df):
    for col in df.columns:
        if col[4]=='1':
            df[col]=df[col].apply(lambda x: rating(x, 5))
        elif col[4]=='2':
            df[col]=df[col].apply(lambda x: rating(x, 4.8))
        elif col[4]=='3':
            df[col]=df[col].apply(lambda x: rating(x, 4.6))
        elif col[4]=='4':
            df[col]=df[col].apply(lambda x: rating(x, 4.4))
        elif col[4]=='5':
            df[col]=df[col].apply(lambda x: rating(x, 4.2))
    return df
#Preprocessing of dataframe to drop missing values and get dummies.
def preprocessing(df):
    if df.isna().any:
        df.dropna(how='any', inplace=True)
    else:
        pass
    #Get Dummies for all heroes
    heroes = pd.get_dummies(df, columns=['Hero1', 'Hero2', 'Hero3', 'Hero4', 'Hero5'])
    return heroes

#Concatenate the columns reducing dimension to just 31 columns one per hero:
def concat_melt(df):
    
    list_heroes = []
    index = ['1', '2', '3', '4', '5']
    
    for col in df.columns:
        list_heroes.append(col[6:])

    for hero in list_heroes[1:32]:
        df[hero] = df[f'Hero{index[0]}_{hero}'] + df[f'Hero{index[1]}_{hero}'] + df[f'Hero{index[2]}_{hero}'] + df[f'Hero{index[3]}_{hero}'] + df[f'Hero{index[4]}_{hero}']
    
    # Drop extra columns and Battle_tags
    df.drop(labels=df.loc[:,'Hero1_Ana':'Hero5_Zenyatta'], axis=1, inplace=True)

    df = df.melt(id_vars='Battle_Tag')
    return df




heroes_preprocessed = preprocessing(big_check)
heroes_curated = apply_curation(heroes_preprocessed)

heroes = concat_melt(heroes_curated)
heroes.rename(columns={"variable":"Hero", "value":"Ratings"}, inplace = True)


# Create Role category for each Hero;
tanks = ['D.Va','Orisa', 'Reinhardt', 'Roadhog', 'Sigma', 'Winston', 'Wrecking Ball', 'Zarya']
damage = ['Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker']
support = ['Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

all_heroes = tanks+damage+support
roles = heroes.copy()
roles['Role'] = ['Tank' if x in tanks else 'Damage' if x in damage else 'Support' for x in heroes['Hero']] 



# importing relevant libraries
from surprise import Reader, Dataset, accuracy
from surprise.model_selection import train_test_split

from surprise.model_selection import cross_validate
from surprise.prediction_algorithms import SVD
from surprise.prediction_algorithms import KNNWithMeans, KNNBasic, KNNBaseline
from surprise.model_selection import GridSearchCV


#Read in Values as a Surprise Dataset:
reader = Reader(rating_scale=(1,5))

train_data = Dataset.load_from_df(heroes[['Battle_Tag', 'Hero', 'Ratings']], reader)

trainset, testset = train_test_split(train_data, test_size=.25)
# trainset = train_data.build_full_trainset()





# # Instantiate two KNN Basic memory based model
# # ⏰ This cell may take several minutes to run


algobaseitems = KNNBaseline(sim_options={'name':'cosine', 'user_based':False})
start = time.time()
algobaseitems.fit(trainset)
end = time.time()
fit_time = (end - start)

start = time.time()
predictions = algobaseitems.test(testset)
end = time.time()

pred_time = (end-start)
print(f'Fit time: {round(fit_time, 3)} / Predict time: {pred_time} / ---- Accuracy (RMSE): {round(accuracy.rmse(predictions), 3)}')



# Create the hero rating input for users:
from collections import Counter

def hero_rater(battle_tagid, heroes_df, num, role=None):
    # Placeholder lists
    rating_list = []
    duplicate_list = []
    role_list = []
    # I Want 5 ratings total, count num -1 each cycle.
    while num > 0:
        role_freq = Counter(role_list)
        # Obtain a random dataframe entry:
        if role:
            hero = heroes_df[heroes_df['Role'].str.contains(role)].sample(1)
        else:
            hero = heroes_df.sample(1)

        # If Hero in sample has already been obtained then skip 
        if hero['Hero'].values[0] in duplicate_list:
            continue
        # Count role type of heroes sampled: do not allow more than 2 of damage and Tank and 1 of support.   
        if role_freq['Damage']==2 and hero['Role'].values[0] == 'Damage':
            continue
        elif role_freq['Tank']==2 and hero['Role'].values[0] == 'Tank':
            continue
        elif role_freq['Support']==1 and hero['Role'].values[0] == 'Support':
            continue

        # Create hero id in duplicate list for above duplicate check.    
        duplicate_list.append(hero['Hero'].values[0])
        role_list.append(hero['Role'].values[0])


        # Ask for user input about hero / role
        print(hero[['Hero', 'Role']])
        rating = input('How do you rate this Hero on a scale of 1-5?, press n if you do not want to give a rating :\n')

        # If rating 'n' continue to next hero.
        # If outside range 1-5 Return error
        # Otherwise provide dict entry in rating_list placeholder.
        if rating == 'n':
            continue
        elif float(rating) > 5 or float(rating) < 1: 
            print('Error, not within rating scale')
            continue
        else:
            rating_one_hero = {'Battle_Tag':battle_tagid, 'Hero':hero['Hero'].values[0], 'Ratings':rating}
            rating_list.append(rating_one_hero) 
            num -= 1
    return rating_list



def test_rating():
     rating = input('How do you rate this Hero on a scale of 1-5?, press n if you do not want to give a rating :\n')



# define new hero for New User predictions functions
def new_hero_new_user_prediction(user_rating, df, algo, battle_tag=None):
    hero_prediction_list = []
    player_rated_list = [i['Hero'] for i in user_rating]
    # check if user exists in dataframe and predict for them:
    if battle_tag in list(df.Battle_Tag):
        
        for h_id in df['Hero'].unique():
            if h_id not in player_rated_list and h_id not in ['Hanzo', 'Widowmaker', 'Genji', 'McCree']:
                hero_prediction_list.append((h_id, algo.predict(battle_tag, h_id, clip=False)[3]))
        ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        return ranked_heroes[:]
    #Add new users ratings to the dataframe and read in the file
    else: 
        zeroed_user_rating = user_rating + [{'Battle_Tag': user_rating[0]['Battle_Tag'], 'Hero': h, 'Ratings':0} for h in all_heroes if h not in player_rated_list]
        new_ratings_df = df.append(zeroed_user_rating, ignore_index=True, sort=False)
        new_data = Dataset.load_from_df(new_ratings_df[['Battle_Tag', 'Hero', 'Ratings']], reader)
        #fit algorithm to new data
        algo1 = KNNBaseline(sim_options={'name':'cosine', 'user_based':False})
        algo1.fit(new_data.build_full_trainset())
        #return ranked predicted heroes that are not in the user rating list, or Hanzo, Widow, Genji or Mccree:
        for h_id in new_ratings_df['Hero'].unique():
            if h_id not in player_rated_list and h_id not in ['Hanzo', 'Widowmaker', 'Genji']:
                hero_prediction_list.append((h_id, algo1.predict(user_rating[0]['Battle_Tag'], h_id, clip=False)[3]))
        ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        print(ranked_heroes[:10])
        return ranked_heroes[:]


# define New_User predictions functions
def new_user_prediction(user_rating, df, algo, battle_tag=None):
    hero_prediction_list = []
    player_rated_list = [i['Hero'] for i in user_rating]
    # check if user exists in dataframe and predict for them:
    if battle_tag in list(df.Battle_Tag):
        for h_id in df['Hero'].unique():
            if h_id not in ['Hanzo', 'Widowmaker', 'Genji', 'McCree']:
                hero_prediction_list.append((h_id, algo.predict(battle_tag, h_id, clip=False)[3]))
        ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        return ranked_heroes[:]
    
    else:
        zeroed_user_rating = user_rating + [{'Battle_Tag': user_rating[0]['Battle_Tag'], 'Hero': h, 'Ratings':0} for h in all_heroes if h not in player_rated_list]
        #Add new users ratings to the dataframe and read in the file
        new_ratings_df = df.append(zeroed_user_rating, ignore_index=True, sort=False)
        new_data = Dataset.load_from_df(new_ratings_df[['Battle_Tag', 'Hero', 'Ratings']], reader)
        #fit algorithm to new data
        algo1 = KNNBaseline(sim_options={'name':'cosine', 'user_based':False})
        algo1.fit(new_data.build_full_trainset())
        
        #return ranked predicted heroes that are not in the user rating list:
        for h_id in new_ratings_df['Hero'].unique():
            if h_id not in ['Hanzo', 'Widowmaker', 'Genji', 'McCree']:
                hero_prediction_list.append((h_id, algo1.predict(user_rating[0]['Battle_Tag'], h_id, clip=False)[3]))
        ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        return ranked_heroes[:]



from flask import Flask, jsonify, request

# CORS is to allow us to access this API from a different server
from flask_cors import CORS


app = Flask(__name__)

# apply the cors config to allow access
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route("/predict", methods=["POST"])
def predict_top_hero():
    user_ratings = request.get_json()
    print(f'user ratings are {user_ratings}!') 
    fakeResult = [('Ana', 4.3485512861922753), ('Mei', 3.0011787731546877), ('Zarya', 3.8517846004714036), ('Roadhog', 2.7864246532326393), ('Mercy', 1.7086552943912291)]
    return jsonify(fakeResult)

    
if __name__ == '__main__':
    app.run(debug=True)

