#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# Define a list of file names
file_names = ['df_01.csv','df_02.csv', 'df_03.csv', 'df_04.csv', 'df_05.csv', 'df_06.csv', 'df_07.csv', 'df_09.csv']

# Create an empty dictionary to store accuracy scores
accuracy_scores = {}

# Define the mapping of weekdays to numerical values
weekday_mapping = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}

# Iterate over the file names
for file_name in file_names:
    # Load the dataset
    data = pd.read_csv(file_name)
    data = data.dropna(subset=['laf50_per_hour'])
    
    # Convert 'noisiness' column to numeric form
    data['noisiness'] = data['noisiness'].astype(int)
    
    # Map the 'weekday' column to numerical values
    data['weekday'] = data['weekday'].map(weekday_mapping)
    
    # Convert 'date' column to datetime if it's not already in datetime format
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    
    # Shift the 'date' column by one position to get the next date
    data['next_date'] = data['date'].shift(-1)
    
    # Define a condition to check if the next date is exactly 1 hour ahead
    condition = data['next_date'] == (data['date'] + pd.DateOffset(hours=1))
    
    # Select rows that satisfy the condition and drop the rest
    filtered_data = data[condition].copy()
    
    # Select X and Y based on the desired columns
    X = filtered_data.iloc[:, 4:11].copy()
    Y = filtered_data['noisiness'].shift(-1).copy()
    
    # Drop rows where Y is null
    nan_mask = Y.isnull()
    X = X[~nan_mask]
    Y = Y[~nan_mask]
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=19)
    
    # XGBoost
    xgb_model = XGBClassifier()
    xgb_model.fit(X_train, y_train)
    y_pred_xgb = xgb_model.predict(X_test)
    accuracy_xgb = accuracy_score(y_test, y_pred_xgb)
    
    # Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=19)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    accuracy_rf = accuracy_score(y_test, y_pred_rf)
    
    # Decision Tree Classifier
    dt_model = DecisionTreeClassifier(random_state=19)
    dt_model.fit(X_train, y_train)
    y_pred_dt = dt_model.predict(X_test)
    accuracy_dt = accuracy_score(y_test, y_pred_dt)
    
    # Store the accuracy scores in the dictionary
    accuracy_scores[file_name] = {
        'XGBoost Accuracy': accuracy_xgb,
        'Random Forest Accuracy': accuracy_rf,
        'Decision Tree Accuracy': accuracy_dt
    }

# Create a DataFrame from the accuracy_scores dictionary
accuracy_df = pd.DataFrame.from_dict(accuracy_scores, orient='index')

# Print the DataFrame
print(accuracy_df)

