# Python Tips and Tricks

## Lambda Functions
Lambda functions are small anonymous functions in Python. They can take any number of arguments, but can only have one expression.

```python
square = lambda x: x ** 2
print(square(5))  # Output: 25
```

Lambda functions are useful for short operations that are used once or a few times.

## List Comprehensions
List comprehensions provide a concise way to create lists. They consist of brackets containing an expression followed by a for clause.

```python
squares = [x**2 for x in range(10)]
print(squares)  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

This is much more efficient than using a for loop to append items.

## Decorators
Decorators are functions that modify the behavior of a function or class. They are often used for logging, validation, and timing.

```python
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start}")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```
