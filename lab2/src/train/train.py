import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import f1_score, roc_auc_score
import joblib
DATA = 'data/churn_v1.csv'   # Twist 1: change this to churn_v2.csv
df = pd.read_csv(DATA)
numeric = ['tenure_months', 'monthly_charges', 'support_calls']
categorical = ['contract', 'internet_service']
X = df[numeric + categorical]
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = Pipeline([
    ('prep', ColumnTransformer([
        ('num', StandardScaler(), numeric),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
    ])),
    ('clf', LogisticRegression(max_iter=1000)),
])
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
print('F1 :', round(f1_score(y_test, proba > 0.5), 3))
print('AUC:', round(roc_auc_score(y_test, proba), 3))
joblib.dump(model, 'model.joblib')
print('saved model.joblib')