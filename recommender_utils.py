#!/usr/bin/env python
# coding: utf-8

# # Zero to Hero : An Overwatch Hero Recommender Utility file.
import pandas as pd
import numpy as np
from surprise import Reader, Dataset, accuracy
from surprise.prediction_algorithms import KNNWithMeans, KNNBasic, KNNBaseline
import time


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





def prediction(new, user_rating, df, algo, all_heroes, reader, battle_tag=None):
      """Define function to provide new hero for new User

    Parameters:
    new (Bool): provide new hero or not.
    user_rating (list): This is the new user data fed into the model
    df (dataframe): current dataframe with all other users
    algo (model object): The current model being used to make the predictions
    all_heroes (list): list of all_heroes in the game
    reader (Sikit-surprise reader object): used to read int he data for the model to work on.
    battle_tag=None (string): nickname for user if currently in database

    Returns:
    list of tuples: (Hero Name, prediction value)

   """
    hero_prediction_list = []
    player_rated_list = [i['Hero'] for i in user_rating]
    
    
    # check if user exists in dataframe and predict for them:
    if battle_tag in list(df.Battle_Tag):
        for h_id in df['Hero'].unique():
            #Check if a new hero is to be recommended:
            if new:
                #Return only hero recommendations not rated by user:
                if h_id not in top_rated_list:
                    hero_prediction_list.append((h_id, algo.predict(battle_tag, h_id, clip=False)[3]))
                    ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
            # Otherwise return all hero recommendations even if rated by user.
            else:
                hero_prediction_list.append((h_id, algo.predict(battle_tag, h_id, clip=False)[3]))
                ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        print(top_rated_list)
        return ranked_heroes[:]
                
    # If user does not exist in dataframe, add their ratings and data to the dataframe and recalculate
    else: 
        zeroed_user_rating = user_rating + [{'Battle_Tag': user_rating[0]['Battle_Tag'], 'Hero': h, 'Ratings':0} for h in all_heroes if h not in player_rated_list]
        new_ratings_df = df.append(zeroed_user_rating, ignore_index=True, sort=False)
        new_data = Dataset.load_from_df(new_ratings_df[['Battle_Tag', 'Hero', 'Ratings']], reader)
        #fit algorithm to new data
        algo1 = KNNBaseline(sim_options={'name':'cosine', 'user_based':False})
        algo1.fit(new_data.build_full_trainset())
        #return ranked predicted heroes that are not in the user rating list.
        for h_id in new_ratings_df['Hero'].unique():
            #Check if new hero is to be precommended:
            if new:
                if h_id not in player_rated_list:
                    hero_prediction_list.append((h_id, algo1.predict(user_rating[0]['Battle_Tag'], h_id, clip=False)[3]))
                    ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
            else:
                hero_prediction_list.append((h_id, algo1.predict(user_rating[0]['Battle_Tag'], h_id, clip=False)[3]))
                ranked_heroes = sorted(hero_prediction_list, key=lambda x:x[1], reverse=True)
        return ranked_heroes[:]
