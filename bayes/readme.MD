# Exercises in Bayesian statistics

##  Rasmus Bååth's beach party
An [example](rasmus_baath_lake_beach_summer_party.R) inspired by the excellent course [Fundamentals of Bayesian Data Analysis in R](https://www.datacamp.com/courses/fundamentals-of-bayesian-data-analysis-in-r) by Rasmus Bååth.

![posterior density](posterior.png)

## Albert Tarantola's Estimation of the Epicentral Coordinates of a Seismic Event

<img src='https://upload.wikimedia.org/wikipedia/commons/3/31/YFB_2005-12_044.jpg' width='100'>

[Problem 7.1](Estimation_of_the_Epicentral_Coordinates_of_a_Seismic_Event.R) in the book TARANTOLA, Albert. [*Inverse problem theory and methods for model parameter estimation*](http://www.ipgp.fr/~tarantola/Files/Professional/Books/InverseProblemTheory.pdf). [Society for Industrial and Applied Mathematics](https://epubs.siam.org/doi/book/10.1137/1.9780898717921), 2005.![siam](https://epubs.siam.org/na101/home/literatum/publisher/siam/books/content/ot/2005/1.9780898717921/1.9780898717921/production/1.9780898717921.cover.jpg)

The original figure:

![The original Figure 7.1](Tarantola-fig7_1.png)

The figure made using [Stan](https://mc-stan.org/):

![My replication of Figure 7.1](Estimation_of_the_Epicentral_Coordinates_of_a_Seismic_Event.png)

![low uncertainties in arrival time](epicentral-low_uncertainties_in_time_of_arrival.png)
![high uncertainties in arrival time](epicentral-high_uncertainties_in_time_of_arrival.png)

## A bayesian approach to the confidence bounds when sampling from small finite universes
We have a population of N=100 elements, some of the elements have a property of interest.
We take a random sample of n=10 elements from the population and we find a=1 element with 
the property of interest: what can be said about the number of elements in the population
with the property of interest?

[Tommy Wright](https://www.census.gov/research/researchers/profile.php?cv_sub=div&cv_profile=3743)
![Tommy Wright pictures as it appears in the AMSTAT News, the membership magazine of the American Statistical Association](https://magazine.amstat.org/wp-content/uploads/2020/02/Wright_Tommy.jpg) wrote in his book
[*Exact Confidence Bounds when Sampling from Small Finite Universes - 
An Easy Reference Based on the Hypergeometric Distribution*](https://www.springer.com/gp/book/9780387975153)
![In spite of these recent computing developments, the existence of theory, and the ability to
produce exact confidence bounds for A, exact results are rarely given in practice. Why
continue to use and teach approximations, including ones that yield bad results for certain
cases, for such a common and simple problem when exact and simple methods can be used?](https://images.springer.com/sgw/books/medium/9780387975153.jpg)

*What is more beautiful than a simple and important
question with a simple and exact answer that is easy
to provide?*

As we can see, the (frequentist) confidence interval at 95% is [1,38]
![Table at page 114 in Wright](Wright_pag114.jpg)

I have tried [two exercises](proportion_from_a_finite_universe.R) with the Bayesian approach;
in the first I use the knowledge that the likelihood is an hypergeometric random
variable.
In the second I did not use that knowledge but even if I 
ignore the math involving the hypergeometric I am anyway 
able to simulate the data generation process:

![exact likelihood](proportion_from_a_finite_universe-1.png)![simulated likelihood](proportion_from_a_finite_universe-2.png)


