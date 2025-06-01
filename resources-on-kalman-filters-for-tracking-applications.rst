Resources on Kalman filters for tracking applications
#####################################################
:date: 2016-08-14 19:35
:author: sauravtuladhar
:category: Uncategorized
:slug: resources-on-kalman-filters-for-tracking-applications
:status: published

For the last couple of months, I have been working with Kalman filter and its variations for aircraft tracking applications. I have found following resources helpful in the course of learning about Kalman filters.

`Estimation with Applications to Tracking and Navigation: Theory Algorithms and Software , Y. Bar-Shalom; T. Kirubarajan; X. Li <http://www.worldcat.org/title/estimation-with-applications-to-tracking-and-navigation-theory-algorithms-and-software/oclc/248663963&referer=brief_results>`__

`Prof. Y. Bar-Shalom <https://www.ee.uconn.edu/people/faculty/fac_bar>`__ is well known in the area of tracking applications. This book by Bar-Shalom and co-authors is the standard text book for anyone interested in learning about applying Kalman filters. The authors aim to "*make things simple, but not too simple; clear but not too clear*". The book not only presents theoretical derivation of filters, but also discusses implementation details. I have found the discussion on practical issues extremely helpful in the course of implementing the filters myself.

`Kalman and Bayesian Filters in Python <http://nbviewer.jupyter.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/table_of_contents.ipynb>`__

This is a book by Roger Labbe. This book covers a wide range of topics related to Kalman filters and its applications with focus on practical applications. What I liked about this book is that the entire book is composed as a Jupyter notebook. As a result, Roger not only presents the mathematical background but also presents code implementation of the filters. `FilterPy <https://github.com/rlabbe/filterpy>`__ is the accompanying python package which provides implementation of all the filters discussed in the book. If you are interested, it is straight forward to change the sample code in the chapter notebooks and see changes for yourself. This book is a fine example of `literate programming <https://en.wikipedia.org/wiki/Literate_programming>`__.

 
