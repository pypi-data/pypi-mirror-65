from ...utils.function import parse_f
from ...utils.math import haveSameSign

@parse_f()
def secant(fx, epsilon=0.1, x0=-10, x1=10):
  while True:
    y0 = fx(x0)
    y1 = fx(x1)

    x2 = (x0 - (((x1-x0)/(y1 - y0)) * y0))
    y2 = fx(x2)

    if (y2 == 0):
      return x2

    if abs(x0 - x2) <= epsilon:
      return x2

    if haveSameSign(y0, y2):
      x0 = x2
    else:
      x1 = x2