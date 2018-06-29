import numpy as np 
import pandas as pd 
from sklearn import ensemble, svm, preprocessing, model_selection, metrics, linear_model

def main():

	df = pd.read_excel('superbowl.xlsx')
	df2 = pd.read_csv('2018Season.csv')

	teams = dict(enumerate(np.asarray(df2['Team Name'])))
	df2.drop('Team Name', axis=1,inplace=True)

	#df = shuffle(df)
	convert_to_num_(df)
	convert_to_num_(df2)

	x = np.asarray(df.drop('Playoffs', 1).drop('Team Name',1))
	y = np.asarray(df['Playoffs'])

	x = preprocessing.scale(x)

	#x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=.2, shuffle=False)

	#kf = model_selection.KFold(n_splits=10)
	#for train_index, test_index in kf.split(x):
	#	x_train, x_test = x[train_index], x[test_index]
	#	y_train, y_test = y[train_index], y[test_index]

	x2 = preprocessing.scale(df2)

	print()
	print('Model Statistics')

	clf = ensemble.RandomForestClassifier(n_jobs=-1)

	clf.fit(x, y)
	
	predictions = clf.predict(x2)

	print()
	print('2018 NFL Playoffs \n')

	playoff_teams = [teams[i] for i in range(len(x2)) if predictions[i]==1]

	for i in playoff_teams:
		print('The', i, 'will make the Playoffs')

	print()
	features = list(df.columns)[1:10]
	print('FEATURE IMPORTANCES')
	for i in list(zip(features, clf.feature_importances_)):
		print(i)

#End of Main --

def convert_to_num_(df):
	columns = df.columns.values

	def to_key(input):
		return keys[input]

	for col in columns:
		keys = {}
		datatype = df[col].dtype
		if not (datatype == np.int64 or datatype == np.float64):
			j = 1
			for i in df[col]:
				if not i in keys:
					keys[i] = j
					j+=1
			df[col] = df[col].apply(to_key)

def shuffle(df):
	return df.reindex(np.random.permutation(df.index))

if __name__ == '__main__':
	main()