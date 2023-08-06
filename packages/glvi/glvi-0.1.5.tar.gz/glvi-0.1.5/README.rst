glvi
============

glvi is a Python module for machine learning built on top of Scikit-learn and is distributed under the MIT license.

glvi was developed by Mr. Li for evaluating variable importance heterogeneity through a global model built on a large time-space scope.

**glvi 0.1.4 was not supporting Python 2.7 and Python 3.4.**
glvi 0.1.4 and later require Python 3.5 or newer.

glvi requires:

- Python (>= 3.5)
- NumPy (>= 1.11.0)
- SciPy (>= 0.17.0)
- Scikit-learn (>= 0.21.0)
User installation
~~~~~~~~~~~~~~~~~

If you already have a working installation of numpy, scipy, pandas and scikit-learn, the easiest way to install glvi is using ``pip``   ::
	
	pip install -U glvi

User guide
~~~~~~~~~~~~~~~~~

Compute local variable importance based on decrease in node impurity ::

	from glvi import todi
	r_t = todi.lovim(500, max_features=0.3, n_jobs=-1)
	r_t.fit(train_x, train_y)
	local_variable importance = r_t.compute_feature_importance(X,Y,partition_feature = partition_feature, norm=True,n_jobs=-1)

or compute local variable importance based on decrease in accuracy ::

	from glvi import meda
	r_m = meda.lovim(500, max_features=0.3, n_jobs=-1)
	r_m.fit(train_x, train_y_
	local_variable importance = r_m.compute_feature_importance(X,Y,partition_feature = partition_feature, norm=True,n_jobs=-1)
