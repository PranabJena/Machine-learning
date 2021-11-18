# Importing essential libraries
import pandas as pd
import pickle

# Loading the dataset
df = pd.read_csv('ipl.csv')

# --- Data Cleaning ---
# Removing unwanted columns
columns_to_remove = ['mid', 'batsman', 'bowler', 'striker', 'non-striker']
df.drop(labels=columns_to_remove, axis=1, inplace=True)

# Keeping only consistent teams
consistent_teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Rajasthan Royals',
                    'Mumbai Indians', 'Kings XI Punjab', 'Royal Challengers Bangalore',
                    'Delhi Daredevils', 'Sunrisers Hyderabad']
df = df[(df['bat_team'].isin(consistent_teams)) & (df['bowl_team'].isin(consistent_teams))]

# Removing the first 5 overs data in every match
df = df[df['overs']>=5.0]

# Converting the column 'date' from string into datetime object
from datetime import datetime
df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

# --- Data Preprocessing ---
# Converting categorical features using OneHotEncoding method
encoded_df = pd.get_dummies(data=df, columns=['bat_team', 'bowl_team','venue'])

# Rearranging the columns
encoded_df = encoded_df[['date', 'bat_team_Chennai Super Kings', 'bat_team_Delhi Daredevils', 'bat_team_Kings XI Punjab',
              'bat_team_Kolkata Knight Riders', 'bat_team_Mumbai Indians', 'bat_team_Rajasthan Royals',
              'bat_team_Royal Challengers Bangalore', 'bat_team_Sunrisers Hyderabad',
              'bowl_team_Chennai Super Kings', 'bowl_team_Delhi Daredevils', 'bowl_team_Kings XI Punjab',
              'bowl_team_Kolkata Knight Riders', 'bowl_team_Mumbai Indians', 'bowl_team_Rajasthan Royals',
              'bowl_team_Royal Challengers Bangalore', 'bowl_team_Sunrisers Hyderabad',
              'venue_Brabourne Stadium', 'venue_Buffalo Park',
              'venue_De Beers Diamond Oval', 'venue_Dr DY Patil Sports Academy',
              'venue_Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
              'venue_Dubai International Cricket Stadium', 'venue_Eden Gardens',
              'venue_Feroz Shah Kotla',
              'venue_Himachal Pradesh Cricket Association Stadium',
              'venue_Holkar Cricket Stadium',
              'venue_JSCA International Stadium Complex', 'venue_Kingsmead',
              'venue_M Chinnaswamy Stadium', 'venue_MA Chidambaram Stadium, Chepauk',
              'venue_Maharashtra Cricket Association Stadium',
              'venue_New Wanderers Stadium', 'venue_Newlands',
              'venue_OUTsurance Oval',
              'venue_Punjab Cricket Association IS Bindra Stadium, Mohali',
              'venue_Punjab Cricket Association Stadium, Mohali',
              'venue_Rajiv Gandhi International Stadium, Uppal',
              'venue_Sardar Patel Stadium, Motera', 'venue_Sawai Mansingh Stadium',
              'venue_Shaheed Veer Narayan Singh International Stadium',
              'venue_Sharjah Cricket Stadium', 'venue_Sheikh Zayed Stadium',
              "venue_St George's Park", 'venue_Subrata Roy Sahara Stadium',
              'venue_SuperSport Park', 'venue_Wankhede Stadium',
              'overs', 'runs', 'wickets', 'runs_last_5', 'wickets_last_5', 'total']]

# Splitting the data into train and test set
X_train = encoded_df.drop(labels='total', axis=1)[encoded_df['date'].dt.year <= 2016]
X_test = encoded_df.drop(labels='total', axis=1)[encoded_df['date'].dt.year >= 2017]

y_train = encoded_df[encoded_df['date'].dt.year <= 2016]['total'].values
y_test = encoded_df[encoded_df['date'].dt.year >= 2017]['total'].values

# Removing the 'date' column
X_train.drop(labels='date', axis=True, inplace=True)
X_test.drop(labels='date', axis=True, inplace=True)

# --- Model Building ---
# Linear Regression Model
from sklearn.linear_model import Lasso
# from sklearn.model_selection import GridSearchCV
lasso=Lasso()
lasso.fit(X_train,y_train)

# Creating a pickle file for the classifier
filename = 'first-innings-score-lr-model.pkl'
pickle.dump(lasso, open(filename, 'wb'))