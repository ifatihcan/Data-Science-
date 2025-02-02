# -*- coding: utf-8 -*-
"""Wine_Quality_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1woXT99Q3Dbd-bG3Zvaiyo_n7KpTXSC8H

In this assignment you will build models to predict quality of wines.  Please review the data dictionary and data provenance here:

https://archive.ics.uci.edu/ml/datasets/wine+quality

The target variable has been recoded as 1 (quality > 6) and 0 (quality < 7)

1. Load the data
2. Explore the distribution of the target variable
3. Assess if there are any missing values
4. Explore the information value and distribution of features using the pairplot
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
import seaborn as sns
from sklearn import tree

# Upload the Data

from google.colab import files
uploaded = files.upload()

import io
data = pd.read_csv(io.BytesIO(uploaded['whitewine-classification.csv']))

data.head()

#Disturbution of Target Variable
#Columm Named goodwine is the target
data.goodwine.hist()

#Checking Missing Values
sns.heatmap(data.isnull(), cbar=False)

#Check the disturbition by using pariplot
sns.pairplot(data, hue = 'goodwine')

data.describe()

data = data.drop(['free_sulfur_dioxide','residual_sugar'],axis=1)

data.info()

#Replacing missing values and redescribe the data
data['goodwine'].fillna(999, inplace=True)
data.describe()

"""5. Develop logistic regression, kNN (optimize k), random forest and boosted tree models to predict wine quality. Make sure to preprocess the data as needed by the respective models.

6. Assess the performance of each model using the following metrics: Recall, Precision, F1, ROC AUC.  Which is the best model based on ROC AUC?


"""

#Logistic Regression
data = pd.get_dummies(data, drop_first=True)
X = data.drop('goodwine', axis=1)
y = data['goodwine']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

logmodel = LogisticRegression(solver='liblinear')

logmodel.fit(X_train,y_train)

y_pred = logmodel.predict(X_test)

confusion_matrix(y_test,y_pred)

print(classification_report(y_test,y_pred))

logmodel.coef_

import statsmodels.api as sm

bool_cols = X_train.select_dtypes(include='bool').columns
for col in bool_cols:
  X_train[col]=X_train[col].astype(int)


logit_model=sm.Logit(y_train, X_train)
logmodel_2=logit_model.fit()
print(logmodel_2.summary2())

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

logit_roc_auc = roc_auc_score(y_test, logmodel.predict_proba(X_test)[:,1])
fpr, tpr, thresholds = roc_curve(y_test, logmodel.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

print('ROC AUC: ', roc_auc_score(y_test,y_pred))

#KNN Model
#Rescaling the Data
scaler = MinMaxScaler()
X = data.drop('goodwine', axis=1)
X_rescaled = scaler.fit_transform(X)
X_rescaled = pd.DataFrame(X_rescaled, columns=X.columns)

#Describe the Rescaled Data
X_rescaled.describe()

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))

print('ROC AUC: ', roc_auc_score(y_test,y_pred))

#Finding the Optimal K Value
max_K = 100
cv_scores = []

for K in range(1, max_K):
    knn = KNeighborsClassifier(n_neighbors=K)
    scores = cross_val_score(knn, X_train, y_train, cv=5, scoring="roc_auc")
    cv_scores.append(scores.mean())

sns.lineplot(x=range(1,max_K), y=cv_scores)

# The index of the Max ROC AUC value
optimal_k_index = np.argmax(cv_scores)

# Retrieving the optimal k value and also adding 1 because k ranges from 1 to 100 and not from 0 to 100
optimal_k = optimal_k_index + 1

# Retrieving the maximum ROC AUC value
max_roc_auc = cv_scores[optimal_k_index]


print('Optimal k for maximum ROC AUC:', optimal_k)
print('Maximum ROC AUC:', max_roc_auc)

# Optimized kNN model with k=11
knn = KNeighborsClassifier(n_neighbors=11, metric='euclidean')
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

kNN_roc_auc = roc_auc_score(y_test, knn.predict_proba(X_test)[:,1])
knn_fpr, knn_tpr, thresholds = roc_curve(y_test, knn.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='kNN Model (area = %0.2f)' % kNN_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

print('ROC AUC: ', roc_auc_score(y_test,y_pred))

#Random Forest
dt_model = tree.DecisionTreeClassifier(min_samples_leaf=5, max_depth=3)

dt_model.fit(X_train,y_train)

y_pred = dt_model.predict(X_test)

confusion_matrix(y_test,y_pred)

print(classification_report(y_test,y_pred))

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

dt_roc_auc = roc_auc_score(y_test, dt_model.predict_proba(X_test)[:,1])
fpr, tpr, thresholds = roc_curve(y_test, dt_model.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Decision Tree (area = %0.2f)' % dt_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

import graphviz
dot_data = tree.export_graphviz(dt_model, out_file=None,
                      feature_names=X.columns,
                      class_names=['Perished','Survived'],
                      filled=True, rounded=True,
                      special_characters=True)
graph = graphviz.Source(dot_data)
graph

from sklearn.ensemble import RandomForestClassifier

rf_model  = RandomForestClassifier(max_depth=5, random_state=0)
rf_model.fit(X_train,y_train)

y_pred_rf = rf_model.predict(X_test)

confusion_matrix(y_test,y_pred_rf)

print(classification_report(y_test,y_pred_rf))

#Boosted Tree Model
from sklearn.ensemble import AdaBoostClassifier

bt_model = AdaBoostClassifier(n_estimators=100)

bt_model.fit(X_train,y_train)

y_pred_bt = bt_model.predict(X_test)

confusion_matrix(y_test,y_pred_bt)

print(classification_report(y_test,y_pred_bt))

print('ROC AUC: ', roc_auc_score(y_test,y_pred))

#Combining the ROC AUC Curves
# Logistic Regression
logit_roc_auc = roc_auc_score(y_test, logmodel.predict_proba(X_test)[:,1])
fpr, tpr, thresholds = roc_curve(y_test, logmodel.predict_proba(X_test)[:,1])

# kNN Model
kNN_roc_auc = roc_auc_score(y_test, knn.predict_proba(X_test)[:,1])
knn_fpr, knn_tpr, thresholds = roc_curve(y_test, knn.predict_proba(X_test)[:,1])


# Random Forest
rf_roc_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:,1])
rf_fpr, rf_tpr, rf_thresholds = roc_curve(y_test, rf_model.predict_proba(X_test)[:,1])

# Boosted Tree Model
bt_roc_auc = roc_auc_score(y_test, bt_model.predict_proba(X_test)[:,1])
bt_fpr, bt_tpr, bt_thresholds = roc_curve(y_test, bt_model.predict_proba(X_test)[:,1])




plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot(knn_fpr, knn_tpr, label='KNN (area = %0.2f)' % kNN_roc_auc)
plt.plot(rf_fpr, rf_tpr, label='Random Forest (area = %0.2f)' % rf_roc_auc)
plt.plot(bt_fpr, bt_tpr, label='Boosted tree (area = %0.2f)' % bt_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

"""**Precision:** The Random Forest model achieves the highest precision for classifying wines as good quality, with a score of 0.68. This indicates that when Random Forest labels a wine as good, it is more likely to be correct compared to other models, making it the most reliable model in terms of avoiding false positives.

**Recall:** The Boosted Tree model stands out with the highest recall score for good quality wines, reaching 0.41. This implies that it successfully identifies a higher proportion of actual good quality wines, although it may produce more false positives compared to Random Forest. Thus, it is more effective at capturing true positives.

**F1-Score:** For the balance between precision and recall, the Boosted Tree model again performs the best, with an F1-score of 0.49 for good quality wines. This highlights its ability to maintain a reasonable trade-off, making it a strong candidate if the goal is to optimize both identification and correctness of classification.

**ROC AUC:** The Random Forest leads with an AUC of 0.84, indicating superior discriminative power across the entire range of classification thresholds. It is followed by the Boosted Tree (AUC = 0.82), Logistic Regression (AUC = 0.78), and k-Nearest Neighbors (kNN) (AUC = 0.76). A higher AUC value signifies that Random Forest is the most capable at distinguishing between good and bad quality wines overall.


The Random Forest model emerges as the top performer in terms of overall classification capability, excelling in both precision and ROC AUC. However, the Boosted Tree model is noteworthy for its superior recall and F1-score, suggesting that it might be a better fit if the goal is to identify a larger number of good quality wines, even at the cost of increased false positives.
"""

