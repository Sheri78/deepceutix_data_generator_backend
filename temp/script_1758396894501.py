def divide_by_zero():
  """This function attempts to divide 1 by 0, which will raise a ZeroDivisionError."""
  try:
    result = 1 / 0
    print(f"The result is: {result}")  # This line will not be reached
  except ZeroDivisionError as e:
    print(f"Error: Division by zero is not allowed.  Caught the exception: {e}")

if __name__ == "__main__":
  divide_by_zero()