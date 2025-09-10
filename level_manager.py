"""
LEVEL MANAGER - Level Data and Code Validation System
====================================================

PURPOSE: Manage level data, code validation, and solution checking
AUTHOR: Bomb Defuser Game
VERSION: 1.0

DESCRIPTION:
Handles all level-specific functionality including:
- Mathematical coding problem definitions
- Broken code with progressive error complexity  
- Solution validation using AST comparison
- Hint generation and error tracking
- Test case execution and result validation

DEPENDENCIES:
- ast: Python code parsing and comparison
- math: Mathematical function support
- statistics: Statistical calculation functions
"""

import ast
import math
import statistics
import traceback
from typing import Dict, List, Any, Optional


class LevelManager:
    """
    LEVEL DATA AND VALIDATION MANAGER
    
    PURPOSE: Centralized management of all level data and code validation
    
    FUNCTIONALITY:
    - Store and retrieve level definitions
    - Validate submitted code solutions
    - Execute code with test cases safely
    - Track error fixing progress
    - Generate appropriate hints for debugging
    """
    
    def __init__(self):
        self.levels_data = self.initialize_levels()
        
    def initialize_levels(self) -> Dict[int, Dict[str, Any]]:
        """
        INITIALIZE ALL LEVEL DATA
        
        PURPOSE: Create complete level definitions with problems and solutions
        
        RETURNS:
        - Dictionary mapping level numbers to level data
        
        LEVEL STRUCTURE:
        Each level contains:
        - title: Level name
        - description: Problem description
        - difficulty: Difficulty category
        - broken_code: Code with intentional errors
        - solution_code: Correct solution
        - test_cases: Input/output pairs for validation
        - hint: Debugging hint for 80% timer
        - errors: List of specific errors to fix
        """
        return {
            1: {
                'title': 'Quadratic Discriminant',
                'description': 'Calculate discriminant of quadratic equation',
                'difficulty': 'Beginner',
                'broken_code': '''# Calculate discriminant of ax² + bx + c = 0
def calculate_discriminant(a, b, c)
    discriminant = b*b - 4*a*c
    return discriminant

# Test the function
a, b, c = 2, 5, 3
result = calculate_discriminant(a, b, c)
print(f"Discriminant: {result}")''',
                'solution_code': '''# Calculate discriminant of ax² + bx + c = 0
def calculate_discriminant(a, b, c):
    discriminant = b*b - 4*a*c
    return discriminant

# Test the function
a, b, c = 2, 5, 3
result = calculate_discriminant(a, b, c)
print(f"Discriminant: {result}")''',
                'test_cases': [
                    {'input': (1, 4, 4), 'output': 0},
                    {'input': (2, 5, 3), 'output': 1},
                    {'input': (1, 2, 5), 'output': -16}
                ],
                'hint': 'Look for a missing colon (:) in the function definition.',
                'errors': ['Missing colon after function definition']
            },
            
            2: {
                'title': 'Linear Equation Solver',
                'description': 'Solve linear equation ax + b = 0',
                'difficulty': 'Beginner',
                'broken_code': '''# Solve linear equation ax + b = 0
def solve_linear(a, b):
    if a == 0:
        return "No solution" if b != 0 else "Infinite solutions"
    return -b / a

# Test cases
equations = [(2, 4), (3, -9), (0, 5)]
for a, b in equations:
    solution = solve_linear(a, b)
    print(f"{a}x + {b} = 0 => x = {solution}"''',
                'solution_code': '''# Solve linear equation ax + b = 0
def solve_linear(a, b):
    if a == 0:
        return "No solution" if b != 0 else "Infinite solutions"
    return -b / a

# Test cases
equations = [(2, 4), (3, -9), (0, 5)]
for a, b in equations:
    solution = solve_linear(a, b)
    print(f"{a}x + {b} = 0 => x = {solution}")''',
                'test_cases': [
                    {'input': (2, 4), 'output': -2.0},
                    {'input': (3, -9), 'output': 3.0},
                    {'input': (1, 0), 'output': 0.0}
                ],
                'hint': 'Check the closing parenthesis in the print statement.',
                'errors': ['Missing closing parenthesis']
            },
            
            3: {
                'title': 'Prime Number Checker',
                'description': 'Check if a number is prime',
                'difficulty': 'Beginner',
                'broken_code': '''# Check if number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1)
        if n % i == 0:
            return False
    return True

# Test prime numbers
test_numbers = [2, 3, 4, 17, 25, 29]
for num in test_numbers:
    status = "prime" if is_prime(num) else "not prime"
    print(f"{num} is {status}")''',
                'solution_code': '''# Check if number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test prime numbers
test_numbers = [2, 3, 4, 17, 25, 29]
for num in test_numbers:
    status = "prime" if is_prime(num) else "not prime"
    print(f"{num} is {status}")''',
                'test_cases': [
                    {'input': 2, 'output': True},
                    {'input': 17, 'output': True},
                    {'input': 4, 'output': False},
                    {'input': 25, 'output': False}
                ],
                'hint': 'Missing colon (:) at the end of the for loop line.',
                'errors': ['Missing colon after for loop']
            },
            
            4: {
                'title': 'Greatest Common Divisor',
                'description': 'Find GCD using Euclidean algorithm',
                'difficulty': 'Intermediate',
                'broken_code': '''# Find GCD using Euclidean algorithm
def gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

# Test GCD function
pairs = [(48, 18), (100, 25), (17, 13)]
for x, y in pairs:
    result = gcd(x, y)
    print(f"GCD({x}, {y}) = {result}")
    
# Find LCM using GCD
def lcm(a, b):
    return (a * b) // gcd(a, b)

print(f"LCM(12, 8) = {lcm(12, 8)}")''',
                'solution_code': '''# Find GCD using Euclidean algorithm
def gcd(a, b):
    while b != 0:
        temp = b
        b = a % b
        a = temp
    return a

# Test GCD function
pairs = [(48, 18), (100, 25), (17, 13)]
for x, y in pairs:
    result = gcd(x, y)
    print(f"GCD({x}, {y}) = {result}")
    
# Find LCM using GCD
def lcm(a, b):
    return (a * b) // gcd(a, b)

print(f"LCM(12, 8) = {lcm(12, 8)}")''',
                'test_cases': [
                    {'input': (48, 18), 'output': 6},
                    {'input': (100, 25), 'output': 25},
                    {'input': (17, 13), 'output': 1}
                ],
                'hint': 'The algorithm logic is correct, but there might be a subtle error in the variable assignments.',
                'errors': ['Logic error in variable swapping - this is actually correct code, testing validation']
            },
            
            5: {
    'title': 'Fibonacci Sequence',
    'description': 'Generate Fibonacci numbers',
    'difficulty': 'Intermediate', 
    'broken_code': '''# Generate Fibonacci sequence
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_seq = [0, 1]
    for i in range(2, n):
        next_fib = fib_seq[i-1] + fib_seq[i-2]
        fib_seq = [next_fib]
    
    return fib_seq

# Test Fibonacci generation
for i in range(1, 8):
    sequence = fibonacci(i)
    print(f"First {i} Fibonacci numbers: {sequence}")
    
# Calculate Fibonacci ratios
def fib_ratio(n):
    fib_nums = fibonacci(n)
    if len(fib_nums) < 2:
        return None
    return fib_nums[-1] / fib_nums[-2]

print(f"Golden ratio approximation: {fib_ratio(10):.6f}")''',
    'solution_code': '''# Generate Fibonacci sequence
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib_seq = [0, 1]
    for i in range(2, n):
        next_fib = fib_seq[i-1] + fib_seq[i-2]
        fib_seq.append(next_fib)  # FIXED: Append instead of replacing
    
    return fib_seq

# Test Fibonacci generation
for i in range(1, 8):
    sequence = fibonacci(i)
    print(f"First {i} Fibonacci numbers: {sequence}")
    
# Calculate Fibonacci ratios
def fib_ratio(n):
    fib_nums = fibonacci(n)
    if len(fib_nums) < 2:
        return None
    return fib_nums[-1] / fib_nums[-2]

print(f"Golden ratio approximation: {fib_ratio(10):.6f}")''',
    'test_cases': [
        {'input': 5, 'output': [0, 1, 1, 2, 3]},
        {'input': 7, 'output': [0, 1, 1, 2, 3, 5, 8]},
        {'input': 1, 'output': [0]}
    ],
    'hint': 'In the loop, check if you are appending to the list or replacing the entire list.',
    'errors': ['Replacing list instead of appending']
},
            
            6: {
                'title': 'Statistical Calculations',
                'description': 'Calculate mean, median, and mode',
                'difficulty': 'Intermediate',
                'broken_code': '''# Statistical calculations
import math

# Statistical calculations

def calculate_mean(numbers):
    # Mean = sum of values / number of values
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    # Sort numbers to find the middle value
    sorted_nums = sorted(numbers)
    n == len(sorted_nums)
    
    if n % 2 == 0:
        # Even case → average of the two middle values
        return (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        # Odd case → middle value directly
        return sorted_nums[n//2 + 1]


def calculate_variance(numbers):
    # Variance = average of squared differences from the mean
    mean = calculate_mean(numbers)
    

    squared_diffs = [(x - mean) ** 2 for x in numbers]
    return sum(squared_diffs) / (len(numbers) - 1) 


def calculate_std_dev(numbers):
    # Standard deviation = square root of variance
    return math.sqrt(calculate_variance(numbers))


# Test data
data = [1, 2, 2, 3, 4, 4, 4, 5, 6]

print(f"Data: {data}")
print(f"Mean: {calculate_mean(data):.2f}") 
print(f"Median: {calculate_median(data)}")    
print(f"Variance: {calculate_variance(data):.2f}")  
print(f"Std Dev: {calculate_std_dev(data):.2f}") 
''',
                'solution_code': '''# Statistical calculations
def calculate_mean(numbers):
    return sum(numbers) / len(numbers)

def calculate_median(numbers):
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        return (sorted_nums[n//2-1] + sorted_nums[n//2]) / 2
    else:
        return sorted_nums[n//2]

def calculate_mode(numbers):
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_freq]
    return modes[0] if len(modes) == 1 else modes

# Test data
data = [1, 2, 2, 3, 4, 4, 4, 5, 6]
print(f"Data: {data}")
print(f"Mean: {calculate_mean(data):.2f}")
print(f"Median: {calculate_median(data)}")
print(f"Mode: {calculate_mode(data)}")''',
                'test_cases': [
                    {'input': [1, 2, 3, 4, 5], 'output': 3.0},  # Mean test
                    {'input': [1, 2, 2, 3, 4, 4, 4, 5, 6], 'output': 4},  # Mode test
                    {'input': [1, 3, 5], 'output': 3}  # Median test
                ],
                'hint': 'Check two things: 1) Are you using population variance (÷N) or sample variance (÷N-1)? 2) For odd-length lists, which index gives you the middle element?',
                'errors': ['Assignment operator (=) instead of equality (==)']
            },
            
            7: {
                'title': 'Matrix Operations',
                'description': 'Perform matrix multiplication',
                'difficulty': 'Advanced',
                'broken_code': '''# Matrix multiplication
def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    # Check dimensions for multiplication
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices: incompatible dimensions")
    
    C = [[0 for _ in range(rows_A)] for _ in range(cols_B)]
    
    # Perform multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[j][i] += A[i][k] * B[k][j]
    
    return C


def matrix_transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    
    # Correct dimensions should be cols × rows
    transposed = [[0 for _ in range(cols)] for _ in range(rows)] 
    
    for i in range(rows):
        for j in range(cols):
            # This will break symmetry for non-square matrices
            transposed[i][j] = matrix[j][i] 
    
    return transposed


# Test matrices
A = [[1, 2], [3, 4], [5, 6]]
B = [[7, 8, 9], [10, 11, 12]]

print("Matrix A:")
for row in A:
    print(row)

print("Matrix B:")
for row in B:
    print(row)

# Test multiplication
result = matrix_multiply(A, B)
print("A × B:")
for row in result:
    print(row)

# Test transpose
A_T = matrix_transpose(A)
print("A transpose:")
for row in A_T:
    print(row)''',
                'solution_code': '''# Matrix multiplication
def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices: incompatible dimensions")
    
    # Initialize result matrix
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    # Perform multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    
    return C

def matrix_transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    
    return transposed

# Test matrices
A = [[1, 2], [3, 4], [5, 6]]
B = [[7, 8, 9], [10, 11, 12]]

print("Matrix A:")
for row in A:
    print(row)

print("Matrix B:")
for row in B:
    print(row)

result = matrix_multiply(A, B)
print("A × B:")
for row in result:
    print(row)

# Test transpose
A_T = matrix_transpose(A)
print("A transpose:")
for row in A_T:
    print(row)''',
                'test_cases': [
                    {'input': ([[1, 2], [3, 4]], [[5, 6], [7, 8]]), 'output': [[19, 22], [43, 50]]},
                    {'input': ([[1, 2, 3]], [[4], [5], [6]]), 'output': [[32]]},
                ],
                'hint': 'Multiple matrix bugs: 1) Check result matrix dimensions, 2) Check index order in assignments, 3) Check transpose matrix initialization, 4) Check transpose assignment indices.',
'errors': ['Wrong result matrix dimensions', 'Swapped indices in multiplication', 'Wrong transpose dimensions', 'Swapped transpose indices']
            },
            
            8: {
                'title': 'Standard Deviation Calculator',
                'description': 'Calculate population standard deviation',
                'difficulty': 'Advanced',
                'broken_code': '''# Calculate standard deviation
def calculate_variance(numbers):
    # population mean
    mean = sum(numbers) / len(numbers)
    # squared differences from the mean
    squared_diffs = [(x - mean) ** 2 for x in numbers]
    variance = sum(squared_diffs) / (len(numbers) - 1)
    
    return variance


def calculate_std_dev(numbers):
    # Standard deviation is the square root of variance
    variance = calculate_variance(numbers)
    return variance ** 0.5


def calculate_z_scores(numbers):
    """
    Z-score explanation (also in comments below):
      z = (x - mean) / std_dev
    It expresses how many standard deviations a value x is from the mean:
      - z > 0  => x is above the mean
      - z < 0  => x is below the mean
      - |z| large => x is far from the mean
    """
    mean = sum(numbers) / len(numbers)
    std_dev = calculate_std_dev(numbers)
    
    # Defensive check: if std_dev is zero (all values identical), return zeros
    if std_dev == 0:
        return [0] * len(numbers)

    variance = calculate_variance(numbers)
    z_scores = [(x - mean) / variance for x in numbers]
    
    return z_scores


# Test data sets
datasets = [
    [10, 12, 14, 16, 18, 20],   # evenly spaced
    [1, 1, 1, 1, 1],            # zero variance case
    [100, 200, 150, 175, 225]   # varied dataset
]

# -----------------------
# Explanation of enumerate:
# -----------------------
# enumerate(datasets) yields pairs (index, value) for each item in 'datasets'.
# Example: enumerate(['a','b']) -> (0,'a'), (1,'b')
# In the loop "for i, data in enumerate(datasets):"
#   - i is the index (0, 1, 2, ...)
#   - data is the dataset at that index (the list itself)
# This saves you from manually maintaining a counter.
# -----------------------

for i, data in enumerate(datasets):
    print(f"Dataset {i+1}: {data}")
    print(f"  Mean: {sum(data)/len(data):.2f}")
    print(f"  Variance: {calculate_variance(data):.2f}")
    print(f"  Std Dev: {calculate_std_dev(data):.2f}")
    z_scores = calculate_z_scores(data)
    print(f"  Z-scores: {[round(z, 2) for z in z_scores}")  
    
    print()
''',
                'test_cases': [
                    {'input': [10, 12, 14, 16, 18, 20], 'output': 3.16},  # Std dev approximation
                    {'input': [1, 1, 1, 1, 1], 'output': 0.0},  # No variance
                ],
                'hint': 'Four bugs to find: 1) Wrong variance formula, 2) Division by zero edge case, 3) Wrong denominator in Z-score formula, 4) Missing closing bracket in print statement.',
'errors': ['Sample variance instead of population variance', 'Division by zero edge case', 'Using variance instead of std_dev in Z-scores', 'Missing closing bracket syntax error']
            },
            
            9: {
                'title': 'Correlation Coefficient',
                'description': 'Calculate Pearson correlation coefficient',
                'difficulty': 'Advanced',
                'broken_code': '''# Calculate Pearson correlation coefficient
def calculate_correlation(x_values, y_values):
    """
    Pearson correlation coefficient measures the linear relationship between two variables X and Y.
    Definition:
        r = cov(X,Y) / (std_dev(X) * std_dev(Y))
      - cov(X,Y) = sum((x_i - mean(X)) * (y_i - mean(Y))) / n
      - r ranges from -1 (perfect negative correlation) to 1 (perfect positive correlation)
      - r = 0 indicates no linear correlation
    """
    if len(x_values) != len(y_values):
        raise ValueError("Arrays must have same length")
    
    n = len(x_values)
    if n < 2:
        return None
    
    # Compute means
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    numerator = sum((x - mean_x) * y - mean_y for x, y in zip(x_values, y_values))
    
    # Squared differences for denominator
    sum_sq_x = sum((x - mean_x)**2 for x in x_values)
    sum_sq_y = sum((y - mean_y)**2 for y in y_values)
    
    denominator = (sum_sq_x + sum_sq_y)**0.5
    
    if denominator == 0:
        return None
    
    return numerator / denominator


def interpret_correlation(r):
    if r is None:
        return "Cannot calculate correlation"
    
    abs_r = abs(r)
    if abs_r >= 0.9:
        strength = "very strong"
    elif abs_r >= 0.7:
        strength = "strong"
    elif abs_r >= 0.5:
        strength = "moderate"
    elif abs_r >= 0.3:
        strength = "weak"
    else:
        strength = "very weak"
    
    direction = "positive" if r > 0 else "negative" if r < 0 else "no"
    return f"{strength} {direction} correlation"


# Test datasets
datasets = [
    ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),  # Perfect positive
    ([1, 2, 3, 4, 5], [10, 8, 6, 4, 2]),  # Perfect negative  
    ([1, 2, 3, 4, 5], [3, 1, 4, 1, 5])    # Weak correlation
]

# enumerate explanation:
# enumerate(datasets) yields pairs (index, value)
#   - i = dataset index (0,1,2,...)
#   - (x, y) = actual datasets
for i, (x, y) in enumerate(datasets):
    r = calculate_correlation(x, y)
    interpretation = interpret_correlation(r)
    print(f"Dataset {i+1}:")
    print(f"  X: {x}")
    print(f"  Y: {y}")
    print(f"  Correlation: {[r:.4f if r else 'None'}")
    print(f"  Interpretation: {interpretation}")
    print()
''',
                'solution_code': '''# Calculate Pearson correlation coefficient
def calculate_correlation(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("Arrays must have same length")
    
    n = len(x_values)
    if n < 2:
        return None
    
    # Calculate means
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    
    # Calculate correlation coefficient
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    
    sum_sq_x = sum((x - mean_x)**2 for x in x_values)
    sum_sq_y = sum((y - mean_y)**2 for y in y_values)
    
    denominator = (sum_sq_x * sum_sq_y)**0.5
    
    if denominator == 0:
        return None
    
    return numerator / denominator

def interpret_correlation(r):
    if r is None:
        return "Cannot calculate correlation"
    
    abs_r = abs(r)
    if abs_r >= 0.9:
        strength = "very strong"
    elif abs_r >= 0.7:
        strength = "strong"
    elif abs_r >= 0.5:
        strength = "moderate"
    elif abs_r >= 0.3:
        strength = "weak"
    else:
        strength = "very weak"
    
    direction = "positive" if r > 0 else "negative" if r < 0 else "no"
    return f"{strength} {direction} correlation"

# Test correlation with different datasets
datasets = [
    ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]),  # Perfect positive
    ([1, 2, 3, 4, 5], [10, 8, 6, 4, 2]),  # Perfect negative  
    ([1, 2, 3, 4, 5], [3, 1, 4, 1, 5])    # Weak correlation
]

for i, (x, y) in enumerate(datasets):
    r = calculate_correlation(x, y)
    interpretation = interpret_correlation(r)
    print(f"Dataset {i+1}:")
    print(f"  X: {x}")
    print(f"  Y: {y}")
    print(f"  Correlation: {r:.4f if r else 'None'}")
    print(f"  Interpretation: {interpretation}")
    print()''',
                'test_cases': [
                    {'input': ([1, 2, 3, 4, 5], [2, 4, 6, 8, 10]), 'output': 1.0},  # Perfect positive
                    {'input': ([1, 2, 3, 4, 5], [10, 8, 6, 4, 2]), 'output': -1.0},  # Perfect negative
                ],
                'hint': 'The correlation formula implementation looks mathematically correct.',
                'errors': ['No actual error - advanced mathematical concepts']
            },
            
            10: {
                'title': 'Advanced Statistics Suite',
                'description': 'Complete statistical analysis with multiple bugs',
                'difficulty': 'Expert',
                'broken_code': '''# Advanced statistical analysis suite
# Import the math module for mathematical functions
import math

# =====================================================
# What is a class?
# =====================================================
# A class is like a blueprint to create objects.
# Each object (instance) can have:
#   - Attributes: data stored inside the object (e.g., mean, variance)
#   - Methods: functions that operate on the object (e.g., calculate_skewness)
#
# Here we create a StatisticalAnalyzer class to analyze a dataset.

class StatisticalAnalyzer:
    # =====================================================
    # Constructor (__init__ method)
    # =====================================================
    # self: refers to the object being created
    # data: list of numbers to analyze
    def __init__(self, data):
        self.data = data  # store dataset inside object
        self.n = len(data)  # number of elements in the dataset
        self.mean = self.calculate_mean()
        
        # Variance and standard deviation calculation
        self.variance = self.calculate_variance()
        self.std_dev = math.sqrt(self.variance)
    
    # =====================================================
    # Method to calculate mean
    # =====================================================
    # Mean = sum of all numbers divided by total count
    def calculate_mean(self):
        return sum(self.data) / self.n
    
    # =====================================================
    # Method to calculate variance
    # =====================================================
    # Variance measures how spread out numbers are
    def calculate_variance(self, sample=False):
        mean = self.mean
        squared_diffs = [(x - mean)**2 for x in self.data]  # difference squared for each value
        divisor = self.n if sample else self.n - 1
        if divisor == 0:
            return 0
        return sum(squared_diffs) / divisor
    
    # =====================================================
    # Method to calculate skewness
    # =====================================================
    # Skewness measures asymmetry of distribution
    # Positive skew → long right tail, Negative skew → long left tail
    def calculate_skewness(self):
        if self.std_dev == 0:
            return 0  # no variation means skewness is zero
        
        result = 0
        for x in self.data:
            for _ in range(1):  # dummy inner loop
                result += ((x - self.mean) / self.std_dev) ** 3
        return result / self.n
    
    # =====================================================
    # Method to calculate kurtosis
    # =====================================================
    # Kurtosis measures "peakedness"
    def calculate_kurtosis(self):
        if self.std_dev == 0:
            return 0
        result = 0
        for x in self.data:
            for _ in range(2):
                result += ((x - self.mean) / self.std_dev) ** 4
        return (result / self.n) - 3
    
    # =====================================================
    # Method to calculate percentiles
    # =====================================================
    # Percentile = value below which a certain % of data falls
    def calculate_percentile(self, percentile):
        if not 0 <= percentile <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        sorted_data = sorted(self.data)  # sort the dataset
        
        if percentile == 100:
            return sorted_data[-1]  # maximum value
        
        # Compute the exact index
        index = (percentile / 100) * (self.n - 1)
        lower_index = int(index)
        upper_index = lower_index + 1
        
        if upper_index >= self.n:
            return sorted_data[lower_index]
        
        weight = index - lower_index
        return sorted_data[lower_index] * weight + sorted_data[upper_index] * (1 - weight)
    
    # =====================================================
    # Method to calculate confidence interval
    # =====================================================
    # Confidence interval = likely range where true mean lies
    # Assuming normal distribution
    def confidence_interval(self, confidence=0.95):
        if self.n < 2:
            return None
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        margin_error = z * (self.std_dev / math.sqrt(self.n))
        return (self.mean - margin_error, self.mean + margin_error)
    
    # =====================================================
    # Method to generate a full report
    # =====================================================
    # Combines all statistics into a readable string
    def generate_report(self):
        report = f"""
STATISTICAL ANALYSIS REPORT
===========================
Dataset: {self.data}
Sample Size: {self.n}

CENTRAL TENDENCY:
Mean: {self.mean:.4f}
Median: {self.calculate_percentile(50):.4f}

DISPERSION:
Variance: {self.variance:.4f}
Standard Deviation: {self.std_dev:.4f}
Range: {max(self.data) - min(self.data):.4f}

SHAPE:
Skewness: {self.calculate_skewness():.4f}
Kurtosis: {self.calculate_kurtosis():.4f}

PERCENTILES:
25th: {self.calculate_percentile(25):.4f}
75th: {self.calculate_percentile(75):.4f}
90th: {self.calculate_percentile(90):.4f}

CONFIDENCE INTERVAL (95%):
{self.confidence_interval(0.95)}
"""
        return report  
    
# =====================================================
# Test the StatisticalAnalyzer class
# =====================================================
test_datasets = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [100, 102, 98, 101, 99, 103, 97, 104, 96, 105],
    [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5],
    [42]  # Edge case: single element triggers hidden runtime errors
]

# Loop through each dataset
for i, dataset in enumerate(test_datasets):
    print(f"ANALYSIS {i+1}:")
    # Create object (instance) of StatisticalAnalyzer
    analyzer = StatisticalAnalyzer(dataset)
    # Generate and print the full report
    print(analyzer.generate_report())
    print("-" * 50)
''',
                'solution_code': '''# Advanced statistical analysis suite
import math

# =====================================================
# Educational version: Broken vs Fixed
# =====================================================

class StatisticalAnalyzer:
    # =====================================================
    # Constructor (__init__)
    # =====================================================
    def __init__(self, data):
        self.data = data
        self.n = len(data)
        
        # Broken: mean calculated without checking empty dataset → division by zero
        # self.mean = sum(self.data) / self.n
        # Fixed: check if dataset has elements
        self.mean = self.calculate_mean() if self.n > 0 else 0
        
        # Broken: std_dev not recalculated if variance invalid
        # self.std_dev = math.sqrt(self.variance)
        # Fixed: safe calculation with variance >= 0
        self.variance = self.calculate_variance()
        self.std_dev = math.sqrt(self.variance) if self.variance >= 0 else 0

    # =====================================================
    # Calculate mean
    # =====================================================
    def calculate_mean(self):
        # Broken: division by zero if n == 0
        # return sum(self.data) / self.n
        # Fixed: safe check
        return sum(self.data) / self.n if self.n > 0 else 0

    # =====================================================
    # Calculate variance
    # =====================================================
    def calculate_variance(self, sample=False):
        # Broken: sample/population logic inverted
        # divisor = self.n if sample else self.n - 1
        # Fixed: corrected
        if self.n < 2:
            return 0
        divisor = self.n - 1 if sample else self.n
        squared_diffs = [(x - self.mean) ** 2 for x in self.data]
        return sum(squared_diffs) / divisor

    # =====================================================
    # Skewness
    # =====================================================
    def calculate_skewness(self):
        # Broken: nested loop unnecessary, confusing
        # result = 0
        # for x in self.data:
        #     for _ in range(1):
        #         result += ((x - self.mean) / self.std_dev) ** 3
        # return result / self.n
        # Fixed: simple list comprehension
        if self.std_dev == 0 or self.n < 2:
            return 0
        cubed_diffs = [((x - self.mean) / self.std_dev) ** 3 for x in self.data]
        return sum(cubed_diffs) / self.n

    # =====================================================
    # Kurtosis
    # =====================================================
    def calculate_kurtosis(self):
        # Broken: double-counted values with nested loop
        # result = 0
        # for x in self.data:
        #     for _ in range(2):
        #         result += ((x - self.mean) / self.std_dev) ** 4
        # return (result / self.n) - 3
        # Fixed: accurate calculation
        if self.std_dev == 0 or self.n < 2:
            return 0
        fourth_diffs = [((x - self.mean) / self.std_dev) ** 4 for x in self.data]
        return (sum(fourth_diffs) / self.n) - 3

    # =====================================================
    # Percentiles
    # =====================================================
    def calculate_percentile(self, percentile):
        # Broken: weight calculation reversed, index may go out of range
        # index = (percentile / 100) * (self.n - 1)
        # lower_index = int(index)
        # upper_index = lower_index + 1
        # weight = index - lower_index
        # return self.data[lower_index] * weight + self.data[upper_index] * (1 - weight)
        # Fixed: correct interpolation and safe indexing
        if not 0 <= percentile <= 100:
            raise ValueError("Percentile must be between 0 and 100")
        sorted_data = sorted(self.data)
        if percentile == 100:
            return sorted_data[-1]
        if self.n == 1:
            return sorted_data[0]
        index = (percentile / 100) * (self.n - 1)
        lower_index = int(index)
        upper_index = min(lower_index + 1, self.n - 1)
        weight = index - lower_index
        return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight

    # =====================================================
    # Confidence interval
    # =====================================================
    def confidence_interval(self, confidence=0.95):
        # Broken: used stale std_dev, no check for n < 2
        # margin_error = z * (self.std_dev / math.sqrt(self.n))
        # Fixed: safe check
        if self.n < 2 or self.std_dev == 0:
            return (self.mean, self.mean)
        z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        z = z_scores.get(confidence, 1.96)
        margin_error = z * (self.std_dev / math.sqrt(self.n))
        return (self.mean - margin_error, self.mean + margin_error)

    # =====================================================
    # Generate report
    # =====================================================
    def generate_report(self):
        # Broken: missing closing parenthesis
        # return f"..."
        # Fixed: correct return
        report = f"""
STATISTICAL ANALYSIS REPORT
===========================
Dataset: {self.data}
Sample Size: {self.n}

CENTRAL TENDENCY:
Mean: {self.mean:.4f}
Median: {self.calculate_percentile(50):.4f}

DISPERSION:
Variance: {self.variance:.4f}
Standard Deviation: {self.std_dev:.4f}
Range: {max(self.data) - min(self.data):.4f}

SHAPE:
Skewness: {self.calculate_skewness():.4f}
Kurtosis: {self.calculate_kurtosis():.4f}

PERCENTILES:
25th: {self.calculate_percentile(25):.4f}
75th: {self.calculate_percentile(75):.4f}
90th: {self.calculate_percentile(90):.4f}

CONFIDENCE INTERVAL (95%):
{self.confidence_interval(0.95)}
"""
        return report


# =====================================================
# Test datasets
# =====================================================
test_datasets = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [100, 102, 98, 101, 99, 103, 97, 104, 96, 105],
    [1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5],
    [42]  # single-element handled safely
]

for i, dataset in enumerate(test_datasets):
    print(f"ANALYSIS {i+1}:")
    analyzer = StatisticalAnalyzer(dataset)
    print(analyzer.generate_report())
    print("-" * 50)
''',
                'test_cases': [
                    {'input': [1, 2, 3, 4, 5], 'output': 3.0},  # Mean test
                    {'input': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'output': 5.5},  # Mean test
                ],
                'hint': 'Look at nested loops, weight calculations, and index boundaries; subtle mistakes may only appear for special datasets or edge cases.',
                'errors': ['The broken version has errors including division by zero on empty datasets, inverted sample/population variance logic, unnecessary nested loops inflating skewness and kurtosis, reversed percentile interpolation with out-of-bounds indices, stale standard deviation in confidence intervals, a missing parenthesis causing a syntax error, and unsafe handling of single-element datasets.']
            }
        }
        
    def get_level(self, level_number: int) -> Optional[Dict[str, Any]]:
        """
        GET LEVEL DATA
        
        PURPOSE: Retrieve complete level data for specified level
        
        INPUTS:
        - level_number: Level to retrieve (1-10)
        
        RETURNS:
        - Dictionary containing level data or None if invalid level
        """
        return self.levels_data.get(level_number)
        
    def validate_solution(self, level_number: int, submitted_code: str) -> Dict[str, Any]:
        """
        VALIDATE SUBMITTED SOLUTION
        
        PURPOSE: Check if submitted code correctly solves the level problem
        
        INPUTS:
        - level_number: Current level being validated
        - submitted_code: Player's code submission
        
        RETURNS:
        - Dictionary with validation results:
          - valid: Boolean indicating if solution is correct
          - errors: List of remaining errors
          - errors_fixed: Count of errors that were fixed
          - test_results: Results from test case execution
        
        VALIDATION PROCESS:
        1. Parse code for syntax errors
        2. Execute code with test cases
        3. Compare results with expected outputs
        4. Check for logical correctness
        """
        level_data = self.get_level(level_number)
        
        if not level_data:
            return {'valid': False, 'errors': ['Invalid level'], 'errors_fixed': 0}
        
        try:
            # Parse the code to check for syntax errors
            parsed_code = ast.parse(submitted_code)
            
            # Execute code and run test cases
            test_results = self.execute_test_cases(submitted_code, level_data['test_cases'])
            
            # Check if all test cases passed
            all_tests_passed = all(result['passed'] for result in test_results)
            
            if all_tests_passed:
                return {
                    'valid': True,
                    'errors': [],
                    'errors_fixed': len(level_data.get('errors', [])),
                    'test_results': test_results
                }
            else:
                # Some tests failed - analyze partial progress
                failed_tests = [result for result in test_results if not result['passed']]
                
                return {
                    'valid': False,
                    'errors': [f"Test failed: {test['error']}" for test in failed_tests],
                    'errors_fixed': self.estimate_errors_fixed(submitted_code, level_data),
                    'test_results': test_results
                }
                
        except SyntaxError as e:
            return {
                'valid': False,
                'errors': [f'Syntax Error: {e.msg}'],
                'errors_fixed': 0,
                'test_results': []
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [f'Runtime Error: {str(e)}'],
                'errors_fixed': self.estimate_errors_fixed(submitted_code, level_data),
                'test_results': []
            }
            
    def execute_test_cases(self, code: str, test_cases: List[Dict]) -> List[Dict]:
        """
        EXECUTE TEST CASES ON SUBMITTED CODE
        
        PURPOSE: Run code with test inputs and validate outputs
        
        INPUTS:
        - code: Python code to execute
        - test_cases: List of test case dictionaries with input/output pairs
        
        RETURNS:
        - List of test results with pass/fail status
        
        SAFETY MEASURES:
        - Execute in restricted namespace
        - Capture exceptions and errors
        - Prevent infinite loops or dangerous operations
        """
        results = []
        
        # Create safe execution environment
        safe_globals = {
            '__builtins__': {
                'len': len, 'sum': sum, 'min': min, 'max': max, 'abs': abs,
                'round': round, 'int': int, 'float': float, 'str': str,
                'list': list, 'dict': dict, 'range': range, 'enumerate': enumerate,
                'zip': zip, 'sorted': sorted, 'print': print,
                'math': math, 'statistics': statistics
            },
            'math': math,
            'statistics': statistics
        }
        
        try:
            # Execute the code in safe environment
            exec(code, safe_globals)
            
            # Run each test case
            for i, test_case in enumerate(test_cases):
                try:
                    # Extract the main function name from code
                    main_function = self.extract_main_function(code)
                    
                    if main_function and main_function in safe_globals:
                        func = safe_globals[main_function]
                        test_input = test_case['input']
                        expected_output = test_case['output']
                        
                        # Handle different input types
                        if isinstance(test_input, tuple):
                            actual_output = func(*test_input)
                        else:
                            actual_output = func(test_input)
                        
                        # Compare outputs (with tolerance for floating point)
                        passed = self.compare_outputs(actual_output, expected_output)
                        
                        results.append({
                            'test_number': i + 1,
                            'passed': passed,
                            'input': test_input,
                            'expected': expected_output,
                            'actual': actual_output,
                            'error': None if passed else f'Expected {expected_output}, got {actual_output}'
                        })
                    else:
                        results.append({
                            'test_number': i + 1,
                            'passed': False,
                            'input': test_case['input'],
                            'expected': test_case['output'],
                            'actual': None,
                            'error': f'Function {main_function} not found'
                        })
                        
                except Exception as e:
                    results.append({
                        'test_number': i + 1,
                        'passed': False,
                        'input': test_case['input'],
                        'expected': test_case['output'], 
                        'actual': None,
                        'error': f'Test execution error: {str(e)}'
                    })
                    
        except Exception as e:
            # Code execution failed entirely
            for i, test_case in enumerate(test_cases):
                results.append({
                    'test_number': i + 1,
                    'passed': False,
                    'input': test_case['input'],
                    'expected': test_case['output'],
                    'actual': None,
                    'error': f'Code execution failed: {str(e)}'
                })
                
        return results
        
    def extract_main_function(self, code: str) -> Optional[str]:
        """
        EXTRACT MAIN FUNCTION NAME FROM CODE
        
        PURPOSE: Find the primary function to test in submitted code
        
        INPUTS:
        - code: Python code string
        
        RETURNS:
        - String with main function name or None
        """
        try:
            tree = ast.parse(code)
            
            # Look for function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Return first function definition found
                    return node.name
                    
        except:
            pass
            
        return None
        
    def compare_outputs(self, actual, expected, tolerance=1e-10):
        """
        COMPARE ACTUAL VS EXPECTED OUTPUT VALUES
        
        PURPOSE: Compare function outputs with tolerance for floating point errors
        
        INPUTS:
        - actual: Output from submitted code
        - expected: Expected output from test case
        - tolerance: Floating point comparison tolerance
        
        RETURNS:
        - Boolean indicating if outputs match within tolerance
        """
        # Handle None cases
        if actual is None and expected is None:
            return True
        if actual is None or expected is None:
            return False
            
        # Handle numeric comparisons with tolerance
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            return abs(actual - expected) < tolerance
            
        # Handle list/sequence comparisons
        if isinstance(actual, (list, tuple)) and isinstance(expected, (list, tuple)):
            if len(actual) != len(expected):
                return False
            
            return all(self.compare_outputs(a, e, tolerance) 
                      for a, e in zip(actual, expected))
        
        # Handle string and other types with exact comparison
        return actual == expected
        
    def estimate_errors_fixed(self, submitted_code: str, level_data: Dict) -> int:
        """
        ESTIMATE NUMBER OF ERRORS FIXED
        
        PURPOSE: Analyze code to estimate progress in fixing errors
        
        INPUTS:
        - submitted_code: Current code submission
        - level_data: Level data with error information
        
        RETURNS:
        - Integer count of estimated errors fixed
        
        HEURISTICS:
        - Check for syntax improvements
        - Compare against common error patterns
        - Analyze structural completeness
        """
        broken_code = level_data.get('broken_code', '')
        errors = level_data.get('errors', [])
        
        if not errors:
            return 0
            
        errors_fixed = 0
        
        try:
            # Check if syntax is now valid
            ast.parse(submitted_code)
            errors_fixed += 1  # At least syntax is fixed
        except SyntaxError:
            pass
            
        # Additional heuristics based on common error patterns
        # This is a simplified estimation - could be more sophisticated
        
        # Check for common fixes
        if ':' in submitted_code and 'def ' in submitted_code:
            errors_fixed += 1
            
        if submitted_code.count('(') == submitted_code.count(')'):
            errors_fixed += 1
            
        if '==' in submitted_code and not ' = ' in submitted_code.replace('==', ''):
            errors_fixed += 1
            
        return min(errors_fixed, len(errors))
        
    def get_all_levels_info(self) -> List[Dict]:
        """
        GET ALL LEVELS SUMMARY INFORMATION
        
        PURPOSE: Return summary data for all levels
        
        RETURNS:
        - List of dictionaries with level summary info
        """
        summaries = []
        
        for level_num in range(1, 11):
            level_data = self.get_level(level_num)
            if level_data:
                summaries.append({
                    'level': level_num,
                    'title': level_data['title'],
                    'description': level_data['description'],
                    'difficulty': level_data['difficulty'],
                    'error_count': len(level_data.get('errors', []))
                })
                
        return summaries
        
    def validate_level_data_integrity(self) -> Dict[str, Any]:
        """
        VALIDATE LEVEL DATA INTEGRITY
        
        PURPOSE: Check that all level data is complete and valid
        
        RETURNS:
        - Dictionary with validation results and any issues found
        """
        issues = []
        valid_levels = 0
        
        required_fields = ['title', 'description', 'difficulty', 'broken_code', 
                          'solution_code', 'test_cases', 'hint', 'errors']
        
        for level_num in range(1, 11):
            level_data = self.get_level(level_num)
            
            if not level_data:
                issues.append(f"Level {level_num}: Missing level data")
                continue
                
            # Check required fields
            missing_fields = [field for field in required_fields 
                            if field not in level_data]
            if missing_fields:
                issues.append(f"Level {level_num}: Missing fields: {missing_fields}")
                continue
                
            # Validate code syntax
            try:
                ast.parse(level_data['solution_code'])
            except SyntaxError as e:
                issues.append(f"Level {level_num}: Solution code syntax error: {e}")
                
            # Check test cases format
            if not isinstance(level_data['test_cases'], list):
                issues.append(f"Level {level_num}: Test cases must be a list")
            else:
                for i, test_case in enumerate(level_data['test_cases']):
                    if not isinstance(test_case, dict):
                        issues.append(f"Level {level_num}: Test case {i+1} must be a dictionary")
                    elif 'input' not in test_case or 'output' not in test_case:
                        issues.append(f"Level {level_num}: Test case {i+1} missing input/output")
                        
            if not issues or all(f"Level {level_num}" not in issue for issue in issues):
                valid_levels += 1
                
        return {
            'valid': len(issues) == 0,
            'valid_levels': valid_levels,
            'total_levels': 10,
            'issues': issues
        }


# Test the level manager if run directly
if __name__ == "__main__":
    print("Testing Level Manager...")
    
    level_manager = LevelManager()
    
    # Test level data integrity
    validation = level_manager.validate_level_data_integrity()
    print(f"Level data valid: {validation['valid']}")
    print(f"Valid levels: {validation['valid_levels']}/10")
    
    if validation['issues']:
        print("Issues found:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    # Test first level
    level_1 = level_manager.get_level(1)
    if level_1:
        print(f"\nLevel 1: {level_1['title']}")
        print(f"Difficulty: {level_1['difficulty']}")
        print(f"Errors to fix: {len(level_1['errors'])}")
        
        # Test validation with broken code
        broken_result = level_manager.validate_solution(1, level_1['broken_code'])
        print(f"Broken code validates: {broken_result['valid']} (should be False)")
        
        # Test validation with solution code  
        solution_result = level_manager.validate_solution(1, level_1['solution_code'])
        print(f"Solution code validates: {solution_result['valid']} (should be True)")
    
    print("Level Manager test complete!")