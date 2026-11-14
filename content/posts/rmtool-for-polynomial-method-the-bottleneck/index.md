+++
title = "RMTool for Polynomial Method: The Bottleneck?"
date = 2011-11-09T17:23:00
description = "Thoughts on symbolic computation, portability, and the polynomial method for random matrices."
slug = "rmtool-for-polynomial-method-the-bottleneck"
aliases = ["rmtool-for-polynomial-method-the-bottleneck/"]
draft = false
[taxonomies]
tags = ["research", "mathematics"]
[extra]
legacy_source = "rmtool-for-polynomial-method-the-bottleneck.rst"
+++
I have been reading [The Polynomial Method for Random Matrices](https://arxiv.org/abs/math/0601389) by N. Raj. Rao and A. Edelman as a part of literature review for my PhD research. In this paper, the authors present a method to determine the limiting eigen distribution of a particular subset of random matrices called *algebraic random matrices*. In the proposed method, the Stieltjes transform of the limiting eigen distribution is encoded as a root of a bivariate polynomial. A defined set of transformations (deterministic and stochastic) on the matrix is mapped to an *operation* on the bivariate polynomial. The limiting eigen distribution of the resulting matrix can be determined from the new bivariate polynomial.

This method heavily relies on the symbolic computation methodology. In parallel with the development of the mathematical framework for the polynomial method, the authors have developed a Matlab toolbox called the [RMTool](http://www.eecs.umich.edu/~rajnrao/rmtool/) which leverages the symbolic computation capability of Matlab. However the RMTool uses the Maple Symbolic Toolbox for Matlab which Mathworks no longer supports (above version 2009a). The original RMTool might even have been written in Maple itself and later forked to a Matlab toolbox. This has made RMTool extremely platform dependent, preventing it from being used by other researchers. The method was proposed sometime in 2005 but I can hardly find an alternative reference on this topic or its application. It seems to me that the rigidity of the RMTool may be limiting its potential as a powerful tool in random matrix analysis and application to engineering problems.

I have been looking at possibilities of porting the RMTool to the new Matlab Symbolic Toolbox which is based on MUPad. I am also planning on developing a new package (from scratch :o) on a more robust and compatible platform (Python with Sage). But these ideas are still in early phase and need a thorough understanding of the polynomial method.
