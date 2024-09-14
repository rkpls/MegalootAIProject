import re

def extract_numbers_from_string(s):
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', s)
    
    # Join the found numbers into a single string and convert to integer
    number_str = ''.join(numbers)
    
    # Convert the result to an integer
    return int(number_str)

# Example usage
example_string = "9% @ gold"
result = extract_numbers_from_string(example_string)
print(result)  # Output will be 9
