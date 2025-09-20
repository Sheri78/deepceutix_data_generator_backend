def add_numbers(num1, num2):
  """
  This function adds two numbers together and returns the result.

  Args:
    num1: The first number.
    num2: The second number.

  Returns:
    The sum of num1 and num2.
  """
  sum_result = num1 + num2
  return sum_result

# Example usage:
number1 = 10
number2 = 5
sum_of_numbers = add_numbers(number1, number2)

print(f"The sum of {number1} and {number2} is: {sum_of_numbers}")  # Output: The sum of 10 and 5 is: 15


#  A simpler, more concise version:

def add(x, y):
  return x + y

# Example Usage of the simpler version
result = add(7, 3)
print(result)  # Output: 10