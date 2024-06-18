# FairDream, GridSearch and Baseline models for fairness in binary classification - Benchmark over features of Census income dataset

To investigate the proper effects of  FairDream’s correction (distorted group attention through sample weights),  we compared it in a benchmark experiment with a closely related fairness method:	GridSearch [Agarwal et al., 2018], also an in-processing method of cost-sensitive classification. The full results of our experiment are accessible in this GitHub benchmark repository.

## Experimental conditions
We conducted the experiment over multiple types of models. To grant stability of the experiments, we selected the event predicted by the model (earning over $50,000 or not) for the threshold maximizing the F1-score, commonly used in machine-learning for imbalanced classification as in Census, and applied the default parameters below: 

:lemon: *Gradient boosted trees* using the XGBoost library: 1000 estimators, with the maximal depth of each tree being 3 splits on features – to keep on a binary model with general stables performances on tabular data for classification. 

:lemon: *Random forest trees* using the Scikit-learn library: 100 estimators, with the maximal depth of each tree being 3 splits on features – to introduce a lighter tree-based model.

:lemon: *Neural networks* using the PyTorch library to build a sequential model alternating linear layers (14, 1000) → (1000, 230) → (230, 2) and ReLU layers to break linearity.

:lemon: *Logistic regression* using the Scikit-learn library, with the “liblinear” solver, performing approximate minimization along coordinate directions – to introduce a simpler model in the benchmark.

For each type of model, a baseline model was trained with these default parameters, regardless of fairness objectives. Then to investigate the convergence of FairDream towards Equalized Odds, we analyzed the model through the lens of Demographic Parity, as if Demographic Parity was the initial fairness purpose set by lawmakers. When inequalities of overall positive rates were more than 3:1 across groups (e.g. eligible men for a loan = 42% vs 11% for women), we started a correction to mitigate gaps created by the model on that feature (e.g. sex). With  the  same  default  parameters  as  the  baseline  model,  GridSearch and FairDream tested new weights on 10 new models.	The goal of the competing models was to simultaneously maximize a global statistical criterion (ROC-AUC) and equalize the overall positive rates across groups (Demographic Parity). 

## How to read the results?
In this repository, you can read the results in the following way:

:star2: **For each feature** on which competition took place

 :arrow_forward: In "group_comparison/FEATURE_NAME_MODEL_TYPE"

You will find the plots of FairDream, GridSearch and the initial Baseline model to equalize between groups overall positive rates, true positive rates, false positive rates, AUCs (ROC and PR) and calibration errors (as areas to a perfectly calibrated curve). Take for instance the competition which happened for random forest on sex. The plots highlight FairDream to better equalize true and false positive rates between women and men than the Baseline and GridSearch models, **towards Equalized Odds**:

![rf_sex_equalized_odds](https://github.com/thomsouverain/weights_distortion_impact/blob/main/rf_sex_equalized_odds.png)

:star2: **Over all features**

"group_comparison" plots the differences between groups of a feature (e.g. women and men), which helps **visualize** the ways fairness methods treat them. We also introduced tables to **aggregate** the results on all features. We compared the models of FairDream, GridSearch and Baseline according to two ideas of fairness:

 :arrow_forward: "max_gap_groups -> fairness methods to compare"
 
 **Relative gap between groups** - which model was the worst to equalize groups? 

 We gave each model 1 bad point when it achieved the highest gap between the groups with the min-max scores. 

 :arrow_forward: "worst_group_score -> fairness methods to compare"
 
**Absolute rehabilitation**  – for the group with the lowest score, which model has the highest score? 

Indeed, it can be that a fairness method bridges the gap between groups, though, without necessarily enhancing the situation of the worst treated group. Therefore, relative and absolute counts on scores complement each other to compare our fairness methods. 

For instance, in "max_gap_groups -> GridSearch, FairDream", we see on 16 features of XGBoost, random forests and logistic regression where correction took place (the results on neural networks being non significant, as FairDream and GridSearch implemented random classifiers to reach perfect Demographic Parity), the performances of GridSearch and FairDream when set the task of equalizing overall positive rates (corresponding to Demographic Parity). 

Whereas on the side of Demographic Parity, GridSearch better equalizes the overall positive rates (FairDream corresponding to the highest gaps between groups in 9/16 cases), this relation reverses for true and false positive rates. Over all features, FairDream achieves better results to equalize false positive rates and, more, true positive rates (GridSearch reaching the highest gaps on 10/16 features):


|                | **all_metrics** | **calibration_error** | **roc_auc** | **pr_auc** | **overall_positive rate** | **false_positive rate** | **true_positive rate** |
| -------------- | --------------- | --------------------- | ----------- | ---------- | ------------------------- | ----------------------- | ---------------------- |
| **GridSearch** | 57              | 8                     | 11          | 12         | 7                         | 9                       | 10                     |
| **FairDream**  | 35              | 8                     | 3           | 2          | 9                         | 7                       | 6                      


Our plots and tables confirm that **on the contrary to a state-of-the-art fairness method** during processing like GridSearch, **FairDream**, initially set for Demographic Parity, performs in a direction which rather satisfies **Equalized Odds**.
