'''
Algorithm based on  decrease in accuracy
'''
import numpy as np
import pandas as pd
from pandas.core.series import Series
from pandas.core.frame import DataFrame
from sklearn.ensemble import RandomForestRegressor
from numpy import float64
from sklearn.utils._joblib import Parallel, delayed
from sklearn.utils.fixes import _joblib_parallel_args
from numpy.random import permutation
from numpy import vstack,mean,square,array,zeros
class lovim(RandomForestRegressor):
    '''
        This class completely inherit scikit-learn's RandomForestRegressor.
        I provide two additional function to compute local variable importance
         importance. One is compute_feature_importance and another is traverse
         which helps compute_feature_importance to traverse every tree in the forest.
    '''

    def __init__(self,
                 n_estimators='warn',
                 criterion="mse",
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.,
                 max_features="auto",
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 min_impurity_split=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        '''
            These parameters are completely same with the class 'RandomForestRegressor', you can
            refer to the help document of sklearn for more detailed information.
        '''
        super(lovim, self).__init__(
            n_estimators=n_estimators,
            criterion=criterion,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            min_weight_fraction_leaf=min_weight_fraction_leaf,
            max_features=max_features,
            max_leaf_nodes=max_leaf_nodes,
            min_impurity_decrease=min_impurity_decrease,
            min_impurity_split=min_impurity_split,
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start)
        self.verbose = verbose
        self.n_estimators = n_estimators # trees
    def compute_feature_importance(self, x, y, partition_feature = None, norm = True, n_jobs = None):
        '''
        :param x: input X of data and must be Pandas.core.frame.DataFrame or Pandas.core.series.Series
        :param y: input Y of data and do not need specify the type, but must be supported in numpy
        :param partition_feature: used for partitioning the data into local data subspaces and must
        be a column of data that can be hashed, but is optional. You can partition the data in advance
        instead and input feature subspace one by one.
        For example, if you want to compute local variable importance for each
        day, you only need to let partition_feature = day of year (1-365).
        Or input the feature subspace for each day one by one.
        :param norm: Yes or No normalise the output leading to the sum of each row equals to one..
        :param n_jobs: The number of jobs paralleling at the same time. Please refer to class Parallel
        in package sklearn for more detailed information.
        :return: local variable importance
        '''
        # to obtain the names of variables
        if not isinstance(x,Series) and not isinstance(x, DataFrame):
            raise TypeError("{0} must be pandas.core.frame.DataFrame or pandas.core.series.Series not {1}".format(x,type(x)))
        columns = x.columns
        # convert input X into numpy.array
        x = array(x, dtype=float64)
        # convert input Y to 1-D array
        y = array(y).ravel()
        # to obtain the number of variables
        self.FN = x.shape[1]
        # Produce data_choose array.This array contains bool values to choose rows for each feature subspace dataset
        if type(partition_feature) != type(None):
            partition_factor = list(partition_feature)
            # use set structure to extract factors
            partition_factor_set = set(partition_factor)
            partition_factor_list = list(partition_factor_set)
            # to obtain the number of group attribute
            self.FL = len(partition_factor_list)
            partition_factor_arr = np.array(partition_factor_list).reshape(self.FL, 1)
            # for each factor find out the rows of input group_by which is equal to it
            data_choose_bool = partition_factor_arr == partition_factor
        else:
            # if there is no group_by inputted, using all input rows
            self.FL = 1
            partition_factor_list = None
            data_choose_bool = np.ones((1, x.shape[0])) == 1
        # Parallel each tree. It is inherited from sklearn, you can refer to sklearn more detailed description.
        indicators = Parallel(n_jobs=n_jobs, verbose=self.verbose, max_nbytes='1M',
                              **_joblib_parallel_args(prefer='threads'))(
            delayed(self.__traverse__)(tree,x,y,data_choose_bool)
            for tree in self.estimators_) # traverse each tree in a forest
        feature_importance_trees = vstack(indicators) # Vertically stack the arrays returned by traverse forming a
        feature_importance_forest = np.average(feature_importance_trees, axis=0)  # To compute averaged feature importance
        if not isinstance(norm, bool):
            raise TypeError('{0} must be True or False not {1}'.format(norm, type(norm)))
        if norm :# whether standardise the output
            # sum up each row
            sum_of_feature_importance = feature_importance_forest.sum(axis=1).reshape(feature_importance_forest.shape[0], 1)
            # each one is divided by the sum of this row
            feature_importance_norm = feature_importance_forest / (sum_of_feature_importance+(sum_of_feature_importance == 0))
        else:
            # directly output without normalization
            feature_importance_norm = feature_importance_forest
        # return the result with the form of DataFrame
        return pd.DataFrame(feature_importance_norm, columns=columns, index=partition_factor_list)
    def __traverse__(self,tree,x,y,data_choose_bool):
        '''
        This function is to compute local variable importance for each feature subspace data set in one tree.
        It returns a 1*n_group*n_feature 3-d array containing the variable importance of all variables for each subspace.
        :param tree: tree in random forests
        :param x: X of input data
        :param y: Y of input data
        :param data_choose_bool: a array contains bool value used for selecting records if group_by
        is not None.
        :return:a 1*n_group*n_feature 3-d array containing the variable importance
        of all variables for each group
        '''
        # one-time getting the index for selecting records
        data_choose_index = [np.where(data_choose_bool_rows)[0] for data_choose_bool_rows in data_choose_bool]
        # permutating the index for selecting records
        permutated_choose_index = [permutation(data_choose_index_rows) for data_choose_index_rows in data_choose_index]
        # compute sum of squared error (sse) before permutation for each record so-called original error
        sse = square(y-tree.predict(x))
        # generate a array to contain the results
        tree_feature_importance_array = zeros((1, self.FL, self.FN))
        # traverse all subspace data sets
        for each_set in range(self.FL):
            # select records without permutation
            un_permutated_x = x[data_choose_index[each_set]]
            # select and permutate the records
            permutated_x_copy = x[permutated_choose_index[each_set]].copy()
            # select original sse for the specified feature subspace dataset
            sse_sp_set = sse[data_choose_index[each_set]]
            # select input Y
            chose_y = y[data_choose_index[each_set]]
            for feature_k in range(self.FN):
                un_permutated_x_copy = un_permutated_x.copy()
                # get X whose variable at index "index2" is permutated
                un_permutated_x_copy[:, feature_k] = permutated_x_copy[:, feature_k]
                # get sum of squared error after permutation for the specified feature subspace data set and feature k
                spse_sp_set_k = square(chose_y-tree.predict(un_permutated_x_copy))
                # the difference of mse before and after permutation is the variable importance for the
                TVI_set_k = mean(spse_sp_set_k - sse_sp_set)
                tree_feature_importance_array[0, each_set, feature_k] = TVI_set_k
        return tree_feature_importance_array
