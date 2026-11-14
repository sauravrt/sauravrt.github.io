+++
title = "Bayesian Learning: Part I"
description = "An introduction to Bayesian inference and linear regression, recovered from the old site."
slug = "bayesian-learning-part-1"
aliases = ["Bayesian_Learning_Part1/"]
draft = true
[taxonomies]
tags = ["mathematics", "research"]
[extra]
legacy_source = "Bayesian_Learning_Part1/index.html"
math = true
+++
> Migration draft: the original publication date has not been recovered. This
> page is excluded from the public build until its date and equations have
> been reviewed.

In this post I want to lay out some of the basic concepts of Bayesian inference as used in the machine learning context. The content on this post is heavily derived from [1, 2]. This post and my interest in Bayesian inference has been inspired by talks I attend with the [Boston Bayesian Meetup](https://www.meetup.com/Boston-Bayesians) group.

In supervised machine learning, we wish to learn a relation between two variables \\(A\\) and \\(B\\) given some sample examples. Once the relation has been 'learned', then we can predict 'what is \\(B\\)' given \\(A\\). In practice the measurement of both the dependent (\\(B\\)) and independent (\\(A\\)) variable is inexact and the relation between them is not deterministic. Given this inherent uncertainty it does not make sense to have a deterministic prediction for \\(B\\) with complete certainty. A probabilistic approach is better suited for meaningful reasoning in the presence of uncertainty.

The probabilistic approach treats both \\(A\\) and \\(B\\) as random variables and relates the two via the conditional probability \\(P(B|A)\\), i.e., the probability of \\(B\\) given a specific value of \\(A\\). The first step in machine learning is to approximate the likelihood \\(P(B|A)\\) with an appropriate model based on a given set of examples of \\(A\\) and \\(B\\). Typically, the conditional probability \\(P(B|A)\\) has a parameterized model

\\[P(B|A) = f(A;\mathbf{w}),\\]

where \\(\mathbf{w}\\) is a vector of model parameters. Then given a set \\(\mathcal{D}\\) of \\(N\\) examples \\(\mathcal{D} = \{A_n,B_n\}_{n=1:N}\\), a conventional approach involves optimization (e.g. maximum likelihood, least-squares fit) of our model for the given data \\(\mathcal{D}\\) with respect to the parameters \\(\mathbf{w}\\). With the optimal parameters \\(\mathbf{w}_{opt}\\) computed, we can predict the unknown \\(B\\) by evaluating \\(f(A_*;\mathbf{w}_{opt})\\) given \\(A_*\\).

The Bayesian inference approach treats the model parameters \\(\mathbf{w}\\) as random variables. The conditional probability of \\(B\\) now depends on both \\(A\\) and \\(\mathbf{w}\\): \\(P(B|A,\mathbf{w})\\). Rather than 'learning' specific values for \\(\mathbf{w}\\), we can infer a *posterior* distribution \\(P(\mathbf{w}|A,B)\\) over the parameters \\(\mathbf{w}\\) using Bayes' rule.

In general, the Bayesian approach for learning model parameters involves the following steps:

- Given \\(n\\) data, \\(\mathcal{D}\\), write down the likelihood expression \\(P(B|\mathbf{w})\\).
- Specify a prior: \\(p(\mathbf{w})\\).
- Compute the posterior:

\\[p(\mathbf{w}|B) = \frac{p(B|\mathbf{w})p(\mathbf{w})}{p(B)}.\\]

## Linear prediction

Let's look at an example of the classic linear regression problem. A training dataset \\(\mathcal{D}\\) with \\(N\\) examples \\(\{\mathbf{x}_{1:N},y_{1:N}\}\\) is given. Each input \\(\mathbf{x}_i \in \mathbb{R}^M\\) is a vector with \\(M\\) attributes and each output \\(y_i \in \mathbb{R}\\) is considered univariate. In linear prediction, the relation between input and output in the training dataset is approximated by a parameterized linear model \\(y(\mathbf{x},\boldsymbol{\theta})\\) where the parameter vector is \\(\boldsymbol{\theta} = \{\theta_1,\theta_2,\ldots,\theta_M\}\\). The linear model is expressed as:

\\[y_i = \sum_{j=1}^M x_{ij}\theta_j,\\]

or a more compact matrix form is

\\[\mathbf{y} = \mathbf{X}\boldsymbol{\theta},\\]

where \\(\mathbf{y}\\) is an \\(N \times 1\\) vector whose entries are \\(N\\) outputs of training data and \\(\mathbf{X}\\) is an \\(N \times M\\) matrix whose rows are the input vectors of the training dataset. The problem is to estimate the parameters \\(\boldsymbol{\theta}\\) such that our linear model gives the 'best' fit to the provided training dataset \\(\mathcal{D}\\). The estimated parameter \\(\hat{\boldsymbol{\theta}}\\) can be used to predict the output for input values not in the training dataset.

### Least squares

The least-squares (LS) estimate of the parameter:

\\[\hat{\boldsymbol{\theta}} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.\\]

### Maximum likelihood

The maximum likelihood (ML) estimate of the parameters \\(\boldsymbol{\theta}\\) is the same as the LS estimate. Hence the LS parameter estimate is optimal in the ML sense.

### Bayesian linear regression

*Posterior mean*:

\\[\boldsymbol{\theta} = (\lambda\mathbf{I}_M + \mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}.\\]

*Posterior variance* (as written in the legacy page):

\\[\mathbf{V}_N = \sigma^2(\lambda\mathbf{I}_M + \mathbf{x}^T\mathbf{x})^{-1}.\\]

Here \\(\lambda\\) is a constant (to be defined).

## References

1. Bayesian Inference: An Introduction to Principles and Practice in Machine Learning, Michael E. Tipping, Microsoft Research, Cambridge, U.K. ([papers](http://www.miketipping.com/papers.htm)).
2. Machine Learning (CPSC 540) lecture notes from Prof. Nando de Freitas, UBC ([course page](http://www.cs.ubc.ca/~nando/540-2013/index.html)).
