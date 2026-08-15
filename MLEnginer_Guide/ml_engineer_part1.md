# Machine Learning Engineer 200 Interview Questions & Answers - Part 1

This is Volume 1 of the Machine Learning Engineer Interview Preparation Guide, containing **Questions 1 to 100**. It covers Mathematical Foundations, Optimizers, Loss Functions, Classical ML, Deep Learning, and Transformer Architecture details tailored to crack Google ML Engineer technical interviews.

---

## 📋 Table of Contents (Part 1)
1. [ML Fundamentals & Mathematical Foundations (Q1 - Q30)](#1-ml-fundamentals--mathematical-foundations-q1---q30)
2. [Classical Machine Learning & Feature Engineering (Q31 - Q60)](#2-classical-machine-learning--feature-engineering-q31---q60)
3. [Deep Learning & Transformer Architectures (Q61 - Q100)](#3-deep-learning--transformer-architectures-q61---q100)

---

## 1. ML Fundamentals & Mathematical Foundations (Q1 - Q30)

#### Q1: Explain the Bias-Variance Tradeoff mathematically and conceptually.
**Answer:**
Expected Generalization Error of a model can be decomposed into three components:
$$\text{Expected Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}$$
*   **Bias**: Error introduced by approximating a complex real-world problem with a simplified model (High Bias $\rightarrow$ Underfitting).
*   **Variance**: Model's sensitivity to small fluctuations in the training dataset (High Variance $\rightarrow$ Overfitting).
*   **Irreducible Error**: Inherent noise in the data/target mapping.

#### Q2: What is Gradient Descent? Differentiate Batch GD, Stochastic GD (SGD), and Mini-Batch GD.
**Answer:**
An iterative optimization algorithm that updates parameters $\theta$ in the opposite direction of the gradient of the loss function $\nabla_\theta L(\theta)$ multiplied by learning rate $\eta$:
$$\theta_{t+1} = \theta_t - \eta \nabla_\theta L(\theta_t)$$
*   **Batch GD**: Computes gradient using the entire dataset per update (accurate, but slow/OOM on big data).
*   **SGD**: Computes gradient using a single random sample per update (fast, but noisy gradient paths).
*   **Mini-Batch GD**: Computes gradient over a small batch of $B$ samples (e.g., $B=32, 128$) balancing computational speed and gradient stability (industry standard).

#### Q3: Explain Momentum in SGD optimization.
**Answer:** Accumulates a exponentially decaying moving average of past gradients to accelerate velocity in directions of persistent gradient and damp oscillations:
$$v_{t} = \beta v_{t-1} + (1 - \beta) \nabla_\theta L(\theta_t)$$
$$\theta_{t+1} = \theta_t - \eta v_t$$

#### Q4: How does the Adam Optimizer work? Why is AdamW preferred over Adam for Transformer training?
**Answer:**
**Adam (Adaptive Moment Estimation)** maintains moving averages of both first moments (mean $m_t$) and second moments (uncentered variance $v_t$) of gradients:
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}, \quad \theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$
*   **AdamW**: Decouples L2 weight decay regularization from gradient updates. In standard Adam, L2 weight decay gets adapted by $\sqrt{v_t}$, weakening regularization for parameters with large historical gradients. AdamW subtracts weight decay directly: $\theta_{t+1} = \theta_{t+1} - \eta \lambda \theta_t$.

#### Q5: Compare L1 (Lasso) vs. L2 (Ridge) Regularization.
**Answer:**
*   **L1 Regularization (Lasso)**: Adds penalty $\lambda \sum |\theta_i|$ to loss function. Constrains parameter budget within a diamond-shaped L1 ball whose vertices lie on coordinate axes, driving less important weights strictly to **zero** (produces sparse models for feature selection).
*   **L2 Regularization (Ridge)**: Adds penalty $\lambda \sum \theta_i^2$. Constrains parameter budget within a smooth circular L2 sphere, shrinking weights toward zero without forcing them to exact zero.

#### Q6: Explain Cross-Entropy Loss mathematically.
**Answer:** Measures performance of a classification model whose output is a probability value between 0 and 1:
$$\text{Binary Cross-Entropy (BCE)} = -\frac{1}{N} \sum_{i=1}^N \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i) \right]$$
$$\text{Categorical Cross-Entropy (Multi-class)} = -\sum_{c=1}^C y_{i,c} \log(\hat{y}_{i,c})$$

#### Q7: What is Focal Loss, and why is it used for class imbalance in object detection?
**Answer:** Modifies standard Cross-Entropy loss by adding a modulating factor $(1 - p_t)^\gamma$ to down-weight easy, well-classified background examples, allowing model training to focus heavily on hard negative/positive examples:
$$\text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)$$

#### Q8: What is Triplet Loss in Metric Learning?
**Answer:** Used to learn embeddings such that an Anchor ($A$) is closer to a Positive example ($P$) than to a Negative example ($N$) by a margin $\alpha$:
$$L(A, P, N) = \max \left( 0, \|f(A) - f(P)\|^2 - \|f(A) - f(N)\|^2 + \alpha \right)$$

#### Q9: What is the Vanishing and Exploding Gradient Problem?
**Answer:**
During backpropagation through deep networks or unrolled RNNs, gradients are computed using the chain rule $\prod \frac{\partial h_t}{\partial h_{t-1}}$.
*   If layer weight eigenvalues $< 1$, gradients decay exponentially to 0 (Vanishing), causing early layers to stop learning.
*   If layer weight eigenvalues $> 1$, gradients grow exponentially to infinity (Exploding), causing numerical instability/`NaN` weights.
*   *Fixes*: Residual connections (Skip connections), Layer Normalization, Gradient Clipping, ReLU/GELU activations, proper weight initialization (He/Xavier).

#### Q10: What is Gradient Clipping?
**Answer:** A technique to prevent exploding gradients by capping gradient norms to a maximum threshold $c$:
$$\text{if } \|g\| > c \implies g \leftarrow c \cdot \frac{g}{\|g\|}$$

#### Q11: Explain Xavier (Glorot) vs. He (Kaiming) Weight Initialization.
**Answer:**
*   **Xavier Initialization**: Sets weights from distribution with variance $\text{Var}(W) = \frac{2}{n_{in} + n_{out}}$. Designed for symmetric activation functions with linear regimes (Tanh, Sigmoid).
*   **He (Kaiming) Initialization**: Sets weights from distribution with variance $\text{Var}(W) = \frac{2}{n_{in}}$. Designed for asymmetric non-linear activation functions (ReLU, Leaky ReLU).

#### Q12: What is the Curse of Dimensionality?
**Answer:** As the number of feature dimensions grows, the volume of feature space grows exponentially, making data points extremely sparse. Distance metrics (Euclidean distance) become equidistant between all pairs of points, degrading clustering and classification algorithms.

#### Q13: Explain Eigenvalues and Eigenvectors in Principal Component Analysis (PCA).
**Answer:**
PCA finds orthogonal axes of maximum variance in high-dimensional data.
*   The **Covariance Matrix** $C = \frac{1}{N} X^T X$ is decomposed into $C v = \lambda v$.
*   **Eigenvectors** ($v$) define the directions of the principal component axes.
*   **Eigenvalues** ($\lambda$) quantify the amount of data variance captured along each corresponding eigenvector axis.

#### Q14: What is Singular Value Decomposition (SVD)?
**Answer:** Factorizes any $m \times n$ matrix $A$ into three matrices:
$$A = U \Sigma V^T$$
Where $U$ contains left-singular vectors (data points in feature space), $\Sigma$ is a diagonal matrix of singular values, and $V^T$ contains right-singular vectors (feature loadings). Used in PCA, matrix factorization for recommender systems, and LSA.

#### Q15: Explain Precision, Recall, F1-Score, and ROC-AUC.
**Answer:**
*   $\text{Precision} = \frac{TP}{TP + FP}$: Proportion of positive identifications that were actually correct (low FP).
*   $\text{Recall} = \frac{TP}{TP + FN}$: Proportion of actual positives identified correctly (low FN).
*   $\text{F1-Score} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$: Harmonic mean of precision and recall.
*   **ROC-AUC**: Area Under the Receiver Operating Characteristic Curve (plotting True Positive Rate vs False Positive Rate across all decision thresholds). Measures model ranking capability independent of threshold choice.

#### Q16: When should you prefer PR-AUC (Precision-Recall AUC) over ROC-AUC?
**Answer:** In highly imbalanced datasets (e.g., fraud detection where 0.01% of transactions are fraud). ROC-AUC can present an overly optimistic score because False Positive Rate $\frac{FP}{FP + TN}$ remains small due to huge $TN$ count. PR-AUC focuses strictly on positive class performance.

#### Q17: What is Maximum Likelihood Estimation (MLE)?
**Answer:** A method of estimating parameters $\theta$ of a probability distribution by maximizing the Likelihood function $L(\theta; X) = \prod_{i=1}^N P(x_i | \theta)$, or equivalently minimizing the negative log-likelihood $\sum -\log P(x_i | \theta)$.

#### Q18: Compare MLE (Maximum Likelihood Estimation) vs MAP (Maximum A Posteriori).
**Answer:**
*   **MLE**: Estimates parameters $\theta$ purely from observed data: $\hat{\theta}_{MLE} = \arg\max_\theta P(X | \theta)$.
*   **MAP**: Incorporates prior knowledge/distribution $P(\theta)$ via Bayes Rule: $\hat{\theta}_{MAP} = \arg\max_\theta P(X | \theta) P(\theta)$. L1 and L2 regularization correspond to MAP estimation using Laplace and Gaussian priors, respectively.

#### Q19: What is Kullback-Leibler (KL) Divergence?
**Answer:** Measures the asymmetric difference between two probability distributions $P(x)$ and $Q(x)$:
$$D_{KL}(P \parallel Q) = \sum_{x} P(x) \log \left( \frac{P(x)}{Q(x)} \right)$$
Used in Variational Autoencoders (VAEs) and RLHF policy alignment loss (PPO).

#### Q20: Explain Jensen's Inequality and its role in Machine Learning.
**Answer:** For a convex function $f$ and random variable $X$, $f(E[X]) \le E[f(X)]$. Forms the mathematical foundation for proving the convergence of the Expectation-Maximization (EM) algorithm and deriving the Evidence Lower Bound (ELBO) in VAEs.

#### Q21: What is Learning Rate Warmup, and why is it essential for Transformers?
**Answer:** Gradually increasing learning rate linearly from zero to peak rate during initial training steps (e.g., first 10,000 steps) before applying cosine decay. Prevents early gradient instability from destroying randomly initialized layer normalization and attention weights.

#### Q22: Explain the difference between Parametric vs. Non-Parametric Models.
**Answer:**
*   **Parametric Models**: Summarize data into a fixed number of parameters independent of training set size (e.g., Linear Regression, Logistic Regression, Neural Networks). Fast inference, fixed memory size.
*   **Non-Parametric Models**: Number of parameters grows with training data volume (e.g., k-Nearest Neighbors, Decision Trees, Kernel SVMs). Flexible, but higher inference memory cost.

#### Q23: What is Data Imbalance, and what techniques mitigate it?
**Answer:** When one target class significantly outnumbers others.
*   *Mitigation Strategies*:
    1.  **Resampling**: Oversampling minority class (SMOTE) or Undersampling majority class.
    2.  **Cost-Sensitive Learning**: Assigning higher class weights in loss functions.
    3.  **Focal Loss**: Down-weighting easy majority examples.
    4.  **Metric Selection**: Using PR-AUC and Macro F1-score instead of Accuracy.

#### Q24: Explain the difference between Bagging and Boosting.
**Answer:**
*   **Bagging (Bootstrap Aggregating)**: Trains multiple independent base estimators in parallel on random bootstrap subsets of data and averages predictions (reduces Variance, e.g., Random Forest).
*   **Boosting**: Trains base estimators sequentially where each new model focuses on errors/residuals made by previous models (reduces Bias, e.g., XGBoost, LightGBM).

#### Q25: What is Cosine Distance vs Euclidean Distance?
**Answer:**
*   **Euclidean Distance**: $d(u, v) = \sqrt{\sum (u_i - v_i)^2}$. Measures spatial magnitude difference.
*   **Cosine Similarity**: $\cos(\theta) = \frac{u \cdot v}{\|u\| \|v\|}$. Measures angle direction agreement between vectors, bounded between -1 and 1. Cosine Distance = $1 - \cos(\theta)$.

#### Q26: What is a Confusion Matrix? Derive TPR, FPR, PPV, and NPV.
**Answer:**
| | Predicted Positive | Predicted Negative |
|---|---|---|
| **Actual Positive** | True Positive (TP) | False Negative (FN) |
| **Actual Negative** | False Positive (FP) | True Negative (TN) |
*   **TPR (Sensitivty/Recall)** = $\frac{TP}{TP + FN}$
*   **FPR** = $\frac{FP}{FP + TN}$
*   **PPV (Precision)** = $\frac{TP}{TP + FP}$
*   **NPV** = $\frac{TN}{TN + FN}$

#### Q27: What is Stochastic Gradient Langevin Dynamics (SGLD)?
**Answer:** A Bayesian MCMC optimization algorithm that adds Gaussian noise to mini-batch gradients, allowing parameter sampling from the full posterior distribution rather than converging to a single point estimate.

#### Q28: What is Label Smoothing, and why does it prevent overconfidence?
**Answer:** Replaces hard one-hot target vectors ($[0, 1, 0]$) with softened distributions ($[0.05, 0.90, 0.05]$):
$$y_{smooth} = (1 - \epsilon) y_{one\_hot} + \frac{\epsilon}{K}$$
Prevents the final logit layer from pushing logit outputs to extreme infinity values, improving calibration and generalization.

#### Q29: Explain Empirical Risk Minimization (ERM) vs Structural Risk Minimization (SRM).
**Answer:**
*   **ERM**: Minimizes average loss purely over training samples: $\min_\theta \frac{1}{N} \sum L(f(x_i; \theta), y_i)$.
*   **SRM**: Minimizes empirical risk plus a capacity complexity penalty term (regularization $\lambda R(\theta)$) to bound generalization error via VC-dimension.

#### Q30: What is the Law of Large Numbers (LLN) and Central Limit Theorem (CLT)?
**Answer:**
*   **LLN**: As sample size $N$ approaches infinity, sample mean converges to population true mean $E[X]$.
*   **CLT**: As sample size $N$ becomes large ($N \ge 30$), distribution of sample means approaches a Normal (Gaussian) distribution regardless of original population shape.

---

## 2. Classical Machine Learning & Feature Engineering (Q31 - Q60)

#### Q31: Explain Logistic Regression and derive the Sigmoid function.
**Answer:** Logistic Regression models probability of binary output using Sigmoid activation applied to linear logit combinations $z = w^T x + b$:
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$
*   *Log-Odds*: $\log\left(\frac{p}{1-p}\right) = w^T x + b$.
*   *Optimization*: Parameters optimized via Binary Cross-Entropy using Gradient Descent (no closed-form solution exists).

#### Q32: How do Decision Trees split node boundaries? Compare Gini Impurity vs Entropy.
**Answer:** Decision trees evaluate candidate feature splits to maximize Information Gain.
*   **Gini Impurity**: $G = 1 - \sum_{i=1}^C p_i^2$ (computationally faster, default in scikit-learn).
*   **Entropy (Information Theory)**: $H = -\sum_{i=1}^C p_i \log_2(p_i)$ (information gain = $H_{parent} - H_{children}$).

#### Q33: Explain Random Forest and why it mitigates decision tree overfitting.
**Answer:** An ensemble Bagging method that builds $N$ independent decision trees using:
1.  **Bootstrap Sampling (Bagging)**: Each tree is trained on a random sample with replacement.
2.  **Random Subspace Method**: At each split node, only a random subset of $\sqrt{d}$ features is evaluated.
*   *Overfitting Mitigation*: Averaging across uncorrelated trees reduces overall variance without increasing bias: $\text{Var}_{ensemble} = \rho \sigma^2 + \frac{1-\rho}{N} \sigma^2$.

#### Q34: Explain Gradient Boosted Decision Trees (GBDT) and how XGBoost optimizes execution.
**Answer:** GBDT builds trees sequentially, where each new tree fits the pseudo-residuals (negative gradient of loss) of previous ensemble trees.
*   **XGBoost Optimizations**:
    1.  **Second-Order Taylor Expansion**: Uses both first gradients ($g_i$) and second-order Hessians ($h_i$) for split scoring.
    2.  **Regularization**: Includes $L1$ ($\alpha$) and $L2$ ($\lambda$) penalty terms on leaf weights.
    3.  **Column Block Sorting**: Parallelizes split searches across pre-sorted feature blocks.
    4.  **Sparsity Awareness**: Automatically handles missing data values.

#### Q35: Compare XGBoost vs. LightGBM vs. CatBoost.
**Answer:**
*   **XGBoost**: Level-wise (depth-wise) tree growth. High accuracy, robust, slightly slower training.
*   **LightGBM**: Leaf-wise tree growth with Histogram binning and Gradient-based One-Side Sampling (GOSS). Ultra-fast training on massive datasets.
*   **CatBoost**: Symmetric tree structure with Ordered Target Statistics. Exceptionally fast out-of-the-box handling of categorical features without manual encoding.

#### Q36: Explain K-Means Clustering and its key limitations.
**Answer:** An unsupervised partition algorithm that minimizes Within-Cluster Sum of Squares (WCSS):
1.  Initialize $K$ cluster centroids randomly.
2.  Assign each data point to nearest centroid.
3.  Recompute centroids as mean of assigned points. Repeat until convergence.
*   *Limitations*: Must pre-specify $K$, sensitive to initial centroid placement (mitigated by K-Means++), struggles with non-spherical clusters or varying cluster densities.

#### Q37: What is DBSCAN (Density-Based Spatial Clustering of Applications with Noise)?
**Answer:** A density-based clustering algorithm that groups points exceeding core density thresholds (`eps` radius and `minPts` count).
*   *Advantages*: Does not require pre-specifying cluster count $K$, discovers arbitrary non-spherical cluster shapes, identifies outliers as noise points.

#### Q38: Explain Support Vector Machines (SVM) and the Kernel Trick.
**Answer:** SVM finds a maximum-margin hyperplane separating binary classes by maximizing margin distance $\frac{2}{\|w\|}$ subject to $y_i(w^T x_i + b) \ge 1$.
*   **Kernel Trick**: Computes inner products in a high-dimensional feature space $\langle \phi(x), \phi(z) \rangle = K(x, z)$ directly using kernel functions (RBF, Polynomial) without explicitly calculating high-dimensional transformations $\phi(x)$.

#### Q39: What is One-Hot Encoding vs. Ordinal Encoding vs. Target Encoding?
**Answer:**
*   **One-Hot Encoding**: Converts categorical levels into binary vector columns (causes dimensionality explosion for high-cardinality features).
*   **Ordinal Encoding**: Maps ordered categories to sequential integers (e.g., Low=1, Med=2, High=3).
*   **Target Encoding**: Replaces category levels with mean value of target variable for that category (requires smoothing and out-of-fold cross-validation to prevent target leakage).

#### Q40: What is Target Leakage, and how do you detect and prevent it?
**Answer:** Occurs when training features contain information about the target variable that will not be available at real-time inference (e.g., including `date_refund_issued` in a model predicting customer churn).
*   *Prevention*: Strict temporal train/test splitting, removing post-event attributes, auditing feature importance (unexpectedly high 0.99 AUC scores).

#### Q41: Explain SHAP (Shapley Additive exPlanations) values in Feature Importance.
**Answer:** A game-theoretic approach to model interpretability that calculates the marginal contribution of each feature across all possible feature combinations. Satisfies properties of Efficiency, Symmetry, Dummy, and Additivity.

#### Q42: What is Naive Bayes Classification, and why is it called "Naive"?
**Answer:** Applies Bayes' Theorem to predict class probability:
$$P(Y | X) \propto P(Y) \prod_{i=1}^d P(x_i | Y)$$
*   It is "Naive" because it assumes all features $x_i$ are conditionally independent given class label $Y$, an assumption rarely true in real data, yet performs surprisingly well for text classification (Spam filtering).

#### Q43: Write a Python scikit-learn pipeline for numeric scaling and categorical encoding.
**Answer:**
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, ['age', 'income', 'credit_score']),
    ('cat', cat_transformer, ['gender', 'occupation'])
])

clf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
```

#### Q44: What is K-Fold Cross-Validation vs. Stratified K-Fold?
**Answer:**
*   **K-Fold**: Splits dataset into $K$ equal folds; trains on $K-1$ folds and tests on remaining fold iteratively $K$ times.
*   **Stratified K-Fold**: Preserves target class percentage proportions in every fold (essential for imbalanced classification tasks).

#### Q45: What is t-SNE (t-Distributed Stochastic Neighbor Embedding) vs. UMAP?
**Answer:**
*   **t-SNE**: Non-linear dimensionality reduction technique for data visualization that maps high-dimensional distance probabilities to Student-t distributions in 2D/3D space. Preserves local structure well, but slow on large datasets and distorts global geometry.
*   **UMAP**: Based on Riemannian geometry; faster than t-SNE, preserves both local and global data topology better.

#### Q46: Explain Principal Component Analysis (PCA) step-by-step.
**Answer:**
1.  Standardize feature matrix $X$ (mean=0, variance=1).
2.  Compute Covariance Matrix $C = \frac{1}{N-1} X^T X$.
3.  Compute Eigenvalues and Eigenvectors of $C$.
4.  Sort Eigenvectors by descending Eigenvalue magnitude.
5.  Select top $k$ Eigenvectors to form projection matrix $W$.
6.  Project $X_{new} = X W$.

#### Q47: What is SMOTE (Synthetic Minority Over-sampling Technique)?
**Answer:** Generates synthetic samples for minority class by selecting a minority instance, finding its $k$-nearest minority neighbors, and creating synthetic points along the line segment connecting them:
$$x_{new} = x_i + \lambda (x_{neighbor} - x_i), \quad \lambda \sim U(0, 1)$$

#### Q48: What is Information Gain Ratio, and why does C4.5 use it over Information Gain?
**Answer:** Information Gain biases decision tree splits toward high-cardinality categorical features (e.g., `user_id`). Information Gain Ratio divides Information Gain by Intrinsic Info (split entropy) to normalize for feature level count.

#### Q49: What is Isolation Forest for Anomaly Detection?
**Answer:** An unsupervised algorithm that isolates anomalies by randomly selecting features and split values. Because anomaly points are rare and distinct, they require fewer recursive splits to isolate (have significantly shorter tree path lengths).

#### Q50: Explain VIF (Variance Inflation Factor) for Multicollinearity detection.
**Answer:** Measures how much variance of an estimated regression coefficient increases due to collinearity with other features:
$$\text{VIF}_i = \frac{1}{1 - R_i^2}$$
VIF values $> 5\text{--}10$ indicate severe multicollinearity requiring feature removal or PCA reduction.

#### Q51: Differentiate L1-based Feature Selection vs Recursive Feature Elimination (RFE).
**Answer:**
*   **L1-based Selection**: Fits Lasso model once; features with non-zero weights are selected.
*   **RFE**: Iteratively trains estimator model, ranks feature importances, prunes smallest importance feature, and retrains until specified target feature count remains.

#### Q52: What is the Elbow Method and Silhouette Score in K-Means clustering?
**Answer:**
*   **Elbow Method**: Plots WCSS against cluster count $K$; selects $K$ where rate of WCSS decrease sharply bends ("elbow").
*   **Silhouette Score**: Evaluates cluster separation quality per point: $s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$. Values closer to $+1$ indicate well-clustered data.

#### Q53: Explain Logistic Regression Cost Function derivation from NLL.
**Answer:** Likelihood for $N$ independent Bernoulli trials: $L(w) = \prod \hat{y}_i^{y_i} (1 - \hat{y}_i)^{1-y_i}$. Taking negative log yields Binary Cross-Entropy Loss $J(w) = -\frac{1}{N} \sum [y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i)]$.

#### Q54: What is Hierarchical Clustering (Agglomerative vs Divisive)?
**Answer:**
*   **Agglomerative (Bottom-Up)**: Starts with each point as its own cluster and recursively merges closest cluster pairs based on linkage (Single, Complete, Average, Ward) until one cluster remains.
*   **Divisive (Top-Down)**: Starts with one root cluster containing all data and recursively splits.

#### Q55: What is Data Leakage in Cross-Validation, and how do you prevent it?
**Answer:** Applying scaling (StandardScaler), imputation, or feature selection steps over the entire dataset BEFORE performing CV splits. *Prevention*: Wrap preprocessors and models inside `sklearn.pipeline.Pipeline` so fits occur strictly inside individual training CV folds.

#### Q56: Explain Quantile Transformer vs Power Transformer (Box-Cox / Yeo-Johnson).
**Answer:**
*   **Quantile Transformer**: Maps data to a uniform or normal distribution using empirical cumulative distribution functions (robust to outliers, distorts linear relationships).
*   **Power Transformer**: Parametric transformations designed to stabilize variance and map non-normal skewed data into Gaussian-like distributions.

#### Q57: What is Adaboost (Adaptive Boosting)?
**Answer:** Sequential ensemble algorithm that assigns weights to training data points. Misclassified points in iteration $t$ receive higher weights in iteration $t+1$, forcing subsequent weak decision tree stumps to focus on hard samples.

#### Q58: Explain ElasticNet Regularization.
**Answer:** Combines L1 and L2 penalties into a single objective function:
$$\mathcal{L}_{ElasticNet} = \mathcal{L} + \lambda \left( \alpha \sum |\theta_i| + \frac{1-\alpha}{2} \sum \theta_i^2 \right)$$
Balances feature sparsity (L1) with correlated feature group stability (L2).

#### Q59: What is Calibration Curve (Reliability Diagram) in classification models?
**Answer:** Plots predicted output probabilities against actual observed positive class frequencies. Models like SVMs or Naive Bayes output poorly calibrated probabilities requiring Sigmoidal (Platt Scaling) or Isotonic Regression recalibration.

#### Q60: Explain Multi-Task Learning (MTL) hard vs soft parameter sharing.
**Answer:**
*   **Hard Parameter Sharing**: Shared hidden layers across all tasks with task-specific output head layers (reduces overfitting).
*   **Soft Parameter Sharing**: Each task maintains its own network parameters, but parameter distance constraints ($L2$ distance) are enforced between task network parameters.

---

## 3. Deep Learning & Transformer Architectures (Q61 - Q100)

#### Q61: What is a Multilayer Perceptron (MLP)?
**Answer:** A feedforward artificial neural network consisting of an Input layer, one or more Hidden layers, and an Output layer, where every neuron in a layer is fully connected to the next layer via trainable weight matrices $W$ and bias vectors $b$ passed through non-linear activation functions $\sigma(W x + b)$.

#### Q62: Explain Backpropagation mathematically using Chain Rule.
**Answer:** Method used to compute error loss gradients with respect to every weight in a neural network:
For loss $L$, output $y = \sigma(z)$, and $z = w x + b$:
$$\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial z} \cdot \frac{\partial z}{\partial w}$$
Gradients are propagated backwards from output layer to input layer.

#### Q63: Compare Activation Functions: Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, SwiGLU.
**Answer:**
*   **Sigmoid**: $\frac{1}{1+e^{-x}}$. Saturated gradients at extremes cause vanishing gradients.
*   **Tanh**: Zero-centered version of Sigmoid ($[-1, 1]$).
*   **ReLU**: $\max(0, x)$. Fast execution, avoids vanishing gradients for $x>0$; suffers from "Dying ReLU" for $x \le 0$.
*   **Leaky ReLU**: $\max(\alpha x, x)$ with small $\alpha=0.01$ preventing dead neurons.
*   **GELU (Gaussian Error Linear Unit)**: $x \Phi(x)$. Smooth non-linear activation weighting inputs by their normal probability (standard in BERT, GPT-3).
*   **SwiGLU**: Swish-gated linear unit $SwiGLU(x) = Swish_\beta(x W) \otimes (x V)$. Standard activation in modern LLMs (Llama, PaLM).

#### Q64: What is Batch Normalization vs. Layer Normalization?
**Answer:**
*   **Batch Normalization (BatchNorm)**: Normalizes feature activations across the **batch dimension** $B$ for each feature channel. Highly effective in CNNs; fails when batch size is small or for variable sequence lengths.
*   **Layer Normalization (LayerNorm)**: Normalizes activations across the **feature channel dimension** $D$ for each individual sample independently. Standard in Transformers and NLP.

```
BatchNorm:   [Batch x Height x Width] -> Normalized per Channel
LayerNorm:   [Channels x Features]    -> Normalized per Sequence Sample
```

#### Q65: Explain Convolutional Neural Networks (CNNs) core operations: Convolutions, Stride, Padding, Pooling.
**Answer:**
*   **Convolution**: Sliding kernel filter $K$ performing element-wise multiplication over input image tensor.
*   **Stride**: Step size by which kernel slides across input matrix.
*   **Padding ('valid' vs 'same')**: Adding border rows/cols (usually zeros) to control spatial output dimension size.
*   **Pooling (Max/Average)**: Downsampling operation reducing spatial dimensions while retaining spatial translation invariance.

#### Q66: What is ResNet and why do Residual Connections (Skip Connections) work?
**Answer:** ResNet introduces skip connections that reformulate layer mapping as learning a residual function $F(x) = H(x) - x$, producing output $y = F(x) + x$.
*   *Why it works*: Direct linear skip connection allows gradients to flow directly during backpropagation without passing through weight multiplications ($\frac{\partial y}{\partial x} = \frac{\partial F}{\partial x} + 1$), eliminating vanishing gradients in deep 100+ layer networks.

#### Q67: Explain Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTM) cells.
**Answer:**
*   **RNN**: Processes sequential data maintaining hidden state $h_t = \tanh(W x_t + U h_{t-1})$. Suffers from vanishing gradients over long sequences.
*   **LSTM**: Solves vanishing gradients using a persistent **Cell State** ($C_t$) regulated by 3 gates:
    1.  **Forget Gate**: $f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$ (what to discard from cell state).
    2.  **Input Gate**: $i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$ (what new info to store).
    3.  **Output Gate**: $o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$ (what to output as hidden state $h_t$).

#### Q68: What is the Transformer Architecture, and why did it replace LSTMs?
**Answer:** Introduced in "Attention Is All You Need" (Vaswani et al., 2017).
*   *Why it replaced LSTMs*: LSTMs process sequences sequentially ($t_1 \to t_2 \to t_3$), preventing GPU parallelization. Transformers use Self-Attention over entire sequences simultaneously, enabling massive GPU/TPU parallel training.

#### Q69: Explain Self-Attention mathematically: Queries ($Q$), Keys ($K$), and Values ($V$).
**Answer:**
Given input embedding sequence $X$, linear projections create $Q = X W_Q$, $K = X W_K$, $V = X W_V$:
$$\text{Attention}(Q, K, V) = \text{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V$$
*   $Q K^T$: Calculates pairwise similarity dot products between all token pairs.
*   $\sqrt{d_k}$: Scaling factor preventing dot product values from growing overly large in high dimensions (which would cause Softmax gradients to saturate).
*   $\text{Softmax}(\dots)$: Converts similarity scores to attention weight probabilities summing to 1.
*   $\dots V$: Computes weighted sum of value vectors.

#### Q70: What is Multi-Head Attention (MHA)?
**Answer:** Splits Query, Key, and Value projections into $h$ parallel sub-spaces ("heads"), allowing model to simultaneously attend to information from different representation positions and aspects (e.g., syntactic vs semantic relationships):
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W_O$$

#### Q71: Compare Encoder-Only vs Decoder-Only vs Encoder-Decoder Transformers.
**Answer:**
*   **Encoder-Only (BERT, RoBERTa)**: Uses bidirectional self-attention. Excellent for classification, extraction, and embedding generation.
*   **Decoder-Only (GPT-4, Llama, PaLM)**: Uses causal masked self-attention (tokens can attend only to preceding left tokens). Standard for autoregressive text generation.
*   **Encoder-Decoder (T5, BART)**: Encoder processes full source input bidirectionally; Decoder generates output sequence using cross-attention over encoder outputs. Standard for translation and summarization.

#### Q72: What is Causal Masking in Transformer Decoders?
**Answer:** Setting upper-triangular matrix entries in attention score matrix $Q K^T$ to $-\infty$ before Softmax, ensuring token position $i$ cannot attend to future tokens $j > i$ during autoregressive training.

#### Q73: Write PyTorch code for Scaled Dot-Product Self-Attention.
**Answer:**
```python
import torch
import torch.nn as nn
import math

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k):
        super().__init__()
        self.scale = 1.0 / math.sqrt(d_k)

    def forward(self, q, k, v, mask=None):
        # q, k, v shape: [batch_size, num_heads, seq_len, d_k]
        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        attn_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, v)
        return output, attn_weights
```

#### Q74: Explain Positional Encodings in Transformers: Absolute Sinusoidal vs. RoPE (Rotary Position Embeddings).
**Answer:**
Because Self-Attention is permutation-invariant, positional information must be added.
*   **Absolute Sinusoidal**: Adds fixed sine/cosine wave vectors directly to input word embeddings ($X + PE$).
*   **RoPE (Rotary Position Embedding)**: Multiplies Query and Key vectors by a complex rotation matrix operating on 2D sub-vector planes. Encodes **relative** positional distance naturally through dot products $\langle R_{\Theta, m} Q, R_{\Theta, n} K \rangle = Q^T R_{\Theta, n-m} K$, allowing better context extrapolation.

#### Q75: What is RMSNorm (Root Mean Square Normalization)?
**Answer:** A simplified variation of LayerNorm that normalizes activations using Root Mean Square value without estimating mean shifts ($\mu=0$):
$$\bar{a}_i = \frac{a_i}{\text{RMS}(a)} \gamma_i, \quad \text{where } \text{RMS}(a) = \sqrt{\frac{1}{d} \sum_{i=1}^d a_i^2 + \epsilon}$$
Reduces computation time by 10-50% while achieving matching performance in modern LLMs (Llama).

#### Q76: Explain Multi-Query Attention (MQA) vs Grouped-Query Attention (GQA).
**Answer:**
*   **Multi-Head Attention (MHA)**: Every Query head has its own dedicated Key ($K$) and Value ($V$) head (high KV cache memory footprint during inference).
*   **Multi-Query Attention (MQA)**: All Query heads share a SINGLE single Key and Value head (drastically reduces KV cache size; slight accuracy degradation).
*   **Grouped-Query Attention (GQA)**: Divides Query heads into $G$ groups, where each group shares one Key and Value head (balances inference speed and accuracy; used in Llama-2-70B).

```
MHA:  8 Query Heads  <->  8 Key/Value Heads
GQA:  8 Query Heads  <->  2 Grouped Key/Value Heads
MQA:  8 Query Heads  <->  1 Shared Key/Value Head
```

#### Q77: What is Dropout, and how does it act as Ensemble Learning?
**Answer:** Randomly sets a fraction $p$ of hidden layer neuron activations to zero during each forward training pass. Forces network to learn redundant representations.
*   *Ensemble Interpretation*: Training a network with $N$ neurons using Dropout is equivalent to training an implicit ensemble of $2^N$ sub-networks sharing weights.

#### Q78: Explain Group Normalization (GroupNorm) and Instance Normalization.
**Answer:**
*   **GroupNorm**: Divides feature channels into groups and normalizes activations per group per sample. Independent of batch size (ideal for small-batch object detection).
*   **InstanceNorm**: Normalizes across spatial dimensions per channel per sample (used in style transfer GANs).

#### Q79: What is Autoencoder vs Variational Autoencoder (VAE)?
**Answer:**
*   **Autoencoder**: Deterministically compresses input $x$ into fixed latent vector $z$, and reconstructs $\hat{x}$. Latent space is unconstrained with gaps.
*   **VAE**: Probabilistic model that maps input $x$ to parameters of a continuous probability distribution ($\mu, \sigma$). Uses **Reparameterization Trick** $z = \mu + \sigma \odot \epsilon$ (where $\epsilon \sim \mathcal{N}(0, I)$) to allow backpropagation through stochastic sampling.

#### Q80: Explain Generative Adversarial Networks (GANs) and Minimax Game Loss.
**Answer:** Consists of two competing networks:
1.  **Generator ($G$)**: Tries to produce realistic fake images from random noise $z$.
2.  **Discriminator ($D$)**: Tries to distinguish real images from fake generated images.
*   *Minimax Objective*:
$$\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{data}}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

#### Q81: What is Diffusion Model Architecture (Forward vs Reverse Process)?
**Answer:**
*   **Forward Process**: Slowly destroys structure of an image by adding Gaussian noise step-by-step over $T$ steps until image becomes pure noise.
*   **Reverse Process**: Neural Network (U-Net) is trained to predict and remove noise step-by-step to generate clean images from random noise.

#### Q82: What is the KV Cache in LLM Inference?
**Answer:** During autoregressive token generation, past token Key ($K$) and Value ($V$) tensors are saved in GPU VRAM memory. Prevents recomputing KV tensors for historical tokens on every new output token step.

#### Q83: Explain KV Cache Memory Calculation for an LLM.
**Answer:**
$$\text{Memory per Token} = 2 \times (\text{Layers}) \times (\text{KV Heads}) \times (\text{Head Dim}) \times (\text{Bytes per Param})$$
*   *Example*: For 70B model (80 layers, 8 KV heads, 128 head dim, FP16 2 bytes):
$$\text{Memory} = 2 \times 80 \times 8 \times 128 \times 2 = 327,680 \text{ bytes/token} \approx 0.327 \text{ MB per token}$$
For sequence length 4,000, single request KV Cache $= 1.31 \text{ GB VRAM}$.

#### Q84: What is FlashAttention?
**Answer:** An exact attention algorithm optimization that speeds up attention computation and reduces memory footprint from $O(N^2)$ to $O(N)$.
*   *Mechanism*: Uses **tiling** to compute Softmax reduction blocks incrementally in fast GPU SRAM memory without reading/writing intermediate $N \times N$ attention matrices to high-bandwidth GPU HBM memory.

#### Q85: What is Weight Decay vs L2 Regularization in PyTorch?
**Answer:**
*   For standard SGD, Weight Decay and L2 Regularization are mathematically identical.
*   For adaptive optimizers (Adam), L2 Regularization modifies gradients before moment tracking, while Weight Decay directly decrements parameters after optimizer step execution (AdamW).

#### Q86: What is Gradient Accumulation?
**Answer:** Simulating a large batch size when constrained by GPU VRAM memory. Computes forward/backward passes for $K$ micro-batches, accumulating gradients using `loss.backward()`, and calling `optimizer.step()` and `optimizer.zero_grad()` only once every $K$ steps.

#### Q87: Explain Mixed Precision Training (FP32 vs FP16 vs BF16).
**Answer:**
*   **FP32**: Single precision (32 bits: 1 sign, 8 exponent, 23 mantissa). Standard numerical accuracy.
*   **FP16**: Half precision (16 bits: 1 sign, 5 exponent, 10 mantissa). Fast, but narrow dynamic range causes underflow/overflow (requires Loss Scaling).
*   **BF16 (Bfloat16)**: Brain Floating Point (16 bits: 1 sign, 8 exponent, 7 mantissa). Same dynamic range as FP32, preventing underflow without loss scaling (standard on Google TPUs and NVIDIA A100/H100 GPUs).

#### Q88: What is Internal Covariate Shift in Deep Neural Networks?
**Answer:** The continuous shift in the distribution of network activation inputs to deeper layers during training as preceding layer weights update. Mitigated by Batch Normalization and Layer Normalization.

#### Q89: Explain Vision Transformers (ViT).
**Answer:** Applies standard Transformer architecture directly to non-overlapping image patches:
1.  Split image ($H \times W$) into non-overlapping $16 \times 16$ patches.
2.  Flatten patches and project linearly into 1D embeddings.
3.  Add Learnable Positional Embeddings and prepend `[CLS]` token.
4.  Pass through standard Transformer Encoder for image classification.

#### Q90: What is Contrastive Learning (SimCLR / CLIP)?
**Answer:** Unsupervised representation learning paradigm that pulls augmented views of the same image (positive pairs) together in embedding space while pushing different images (negative pairs) apart using InfoNCE Loss:
$$\mathcal{L}_{InfoNCE} = -\log \frac{\exp(\text{sim}(z_i, z_j) / \tau)}{\sum \exp(\text{sim}(z_i, z_k) / \tau)}$$

#### Q91: What is Neural Architecture Search (NAS)?
**Answer:** Automating the design of neural network architectures using reinforcement learning, evolutionary algorithms, or gradient-based search (DARTS) to find optimal trade-offs between model accuracy and hardware latency constraints.

#### Q92: Explain Deep Residual Shrinkage Networks.
**Answer:** Variant of ResNet that incorporates soft-thresholding as trainable sub-layers to eliminate noise features in signal processing and vibration diagnostics.

#### Q93: What is Teacher-Student Network Distillation?
**Answer:** A model compression framework where a small "Student" network is trained to mimic output probability distributions (soft targets) generated by a large "Teacher" model using KL Divergence loss at higher temperature $T$:
$$\mathcal{L} = (1 - \alpha) \mathcal{L}_{CE}(y, \hat{y}_{student}) + \alpha T^2 \mathcal{L}_{KL}(p_{teacher}^T \parallel p_{student}^T)$$

#### Q94: What is Spatial Pyramid Pooling (SPP) in CNNs?
**Answer:** A pooling layer that generates fixed-length output vectors regardless of input image aspect ratio/size, removing rigid fixed input dimension restrictions in CNN architectures.

#### Q95: Explain Depthwise Separable Convolutions (MobileNets).
**Answer:** Factorizes standard 3D convolutions into two lightweight steps:
1.  **Depthwise Convolution**: Single spatial filter per input channel.
2.  **Pointwise Convolution**: $1 \times 1$ convolution combining channel outputs.
*   *Result*: Reduces computational cost and parameter count by $8\text{--}9\times$.

#### Q96: What is Anchor Box in Object Detection (Faster R-CNN / YOLO)?
**Answer:** Pre-defined bounding boxes of various aspect ratios and scales placed across spatial grid cells. Object detectors predict offsets ($\Delta x, \Delta y, \Delta w, \Delta h$) and confidence scores relative to anchor box coordinates.

#### Q97: Explain Non-Maximum Suppression (NMS) in Object Detection.
**Answer:** Post-processing technique that eliminates redundant overlapping bounding boxes:
1.  Sort candidate boxes by detection confidence score.
2.  Select box with highest confidence score.
3.  Calculate Intersection over Union (IoU) with all remaining candidate boxes.
4.  Discard boxes with $\text{IoU} > \text{threshold}$ (e.g., $0.5$). Repeat.

#### Q98: What is Focal Loss vs Cross Entropy Loss in RetinaNet?
**Answer:** Standard Cross-Entropy assigns non-negligible loss to millions of easy background candidate bounding boxes. Focal Loss down-weights easy background samples by $(1 - p_t)^\gamma$, allowing detector training to focus on true objects.

#### Q99: What is Auto-Regressive vs Auto-Encoding Models?
**Answer:**
*   **Auto-Regressive (GPT)**: Predicts next token conditioned strictly on past tokens $P(x_t | x_1, \dots, x_{t-1})$.
*   **Auto-Encoding (BERT)**: Predicts masked tokens using bidirectional context $P(x_{masked} | x_{unmasked})$.

#### Q100: Explain the SwiGLU activation function formula used in Llama models.
**Answer:**
$$\text{SwiGLU}(x) = \text{Swish}_\beta(x W) \otimes (x V)$$
Where $\text{Swish}_\beta(x) = x \cdot \sigma(\beta x)$ and $\otimes$ represents element-wise matrix multiplication. SwiGLU replaces standard GELU / ReLU activations in modern LLM Feed-Forward sub-layers, improving model convergence and benchmark benchmarks.
