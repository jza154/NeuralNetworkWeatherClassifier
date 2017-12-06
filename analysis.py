import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import make_pipeline
from skimage import color
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
#from skmultilearn.adapt import MLkNN



def rgbtoint(y):

    #y11 = "[" + y
    #y2,y3 = y.split("]")
    #y2 = y11.strip('[]')
    nr = [str(i) for i in y[:-1].split()]
    r = nr[0]
    g = nr[1]
    b = nr[2]
    b = b[:-1]
    finalint = ((int(r)*256^2) + (int(g)*256) + int(b))
    #finalint = ((int(r)*0.2125) + (int(g)*0.7154) + (int(b)*0.0721))
    return finalint


data= pd.read_csv('csv_all_data/weather_imagetestRGB.csv')
data=data.drop(data.columns[[0]], axis=1)
data=data.drop(data.columns[[-1]], axis=1)
data=data.drop(data.columns[[-3]], axis=1)
data=data.drop(data.columns[[-2]], axis=1)


#print(data)

#data['0']= data['0'].apply(lambda x:x[1])

#datafake = data['0'].values.tolist()

#print(datafake)

x=data.loc[:, data.columns != 'Weather']






x = x.applymap(lambda x: x.strip('[]'))
x = x.applymap(lambda x: x[:-1])
x = x.applymap(lambda x: rgbtoint(x))








#X= x.values

#print(x)
#data.to_csv('datacsv.csv')


#x = x.astype(float)




#X = x[:, np.newaxis]
#X = np.stack(x)

X = x.as_matrix()


#X.to_csv('xcsv.csv')
#print(X)

# mlb = MultiLabelBinarizer()



y = data['Weather'].as_matrix()


#mlb = MultiLabelBinarizer()
#yfinal = mlb.fit_transform(y)



# print(y.shape)
# print(X.shape)

# model = LinearRegression(fit_intercept=True)
# model.fit(X, y)
# print(model.coef_[0], model.intercept_)





X_train, X_test, y_train, y_test = train_test_split(X, y)





bayes_model = GaussianNB()
bayes_model.fit(X_train, y_train)
modelscore = bayes_model.score(X_test, y_test)
y_predicted = bayes_model.predict(X_test)
#print(accuracy_score(y_test, y_predicted))
print(bayes_model.score(X_test, y_test))
#print(classification_report(y_test, y_predicted))





'''
model = make_pipeline(
    PCA(5),
    SVC(kernel='linear', C=2.0)
    )
'''

'''
model = SVC(kernel='linear', C=10)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
'''




'''
knn_rgb_model = MLkNN(k=3)
knn_rgb_model.fit(X_train, y_train)
print(knn_rgb_model.score(X_test, y_test))
'''






# y_predicted=bayes_model.predict(X_test)
# # y_predicted_bayes = bayes_model.predict(X_S)
# print(accuracy_score(y_test, y_predicted))
 


# knn_rgb_model = KNeighborsClassifier(n_neighbors=15)
# knn_rgb_model.fit(X_train, y_train)
# print(knn_rgb_model.score(X_test, y_test))
# y_predicted_svc= svc_model.predict(X_S)
# y_svc=pd.DataFrame(y_predicted_svc)






#maybe use sklearn.neural_network.MLPClassifier
'''
model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=())
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
'''





