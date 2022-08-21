import pandas as pd
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle
from data_generate import num_class

# combining all data into one
hand_df = pd.DataFrame()
for i in range(num_class):
    hand_new = pd.read_csv(f'hand-{i}.csv')
    hand_df = hand_df.append(hand_new)
hand_df = hand_df.sample(frac=1)

# splitting datasets
x, y = hand_df.drop('y', axis=1), hand_df['y']
x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    random_state=14,
                                                    test_size=0.5)

# training the model
sgd_clf = SGDClassifier(random_state=20)
sgd_clf.fit(x_train, y_train)
pickle.dump(sgd_clf, open('hand_model.sav', 'wb'))

# model accuracy score
y_pred = sgd_clf.predict(x_test)
acc_score = accuracy_score(y_test, y_pred)
print('Hand Accuracy Score : ', acc_score)
