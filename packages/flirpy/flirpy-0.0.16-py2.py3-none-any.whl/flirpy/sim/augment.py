import numpy as np:

def add_gaussian(image, mean=1, std=1):

    blob = np.random.multivariate_normal

    return image

def add_skew_gaussian(image, skew_x=3, skew_y=3, size=10):
    a = -skew_x/2+skew_x*random.random()
    b = -skew_y/2+skew_y*random.random()

    x = np.linspace(-max(skew_x, skew_y),max(skew_x, skew_y), 10)

    return np.dot(skewnorm.pdf(x, a).reshape((-1,1)),  skewnorm.pdf(x, b).reshape((1,-1)))
