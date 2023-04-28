def lerp(A: float, B: float, t: float):
  '''
  A - first number
  B - second number
  t - interpolation factor, a number between 0 and 1
  function to get an intermediate value between A and B
  '''
  return A + (B - A) * t