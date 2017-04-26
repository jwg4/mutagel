def fibonacci(n):
    if n < 2:
        return 0
    else:
        return fibonacci(n-2) + fibonacci(n-1)
