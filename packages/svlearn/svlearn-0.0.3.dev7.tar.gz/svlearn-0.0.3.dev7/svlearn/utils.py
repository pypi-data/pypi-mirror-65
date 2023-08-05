"""Utils for ML

"""

import numpy as np
import pandas as pd

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import make_scorer
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from scipy import interp

from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import mutual_info_regression

from sklearn.feature_selection import f_classif
from sklearn.feature_selection import mutual_info_classif

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
from sklearn.cluster import KMeans

from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression 

import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import OneHotEncoder

from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

from IPython.display import display, Markdown, HTML

import category_encoders

from sklearn import svm
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope

__HTML = 'HTML'
__DISPLAY = 'DISPLAY'

__line_to_print = "________________________________________"

def print_func(value_to_print, mode=None):
	"""Display or Print an object or string

	Args:
		value_to_print (Union[str, object]): Value to print
		mode (optional[str]): Defaults to None.
			Accepts either `DISPLAY` or `HTML`

	"""
	
	if(mode == __DISPLAY):
		display(value_to_print)
	elif(mode == __HTML):
		display(HTML(value_to_print))
	else:
		print(value_to_print)

def print_separator():
	"""Prints a separator line using 80 underscores

	"""

	print_func(__line_to_print + __line_to_print)

def print_new_line():
	"""Prints a new line

	"""

	print_func("")

def get_dataframe_from_array(data_array, columns):
	"""Convert ndarray to pd.DataFrame for the given list of columns

	Args:
		data_array (ndarray): Array to convert to pd.DataFrame
		columns (Union[array-like]): Column Names for the pd.DataFrame

	Returns:
		pd.DataFrame

	"""
	
	df = pd.DataFrame(data_array, columns=columns)
	print_func("-> Loaded dataframe of shape " + str(df.shape))
	print_separator()
	return df

def about_dataframe(df):
	"""Describe DataFrame and show it's information

	Args:
		df (DataFrame): Pandas DataFrame to describe and info

	"""
	
	print_func("-> Data Describe\n")
	print_func(df.describe(include = "all").transpose(), mode=__DISPLAY)
	print_separator()
	
	print_func("-> Data Info\n")
	print_func(df.info(), mode=__DISPLAY)
	print_separator()
	null_values_info(df)
	
def null_values_info(df):
	"""Show null value information of a DataFrame

	Args:
		df (DataFrame): Pandas DataFrame for which null values should be displayed

	"""
	
	df = df.copy()
	kount_of_null_values = df.isnull().sum().sum()
	if(kount_of_null_values > 0):
		print_func("-> Null Values Info")
		df_null_values_sum = df.isnull().sum()

		html_to_display = "<table><tbody><tr>"
		num_of_columns_with_null = 0
		for idx, each_feature in enumerate(sorted(df_null_values_sum.keys())):
			if(df_null_values_sum.loc[each_feature] > 0):
				html_to_display = (html_to_display + "<td>" + each_feature + 
								"</td>" + "<td>" +
								str(df_null_values_sum.loc[each_feature]) + 
								"</td>")
				num_of_columns_with_null = num_of_columns_with_null + 1
			if(num_of_columns_with_null%4 == 0):
				html_to_display = html_to_display + "</tr><tr>"
		html_to_display = html_to_display + "</tr></tbody></table>"
		print_func(html_to_display, mode=__HTML)
	else:
		print_func("-> No Null Values")
	
	print_separator()

def fill_null_values(df, column, value, row_index):
	"""Fill null values in a dataframe column

	Args:
		df (DataFrame): Pandas DataFrame that will be updated
		column (str): Column in the target dataframe that will be updated
		value: (Union[int, str, object]): New value that will replace 
			null values
		row_index (Union[Index, array-like]): Index of rows to be updated

	"""
	
	num_of_rows = row_index.shape[0]
	
	df.iloc[row_index, df.columns.get_loc(column)] = value
	print_func("{0:d} rows updated for '".format(num_of_rows) + column 
					+ "' with '" + str(value) + "'")

def columns_info(df, cat_count_threshold, show_group_counts=False):
	"""Prints and returns column info for a given dataframe

	Args:
		df (DataFrame): Pandas DataFrame
		cat_count_threshold (int): If a column in the dataframe 
			has unique value count less than this threshold then it 
			will be tagged as 'categorical'
		show_group_counts (boolean): If True then prints the individual 
			group counts for each column

	Example:

		>>> object_cat_cols, 
		>>>    numeric_cat_cols,
		>>>    numeric_cols = 
		>>>        utils.columns_info(data, 
		>>>                            cat_count_threshold=5, 
		>>>                            show_group_counts = True)

	"""
	
	if(cat_count_threshold is None):
		cat_count_threshold = 10
	
	all_columns = df.columns
	numeric_cat_columns = sorted(df._get_numeric_data().columns) 
	# https://stackoverflow.com/questions/29803093/
	# check-which-columns-in-dataframe-are-categorical
	object_cat_columns = sorted(list(set(all_columns) 
							- set(numeric_cat_columns)))
	
	print_func("-> Columns will be tagged as categorical if number " + 
					" of categories are less than or equal to " + 
					str(cat_count_threshold))
	print_separator()
	
	kount = 0
	selected_object_cat_columns = []
	object_columns_not_identified_as_category = []
	to_print = "-> Count of 'object' type categorical columns {0:d}\n"
	to_print_detail = ""
	for object_column in object_cat_columns:
		if(df[object_column].unique().shape[0] <= cat_count_threshold):
			if(show_group_counts):
				to_print_detail = ( to_print_detail + 
					str(df.groupby(object_column)[object_column].count()) )
				to_print_detail = ( to_print_detail + 
					"\n" + 
					"\n________________________________________\n\n" )
			kount += 1
			selected_object_cat_columns.append(object_column)
		else:
			object_columns_not_identified_as_category.append(object_column)
	
	if(kount > 0):
		print_func(to_print.format(kount))
		print_func(selected_object_cat_columns)
		print_new_line()
		if(to_print_detail != ""):
			print_func(to_print_detail)
		print_separator()
	
	if(len(object_columns_not_identified_as_category) > 0):
		print_func("-> Count of 'object' type non categorical columns: " + 
					str(len(object_columns_not_identified_as_category)) + 
					"\n")
		print_func(object_columns_not_identified_as_category)
		print_new_line()
		print_separator()
	
	kount = 0
	selected_numeric_cat_columns = []
	numeric_columns = []
	to_print = "-> Count of 'numeric' type categorical columns {0:d}\n" 
	to_print_detail = ""
	for numeric_column in numeric_cat_columns:
		if(df[numeric_column].unique().shape[0] <= cat_count_threshold):
			if(show_group_counts):
				to_print_detail = (to_print_detail + 
					str(df.groupby(numeric_column)[numeric_column].count()) )
				to_print_detail = ( to_print_detail + "\n" + 
									"\n" + __line_to_print + "\n\n" )
			kount += 1
			selected_numeric_cat_columns.append(numeric_column)
		else:
			numeric_columns.append(numeric_column)
	
	if(kount > 0):
		print_func(to_print.format(kount))
		print_func(selected_numeric_cat_columns)
		print_new_line()
		if(to_print_detail != ""):
			print_func(to_print_detail)
		print_separator()
	
	if(len(numeric_columns) > 0):
		print_func("Count of 'numeric' type columns: {0:d}\n".
			format(len(numeric_columns)))
		print_func(numeric_columns)
		print_new_line()
		print_separator()
	
	return (selected_object_cat_columns, 
		selected_numeric_cat_columns, 
		numeric_columns)

def get_X_and_y(df, y_column):
	"""Splits pd.dataframe into X (predictors) and y (response)

	Args:
		df (DataFrame): Pandas DataFrame
		y_column (str): The response column name

	Returns:
		X (DataFrame): All columns except the response will be in X
		y (Series): Only the response column from dataframe

	"""
	
	X = df[[i for i in list(df.columns) if i != y_column]]
	y = df[y_column]
	
	print_func("-> X set to " + ', '.join(
				df.columns[~df.columns.isin( [y_column] ) ] ))
	print_func("-> y set to " + y_column)
	print_separator()
	
	return X, y

def __get_plot_attrs(**kwargs):
	if 'hue_column' not in kwargs:
		kwargs['hue_column'] = None
	
	if 'split_plots_by' not in kwargs:
		kwargs['split_plots_by'] = None
	
	if 'height' not in kwargs:
		kwargs['height'] = 4
	
	if 'aspect' not in kwargs:
		kwargs['aspect'] = 1
	
	if 'kde' not in kwargs:
		kwargs['kde']=True
		
	return ( kwargs['hue_column'], 
		kwargs['split_plots_by'], 
		kwargs['height'], 
		kwargs['aspect'],
		kwargs['kde'])

def count_plots(df, columns, **kwargs):
	"""Count Plots using seaborn

	Display Count plots for the given columns in a DataFrame

	Args:
		df (DataFrame): Pandas DataFrame
		columns (array-like): Columns for which count plot has to be shown
		kwargs (array[str]): Keyword Args

	KeywordArgs:
		hue_column (str): Color
		split_plots_by (str): Split seaborn facetgrid by column such as Gender

		height (float): Sets the height of plot

		aspect (float): Determines the width of the plot based on height

	Example:
		>>> utils.count_plots(data, object_cat_cols, height=4, aspect=1.5)

	"""
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	columns = pd.Series(columns)
	
	i = 0
	plt.ion()
	columns = columns[~columns.isin([hue_column, split_plots_by])]
	for each_col in columns:
		order=df.groupby(each_col)
		print_func("Count Plot for: " + str(each_col))
		
		g = sns.catplot( x=each_col, hue=hue_column, 
						col=split_plots_by, kind="count", 
						data=df, order=order.indices.keys(), 
						height=height, aspect=aspect )
			
		g.set_xticklabels(rotation=40)
		plt.show(block=False)
		print_new_line()
		# display(HTML("<input type='checkbox' id='" + each_col + 
		# "' value='" + each_col + "'>" + each_col + "<br />"))
		i = i + 1

def count_compare_plots(df1, df1_title, df2, df2_title, column, **kwargs):
	"""Show Count Plots of two DataFrames for comparision

	Can be used to compare how Fill NA affects the distribution of a column

	Args:
		

	Example:
		The below example uses nhanes dataset.

		>>> for each_column in object_cat_columns:
		>>>    data[each_column] = data[each_column].fillna(
		>>>    data.groupby(['Gender'])[each_column].ffill())
		>>> for each_column in object_cat_columns:
		>>>    str_count_of_nas = str(len(
		>>>        data_raw.index[data_raw.isnull()[each_column]]))
		>>>    str_count_of_nas = ' (Count of NAs:' + str_count_of_nas + ')'
		>>>    utils.count_compare_plots(df1=data_raw, 
		>>>    df1_title='Before Fill-NA' + str_count_of_nas, 
		>>>            df2=data, 
		>>>            df2_title='After Fill-NA', 
		>>>            column=each_column, 
		>>>            height=4, 
		>>>            aspect=1.5, 
		>>>            hue_column='Diabetes', 
		>>>            split_plots_by='Gender')

	"""
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	print_func("Count Plot for: " + str(column))
	
	f, axes = plt.subplots(2)

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, 
					kind="count", data=df1, height=height, aspect=aspect )
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df1_title, fontsize=16)
	
	###

	g = sns.catplot( x=column, hue=hue_column, col=split_plots_by, 
					kind="count", data=df2, height=height, aspect=aspect)
	g.set_xticklabels(rotation=40)
	g.fig.suptitle(df2_title, fontsize=16)
	
	####

	plt.close(1)
	plt.show()
	print_new_line()

def dist_plots(df, columns, **kwargs):
	"""Dist Plots using seaborn

	Args:
		df (DataFrame): Pandas DataFrame.
		columns ([str]): Plot only for selected columns.
		**kwargs: Keyword arguments.

	Keyword Args:
		hue_column (str): Color
		split_plots_by (str): Split seaborn facetgrid by column such as Gender
		height (float): Sets the height of plot
		aspect (float): Determines the width of the plot based on height

	Example:
		>>> utils.dist_plots(data, numeric_cols, height=4, aspect=1.5,
		>>>    hue_column='class', kde=False)

	Returns: Nothing
	"""
	
	kwargs['kde']=False
	
	kde_plots(df, columns, **kwargs)

def kde_plots(df, columns, **kwargs):
	"""KDE Plots using seaborn

	Args:
		df (DataFrame): DataFrame
		columns ([str]): Plot only for selected columns.
		**kwargs: Keyword arguments.

	Keyword Args:
		hue_column: for color coding
		split_plots_by: split seaborn FacetGrid by column, example: Gender
		height: sets the height of plot
		aspect: determines the widht of the plot based on height

	Example:
		>>> utils.kde_plots(data, numeric_cols, height=4, aspect=1.5, 
		>>>    hue_column='class')

	"""
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	columns = pd.Series(columns)
	
	for each_col in columns:
		if(kde):
			print_func("KDE Plot for: " + str(each_col))
		else:
			print_func("Histogram for: " + str(each_col))
		
		if(split_plots_by is None):
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col]], 
								height=height, 
								aspect=aspect)
			else:
				g = sns.FacetGrid(df[[each_col, hue_column]], 
								hue=hue_column, 
								height=height, 
								aspect=aspect)
		else:
			if(hue_column is None):
				g = sns.FacetGrid(df[[each_col, split_plots_by]], 
								col=split_plots_by, 
								height=height, 
								aspect=aspect)
			else:
				g = sns.FacetGrid(df[[each_col, hue_column, split_plots_by]], 
								hue=hue_column, 
								col=split_plots_by, 
								height=height,
								aspect=aspect)
					
		g = (g.map(sns.distplot, each_col, hist=True, kde=kde))
		g.add_legend()
		plt.show()
		print_new_line()

def kde_compare_plots(df1, df1_title, df2, df2_title, column, **kwargs):
	"""Summary line.

	Extended description of function.

	Args:
		

	"""
	
	(hue_column, 
	split_plots_by, 
	height, 
	aspect, 
	kde) = __get_plot_attrs(**kwargs)
	
	print_func("Count Plot for: " + str(column))
	
	f, axes = plt.subplots(2)
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df1[[column, hue_column]], hue=hue_column, 
						col=split_plots_by, height=height, 
						aspect=aspect)
	else:
		g = sns.FacetGrid(df1[[column, hue_column, split_plots_by]], 
						hue=hue_column, col=split_plots_by, height=height, 
						aspect=aspect)
	g = (g.map(sns.distplot, column, hist=True))
	g.add_legend()
	g.fig.suptitle(df1_title, fontsize=16)
	
	####
	
	if(split_plots_by is None):
		g = sns.FacetGrid(df2[[column, hue_column]], hue=hue_column, 
						col=split_plots_by, height=height, 
						aspect=aspect)
	else:
		g = sns.FacetGrid(df2[[column, hue_column, split_plots_by]], 
						hue=hue_column, col=split_plots_by, height=height, 
						aspect=aspect)
			
	g = (g.map(sns.distplot, column, hist=True))
	g.add_legend()
	g.fig.suptitle(df2_title, fontsize=16)
	
	plt.close(1)
	plt.show()
	print_new_line()
	
def encode_columns(df, method, columns = []):
	"""Summary line.

	Extended description of function.

	Args:
		

	"""
	
	kount = 0
	df = df.copy()
		
	for columnName in columns:
		if(method == 'labelencoder'):
			label_encoder = LabelEncoder()
			df[columnName] = label_encoder.fit_transform(
													df[columnName].astype(str))
			print_func("-> Transformed [" + columnName + 
						"] using sklearn.LabelEncoder")
			print_func("--> Classes: " + str(label_encoder.classes_))
		elif(method == 'binary'):
			label_binarizer = LabelBinarizer()
			lb_results = label_binarizer.fit_transform(df[columnName])
			print_func("-> Transformed [" + columnName + 
						"] using sklearn.LabelBinarizer")
			if(label_binarizer.y_type_ == 'multiclass'):
				print_func("--> Type of target data is: " + 
							label_binarizer.y_type_)
				temp_df = pd.DataFrame(lb_results, 
										columns = label_binarizer.classes_, 
										index = df.index)
				df = df.join(temp_df)
				print_func("--> Added following columns to dataframe: " + 
							str(label_binarizer.classes_))
		elif(method == 'onehot'):
			one_hot_encoder = OneHotEncoder(sparse=False)
			ohe_results = one_hot_encoder.fit_transform(df[[columnName]])
			print_func("-> Transformed [" + columnName + 
						"] using sklearn.OneHotEncoder")
			temp_df = pd.DataFrame(ohe_results, 
								columns = one_hot_encoder.get_feature_names())
			df = pd.concat([df,temp_df],axis=1)
			print_func("--> Added following columns to returned dataframe: "+
						str(one_hot_encoder.categories))
		elif(method == 'pd_dummies'):
			df = pd.get_dummies(df, columns = columnName)
			print_func("-> Transformed [" + columnName + 
				"] using pd.get_dummies")
		
		kount = kount + 1
		if(kount < len(columns)):
			print_func("")
		
	print_separator()
	return df

def do_scaling(df, method, columns_to_scale=[]):
	"""Scale data using the specified method

	Columns specified in the arguments will be scaled

	Args:
		df (DataFrame): Pandas DataFrame
		columns (array-like): List of columns that will be scaled

	Returns:
		df (DataFrame)

	"""
	
	if(method == 'StandardScaler'):
		scaler = StandardScaler()
	elif(method == 'RobustScaler'):
		scaler = RobustScaler()
	
	print_func("-> Data scaled using " + method)
	print_separator()
	df_scaled = pd.DataFrame(
					scaler.fit_transform(
							df[columns_to_scale]), columns=columns_to_scale)
	df_not_scaled = df[ df.columns[ ~df.columns.isin( columns_to_scale ) ] ]
	df_scaled = df_scaled.join(df_not_scaled)
	
	return df_scaled
		
def do_feature_selection(X, y, method):
	"""Summary line.

	Extended description of function.

	Args:
		

	"""
	
	if(method == 'f_regression'):
		skbest = SelectKBest(f_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		print_func("-> Selected Features using skbest.f_regression")
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		print_func(sf_df)
	elif(method == 'mutual_info_regression'):
		skbest = SelectKBest(mutual_info_regression, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		print_func("-> Selected Features using " + 
			"skbest.mutual_info_regression")
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		print_func(sf_df)
	elif(method == 'RandomForestRegressor'):
		rf = RandomForestRegressor()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
			random_state=42)
		rf.fit(X_train, y_train)
		
		cv_res = cross_validate(rf, X, y, cv=5, 
								scoring=('r2', 'neg_mean_squared_error'), 
								return_train_score=True,
								return_estimator =True)
									
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]

		feature_importances = pd.DataFrame(
			bst_tst_estimator.feature_importances_ ,
			index = X.columns,
			columns=['importance']).sort_values('importance', 
				ascending=False)
		print_func("-> Selected Features using Random Forest Regressor")
		print_func(feature_importances)
	elif(method == 'f_classif'):
		skbest = SelectKBest(f_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		print_func("-> Selected Features using skbest.f_classif")
		sf_data = {'Feature Name':selected_features.values, 
			'Score':skbest.scores_[mask]} 
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		print_func(sf_df)
	elif(method == 'mutual_info_classif'):
		skbest = SelectKBest(mutual_info_classif, k=X.shape[1]).fit(X,y)
		mask = skbest.get_support()
		selected_features = X.columns[mask]

		print_func("-> Selected Features using " + 
			"skbest.mutual_info_classif")
		sf_data = {'Feature Name':selected_features.values, 
		'Score':skbest.scores_[mask]}
		sf_df = pd.DataFrame(sf_data)
		sf_df.sort_values('Score', ascending=False, inplace=True)
		print_func(sf_df)
	elif(method == 'RandomForestClassifier'):
		rf = RandomForestClassifier()
		
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
			random_state=42)
		rf.fit(X_train, y_train)
		
		cv_res = cross_validate(rf, X, y, cv=5, 
								scoring=('r2', 'neg_mean_squared_error'), 
								return_train_score=True,
								return_estimator =True)
									
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]

		feature_importances = pd.DataFrame(
			bst_tst_estimator.feature_importances_ ,
			index = X.columns,
			columns=['importance']).sort_values('importance', 
				ascending=False)
		print_func("-> Selected Features using Random Forest Classifier")
		print_func(feature_importances)
	
	print_separator()

def do_cross_validate(X, y, estimator_type, estimator, cv, **kwargs):
	"""Cross Validate (sklearn)

	Args:

	Example:
		>>> cv_iterator = ShuffleSplit(n_splits=2, test_size=0.2, random_state=31)
		>>> cv_results = utils.do_cross_validate(X_train, 
		>>>    y_train, 
		>>>    'Classification', 
		>>>    'DecisionTreeClassifier', 
		>>>    cv=cv_iterator, 
		>>>    kernel='rbf', 
		>>>    C=1, 
		>>>    gamma=0.01)

	"""
	
	estimator_name = estimator
	if(estimator == 'LinearRegression'):
		estimator = LinearRegression()
	elif(estimator == 'LinearSVR'):
		estimator = LinearSVR()
	elif(estimator == 'SVR'):
		estimator = SVR()
	elif(estimator == 'LDA'):
		estimator = LinearDiscriminantAnalysis()
	elif(estimator == 'SVC'):
		estimator = SVC(kernel=kwargs['kernel'], 
			C=kwargs['C'], gamma=kwargs['gamma'])
	elif(estimator == 'DecisionTreeClassifier'):
		estimator = DecisionTreeClassifier()
	elif(estimator == 'RandomForestClassifier'):
		estimator = RandomForestClassifier(
			n_estimators=kwargs['n_estimators'], 
			max_features=kwargs['max_features'], 
			criterion=kwargs['criterion'])
	elif(estimator == 'GradientBoostingClassifier'):
		estimator = GradientBoostingClassifier( 
			n_estimators=int(kwargs['n_estimators']), 
			learning_rate=kwargs['learning_rate'], 
			max_depth=kwargs['max_depth'], 
			random_state=int(kwargs['random_state']) )
	elif(estimator == 'LogisticRegression'):
		estimator = LogisticRegression(
			solver=kwargs['solver'],
			max_iter=kwargs['max_iter'])
	else:
		estimator = None
	
	if(estimator is None):
		print("Estimator name not specified")
		print_separator()
		return
	
	if(estimator_type == 'Regression'):
		cv_res = cross_validate(estimator, 
			X, y, 
			cv=cv, 
			scoring=('r2', 'neg_mean_squared_error'), 
			return_train_score=True, 
			return_estimator=True)
		
		# train_r2		
		bst_trn_r2_idx = np.argmax(cv_res['train_r2'])
		bst_trn_r2 = cv_res['train_r2'][bst_trn_r2_idx]
		bst_trn_estimator = cv_res['estimator'][bst_trn_r2_idx]
		test_for_bst_trn_r2 = cv_res['test_r2'][bst_trn_r2_idx]
		fit_time_for_bst_trn_r2 = cv_res['fit_time'][bst_trn_r2_idx]
		score_time_for_bst_trn_r2 = cv_res['score_time'][bst_trn_r2_idx]
		mean_train_r2_score = np.mean(cv_res['train_r2'])
		
		# test_r2
		bst_tst_r2_idx = np.argmax(cv_res['test_r2'])
		bst_tst_r2 = cv_res['test_r2'][bst_tst_r2_idx]
		bst_tst_estimator = cv_res['estimator'][bst_tst_r2_idx]
		trn_for_bst_tst_r2 = cv_res['train_r2'][bst_tst_r2_idx]
		fit_time_for_bst_tst_r2 = cv_res['fit_time'][bst_tst_r2_idx]
		score_time_for_bst_tst_r2 = cv_res['score_time'][bst_tst_r2_idx]
		mean_test_r2_score = np.mean(cv_res['test_r2'])
		
		print("-> " + estimator_name + " scores\n");
		print("-> Mean Train R2 Score: %0.4f\n" %(mean_train_r2_score))
		print("-> Best Train R2 Score: %0.4f, " + 
			"Corresponding Test R2 Score: %0.4f, " + 
			"Best Train R2 Index: %d \n" 
			%(bst_trn_r2, test_for_bst_trn_r2, bst_trn_r2_idx))
		print("-> Mean Test R2 Score: %0.4f\n" %(mean_test_r2_score))
		print("-> Best Test R2 Score: {0:0.4f}, " + 
			"Corresponding Train R2 Score: {1:0.4f}, " + 
			"Best Test R2 Index: {2:d}".format(
				bst_tst_r2, trn_for_bst_tst_r2, bst_tst_r2_idx))
		
	elif (estimator_type == 'Classification'):
		scoring = {'accuracy': make_scorer(accuracy_score), 
				   'precision': make_scorer(precision_score, average='macro'), 
				   'recall': make_scorer(recall_score, average='macro'),
				   'roc': make_scorer(recall_score, average='macro')
				  }
		cv_res = cross_validate(estimator, 
			X, y, 
			cv=cv, 
			scoring=scoring, 
			return_train_score=True,
			return_estimator=True)
		
		# best trn_acc
		bst_trn_acc_index = np.argmax(cv_res['train_accuracy'])
		
		bst_trn_acc = cv_res['train_accuracy'][bst_trn_acc_index]
		tst_acc_for_bst_trn_acc = cv_res['test_accuracy'][bst_trn_acc_index]
		
		trn_prec_for_bst_trn_acc = cv_res['train_precision'][bst_trn_acc_index]
		tst_prec_for_bst_trn_acc = cv_res['test_precision'][bst_trn_acc_index]
		
		trn_rec_for_bst_trn_acc = cv_res['train_recall'][bst_trn_acc_index]
		tst_rec_for_bst_trn_acc = cv_res['test_recall'][bst_trn_acc_index]
		
		trn_roc_for_bst_trn_acc = cv_res['train_roc'][bst_trn_acc_index]
		tst_roc_for_bst_trn_acc = cv_res['test_roc'][bst_trn_acc_index]
		
		# best tst_acc
		bst_tst_acc_index = np.argmax(cv_res['test_accuracy'])
		
		bst_tst_acc = cv_res['test_accuracy'][bst_tst_acc_index]
		trn_acc_for_bst_tst_acc = cv_res['train_accuracy'][bst_tst_acc_index]
		
		trn_prec_for_bst_tst_acc = cv_res['train_precision'][bst_tst_acc_index]
		tst_prec_for_bst_tst_acc = cv_res['test_precision'][bst_tst_acc_index]
		
		trn_rec_for_bst_tst_acc = cv_res['train_recall'][bst_tst_acc_index]
		tst_rec_for_bst_tst_acc = cv_res['test_recall'][bst_tst_acc_index]
		
		trn_roc_for_bst_tst_acc = cv_res['train_roc'][bst_tst_acc_index]
		tst_roc_for_bst_tst_acc = cv_res['test_roc'][bst_tst_acc_index]
		
		
		# best trn_prec
		bst_trn_prec_index = np.argmax(cv_res['train_precision'])
		
		bst_trn_prec = cv_res['train_precision'][bst_trn_prec_index]
		tst_prec_for_bst_trn_prec=cv_res['test_precision'][bst_trn_prec_index]
		
		trn_acc_for_bst_trn_prec = cv_res['train_accuracy'][bst_trn_prec_index]
		tst_acc_for_bst_trn_prec = cv_res['test_precision'][bst_trn_prec_index]
		
		tst_rec_for_bst_trn_prec = cv_res['test_recall'][bst_trn_prec_index]
		trn_rec_for_bst_trn_prec = cv_res['train_recall'][bst_trn_prec_index]
		
		trn_roc_for_bst_trn_prec = cv_res['train_roc'][bst_trn_prec_index]
		tst_roc_for_bst_trn_prec = cv_res['test_roc'][bst_trn_prec_index]
		
		
		# best tst_prec
		bst_tst_prec_index = np.argmax(cv_res['test_precision'])
		
		bst_tst_prec = cv_res['test_precision'][bst_tst_prec_index]
		trn_prec_for_bst_tst_prec=cv_res['train_precision'][bst_tst_prec_index]
		
		trn_acc_for_bst_tst_prec = cv_res['train_accuracy'][bst_tst_prec_index]
		tst_acc_for_bst_tst_prec = cv_res['test_precision'][bst_tst_prec_index]
		
		tst_rec_for_bst_tst_prec = cv_res['test_recall'][bst_tst_prec_index]
		trn_rec_for_bst_tst_prec = cv_res['train_recall'][bst_tst_prec_index]
		
		trn_roc_for_bst_tst_prec = cv_res['train_roc'][bst_tst_prec_index]
		tst_roc_for_bst_tst_prec = cv_res['test_roc'][bst_tst_prec_index]
		
		
		# best trn_rec
		bst_trn_rec_index = np.argmax(cv_res['train_recall'])
		
		bst_trn_rec = cv_res['train_recall'][bst_trn_rec_index]
		tst_rec_for_bst_trn_rec = cv_res['test_recall'][bst_trn_rec_index]
		
		trn_prec_for_bst_trn_rec = cv_res['train_precision'][bst_trn_rec_index]
		tst_prec_for_bst_trn_rec = cv_res['test_precision'][bst_trn_rec_index]
		
		trn_acc_for_bst_trn_rec = cv_res['train_accuracy'][bst_trn_rec_index]
		tst_acc_for_bst_trn_rec = cv_res['test_precision'][bst_trn_rec_index]
		
		trn_roc_for_bst_trn_rec = cv_res['train_roc'][bst_trn_rec_index]
		tst_roc_for_bst_trn_rec = cv_res['test_roc'][bst_trn_rec_index]
		
		
		# best tst_rec
		bst_tst_rec_index = np.argmax(cv_res['test_recall'])
		
		bst_tst_rec = cv_res['test_recall'][bst_tst_rec_index]
		trn_rec_for_bst_tst_rec = cv_res['train_recall'][bst_tst_rec_index]
		
		trn_prec_for_bst_tst_rec = cv_res['train_precision'][bst_tst_rec_index]
		tst_prec_for_bst_tst_rec = cv_res['test_precision'][bst_tst_rec_index]
		
		trn_acc_for_bst_tst_rec = cv_res['train_accuracy'][bst_tst_rec_index]
		tst_acc_for_bst_tst_rec = cv_res['test_precision'][bst_tst_rec_index]
		
		trn_roc_for_bst_tst_rec = cv_res['train_roc'][bst_tst_rec_index]
		tst_roc_for_bst_tst_rec = cv_res['test_roc'][bst_tst_rec_index]
		
		
		# best trn_roc
		bst_trn_roc_index = np.argmax(cv_res['train_roc'])
		
		bst_trn_roc = cv_res['train_roc'][bst_trn_roc_index]
		tst_roc_for_bst_trn_roc = cv_res['test_roc'][bst_trn_roc_index]
		
		trn_rec_for_bst_trn_roc = cv_res['train_recall'][bst_trn_roc_index]
		tst_rec_for_bst_trn_roc = cv_res['test_recall'][bst_trn_roc_index]
		
		trn_prec_for_bst_trn_roc=cv_res['train_precision'][bst_trn_roc_index]
		tst_prec_for_bst_trn_roc = cv_res['test_precision'][bst_trn_roc_index]
		
		trn_acc_for_bst_trn_roc = cv_res['train_accuracy'][bst_trn_roc_index]
		tst_acc_for_bst_trn_roc = cv_res['test_precision'][bst_trn_roc_index]
		
		
		# best tst_roc
		bst_tst_roc_index = np.argmax(cv_res['test_roc'])
		
		bst_tst_roc = cv_res['test_roc'][bst_tst_roc_index]
		trn_roc_for_bst_tst_roc = cv_res['train_roc'][bst_tst_roc_index]
		
		trn_prec_for_bst_tst_roc=cv_res['train_precision'][bst_tst_roc_index]
		tst_prec_for_bst_tst_roc = cv_res['test_precision'][bst_tst_roc_index]
		
		trn_acc_for_bst_tst_roc = cv_res['train_accuracy'][bst_tst_roc_index]
		tst_acc_for_bst_tst_roc = cv_res['test_precision'][bst_tst_roc_index]
		
		trn_rec_for_bst_tst_roc = cv_res['train_recall'][bst_tst_roc_index]
		tst_rec_for_bst_tst_roc = cv_res['test_recall'][bst_tst_roc_index]
		
		
		indices = ['Train Accuracy', 'Test Accuracy', 
			'Train Precision', 'Test Precision', 'Train Recall', 
			'Test Recall', 'Train ROC', 'Test ROC']
		columns = ['Index', 'Best', 'Train Accuracy', 
			'Test Accuracy', 'Train Precision', 'Test Precision', 
			'Train Recall', 'Test Recall', 'Train ROC', 'Test ROC']
					
		d = [
			 [ bst_trn_acc_index, bst_trn_acc, 
				bst_trn_acc, tst_acc_for_bst_trn_acc, 
				trn_prec_for_bst_trn_acc, tst_prec_for_bst_trn_acc, 
				trn_rec_for_bst_trn_acc, tst_rec_for_bst_trn_acc, 
				trn_roc_for_bst_trn_acc, tst_roc_for_bst_trn_acc ],
			 
			 [ bst_tst_acc_index, bst_tst_acc, 
				trn_acc_for_bst_tst_acc, bst_tst_acc, 
				trn_prec_for_bst_tst_acc, tst_prec_for_bst_tst_acc, 
				trn_rec_for_bst_tst_acc, tst_rec_for_bst_tst_acc, 
				trn_roc_for_bst_tst_acc, tst_roc_for_bst_tst_acc ],
			 
			 [ bst_trn_prec_index, bst_trn_prec, 
				trn_acc_for_bst_trn_prec, tst_acc_for_bst_trn_prec, 
				bst_trn_prec, tst_prec_for_bst_trn_prec, 
				trn_rec_for_bst_trn_prec, tst_rec_for_bst_trn_prec, 
				trn_roc_for_bst_trn_prec, tst_roc_for_bst_trn_prec ],
			 
			 [ bst_tst_prec_index, bst_tst_prec, 
				trn_acc_for_bst_tst_prec, tst_acc_for_bst_tst_prec, 
				trn_prec_for_bst_tst_prec, bst_tst_prec, 
				trn_rec_for_bst_tst_prec, tst_rec_for_bst_tst_prec, 
				trn_roc_for_bst_tst_prec, tst_roc_for_bst_tst_prec ],
			 
			 [ bst_trn_rec_index, bst_trn_rec, 
				trn_acc_for_bst_trn_rec, tst_acc_for_bst_trn_rec, 
				trn_prec_for_bst_trn_rec, tst_prec_for_bst_trn_rec, 
				bst_trn_rec, tst_rec_for_bst_trn_rec, 
				trn_roc_for_bst_trn_rec, tst_roc_for_bst_trn_rec ],
			 
			 [ bst_tst_rec_index, bst_tst_rec, 
				trn_acc_for_bst_tst_rec, tst_acc_for_bst_tst_rec, 
				trn_prec_for_bst_tst_rec, tst_prec_for_bst_tst_rec, 
				trn_rec_for_bst_tst_rec, bst_tst_rec, 
				trn_roc_for_bst_tst_rec, tst_roc_for_bst_tst_rec ],
				
			 [ bst_trn_roc_index, bst_trn_roc, 
				trn_acc_for_bst_trn_roc, tst_acc_for_bst_trn_roc, 
				trn_prec_for_bst_trn_roc, tst_prec_for_bst_trn_roc, 
				trn_rec_for_bst_trn_roc, tst_rec_for_bst_trn_roc, 
				bst_trn_roc, tst_roc_for_bst_trn_roc ],
			 
			 [ bst_tst_roc_index, bst_tst_roc, 
				trn_acc_for_bst_tst_roc, tst_acc_for_bst_tst_roc, 
				trn_prec_for_bst_tst_roc, tst_prec_for_bst_tst_roc, 
				trn_rec_for_bst_tst_roc, tst_rec_for_bst_tst_roc, 
				trn_roc_for_bst_tst_roc, bst_tst_roc ],
			]
		
		df = pd.DataFrame(d, index = indices, columns = columns)
		
		print_func("-> " + estimator_name + " scores") 
		print_func(df, mode=__DISPLAY) # to format output similar to Jupyter's output
		
		# print(cv_res.keys())
	else:
		print_func("Estimator Type not specificed")
		print_separator()
		return
	
	print_separator()
	# print(cv_res.keys())
	
	return cv_res

def print_confusion_matrix(y_true, y_pred):
	"""Prints the confision matrix with columns and index labels

	Args:
		y_true (Union[ndarray, pd.Series]): Actual Response
		y_pred (Union[ndarray, pd.Series]): Predicted Response

	"""
	
	unique_classes = np.unique(y_true)
	unique_classes = sorted(unique_classes)
	if(-1 in unique_classes):
		unique_classes = sorted(unique_classes, reverse=True)
	
	cfm_i = pd.DataFrame(
				confusion_matrix(y_true, y_pred, labels=unique_classes))
	cfm_columns = []
	cfm_index = []
	# https://scikit-learn.org/stable/modules/generated/
	# sklearn.metrics.confusion_matrix.html
	#
	# List of labels to index the matrix. This may be used to reorder 
	# or select a subset of labels.
	# If none is given, those that appear at least once in y_true or 
	# y_pred are used in sorted order
	# 
	# As no labels are passed as args in the call to confusion_matrix 
	# then the classes are assigned on sorted order of unique values 
	# from response
	for each_class in unique_classes:
		cfm_columns.append("Predicted Class: " + str(each_class))
		cfm_index.append("Actual Class: " + str(each_class))
		
	cfm_i.columns = cfm_columns
	cfm_i.index = cfm_index
	print_func("-> Confusion Matrix")
	print_func(cfm_i,mode=__DISPLAY)

def plot_decision_boundary(x_axis_data, y_axis_data, response, estimator, 
							x_axis_column = None, y_axis_column = None):
	"""Plots the decision boundary

	

	Args:
		

	"""
	
	plt.figure(figsize=(12,6))
	plt.scatter( x_axis_data, y_axis_data, c=response, cmap=plt.cm.Paired )
	
	plt.xlabel(x_axis_column)
	plt.ylabel(y_axis_column)
		
	h = .02  # step size in the mesh
	# create a mesh to plot in
	x_min, x_max = x_axis_data.min() - 1, x_axis_data.max() + 1
	y_min, y_max = y_axis_data.min() - 1, y_axis_data.max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), 
		np.arange(y_min, y_max, h))

	# Plot the decision boundary. For that, we will assign a color to each
	# point in the mesh [x_min, m_max]x[y_min, y_max].
	Z = estimator.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.contour(xx, yy, Z, cmap=plt.cm.Paired)

def plot_roc_curve_binary_class(y_true, y_pred):
	"""Summary line.

	Extended description of function.

	Args:
		

	"""
	
	num_of_classes = len(np.unique(y_true))
	if(num_of_classes != 2):
		print("Number of classes should be equal to 2")
		return None
	
	fpr, tpr, thresholds = roc_curve(y_true, y_pred)
	roc_auc = roc_auc_score(y_true, y_pred)
	lw = 2
	plt.figure(figsize=(12,6))
	plt.plot(fpr, tpr, lw=2)
	
	# random predictions curve
	plt.plot([0, 1], [0, 1], linestyle='--', lw=lw)
	
	plt.xlim([-0.001, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver Operating Characteristic (area = %0.3f)' %roc_auc)
	
	return fpr, tpr, roc_auc

# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html
def plot_roc_curve_multiclass(estimator, X_train, X_test, y_train, y_test):
	"""Summary line.

	Extended description of function.

	Args:
		

	"""
	
	# converts 3 classes in one column to 3 columns binary matrix
	y_test = label_binarize(y_test, classes=classes)
	
	# get the total number of classes in y_test
	num_of_classes = y_test.shape[1]
	
	# Learn to predict each class against the other
	classifier = OneVsRestClassifier(estimator)
	
	# as of now found that SVM only has the decision_function implemented
	if hasattr(classifier, "decision_function"):
		y_test_pred = classifier.fit(X_train, 
									y_train).decision_function(X_test)
	else:
		y_test_pred = classifier.fit(X_train, y_train).predict_proba(X_test)
	
	# Compute ROC curve and ROC area for each class
	fpr = dict()
	tpr = dict()
	roc_auc = dict()
	for i in range(num_of_classes):
		fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_test_pred[:, i])
		roc_auc[i] = auc(fpr[i], tpr[i])

	# Compute micro-average ROC curve and ROC area
	fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), 
												y_test_pred.ravel())
	roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
	
	# First aggregate all false positive rates
	all_fpr = np.unique(
		np.concatenate([fpr[i] for i in range(num_of_classes)]) )

	# Then interpolate all ROC curves at this points
	mean_tpr = np.zeros_like(all_fpr)
	for i in range(num_of_classes):
		mean_tpr += interp(all_fpr, fpr[i], tpr[i])

	# Finally average it and compute AUC
	mean_tpr /= num_of_classes

	fpr["macro"] = all_fpr
	tpr["macro"] = mean_tpr
	roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

	# Plot all ROC curves
	# plt.figure()
	plt.figure(figsize=(12,6))
	plt.plot(fpr["micro"], tpr["micro"],
			 label='micro-average ROC curve (area = {0:0.2f})'
				   ''.format(roc_auc["micro"]),
			 color='deeppink', linestyle=':', linewidth=4)

	plt.plot(fpr["macro"], tpr["macro"],
			 label='macro-average ROC curve (area = {0:0.2f})'
				   ''.format(roc_auc["macro"]),
			 color='navy', linestyle=':', linewidth=4)

	colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])
	lw = 2
	
	for i, color in zip(range(num_of_classes), colors):
		plt.plot(fpr[i], tpr[i], color=color, lw=lw,
				 label='ROC curve of class {0} (area = {1:0.2f})'
				 ''.format(classes[i], roc_auc[i]))
	
	plt.plot([0, 1], [0, 1], 'k--', lw=lw)
	plt.xlim([-0.001, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Extension of ROC to multi-class')
	plt.legend(loc="lower right")
	plt.show()

def __get_inlier_outlier_info__(df, target_column):
	inliers = df[df[target_column] == 1]
	outliers = df[~(df[target_column] == 1)]
	print_func("-> Inliers and Outliers in the dataframe")
	
	pct_inliers = (inliers.shape[0]/df.shape[0])*100
	pct_outliers = (outliers.shape[0]/df.shape[0])*100
	print_func("-> Inlier Count: " + str(inliers.shape[0]) +
			", Pct: " +  str( round(pct_inliers, 2) ) )
	print_func("-> Outlier Count: " + str(outliers.shape[0]) +
				", Pct: " +  str( round(pct_outliers, 2) ) )
	
	return inliers, outliers

def do_outlier_detection(df, target_column, outlier_classes, 
						method, **kwargs):
	
	predictor_columns = df.columns[~df.columns.isin([target_column])]
	
	# copy of dataframe
	df = df.copy()
	
	# convert target column to str type
	df[target_column] = df[target_column].astype('str')
	
	# assign all values that are outliers as -1
	for outlier_class in outlier_classes:
		df.loc[(df[target_column] == str(outlier_class)), target_column] = -1
	
	# assign the rest as inliers
	df.loc[~(df[target_column] == -1), target_column] = 1
	
	# get inlier and outlier class and sort in descending order
	# for classification report
	unique_classes = sorted(np.unique(df[target_column]), reverse=True)
	
	if(method == 'OneClassSVM'):
		print_func("-> Using " + method +" for Outlier Detection")
		print_new_line()
		inliers, outliers = __get_inlier_outlier_info__(df, target_column)
		# inliers = df[df[target_column] == 1]
		# outliers = df[~(df[target_column] == 1)]
		# print_func("-> Separating Inliers and Outliers")
		
		# pct_inliers = (inliers.shape[0]/df.shape[0])*100
		# pct_outliers = (outliers.shape[0]/df.shape[0])*100
		# print_func("-> Inlier Count: " + str(inliers.shape[0]) +
				# ", Pct: " +  str( round(pct_inliers, 2) ) )
		# print_func("-> Outlier Count: " + str(outliers.shape[0]) +
					# ", Pct: " +  str( round(pct_outliers, 2) ) )

		del inliers[target_column]
		del outliers[target_column]
		
		classifier = svm.OneClassSVM(kernel=kwargs['kernel'], nu=kwargs['nu'], 
									gamma='scale')
		classifier.fit(inliers)

		inlier_pred = classifier.predict(inliers)
		error_inlier_pred = inlier_pred[inlier_pred == -1].size
		pct_error_inlier_pred = (error_inlier_pred/inliers.shape[0]) * 100
		print_func("-> Error Inlier Pred (inliers classified as outliers):" + 
			str(error_inlier_pred) + ", Percentage Error: " + 
			str( round(pct_error_inlier_pred,2) ))

		outlier_pred = classifier.predict(outliers)
		error_outlier_pred = outlier_pred[outlier_pred == 1].size
		pct_error_outlier_pred = (error_outlier_pred/outliers.shape[0]) * 100
		print_func("-> Error Outlier Pred (outliers classified as inliers):" + 
						str(error_outlier_pred) + ", Percentage Error: " + 
						str( round(pct_error_outlier_pred,2) ))
		
		print_separator()
		
		y_true = df[target_column]
		y_pred = classifier.predict(df[predictor_columns])
		
		print_func("-> Predict on Entire Data")
		print_confusion_matrix(y_true, y_pred)
		print_separator()
		
		print_func("-> Classification Report after Predict on Entire Data")
		print_new_line()
		print(classification_report(y_true, y_pred, labels=unique_classes))
		print_separator()
		
		if(len(predictor_columns) == 2):
			print_func("-> Decision Boundary")
			plot_decision_boundary(df[predictor_columns[0]], 
								df[predictor_columns[1]], 
								df[target_column], classifier,
								predictor_columns[0],
								predictor_columns[1])
		return classifier
	elif(method == 'EllipticEnvelope'):
		print_func("-> Using " + method +" for Outlier Detection")
		print_new_line()
		inliers, outliers = __get_inlier_outlier_info__(df, target_column)
		
		X, y = get_X_and_y(df, target_column)
		y_true = y
		
		classifier = EllipticEnvelope(contamination=kwargs['contamination'])
		classifier.fit(X)
		y_pred = classifier.predict(X)
		
		print_func("-> Predict on Entire Data")
		print_confusion_matrix(y_true, y_pred)
		print_separator()
		
		print_func("-> Classification Report after Predict on Entire Data\n")
		print_func(
				classification_report(
							y_true, y_pred, labels=unique_classes))
		print_separator()
		
		if(len(predictor_columns) == 2):
			print_func("-> Decision Boundary (Entire Data)")
			plot_decision_boundary(X[predictor_columns[0]], 
									X[predictor_columns[1]], 
									y, classifier, 
									predictor_columns[0],
									predictor_columns[1])
		return classifier
	elif(method == 'IsolationForest'):
		print_func("-> Using " + method +" for Outlier Detection")
		print_new_line()
		inliers, outliers = __get_inlier_outlier_info__(df, target_column)
		
		X, y = get_X_and_y(df, target_column)
		X_train, X_test, y_train, y_test = train_test_split(X, y, 
															random_state=42)
		classifier = IsolationForest(behaviour='new', 
									random_state=42, 
									contamination=kwargs['contamination'])
		classifier.fit(X_train)
		y_test_pred = classifier.predict(X_test)
		
		print_func("-> Predict on Test Data")
		print_confusion_matrix(y_test, y_test_pred)
		print_separator()
		
		print_func("-> Classification Report after Predict on Test Data\n")
		print_func(
				classification_report(
							y_test, y_test_pred, labels=unique_classes))
		print_separator()
		
		if(len(predictor_columns) == 2):
			print_func("-> Decision Boundary (Test Data)")
			plot_decision_boundary(X_test[predictor_columns[0]], 
									X_test[predictor_columns[1]], 
									y_test, classifier, 
									predictor_columns[0],
									predictor_columns[1])
		return classifier
	elif(method == 'LocalOutlierFactor'):
		print_func("-> Using " + method +" for Outlier Detection")
		print_new_line()
		inliers, outliers = __get_inlier_outlier_info__(df, target_column)
		
		X, y = get_X_and_y(df, target_column)
		classifier = LocalOutlierFactor(n_neighbors=kwargs['n_neighbors'],
										contamination=kwargs['contamination'])
		y_pred = classifier.fit_predict(X)
		
		print_func("-> Predict on Test Data")
		print_confusion_matrix(y, y_pred)
		print_separator()
		
		print_func("Classification Report after Predict on Test Data")
		print_new_line()
		print_func(classification_report(y, y_pred, labels=unique_classes))
		
		if(len(predictor_columns) != 2):
			return classifier
		
		print_separator()
		print_func("-> Detected Outliers Visualization")
		
		n_errors = (y_pred != y).sum()
		# X_scores = classifier.negative_outlier_factor_
		X['Scores'] = classifier.negative_outlier_factor_
		
		if('threshold_for_visualization' not in kwargs):
			threshold_for_visualization = -2
		else:
			threshold_for_visualization = (
					kwargs['threshold_for_visualization'] )
		
		print_func("--> Inliers tend to have a LOF score close to 1 " + 
					" (negative_outlier_factor_ close to -1)")
		
		print_func("--> Threshold For Outlier Visualization is: " + 
					str(threshold_for_visualization))
		
		outlier_boolean_mask = (X['Scores'] < threshold_for_visualization)
		
		number_of_outliers = (X[ outlier_boolean_mask ] ).shape[0]
		print_func("--> Points lower than threshold (Outliers): " +
					str(number_of_outliers))
		
		number_of_inliers = X.shape[0] - number_of_outliers
		
		print_func("--> Points greater than or equal to threshold " +
					"(Inliers): " +	str(number_of_inliers))
		
		X_temp = X.sort_values(by='Scores')
		
		X_temp_outliers = (
			X_temp[X_temp['Scores'] < threshold_for_visualization] )
		X_temp_inliers = (
			X_temp[~(X_temp['Scores'] < threshold_for_visualization)] )
		
		if(X_temp_inliers.shape[0] == 0):
			print_func("--> No Inliers Found")
			return classifier
		
		inlier_starting_score = X_temp_inliers.iloc[0]['Scores']
		print_func("--> Starting Score of Inliers: " + 
					str(inlier_starting_score))
		
		# negative_outlier_factor_ may have large variance between
		# outlier and inlier score which causes an issue with visualization.
		# Resetting the values to a much lower range allows for 
		# outliers to be circled red
		# Limit resetting scores to not more than 2500 points
		# At 0.0002 steps for -50 will hit 0 in 2500 iterations
		# Most likely this will cause the outlier score to overlap
		# So ensure that outlier scores don't overlap with inlier scores
		# Stop the plot using stop_radius_plot
		step = 0.0002
		initial_start = -50
		stop_radius_plot = False
		for index, row in X_temp_outliers.iterrows():
			X.at[index, 'Scores'] = initial_start + step
			step = step + 0.02
			
			# note that these are negative values
			if(initial_start + step == 0 or 
					initial_start + step >= inlier_starting_score):
				stop_radius_plot = True
		
		X.loc[~outlier_boolean_mask, 'Scores'] = ([0] * number_of_inliers)
		
		X_scores = X['Scores']
		
		X_outliers_df = X[outlier_boolean_mask]
		
		print_func("--> Showing Outliers")
		plt.figure(figsize=(14,6))
		plt.scatter(X_outliers_df[predictor_columns[0]], 
					X_outliers_df[predictor_columns[1]], 
					color='k', 
					s=3, 
					label='Outlier points')
		plt.xlim([X[predictor_columns[0]].min() - 0.5, 
					X[predictor_columns[0]].max() + 1])
		plt.ylim([X[predictor_columns[1]].min(), 
					X[predictor_columns[1]].max()])
		# plt.axis('tight')
		plt.xlabel(predictor_columns[0])
		plt.ylabel(predictor_columns[1])
		legend = plt.legend(loc='upper left')
		plt.show()
		
		# for index, row in 
		# X_outliers_df[X_outliers_df[predictor_columns[0]]> 20].iterrows():
			# print("\n--")
			# print(index)
			# print(row)
			# print("**")
			# print(X.iloc[index])
			# print("--\n")
		
		if(stop_radius_plot):
			print_func("--> Currently, for LOF Visualization, " +
						"Calculated values are used instead of Scores " +
						"because negative_outlier_factor_ may have large " +
						"variance. When calculated values overlap with " +
						"threshold value or if more than 2500 outliers " +
						"exist then the plot is not shown")
			return classifier
		
		print_func("--> Showing Outliers and Data")
		plt.figure(figsize=(14,6))
		plt.scatter(X[predictor_columns[0]], 
					X[predictor_columns[1]], 
					color='k', 
					s=3, 
					label='Data points')
		
		scores_away_from_max = X_scores.max() - abs(X_scores)
		min_score_away_from_max = (abs(X_scores.max()) 
									- abs(X_scores.min()))
		
		# plot circles with radius proportional to the outlier scores
		# radius will be bigger when the difference between MAX and 
		# score of a point is high
		radius = (scores_away_from_max/min_score_away_from_max)
		
		plt.scatter(X[predictor_columns[0]], 
					X[predictor_columns[1]], 
					s=100 * radius, 
					edgecolors='r',
					facecolors='none', 
					label='Outlier scores')
		plt.axis('tight')
		plt.xlabel(predictor_columns[0] + "Prediction errors: %d" % (n_errors))
		plt.ylabel(predictor_columns[1])
		legend = plt.legend(loc='upper left')
		legend.legendHandles[0]._sizes = [10]
		legend.legendHandles[1]._sizes = [20]
		plt.show()
		
		return classifier

# def build_sup_model(X, y, algorithm, cv, **kwargs):
	# """Build a model 

	# Args:
		
	# Example:
		
	
	# """