# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# Load data
df = pd.read_csv('Churn_Modelling.csv') 

df['Churn'] = df['Exited']
df.drop(['Exited'], axis=1, inplace=True)


# Select all int64 columns except for the 'Churn' column
cols = df.select_dtypes(include=['int64']).columns[df.select_dtypes(include=['int64']).columns != 'Churn']
# Create a new DataFrame with the selected columns
X = np.asarray(df[cols])
# Display the first 5 rows of the new DataFrame
X[0:5]

y = np.asarray(df['Churn'])
y [0:5]


# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Logistic regression model
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)
print('Logistic Regression Accuracy:', accuracy_score(y_test, y_pred))

# Random forest model 
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
print('Random Forest Accuracy:', accuracy_score(y_test, y_pred))

# Gradient boosting model
gb = XGBClassifier()
gb.fit(X_train, y_train)  
y_pred = gb.predict(X_test)
print('Gradient Boosting Accuracy:', accuracy_score(y_test, y_pred))