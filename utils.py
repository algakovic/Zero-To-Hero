# File used for functions and refactored code imported into the main notebook ('Zero-To-Hero') as utils.py


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


# Create Role category for each Hero;
tanks = ['D.Va','Orisa', 'Reinhardt', 'Roadhog', 'Sigma', 'Winston', 'Wrecking Ball', 'Zarya']
damage = ['Ashe','Bastion','Doomfist','Genji','Hanzo','Junkrat','McCree','Mei','Pharah','Reaper','Soldier: 76','Sombra','Symmetra','Torbjörn','Tracer','Widowmaker']
support = ['Ana','Baptiste','Brigitte','Lúcio','Mercy','Moira','Zenyatta']

all_heroes = tanks+damage+support
roles = heroes.copy()
roles['Role'] = ['Tank' if x in tanks else 'Damage' if x in damage else 'Support' for x in heroes['Hero']] 

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



# # first attempt in learning oop
# class learningRate():
#     df = pd.read_csv('200k_Top5_heroes.csv')
#     #Clean null values
#     if df.isnull().sum().any():
#         df.dropna(how='any', inplace=True)
#     else:
#         pass    
    
#     def __init__(self, test_size):
# #         self.split = train_test_split(?)
#         self._volume = round((1-test_size)*self.shape[0])
#         self._train_size = str(round(1-test_size, 1)*100)+ '%'
#         self._isnull = df.isnull().sum()
