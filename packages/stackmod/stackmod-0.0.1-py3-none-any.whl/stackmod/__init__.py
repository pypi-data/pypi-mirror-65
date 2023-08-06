from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd


class StackModel:
	"""
	This class is only applicable for regression tasks for now.
	"""
	def __init__(self, estimators, meta_model, n_folds=5):
		if n_folds < 1:
			raise BaseException('Number of folds must be at least 1')
			return
		else:
			self.n_folds = n_folds
			
		self.estimators = estimators
		self.meta_model = meta_model
		
		self.estimators_score = {}

		self.X_train = None
		self.y_train = None
	
	def fit(self, X, y):
		"""
		
		"""
		# save train data for scoring estimators later
		self.X_train = X
		self.y_train = y
		
		X_train_meta, y_train_meta  = self.__train_set(X, y)
		
		self.meta_model.fit(X_train_meta, y_train_meta)
	
	def predict(self, X_test, y_test=None):
		"""
		If y is set then scores to estimators will be calculated. Otherwise, self.estimators_score will stay "None". 
		"""
		X_test_meta = self.__test_set(X_test, y_test)
		return self.meta_model.predict(X_test_meta)
		
	def __train_set(self, X, y):
		"""
		Gets train set for meta model
		"""
		kf = KFold(self.n_folds)
		train_set = []
		
		# we are working with numpy arrays only
		if type(X) == pd.DataFrame:
			X = X.values
		
		if type(y) == pd.Series:
			y = y.values

		for train, test in kf.split(X):
			X_train, X_test = X[train], X[test]
			y_train, y_test = y[train], y[test]
			
			mp = []

			for m in self.estimators:
				m.fit(X_train, y_train)

				# prediction of an estimator, a fold of a new train set
				mp.append(m.predict(X_test))

			# add target  
			mp.append(y_test)
			
			# the fold complete
			train_set.append(np.stack(mp, axis=1))

		# stack folds to get the new train set
		ts = np.vstack(train_set)
		
		# to figure out where data and target
		indices = len(self.estimators)
		
		# devide the train set for meta model into data and target
		X_meta = ts[:,:indices]
		y_meta = ts[:,indices]
		
		return X_meta, y_meta
		
	def __test_set(self, X_test, y_test):
		"""
		Gets test set for meta-model by making predictions of estimators on the whole original train set
		"""
		if self.X_train is None or self.y_train is None:
			raise BaseException('Before predict you must call fit function!')
			
		# init score dictionary
		self.estimators_score = {}
		mp = []

		for m in self.estimators:
			# fit week model to original train set
			m.fit(self.X_train, self.y_train)
			p = m.predict(X_test)
			mp.append(p)
			# save the estimator score
			if y_test is not None:
				self.estimators_score[type(m).__name__] = r2_score(y_test, p)
		
		# stack features = predictions of estimators
		return np.stack(mp, axis=1)
