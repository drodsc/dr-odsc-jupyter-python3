#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pylint: disable-all
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

import pickle
import pandas as pd
import numpy as np

PATH_TO_DATAFRAME = (
    '../Data/10k_diabetes_ODSC_Training.csv'
)

# Train/test split
df = pd.read_csv(PATH_TO_DATAFRAME)
y = df.pop('readmitted')
X_train, X_test, y_train, y_test = train_test_split(df, y)

numeric_features = list(X_train.select_dtypes(include=np.number).columns.values)
text_features = ['diag_1_desc', 'diag_2_desc', 'diag_3_desc']
categorical_features = list(set(X_train.columns) - set(numeric_features + text_features))


# Set up preprocessing steps for each type of feature
text_preprocessing = Pipeline([('TfIdf', TfidfVectorizer())])

categorical_preprocessing = Pipeline(
    [
        ('Imputation', SimpleImputer(strategy='constant', fill_value='?')),
        ('One Hot Encoding', OneHotEncoder(handle_unknown='ignore')),
    ]
)

numeric_preprocessing = Pipeline(
    [('Imputation', SimpleImputer(strategy='mean')), ('Scaling', StandardScaler())]
)


preprocessing = make_column_transformer(
    (numeric_features, numeric_preprocessing),
    (text_features[0], text_preprocessing),
    (text_features[1], text_preprocessing),
    (text_features[2], text_preprocessing),
    (categorical_features, categorical_preprocessing),
)

# Define a pipeline to search for the best combination of PCA truncation
# and classifier regularization.

pipeline = Pipeline( steps=
    [('Preprocessing', preprocessing), ('RF', RandomForestClassifier())]
)


# In[5]:


# Parameters of pipelines can be set using ‘__’ separated parameter names:
param_grid = [
        {#'RF__bootstrap': [False, True],
         'RF__n_estimators': [10],
         'RF__max_features': [0.6, 0.8],
         'RF__min_samples_leaf': [3, 5],
         'RF__min_samples_split': [3, 5]
        },
    ]

grid = GridSearchCV(pipeline, cv=5, n_jobs=1,param_grid=param_grid, iid=False,verbose=5)

grid.fit(X_train, y_train)

print("Best parameter (CV score=%0.3f):" % grid.best_score_)
print(grid.best_params_)


# In[35]:


from sklearn.externals import joblib
joblib.dump(grid.best_estimator_, '../Flask_App/python_model/custom_model.pickle')


# In[44]:


grid.cv_results_


# In[ ]:





# In[ ]:





# In[ ]:




