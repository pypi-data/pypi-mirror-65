import random


def randomReal(l, r):
    """ Returns a random real number in the range [l, r] """
    return random.uniform(start, stop)


def randomWhole(l, r):
    """ Returns a random whole number in the range [l, r] """
    return random.randrange(start, stop)


def randomGaussian(mu, sigma):
    """ 
    Returns a random in a gaussian distribution.
    mu is the mean and sigma is the standard deviation.
    """
    return random.gauss(mu, sigma)
