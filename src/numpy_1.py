import numpy as np

a = np.arange(6).reshape(2, 3)
print(a.shape, a.size, a.ndim, a.dtype.name, a.itemsize, type(a))
print(a)

b = np.array([2, 3, 4])
print(b)

c = np.array([(1, 2, 3), (4, 5, 6)], dtype=complex)
print(c, c.dtype.name)

d = np.array([(1, 2, 3), (4, 5, 6), (7, 8, 9)], dtype=np.uint8)
print(d, d.dtype.name)

e = np.zeros((3,4))
print(e)

f = np.ones((2,3), dtype=np.uint8)
print(f, f.dtype.name)

g = np.empty((2,3))
print(g)

h = np.arange(10, 35, 5)
print(h)

i = np.linspace(0, 1, 5)
print(i)

import math
j = np.linspace(0, 2*math.pi, 100)
print(np.sin(j))

palette = np.array([
    [0,0,0],
    [255,0,0],
    [0,255,0],
    [0,0,255],
    [255,255,255]
])
image = np.array([[0,1,2,0],
                  [0,3,4,0]
                  ])
print(palette[image])

k = np.arange(12).reshape((3,4))
l = k > 4
print(k)
print(l)
print(k[l])


import matplotlib.pyplot as plt
def mandelbrot( h,w, maxit=20 ):
    """Returns an image of the Mandelbrot fractal of size (h,w)."""
    y,x = np.ogrid[ -1.4:1.4:h*1j, -2:0.8:w*1j ]
    c = x+y*1j
    z = c
    divtime = maxit + np.zeros(z.shape, dtype=int)

    for i in range(maxit):
        z = z**2 + c
        diverge = z*np.conj(z) > 2**2            # who is diverging
        div_now = diverge & (divtime==maxit)  # who is diverging now
        divtime[div_now] = i                  # note when
        z[diverge] = 2                        # avoid diverging too much

    return divtime
plt.imshow(mandelbrot(400,400))
plt.show()