# -*- coding: utf-8 -*-
"""Churn_Predictor.ipynb

### Author - Dibyatanu Banik
"""

# Read the data
import pandas as pd
import numpy as np


url = 'https://raw.githubusercontent.com/Dibyatanu91/Customer-Churn-Telco-Dataset-/master/TelcoChurn.csv'

df = pd.read_csv(url)

# check the data
print(list(df))
print(df.shape)
df.head()

from google.colab import drive
drive.mount('/content/drive')

"""# **Basic Data Exploration**"""

# lets get familiar with the data

print("# of rows : " ,df.shape[0])
print("# of columns : " ,df.shape[1])
print("------------------------------")
print("# of missing values : \n", df.isnull().sum())
print("------------------------------")
print("Datatypes : \n", df.dtypes)
print("------------------------------")
print("unique values : \n", df.nunique())

# Unique values of certain columns
print("Columns                Values")
print("------------------------------")
print("Multiple lines:  ", df.MultipleLines.unique())
print("------------------------------")
print("InternetService: ", df.InternetService.unique())
print("------------------------------")
print("Contract:        ", df.Contract.unique())
print("------------------------------")
print("OnlineBackup:    ", df.OnlineBackup.unique())
print("------------------------------")
print("OnlineSecurity:  ", df.OnlineSecurity.unique())
print("------------------------------")
print("TechSupport:     ", df.TechSupport.unique())
print("------------------------------")
print("StreamingTV:     ", df.StreamingTV.unique())
print("------------------------------")
print("StreamingMovies: ", df.StreamingTV.unique())
print("------------------------------")
print("Contract:        ", df.Contract.unique())
print("------------------------------")
print("PaymentMethod:   ", df.PaymentMethod.unique())
print("------------------------------")

"""# **Data Preparation**"""

# replacing the gaps with null values in 'Total Charges' column (since it contains string)
df['TotalCharges'] = df["TotalCharges"].replace(" ",np.nan)

#convert 'Total Charges' from object to float type
df["TotalCharges"] = df["TotalCharges"].astype(float)

# cross checking null values in 'Total Charges'
df.isna().sum()

# removing the null values
df = df.dropna()

# Shape of dataset
print(df.shape)

#replacing the values of 'Senior Citizen' columns from 1,0 to Yes,No
df["SeniorCitizen"] = df["SeniorCitizen"].replace({1:"Yes",0:"No"})

#Separating churn and non churn customers
churn     = df[df["Churn"] == "Yes"]
not_churn = df[df["Churn"] == "No"]


df['tenure(yr)'] = ['0-1 Years' if x <=12   
                                  else 
                                  '1-2 Years' if x>12 and x<=24
                                  else 
                                  '2-3 Years' if x>24 and x<=36
                                  else 
                                  '3-4 Years' if x>36 and x<=48
                                  else 
                                  '4-5 Years' if x>48 and x<=60
                                  else 'more than 5' 
                                  for x in df['tenure']]

# check the data
print(df.dtypes)
df.head()

"""# **Exploratory Data Analysis and Visualizations**"""

#Remove comment to install plotly in the first run
#!pip install plotly==4.6.0

#Plot the target variable to check the number of churned customers compared to those who did not churn
ax = sns.catplot(y="Churn", kind="count", data=df, height=2.6, aspect=2.5, orient='h')

"""It can be seen that the target is imbalanced, and our desired outcome (Churn=1) is a rare event.

Function to create Pie Chart
"""

# import plotly graph objects
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# define function to create Pie chart
def pie(labels1,values1,labels2,values2,title,titleText):
    fig = make_subplots(1, 2, specs=[[{'type':'domain'},{'type':'domain'}]],
                        subplot_titles=title)
    fig.add_trace(go.Pie(labels=labels1, values=values1, scalegroup='one',
                        name="pie chart 1"), 1, 1)
    fig.add_trace(go.Pie(labels=labels2, values=values2, scalegroup='one',
                        name="pie chart 2"), 1, 2)


    fig.update_layout(title_text=titleText)
    fig.show()

#labels and values for Gender Distribution
labels1 = churn["gender"].value_counts().keys().tolist()
values1 = churn["gender"].value_counts().values.tolist()

labels2 = not_churn["gender"].value_counts().keys().tolist()
values2 = not_churn["gender"].value_counts().values.tolist()

title1 = ['Gender Dist. in Churned partition', 'Gender Dist. in non-Churned partition']
titleText1 = 'Gender Distribution'

#labels for Senior Citizen
labels3 = churn["SeniorCitizen"].value_counts().keys().tolist()
values3 = churn["SeniorCitizen"].value_counts().values.tolist()

labels4 = not_churn["SeniorCitizen"].value_counts().keys().tolist()
values4 = not_churn["SeniorCitizen"].value_counts().values.tolist()

title2 = ['Senior Citizen in Churned partition', 'Senior Citizen in non-Churned partition']
titleText2 = 'Senior Citizen Distribution'

churn.head(2)

"""Function to create Kernel Density Plot"""

# define duntion for KDE plot
def kdeplot(feature):
    plt.figure(figsize=(15, 4))
    plt.title("KDE for {}".format(feature))
    ax0 = sns.distplot(df[df['Churn'] == 'No'][feature].dropna(), color= 'navy', label= 'Churn: No')
    ax1 = sns.distplot(df[df['Churn'] == 'Yes'][feature].dropna(), color= 'orange', label= 'Churn: Yes')
    ax1.set_xlabel("---------------------------------------V a l u e s---------------------------->")
    ax1.set_ylabel("----Probability Density----->")

"""Barplot Function"""

# function to plot bar chart based on percentage of data
def barplot_percentages(feature, orient='v', axis_name="percentage of customers"):
    ratios = pd.DataFrame()

    g = df.groupby(feature)["Churn"].value_counts().to_frame()
    g = g.rename({"Churn": axis_name}, axis=1).reset_index()
    g[axis_name] = g[axis_name]/len(df)


    if orient == 'v':
        ax = sns.barplot(x=feature, y= axis_name, hue='Churn', data=g, orient=orient)
        ax.set_yticklabels(['{:,.0%}'.format(y) for y in ax.get_yticks()])
    else:
        ax = sns.barplot(x= axis_name, y=feature, hue='Churn', data=g, orient=orient)
        ax.set_xticklabels(['{:,.0%}'.format(x) for x in ax.get_xticks()])
    ax.plot()


# table by grouping on categorical tenure and target 
avg_tgc = df.groupby(["tenure(yr)","Churn"])[["MonthlyCharges",
                                                    "TotalCharges"]].mean().reset_index()

#function for tracing 
def mean_charges(column,aggregate) :
    tracer = go.Bar(x = avg_tgc[avg_tgc["Churn"] == aggregate]["tenure(yr)"],
                    y = avg_tgc[avg_tgc["Churn"] == aggregate][column],
                    name = aggregate,marker = dict(line = dict(width = 1)),
                    text = "Churn"
                   )
    return tracer


#function for layout
def layout_plot(title,xaxis_lab,yaxis_lab) :
    layout = go.Layout(dict(title = title,
                            plot_bgcolor  = "rgb(243,243,243)",
                            paper_bgcolor = "rgb(243,243,243)",
                            xaxis = dict(gridcolor = 'rgb(255, 255, 255)',title = xaxis_lab,
                                         zerolinewidth=1,ticklen=5,gridwidth=2),
                            yaxis = dict(gridcolor = 'rgb(255, 255, 255)',title = yaxis_lab,
                                         zerolinewidth=1,ticklen=5,gridwidth=2),
                           )
                      )
    return layout
    

#plot1 - mean monthly charges by tenure 
trace1  = mean_charges("MonthlyCharges","Yes")
trace2  = mean_charges("MonthlyCharges","No")
layout1 = layout_plot("Average Monthly Charges by Tenure",
                      "Tenure","Monthly Charges")
data1   = [trace1,trace2]
fig1    = go.Figure(data=data1,layout=layout1)

#plot2 - mean total charges by tenure 
trace3  = mean_charges("TotalCharges","Yes")
trace4  = mean_charges("TotalCharges","No")
layout2 = layout_plot("Average Total Charges by Tenure",
                      "Tenure","Total Charges")
data2   = [trace3,trace4]
fig2    = go.Figure(data=data2,layout=layout2)

"""### Pie Charts"""

# Pie chart for Gender distribution with respect to target
pie(labels1,values1,labels2,values2,title1,titleText1)

"""Here it is quite clear that the gender distribution in Churned and non-churned customers is almost equal. Thus, gender might not be a very good predictor for churn."""

# Pie chart for Senior Citizen distribution with respect to target
pie(labels3,values3,labels4,values4,title2,titleText2)

"""On the other hand, I do see a difference of almost 50% in the amount of senior citizens in Churned and non-churned partitions. This variable might turn out to be an important feature for prediction.

### Kernel Density plots of Continuous predictors
"""


kdeplot('tenure')
kdeplot('MonthlyCharges')
kdeplot('TotalCharges')

"""Looking at the KDE plots, I can say that:
* Recent clients are more likely to churn
* Clients with higher MonthlyCharges are also more likely to churn
* Tenure and MonthlyCharges are probably important features

### Bar Plots
"""

# Bar chart for payment method with respect to target
plt.figure(figsize=(9, 4.5))
barplot_percentages("PaymentMethod", orient='h')

"""In the bar chart above, it can be seen that where the method of payment is Electronic Cheque, the percentage of customers churning is very high with respect to those not churning. Thus this seems to be an important predictor."""

import plotly.io as pio
# Bar chart for Tenure vs. Monthly charges with respect to target
pio.show(fig1)
# Bar chart for Tenure vs. average total charges with respect to target
pio.show(fig2)

"""Looking at both the visualizations above, it can be seen that for an increase in tenure, the monthly charges and total charges increase in almost a linear fashion, and the number of customers churning too increases along with tenure. Also, the increase seems to be gradual for an increase in monthly charges, but quite steep for an increase in total charges.

### Correlation Matrix for continuous predictors
"""

# create a correlation matrix for numeric variables in the data
correlation_matrix = df.corr().round(2)
#correlation_matrix
# specify dimensions of plot
sns.set(rc={'figure.figsize':(5,4)})

# create a heatmap to increase interpretability
sns.heatmap(data=correlation_matrix, annot=True)
plt.show()

"""### Scatter plot matrix for continuous predictors"""

# Scatterplot Matrix

sns.pairplot(df[list(df)], height=2.2)

"""Both the Scatterplot Matrix and the Correlation Matrix show that Total charges is highly correlated to tenure, and has quite a bit correlation to the monthly charges. Thus, it might be possible that using total charges along with the other two columns might result in redundancy."""


#df.describe(include='all')
df.describe()

"""### EDA plots for Categorical Predictors"""

# plot and check the variables gender, senior citizen, partner and dependents
cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']

fig = plt.figure(figsize = (15,16))
sns.set(style="whitegrid", palette="deep", color_codes=True)

# for loop to plot the charts for all four variables
for col,i in zip(cols, range(1,len(cols)*4,3)):
  a = fig.add_subplot(4,3,i)
  sns.countplot(data = df, x = col, ax=a)     # count plot
  a = fig.add_subplot(4,3,i+1)
  sns.boxplot(data = df, x = col, y = 'MonthlyCharges' , ax=a)    # boxplot
  a = fig.add_subplot(4,3,i+2)
  sns.violinplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn' , ax=a)      # violin plot
  sns.swarmplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn', alpha = 0.6, ax=a)   # swarmplot
  
fig.tight_layout()

#plt.show()

"""For the senior citizen variable, it can be seen that the monthly charges have an effect on the customer churn."""

# plot and check variables phone service, multiple lines, internet service, online security
cols = ['PhoneService', 'MultipleLines', 'InternetService',
       'OnlineSecurity']

fig = plt.figure(figsize = (15,16))
sns.set(style="whitegrid", palette="deep", color_codes=True)

# for loop to plot the same set of plots for all four variables
for col,i in zip(cols, range(1,len(cols)*4,3)):
  a = fig.add_subplot(4,3,i)
  sns.countplot(data = df, x = col, ax=a)   # count plot
  a = fig.add_subplot(4,3,i+1)
  sns.boxplot(data = df, x = col, y = 'MonthlyCharges' , ax=a)    # boxplot
  a = fig.add_subplot(4,3,i+2)
  sns.violinplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn' , ax=a)    #violin plot
  sns.swarmplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn', alpha = 0.6, ax=a)   #swarm plot
  
fig.tight_layout()

#plt.show()

"""Phone Service, Multiple Lines and Internet service seem to have an impact on the churn based on the monthly charges."""

# plot and check variables online backup, device protection, tech support and streaming tv
cols = ['OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV']

fig = plt.figure(figsize = (15,16))
sns.set(style="whitegrid", palette="deep", color_codes=True)

# for loop to plot the same set of plots for all four variables
for col,i in zip(cols, range(1,len(cols)*4,3)):
  a = fig.add_subplot(4,3,i)
  sns.countplot(data = df, x = col, ax=a)   # count plot
  a = fig.add_subplot(4,3,i+1)
  sns.boxplot(data = df, x = col, y = 'MonthlyCharges' , ax=a)  # boxplot
  a = fig.add_subplot(4,3,i+2)
  sns.violinplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn' , ax=a)    #violin plot
  sns.swarmplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn', alpha = 0.6, ax=a)   # swarm plot
  
fig.tight_layout()

#plt.show()

"""Streaming TV seems to be a useful variable, looking at its violin plot."""

# plot and check variables streaming movies, contract, paperless billing, payment method
cols = ['StreamingMovies', 'Contract', 'PaperlessBilling',
       'PaymentMethod']

fig = plt.figure(figsize = (15,16))
sns.set(style="whitegrid", palette="deep", color_codes=True)

# for loop to plot the same set of plots for all four variables
for col,i in zip(cols, range(1,len(cols)*4,3)):
  a = fig.add_subplot(4,3,i)
  sns.countplot(data = df, x = col, ax=a)   # count plot
  a = fig.add_subplot(4,3,i+1)
  sns.boxplot(data = df, x = col, y = 'MonthlyCharges' , ax=a)    # boxplot
  a = fig.add_subplot(4,3,i+2)
  sns.violinplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn' , ax=a)    # violin plot
  sns.swarmplot(data = df, x = col, y = 'MonthlyCharges', hue='Churn', alpha = 0.6, ax=a)   # swarm plot
  
fig.tight_layout()

#plt.show()

"""Contract and Paperless billing can be seen to have an effect on the churn according to the variation in their monthly charges.

### Tables
"""

# subset the data to Churn = Yes to focus only on the churned customers
dft = df[df['Churn']=='Yes']

# check the subsetted data
print(dft.Churn.unique())
print(dft.shape)
dft.head()

# table displaying number of churned customers based on their tenure and contract type
pd.crosstab(dft['tenure(yr)'], dft['Contract'], values=dft['Churn'], aggfunc='count').dropna()

"""It can be seen that most of the churn happens when the contract is month-to-month for a tenure of 2-3 years. This logically also seems convincing, based on the fact that such an arrangement will make it easier for customers to quit availing the service."""

# table displaying number of churned customers based on whether they have any partner or dependents
pd.crosstab(dft['Partner'], dft['Dependents'], values=dft['Churn'], aggfunc='count')

"""Customers that do not have an partner or dependents seem to be contributing most of the churn."""

# Aggregating number of churned customers based on whether they stream tv or movies
dft.groupby(['StreamingTV', 'StreamingMovies']).agg({'Churn':'count'})

"""Looking at the table above, it can be seen that customers that either stream both movies and tv, or stream none appear to be churning the most."""

# Aggregating number of churned customers based on the combination of connections they have
dft.groupby(['PhoneService', 'InternetService', 'MultipleLines']).agg({'Churn':'count'})

"""Here it can be said that the customers having Fiber Optic internet service seem to be churning the most, irrespective of what kind of line they get."""

# Aggregating number of churned customers, based on the combinations of services the avail
dft.groupby(['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport']).agg({'Churn':'count'})

"""With respect to the service offered by Telecom, most of the churn is happening in customers that do not get any online backup, online security, device protection and tech support.

## **Feature engineering**
"""

# original data
df

# reset index to maintain consistency throughout the rest of the notebook
df = df.reset_index().iloc[:,1:]
df

"""### Seperating the categorical and continuous data"""

# seperate numerical and categorical variables
print(df.shape)
print(df.head())
dfn = df[['tenure',	'MonthlyCharges',	'TotalCharges']]     # dataframe for numerical predictors (continuous data)
print(dfn.shape)

cat_vars = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',       # categorical predictors
        'PhoneService', 'MultipleLines', 'InternetService',
       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
       'PaymentMethod']
dfc = df[cat_vars]    # dataframe for categorical predictors
print(dfc.shape)

# to create dummy variables
for var in cat_vars:
  catList = 'var'+'_'+var
  catList = pd.get_dummies(dfc[var], drop_first=True, prefix=var)
  dfc = dfc.join(catList)
  #data = data1

print(dfc.columns)
print(dfc.shape)

# drop original categorical variables and keep only dummies
data_vars = dfc.columns.values.tolist()
to_keep = [i for i in data_vars if i not in cat_vars]
dfc=dfc[to_keep]

# check data
print(dfc.shape)
print(dfc.columns)
dfc.head()

# this part of the code is to store numeric and continuous data (original) in a separate df for SMOTE analysis
# without poly/log feature
df_SMOTE = dfn.join(dfc)
df_SMOTE = df_SMOTE.join(df['Churn'])
df_SMOTE["Churn"] = df_SMOTE["Churn"].replace({"Yes":1,"No":0})
print(df_SMOTE.shape)

"""### Polynomial features"""

# original numerical data
print("Original Data")
print(dfn.shape)
print(dfn.head()) 

# create interaction terms for numerical variables
from sklearn.preprocessing import PolynomialFeatures

poly_features = PolynomialFeatures(degree=2)
dfn_poly = poly_features.fit_transform(dfn)
names = poly_features.get_feature_names(dfn.columns)
tmp1 = pd.DataFrame(dfn_poly, columns=names)
tmp1 = tmp1.iloc[:,1:]

# check data
print("##########################")
print("Poly Features")
print(tmp1.shape)
tmp1.head()

"""### Log features"""

print(dfn.head())
print(dfn.dtypes)
# creating log variables of original numerical columns
dfn_log = np.log(dfn)
tmp2 = pd.DataFrame(dfn_log)
tmp2.columns=['log_tenure', 'log_Monthlycharges', 'log_TotalCharges']
print(tmp2.shape) # same number of columns with changed values
tmp2.head()

# join the original data and polynomial features with the log features
dfn = tmp1.join(tmp2)

# check the data
print(dfn.shape)
dfn.head()

dfn

"""### **Standardization using min-max technique**"""

# standardize numerical variables and their interaction terms using min-max standardization
from sklearn import preprocessing

colnames = dfn.columns    # to retain column names of original data
print(dfn.shape)
# return dataframe values as numpy array
x = dfn.values
x
# lets take this array of raw numbers and do minmax standardization using built in function
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
#x_scaled
# convert scaled array into pandas dataframe with column names
dfn = pd.DataFrame(x_scaled, columns=colnames)

# check the standardized data
print(dfn.shape)
dfn.head()

# use describe to check range of variables
dfn.describe()

"""### Creating categorical interaction terms"""

n = len(list(dfc)) # number of categorical variables

# create interaction terms for categorical variables
for i in range(0,n-1):
  for j in range(i+1,n):
    col = str(list(dfc)[i]+'_'+list(dfc)[j])    # naming the new column
    #print(col)
    dfc[col] = dfc[list(dfc)[i]]*dfc[list(dfc)[j]]    # interaction term

# check the data
print(dfc.columns)
print(dfc.shape)
dfc.head()

# save the target in an array
target = df['Churn']
target.shape

# check target for nulls
target.isna().sum()

"""### Smoosh the data together"""

# combine the new features and the target together to get a single dataset
df = dfn.join(dfc)
df = df.join(target)

# check the data
print(df.columns)
print(df.shape)
df.head()

# check the target for null values
print(df["Churn"].isna().sum())
# convert the target into int, change the values from Yes/No to 1/0
df["Churn"] = df["Churn"].replace({"Yes":1,"No":0}) # Changing the value of Target variable to 0 and 1
# check the target
print(df["Churn"].isna().sum())
print(df['Churn'].unique())
print(df['Churn'].dtype)

"""# **Modeling**"""

# remove warning
import warnings
warnings.filterwarnings("ignore")

"""### Baseline Model"""

# create a dataframe to store results
model_results = pd.DataFrame([])

# removing any possible null values
df = df.dropna()

# Split out into predictors and target data
X = df.iloc[:, df.columns != 'Churn']
y = df.iloc[:, df.columns == 'Churn']
print("X shape: ", X.shape)
print("y shape: ", y.shape)
print("---------------------------------------")
print("Target Value Distribution: ")
y['Churn'].value_counts()

# import packages for modeling
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
from sklearn.metrics import roc_auc_score,roc_curve,scorer
from sklearn.metrics import f1_score
import statsmodels.api as sm
from sklearn.metrics import precision_score,recall_score

# Splitting the data into train and validation partition
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =.3, random_state = 420, stratify = y )

# Generate a baseline model using Logistic Regression
Baseline =LogisticRegression(C=1.0, class_Iight=None, dual=False, fit_intercept=True, # C set to 1 which works as inverse of regularization strength
          intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
          penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
          verbose=0, warm_start=False)

# fit the model and check the performance
Baseline.fit(X_train, y_train)
train_pred = Baseline.predict(X_train)
test_pred   = Baseline.predict(X_test)

# function to check the model accuracy
def Accuracy_Information(y_training, X_training, y_testing, X_testing, train_pred, test_pred):
    print("Accuracy:\n", accuracy_score(y_testing, test_pred))  # accuracy for predictions on test data
    print("\nConfusion Matrix for Training data:\n", confusion_matrix(y_training, train_pred))      # confusion matrix for training data
    print("\nConfusion Matrix for Test Data:\n", confusion_matrix(y_testing, test_pred))      # confusion matrix for test data
    print("\nClassification Report:\n", classification_report(y_testing, test_pred))

# Check Accuracy of baseline model
Accuracy_Information(y_train,X_train,y_test,X_test,train_pred,test_pred )

# save model results into the result table
c = classification_report(y_test, test_pred, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Baseline Model (Logistic Regression)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

#import necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import BaggingClassifier

"""### Spotcheck Algorithm"""

# spotcheck Algorithm

models =[] # define a list
models.append(('LR',LogisticRegression()))
models.append(('GBC',GradientBoostingClassifier()))
models.append(('DTC',DecisionTreeClassifier()))
models.append(('RFC',RandomForestClassifier()))
models.append(('LDA',LinearDiscriminantAnalysis()))
models.append(('KNC',KNeighborsClassifier()))
models.append(('GNB',GaussianNB()))
models.append(('ETC',ExtraTreesClassifier()))
models.append(('BC',BaggingClassifier()))

# Splitting the data
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =.3, random_state = 420, stratify = y )

# Evaluate each model
result = []
names = []
for name, model in models:
    kfold = KFold(n_splits=20, random_state= 420, shuffle=True) # define k-fold validation
    cv_result = cross_val_score(model, X_train, y_train, cv = kfold, scoring='accuracy')    # use k-fold validation
    result.append(cv_result)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_result.mean(), cv_result.std())
    print(msg)

from matplotlib import pyplot

# Compare Algorithms
fig = pyplot.figure(figsize=(7,7))
fig.suptitle('Scaled Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(result)
ax.set_xticklabels(names)
pyplot.show()

"""Looking at the results of spot check algorithm, Gradient Boosting Classifier turns out to be the best model.

Tuning hyperparameters for Gradient Boosting Classifier:
"""

## ----------- Best Estimator ----------------
# Grid Search(hyper tuning for Gradient Boost Classifier)
from sklearn.model_selection import GridSearchCV

# parameter
grid_param = {'n_estimators':range(20,200,10)}

# Construct a grid search
gs_GradBoost = GridSearchCV(estimator =GradientBoostingClassifier( min_samples_split=2, 
                                                                  min_samples_leaf=1, 
                                                                  subsample=1,
                                                                  max_features='sqrt', 
                                                                  random_state=10), 
            param_grid = grid_param , scoring='accuracy',n_jobs=4,iid=False, cv=5)

# fit using grid search
gs_GradBoost.fit(X_train, y_train)

print("Best scoring(r^2): %.3f" %gs_GradBoost.best_score_)

# Best params
print('\nBest params:\n', gs_GradBoost.best_params_)

# Grid Search(hyper tuning for Gradient Boost Classifier)
from sklearn.model_selection import GridSearchCV

# parameter
grid_param = {'max_depth':range(5,10,2), 'min_samples_split':range(400,800,200)}

# Construct a grid search
gs_GradBoost = GridSearchCV(estimator =GradientBoostingClassifier( min_samples_leaf=1, 
                                                                  subsample=1,
                                                                  random_state=10), 
            param_grid = grid_param, scoring='accuracy',n_jobs=4,iid=False, cv=5)

# fit using grid search
gs_GradBoost.fit(X_train, y_train)

print("Best scoring(r^2): %.3f" %gs_GradBoost.best_score_)

# Best params
print('\nBest params:\n', gs_GradBoost.best_params_)

"""### Gradient Boosting Classifier (with tuned hyperparameters)"""

# fitting the model with all the best prameters from hyper tuning
model1 = GradientBoostingClassifier(n_estimators=110, max_depth= 5, subsample=1,min_samples_split= 600, max_features =19, random_state=10)
model1.fit(X_train,y_train)
predictions_train = model1.predict(X_train) # predicting the hold out data sample
predictions = model1.predict(X_test) # predicting the hold out data sample

# Check accuracy
print('Accuracy of the GBC on test set: {:.3f}'.format(accuracy_score(y_test, predictions)))

# Performance og GBC after hyperparameter tuning
Accuracy_Information(y_train,X_train,y_test,X_test,predictions_train,predictions)

# save the performance results
c = classification_report(y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Gradient Boosting Classifier (with tuned hyperparameters)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""Checking Feature Importance for the Gradient Boosting Classifier:"""

# check feature importance 
from sklearn.inspection import permutation_importance
sns.set(rc={'figure.figsize':(12,100)})

# perform permutation importance
results = permutation_importance(model1, X, y, scoring='accuracy')
# get importance
importance = results.importances_mean
sorted_idx = np.argsort(importance)
pos = np.arange(sorted_idx.shape[0]) + .5
# plot importance graph
plt.barh(pos, importance[sorted_idx], align='center')
plt.yticks(pos, X.columns[sorted_idx])
plt.xlabel('Permutation Feature Importance Scores')
plt.title('Permutation Feature Importance for GBC')
plt.show()

# save the top 60 best features
x_imp = X.columns[sorted_idx[-61:]] #60 variables

"""### Gradient Boosting Classifier with tuned parameters and 60 most important features"""

# fitting the model with all the best prameters from hyper tuning and the most important features
model2 = GradientBoostingClassifier(n_estimators=110, max_depth= 5, subsample=1,min_samples_split= 600, max_features =19, random_state=10)
model2.fit(X_train[x_imp],y_train)
predictions_train_gbc = model2.predict(X_train[x_imp]) # predicting the hold out data sample
predictions_gbc = model2.predict(X_test[x_imp]) # predicting the hold out data sample

# check accuracy
print('Accuracy of the GBC on test set: {:.3f}'.format(accuracy_score(y_test, predictions_gbc)))

# print performance results
Accuracy_Information(y_train,X_train[x_imp],y_test,X_test[x_imp],predictions_train_gbc,predictions_gbc)

# save model performance results
c = classification_report(y_test, predictions_gbc, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Gradient Boosting Classifier (with tuned parameters and important features)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""### Neural Network"""

# data for neural network
dfnn = df.copy()

from sklearn.preprocessing import MinMaxScaler
# Split out validation data set
X_nn = dfnn.iloc[:, dfnn.columns != 'Churn']
y_nn = dfnn.iloc[:, dfnn.columns == 'Churn']

# Splitting data
X_train_nn, X_test_nn, y_train_nn, y_test_nn = train_test_split(X_nn, y_nn, test_size=0.3, stratify =y, random_state=0)

# check target
y_train_nn['Churn'].value_counts()

from tensorflow.keras import layers, Sequential

# set up the model
model = Sequential()
model.add(layers.Dense(64, activation='relu',input_shape=(X_train_nn.shape[1],)))
model.add(layers.Dropout(0.2))
# hidden layer 1
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.2))
# output layer
model.add(layers.Dense(1, activation ='sigmoid'))

# compile the model
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# check target datatype
y_train_nn.dtypes

# early stopping
from tensorflow.keras.callbacks import EarlyStopping

es = EarlyStopping(monitor='val_loss', 
                   mode='min',
                   patience=50, 
                   verbose=1)

# run the model
nmodel = model.fit(X_train_nn, y_train_nn,  # train data
          validation_data=(X_test_nn, y_test_nn), # test data
          epochs=5000,    # specify epochs
          batch_size=50,    # specify batch size
          verbose=0,
          callbacks=[es])   # include early stopping

# predict target using the model
train_pred = model.predict(X_train_nn)
test_pred = model.predict(X_test_nn)

# check preds
test_pred

# plot the training and validation accuracy by epochs
sns.set(rc={'figure.figsize':(6,6)})

model_dict = nmodel.history
loss_values = model_dict['loss'] 
val_loss_values = model_dict['val_loss'] 
epochs = range(1, len(loss_values) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'orange', label='Test loss')
plt.title('Training and Test loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# put the predictions side by side
myPreds = pd.DataFrame(train_pred)
# drop the index
myPreds.reset_index(drop=True)
myPreds.rename(columns={0: "TrainPreds"}, inplace=True)
myPreds.dtypes
myPreds.head()

# dataframe for test preds
myPreds2 = pd.DataFrame(test_pred)
myPreds2.reset_index(drop=True)
myPreds2.rename(columns={0: "TestPreds"}, inplace=True)
myPreds2.dtypes
myPreds2.head()

# actual train target
myActual = pd.DataFrame(np.array(y_train_nn))
myActual.reset_index(drop=True)
myActual.rename(columns={0: "TrainActual"}, inplace=True)
myActual.dtypes
myActual.head()

# actual test target
myActual2 = pd.DataFrame(np.array(y_test_nn))
myActual2.reset_index(drop=True)
myActual2.rename(columns={0: "TestActual"}, inplace=True)
myActual2.dtypes
myActual2.head()

# put the train target and predictions together
myTrain = pd.concat([myActual, myPreds], axis=1)
len(myTrain)

# put the test target and predictions together
myTest = pd.concat([myActual2, myPreds2], axis=1)
len(myTest)

# check performance of the model
Accuracy_Information(y_train_nn,X_train_nn,y_test_nn, X_test_nn, round(myTrain.TrainPreds), round(myTest.TestPreds))

# save model results
c = classification_report(y_test_nn, round(myTest.TestPreds), output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Neural Network', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""### Synthetic Minority Oversampling Technique (SMOTE) -- *With Polynomial and log features*"""

from imblearn.over_sampling import SMOTE

# Split out data set
smote_X = df.iloc[:, df.columns != 'Churn']
smote_y = df.iloc[:, df.columns == 'Churn']

#Split train and test data
smote_X_train,smote_X_test,smote_y_train,smote_y_test = train_test_split(smote_X,smote_y,
                                                                         test_size = .3 ,
                                                                         random_state = 420)

#oversampling minority class(Churn = 1) using smote
os = SMOTE(random_state = 0)
os_smote_X,os_smote_y = os.fit_sample(smote_X_train,smote_y_train) # This is where the training data is fed with synthesized data
os_smote_X = pd.DataFrame(data = os_smote_X)
os_smote_y = pd.DataFrame(data = os_smote_y)
os_smote_y =os_smote_y.rename(columns= { 0 : 'Churn'})

# check the partitions
print("--------B E F O R E     S M O T E-----------------")
print(y_train['Churn'].value_counts())

print("--------A F T E R     S M O T E-----------------")
print(os_smote_y['Churn'].value_counts())

"""#### Gradient Boosting Classifier (SMOTE)"""

# training the model with smote variables

Smote_model = GradientBoostingClassifier(n_estimators=110, max_depth= 5, subsample=1,min_samples_split= 600, max_features =19, random_state=10)
Smote_model.fit(os_smote_X,os_smote_y)
predictions_train = Smote_model.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_model.predict(smote_X_test) # predicting the hold out data sample

# check model performance
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model performance metrics
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Gradient Boosting Classifier (SMOTE)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""In spot check modeling, Linear Regression, RFC and LDA also provided good accuracy:

* Linear Regression = .7934
* Random Forest Classifier = .7928
* Linear Discrimminant A   = .7934

So I tried fitting those models with SMOTE values.

#### Logistic Regression (SMOTE)
"""

# Fit Logistic regression
Smote_modelLR = LogisticRegression(penalty='l2')
Smote_modelLR.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelLR.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelLR.predict(smote_X_test) # predicting the hold out data sample

# check model accuracy
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model performance metrics
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Logistic Regression (SMOTE)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Random Forest Classifier (SMOTE)"""

# Random forest classifier model using smote partitions
Smote_modelRFC = RandomForestClassifier()
Smote_modelRFC.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelRFC.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelRFC.predict(smote_X_test) # predicting the hold out data sample

# print accuracy metrics
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model performance
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Random Forest Classifier (SMOTE)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Linear Discriminant Analysis (SMOTE)"""

# Performing Linear Discriminant Analysis using smote partitions
Smote_modelLDA = LinearDiscriminantAnalysis()
Smote_modelLDA.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelLDA.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelLDA.predict(smote_X_test) # predicting the hold out data sample

# print performance
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model results
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Linear Discriminant Analysis (SMOTE)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Confusion metrices for SMOTE models -- *With Polynomial and log features*"""

import itertools
# list of models
lst    = [Smote_model,Smote_modelLR, Smote_modelLDA, Smote_modelRFC]

length = len(lst)
# names of model algorithms
mods   = ['Gradient Boosting Classifier(SMOTE)', 'Logistic Regression(SMOTE)' , 'Linear Discriminant Analysis(SMOTE)', 'Random Forest Classifier(SMOTE)']

fig = plt.figure(figsize=(13,15))
fig.set_facecolor("White")
# plot confusion metrices heat maps
for i,j,k in itertools.zip_longest(lst,range(length),mods) :
    plt.subplot(4,3,j+1)
    predictions = i.predict(smote_X_test)
    conf_matrix = confusion_matrix(predictions,smote_y_test)
    sns.heatmap(conf_matrix,annot=True,fmt = "d",square = True,
                xticklabels=["not churn","churn"],
                yticklabels=["not churn","churn"],
                linewidths = 2,linecolor = "w",cmap = "Set1")
    plt.title(k,color = "Black")
    plt.subplots_adjust(wspace = .3,hspace = .3)

"""#### ROC Curves for SMOTE models -- *With Polynomial and log features*"""

# list of models
lst    = [Smote_model,Smote_modelLR, Smote_modelLDA, Smote_modelRFC]

length = len(lst)
# names of model algorithms
mods   = ['Gradient Boosting Classifier(SMOTE)', 'Logistic Regression(SMOTE)' , 'Linear Discriminant Analysis(SMOTE)', 'Random Forest Classifier(SMOTE)']

plt.style.use("dark_background")
fig = plt.figure(figsize=(12,16))
fig.set_facecolor("#F3F3F3")

# plot ROC curves for all models
for i,j,k in itertools.zip_longest(lst,range(length),mods) :
    qx = plt.subplot(4,3,j+1)
    probabilities = i.predict_proba(smote_X_test)
    predictions   = i.predict(smote_X_test)
    fpr,tpr,thresholds = roc_curve(smote_y_test,probabilities[:,1])
    plt.plot(fpr,tpr,linestyle = "dotted",
             color = "royalblue",linewidth = 2,
             label = "AUC = " + str(np.around(roc_auc_score(smote_y_test,predictions),3)))
    plt.plot([0,1],[0,1],linestyle = "dashed",
             color = "orangered",linewidth = 1.5)
    plt.fill_betIen(fpr,tpr,alpha = .4)
    plt.fill_betIen([0,1],[0,1],color = "k")
    plt.legend(loc = "loIr right",
               prop = {"size" : 12})
    qx.set_facecolor("k")
    plt.grid(True,alpha = .15)
    plt.title(k,color = "black")
    plt.xticks(np.arange(0,1,.3))
    plt.yticks(np.arange(0,1,.3))

"""Looking at the Confusion metrices and ROC curves, Linear Discriminant Analysis appears to be performing the best among the above models.

### Synthetic Minority Oversampling Technique (SMOTE) -- *Without Polynomial and log features*
"""

# check the data once
df_SMOTE.shape

from imblearn.over_sampling import SMOTE

# Split out data set
smote_X = df_SMOTE.iloc[:, df_SMOTE.columns != 'Churn']
smote_y = df_SMOTE.iloc[:, df_SMOTE.columns == 'Churn']

#Split train and test data
smote_X_train,smote_X_test,smote_y_train,smote_y_test = train_test_split(smote_X,smote_y,
                                                                         test_size = .3 ,
                                                                         random_state = 420)

#oversampling minority class(Churn = 1) using smote
os = SMOTE(random_state = 0)
os_smote_X,os_smote_y = os.fit_sample(smote_X_train,smote_y_train) # This is where the training data is fed with synthesized data
os_smote_X = pd.DataFrame(data = os_smote_X)
os_smote_y = pd.DataFrame(data = os_smote_y)
os_smote_y =os_smote_y.rename(columns= { 0 : 'Churn'})

# check shape of partitions before and after smote
print("--------B E F O R E     S M O T E-----------------")
print(y_train['Churn'].value_counts())

print("--------A F T E R     S M O T E-----------------")
print(os_smote_y['Churn'].value_counts())

"""#### Gradient Boosting Classifier (SMOTE)"""

# training Gradient Boosting Classifier with smote variables

Smote_model_nolag = GradientBoostingClassifier(n_estimators=110, max_depth= 5, subsample=1,min_samples_split= 600, max_features =19, random_state=10)
Smote_model_nolag.fit(os_smote_X,os_smote_y)
predictions_train = Smote_model_nolag.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_model_nolag.predict(smote_X_test) # predicting the hold out data sample

# Print accuracy metrics
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save the model results
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Gradient Boosting Classifier (SMOTE with original data)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""In spot check modeling, Linear Regression, RFC and LDA also provided good accuracy:

* Linear Regression = .7934
* Random Forest Classifier = .7928
* Linear Discrimminant A   = .7934

So I tried fitting those models with SMOTE values.

#### Logistic Regression (SMOTE)
"""

# Fit Logistic regression
Smote_modelLR_nolag = LogisticRegression(penalty='l2')
Smote_modelLR_nolag.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelLR_nolag.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelLR_nolag.predict(smote_X_test) # predicting the hold out data sample

# print model performance results
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model results
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Logistic Regression (SMOTE with original data)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Random Forest Classifier (SMOTE)"""

# Random forest classification algorithm using smote
Smote_modelRFC_nolag = RandomForestClassifier()
Smote_modelRFC_nolag.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelRFC_nolag.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelRFC_nolag.predict(smote_X_test) # predicting the hold out data sample

# check performance
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save the model results
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Random Forest Classifier (SMOTE with original data)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Linear Discriminant Analysis (SMOTE)"""

# Linear Discriminant Analysis using smote
Smote_modelLDA_nolag = LinearDiscriminantAnalysis()
Smote_modelLDA_nolag.fit(os_smote_X,os_smote_y)
predictions_train = Smote_modelLDA_nolag.predict(smote_X_train) # predicting the hold out data sample
predictions = Smote_modelLDA_nolag.predict(smote_X_test) # predicting the hold out data sample

# print accuracy and performance results
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,predictions_train,predictions)

# save model results
c = classification_report(smote_y_test, predictions, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Linear Discriminant Analysis (SMOTE with original data)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Confusion metrices for SMOTE models -- *Without Polynomial and log features*"""

# define function to create confusion metrices
def cm(modellist, modNames, IndependentTest, TargetTest):

	lst    = modellist		# list of models

	length = len(lst)

	mods   = modNames			# names of model algorithms

	fig = plt.figure(figsize=(13,15))
	fig.set_facecolor("White")
	for i,j,k in itertools.zip_longest(lst,range(length),mods) :
		plt.subplot(4,3,j+1)
		predictions = i.predict(IndependentTest)
		conf_matrix = confusion_matrix(predictions,TargetTest)
		sns.heatmap(conf_matrix,annot=True,fmt = "d",square = True,
					xticklabels=["not churn","churn"],
					yticklabels=["not churn","churn"],
					linewidths = 2,linecolor = "w",cmap = "Set1")
		plt.title(k,color = "Black")
		plt.subplots_adjust(wspace = .3,hspace = .3)
		
cm([Smote_model_nolag,Smote_modelLR_nolag, Smote_modelLDA_nolag, Smote_modelRFC_nolag], 
				['GBC(SMOTE) w/o poly and lags', 'LR(SMOTE)  w/o poly and lags' , 'LDA(SMOTE) w/o poly and lags', 'RFC(SMOTE) w/o poly and lags'], 
				smote_X_test, 
				smote_y_test)		# call the function to display the confusion metrices

"""#### ROC Curves for SMOTE models -- *Without Polynomial and log variables*"""

# define function to calculate and plot ROC curves for all models
def ROC_graph(modellist, modNames, IndependentTest, IndependentTarget):
    lst    = modellist    # list of models implemented
    length = len(lst)   
    mods   = modNames   # names of models

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12,16))
    fig.set_facecolor("#F3F3F3")
    for i,j,k in itertools.zip_longest(lst,range(length),mods) :
        qx = plt.subplot(4,3,j+1)
        probabilities = i.predict_proba(IndependentTest)
        predictions   = i.predict(IndependentTest)
        fpr,tpr,thresholds = roc_curve(IndependentTarget,probabilities[:,1])
        plt.plot(fpr,tpr,linestyle = "dotted",
                    color = "royalblue",linewidth = 2,
                    label = "AUC = " + str(np.around(roc_auc_score(IndependentTarget,predictions),3)))
        plt.plot([0,1],[0,1],linestyle = "dashed",
                    color = "orangered",linewidth = 1.5)
        plt.fill_between(fpr,tpr,alpha = .4)
        plt.fill_between([0,1],[0,1],color = "k")
        plt.legend(loc = "lower right",
                    prop = {"size" : 12})
        qx.set_facecolor("k")
        plt.grid(True,alpha = .15)
        plt.title(k,color = "black")
        plt.xticks(np.arange(0,1,.3))
        plt.yticks(np.arange(0,1,.3))


 # call function to display ROC curves 
ROC_graph([Smote_model_nolag,Smote_modelLR_nolag, Smote_modelLDA_nolag, Smote_modelRFC_nolag], 
	      ['GBC(SMOTE) w/o poly and lags', 'LR(SMOTE)  w/o poly and lags' , 'LDA(SMOTE) w/o poly and lags', 'RFC(SMOTE) w/o poly and lags'], 
	      smote_X_test, 
	      smote_y_test)

"""Looking at the Confusion metrices and ROC curves, Linear Discriminant Analysis appears to be performing the best among the above models.

### Ensemble Model

#### Ensemble model -- *With log and polynomial features*
"""

from sklearn.model_selection import cross_val_score
from sklearn import model_selection
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

# divide data into predictors and target
X = df.iloc[:, df.columns != 'Churn']
y = df.iloc[:, df.columns == 'Churn']

# partition the dataset into train and test partition
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =.3, random_state = 420, stratify = y )

kfold_vc = model_selection.KFold(n_splits=10, random_state=10)  # define k-fold validation
 
# instantiate different models and append these algorithms into an object ‘estimator’

estimators = []
mod_lr = LogisticRegression()     #logistic Regression
estimators.append(('logistic', mod_lr))

mod_dt = DecisionTreeClassifier()     # Decision Tree Classifier
estimators.append(('DecisionTree', mod_dt))

mod_sv = SVC()    # Support Vector Classifier
estimators.append(('svm', mod_sv))

mod_gb = GradientBoostingClassifier()   # Gradient Boosting Classifier
estimators.append(('GradientBoost', mod_gb))

mod_rfc = RandomForestClassifier()    # Random Forest Classifier
estimators.append(('RandomForest', mod_rfc))

#  instantiate the VotingClassifier() ensemble
ensemble = VotingClassifier(estimators)

#generate the cross validated scores on the data
results_vc = model_selection.cross_val_score(ensemble,X_train, y_train, cv=kfold_vc)
print(results_vc.mean())

# fit the ensemble
Ensemble_model1 = ensemble.fit(X_train, y_train)

train_pred = Ensemble_model1.predict(X_train)   # predict the train target
test_pred   = Ensemble_model1.predict(X_test)   # predict the holdout sample

# print performance metrics
Accuracy_Information(y_train,X_train,y_test,X_test,train_pred,test_pred )

# save model results
c = classification_report(y_test, test_pred, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Ensemble model', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Ensemble model -- *Without log and polynomial features*"""

# seperate the predictors and target
X = df_SMOTE.iloc[:, df_SMOTE.columns != 'Churn']
y = df_SMOTE.iloc[:, df_SMOTE.columns == 'Churn']

# partition the data
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size =.3, random_state = 420, stratify = y )

kfold_vc = model_selection.KFold(n_splits=10, random_state=10)    #define k-fold validation
 
# instantiate different models and append these algorithms into an object ‘estimator’

estimators = []
mod_lr = LogisticRegression()   # Logistic Regression
estimators.append(('logistic', mod_lr))

mod_dt = DecisionTreeClassifier()   # Decision Tree Classifier
estimators.append(('DecisionTree', mod_dt))

mod_sv = SVC()    # Support Vector Classifier
estimators.append(('svm', mod_sv))

mod_gb = GradientBoostingClassifier()   # Gradient Boosting Classifier
estimators.append(('GradientBoost', mod_gb))

mod_rfc = RandomForestClassifier()    # Random Forest Classifier
estimators.append(('RandomForest', mod_rfc))

#  instantiate the VotingClassifier() ensemble
ensemble = VotingClassifier(estimators)

#generate the cross validated scores on the data
results_vc = model_selection.cross_val_score(ensemble,X_train, y_train, cv=kfold_vc)
print(results_vc.mean())

# fit the ensemble model
Ensemble_model2 = ensemble.fit(X_train, y_train)

train_pred = Ensemble_model2.predict(X_train)   # predict the training partition target
test_pred   = Ensemble_model2.predict(X_test)   # predict the holdout sample

# print the model performance
Accuracy_Information(y_train,X_train,y_test,X_test,train_pred,test_pred )

# save model results
c = classification_report(y_test, test_pred, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Ensemble model (original data)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""#### Ensemble Model -- *With SMOTE data*"""

from imblearn.over_sampling import SMOTE

# Split out data set
smote_X = df_SMOTE.iloc[:, df_SMOTE.columns != 'Churn']
smote_y = df_SMOTE.iloc[:, df_SMOTE.columns == 'Churn']

#Split train and test data
smote_X_train,smote_X_test,smote_y_train,smote_y_test = train_test_split(smote_X,smote_y,
                                                                         test_size = .3 ,
                                                                         random_state = 420)

#oversampling minority class(Churn = 1) using smote
os = SMOTE(random_state = 0)
os_smote_X,os_smote_y = os.fit_sample(smote_X_train,smote_y_train) # This is where the training data is fed with synthesized data
os_smote_X = pd.DataFrame(data = os_smote_X)
os_smote_y = pd.DataFrame(data = os_smote_y)
os_smote_y =os_smote_y.rename(columns= { 0 : 'Churn'})


kfold_vc = model_selection.KFold(n_splits=10, random_state=10)    # k-fold validation
 
# instantiate different models and append these algorithms into an object ‘estimator’

estimators = []
mod_lr = LogisticRegression()   # Logistic Regression
estimators.append(('logistic', mod_lr))

mod_dt = DecisionTreeClassifier()   # Decision Tree Classifier
estimators.append(('DecisionTree', mod_dt))

mod_sv = SVC()      # Support Vector Classifier
estimators.append(('svm', mod_sv))

mod_gb = GradientBoostingClassifier() # Gradient Boosting Classifier
estimators.append(('GradientBoost', mod_gb))

mod_rfc = RandomForestClassifier()    # Random Forest Classifier
estimators.append(('RandomForest', mod_rfc))

#  instantiate the VotingClassifier() ensemble
ensemble = VotingClassifier(estimators)

#generate the cross validated scores on the data
results_vc = model_selection.cross_val_score(ensemble,os_smote_X, os_smote_y, cv=kfold_vc)
print(results_vc.mean())

# fit the model
Ensemble_model3 = ensemble.fit(smote_X_train, smote_y_train)

train_pred = Ensemble_model3.predict(smote_X_train)   # predict for the train data
test_pred   = Ensemble_model3.predict(smote_X_test)   # predict for the holdout sample

# print the performance metrics
Accuracy_Information(smote_y_train,smote_X_train,smote_y_test,smote_X_test,train_pred,test_pred )

# save the model results
c = classification_report(smote_y_test, test_pred, output_dict=True)
model_results = model_results.append(pd.DataFrame({'Model': 'Ensemble model (SMOTE)', 'Accuracy':c['accuracy'], 
                                                   'Precision for 1s':c['1']['precision'],
                                                     'Recall for 1s':c['1']['recall']}, index=[0]), ignore_index=True)

"""## Compiled Model Results

The target being a rare event, I focused more on Recall and Precision than accuracy, as I are more interested in True positive rate (Sensitivity).
"""

# Print the model results sorting them according to Recall and Precision
model_results.sort_values(['Recall for 1s',	'Precision for 1s'], ascending=False)

"""After sorting the model results, it can be seen that Linear Discriminant Analysis model built using SMOTE and original variables has the best Recall, and hence, this is chosen as the best model for further analysis.

## Model with the best Recall

#### Feature Importance for the model
"""

# Split out data set
smote_X = df_SMOTE.iloc[:, df_SMOTE.columns != 'Churn']
smote_y = df_SMOTE.iloc[:, df_SMOTE.columns == 'Churn']

# check feature importance 
from sklearn.inspection import permutation_importance
sns.set(rc={'figure.figsize':(12,20)})

# perform permutation importance
results = permutation_importance(Smote_modelLR_nolag , smote_X, smote_y, scoring='accuracy')

#Split train and test data
smote_X_train,smote_X_test,smote_y_train,smote_y_test = train_test_split(smote_X,smote_y,
                                                                         test_size = .3 ,
                                                                         random_state = 420)

#oversampling minority class(Churn = 1) using smote
os = SMOTE(random_state = 0)
os_smote_X,os_smote_y = os.fit_sample(smote_X_train,smote_y_train) # This is where the training data is fed with synthesized data
os_smote_X = pd.DataFrame(data = os_smote_X)
os_smote_y = pd.DataFrame(data = os_smote_y)
os_smote_y =os_smote_y.rename(columns= { 0 : 'Churn'})

# chech the data shapes
print(os_smote_X.shape, os_smote_y.shape)
print(smote_X_test.shape,smote_y_test.shape)

# get importance
importance = results.importances_mean
sorted_idx = np.argsort(importance)
f =X.columns[sorted_idx]
# plot importance graph
pos = np.arange(sorted_idx.shape[0]) + .5
plt.barh(pos, importance[sorted_idx], align='center')
plt.yticks(pos, smote_X.columns[sorted_idx])
plt.xlabel('Permutation Feature Importance Scores')
plt.title('Permutation Feature Importance for LDA')
plt.show()

# get the top 12 important features
important_train_features = os_smote_X.iloc[:, sorted_idx[-12:]]
important_test_features = smote_X_test.iloc[:, sorted_idx[-12:]]

# Sanity check on operations
print('Important train features shape:', important_train_features.shape)
print('Important test features shape:', important_test_features.shape)

# check the target shape
smote_y_test.shape

"""#### Tuning Hyperparameters for the model"""

## ----------- Best Estimator ----------------
# Grid Search(hyper tuning for Logistic Regression)
from sklearn.model_selection import GridSearchCV

# parameters

solver=["svd"]
toll = [0.0001,0.0002,0.0003,0.0004,0.0005,0.0006]

param_grid = dict(solver = solver, tol = toll)

LDA = LinearDiscriminantAnalysis()

# Construct a grid search
gridLDA = GridSearchCV(LDA, param_grid = param_grid, cv=10,
                     scoring="accuracy", n_jobs= 4, verbose = 0)



# fit using grid search
gridLDA.fit(important_train_features, os_smote_y)

print("Best scoring(r^2): %.3f" %gridLDA.best_score_)

# Best params
print('\nBest params:\n', gridLDA.best_params_)

"""#### Best Model -- With tuned hyperparameters and 60 most important features"""

#Fitting the model with best parameters
LDA = LinearDiscriminantAnalysis(solver='svd', tol =.0001)

best_param_model_LDA =LDA.fit(important_train_features, os_smote_y)

train_pred = best_param_model_LDA.predict(important_train_features)    # predict for the training partition
test_pred   = best_param_model_LDA.predict(important_test_features)    # predict for the holdout sample

# check model performance
Accuracy_Information(os_smote_y,important_train_features,smote_y_test,important_test_features,train_pred,test_pred )

"""# Results

Given that the dataset had unbalanced nature of the target variable, I decided to have Recall as the key decision-making criteria for Model Selection over Accuracy. 
* Initially I found Gradient Boosting Classifier to be our best performing estimator and hence I performed hyper parameter boosting on it to make it more robust. Although the accuracy improved the Recall was not that great. 
* I tweaked our approach by bringing SMOTE into the analysis.
* After comparing the recall statistic of all models, Linear Discriminant Analysis Model (SMOTE with original dataset) turned out to be the best performing model, with a recall of 0.796.
* After performing feature importance analysis and hyperparameter tuning for this model, I got a Recall of 0.75. 
* While I implemented SMOTE to achieve better Recall while building the Linear Discriminant Analysis (SMOTE with original dataset), the recall and accuracy of the model actually decreased to a certain extent.

# Conclusion

* After listing down all the models implemented, I found that the best recall I got was 0.796 whereas the best accuracy was 0.81 given by simple logistic regression. This a classic example of a tradeoff between Model accuracy and Recall that must be made primarily based on the specific business requirement of a model.
* For this particular case study, I feel the better the Recall, better the model.
"""
