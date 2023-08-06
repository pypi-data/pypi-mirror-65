# task_substitution
> Solve an auxiliary task using ML.


**This library is created by using [nbdev](https://github.com/fastai/nbdev), please check it out.**

**Task Substitution** is a method of solving an auxiliary problem ( with different features and different target ) in order to better understand the initial problem and solving it efficiently. 

Let's take a look at standard machine learning task, in the figure below you see a regression task with features `f1`, `f2`, `f3` and target variable `y`.

<img src="images/training_set.png">

We want to build on a model on the above dataset to predict for unknown `y` values in the test dataset shown below.

<img src="images/test.png">

**Exploratory Data Analysis**

First step we take to solve the problem is to look at the data, there can be many features with *missing values* or *outliers* which needs to be understood. It is possible that there is a relationship between a missing value and values of other features.

## Recover Missing Values

It is possible for a feature to have a missing value, it could be a data recording issue or bug etc. Often times for numerical features we replace missing value with `mean` or `median` value as a approximation. Sometimes we replace missing value with values like `-9999` so that model treats them differently or sometimes we leave them as is as libraries like `xgboost` and `lightgbm` can handle `nulls`. Let's look at following dataset

<img src="images/missing_full.png">

Here we have a feature `f3` with missing values, this is a numerical feature, what we can do is that we can consider `f3` as target feature and reframe this as regresion problem where we try to predict for missing values.

<img src="images/missing_train.png">

<img src="images/missing_test.png">

The above setup is identical to the original regression task, here we would build a model to use `f1` and `f2` to predict for `f3`. So instead of using `mean`, `median` etc. we can build a model to restore missing values which can help us solve the original problem efficiently.

We have to be careful to not overfit when building such models.

## Check Train Test Distributions

Whenever we train a model we want to use it on a new sample, but what if the new sample comes from a different distribution compared to the data on which the model was trained on. When we deploy our solutions on production we want to be very careful of this change as our models would fail if there is a mismatch in train and test sets. We can pose this problem as an auxiliary task and create a new binary target `y`, where `1` represents whether row comes from `test` set and `0` represents whether it comes from `train` set and then we train our model to predict whether a row comes from `train` or `test` set if the performance ( e.g. `AUC` score ) is high we can conclude that the train and test set come from different distributions. Ofcourse, we need to remove the `original target` from the analysis.

<img src="images/ttm_train.png">

<img src="images/ttm_test.png">

**In the above images you can see two different datasets, we want to verify whether these two come from same distributions or not.** 

Consider the first example set as training set and second one as test set for this example.

<img src="images/ttm_train_with_target.png">

<img src="images/ttm_test_with_target.png">

We create a new target called `is_test` which denotes whether a row belongs to test set or not.

<img src="images/ttm_train_test_combined.png">

**Then we combine training and test set and train a model to predict whether a row comes from train or test set, if our model performs well then we know that these two datasets are from different distributions.**

We would still have to dig deep into looking at whether that's the case but the above method can help identifying which features are have drifted apart in train and test datasets. If you look at feature importance of the model that was used to separated train and test apart you can identify such features.


## Feature Selection using Null Importance

Often we create many features to enhance the power of our ML model, but not all features are beneficial to model performance. There needs to be a way to identify
features which can introduce `noise` to the model and hence must be removed. We can make use of `null importance` to identify and remove such features.

- Use LightGBM model to train on all features and obtain feature importance ( gain ), call it gain_1
- For the same data shuffle the target variable and train model and obtain feature importance ( gain ), call it gain_2
- Calculate ratio = gain_2 / gain_1 and remove features with ratio > 3.
- Use the remaining features to train the model again.

**Note: The ratio threshold of `3` seems arbitrary here, but we can treat this as `hyper-parameter` and choose the value that gives us the best result on the CV.**

Dataframe representing feature importance of useful, useless model and their ratio.
<img src="images/feature_imp.png">

## Feature Importance

Gradient Boosting Trees are very powerful methods when it comes to solving problems in industry and often are the first choice of every practitioner. We often to look at feature importance which different implementations of GBDT provide in help us understanding what features are useful. But during the inference when we have to predict for an unseen example, e.g. in a classification task if our model spits out `0` or `1` it would be useful to know which features were instrumental in identifying it as positive or negative class. This formulation can be extended to multi-classification and regression problems.

- This module implements this [paper](http://www.cs.sjtu.edu.cn/~kzhu/papers/kzhu-infocode.pdf)
- It currently supports XGBoost model and will soon support other implementations.
- We just pass our trained model and it converts the tree representation into a dataframe.
<img src="images/trees_to_df.png">
- Then we calculate score for each node of the tree where we start off from the terminal node and then propagate it up to the root node.
<img src="images/feature_contribution.png">


## Install

task_substitution in on pypi:

```
pip install task_substitution
```

For an editable install, use the following:

```
git clone https://github.com/numb3r33/task_substitution.git
pip install -e task_substitution
```

## How to use

**Recover Missing Values**

>Currently we only support missing value recovery for numerical features, we plan to extend support for other feature types as well. Also the model currently uses LightGBM model to recover missing values.

```
from task_substitution.recover_missing import *
from sklearn.metrics import mean_squared_error

train = train.drop('original_target', axis=1)

model_args = {
          'objective': 'regression',
          'learning_rate': 0.1,
          'num_leaves': 31,
          'min_data_in_leaf': 100,
          'num_boost_round': 100,
          'verbosity': -1,
          'seed': 41
             }
             
split_args = {
    'test_size': .2,
    'random_state': 41
}

# target_fld: feature with missing values.
# cat_flds: categorical features in the original dataset.
# ignore_flds: features you want to ignore. ( these won't be used by LightGBM model to recover missing values)

rec = RecoverMissing(target_fld='f3',
                     cat_flds=[],
                     ignore_flds=['f2'],
                     perf_fn=lambda tr,pe: np.sqrt(mean_squared_error(tr, pe)),
                     split_args=split_args,
                     model_args=model_args
                    )

train_recovered = rec.run(train)
```

**Check train test distributions**

>We use LightGBM model to predict whether a row comes from test or train distribution.

```
import lightgbm as lgb
from task_substitution.train_test_similarity import *
from sklearn.metrics import roc_auc_score

train = train.drop('original_target', axis=1)

split_args = {'test_size': 0.2, 'random_state': 41}

model_args = {
    'num_boost_round': 100,
    'objective': 'binary',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'nthread': -1,
    'verbosity': -1,
    'seed': 41
}

# cat_flds: categorical features in the original dataset.
# ignore_flds: features you want to ignore. ( these won't be used by LightGBM model )

tts = TrainTestSimilarity(cat_flds=[], 
                          ignore_flds=None,
                          perf_fn=roc_auc_score,
                          split_args=split_args, 
                          model_args=model_args)
tts.run(train, test)

# to get feature importance
fig, ax = plt.subplots(1, figsize=(16, 10)
lgb.plot_importance(tts.trained_model, ax=ax, max_num_features=5, importance_type='gain')
```

**Feature Selection using Null Importance**

>We use LightGBM model to remove features based on null importance.

```
from sklearn.datasets import load_boston
data = load_boston()

X = pd.DataFrame(data['data'], columns=data['feature_names'])
y = pd.Series(data['target'])

model_args = {
    'num_boost_round': 300,
    'objective': 'regression',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'nthread': -1,
    'verbosity': -1,
    'seed': 41
}

print(f'Feature list: {X.columns.tolist()}')
fs = FeatureSelection(model_args)
selected_features = fs.select_features(X, y)
print(f'Selected features: {selected_features}')

# ratio of feature importance of useless / useful model
print(fs.ratio_df)
```

**Feature Importance for GBDT**

>Make your GBDT more explainable by calculating feature contribution that reveals the relationship between specific instance and related output. Now in addition to global feature importance we can breakdown our predictions and find out which features played positive or negative role during inference.

```
x,y = make_regression(n_samples=1000,n_features=6,n_informative=3)
xtr, xval, ytr, yval = train_test_split(x, y, test_size=0.5, random_state=41)

model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=10, max_depth=4)
model.fit(xtr,ytr)

lfi     = LocalFeatureImportance(model)
scores  = lfi.propagate_scores()

si = pd.DataFrame(xval[5:6, :], columns=['f0', 'f1', 'f2', 'f3', 'f4', 'f5'])
fc = lfi.get_fi(scores, si)
```


## Contributing

If you want to contribute to `task_substitution` please refer to [contributions guidelines](./CONTRIBUTING.md)
