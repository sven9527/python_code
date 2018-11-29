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