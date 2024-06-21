import pandas as pd


# Lambda Functions: Compact Powerhouses of Python

''' Lambda functions, also known as anonymous functions, are concise, single-expression functions 
    that don't require a traditional def keyword and function name. They offer a convenient way to 
    write short, focused functions on the fly, especially when you need a function as an argument 
    to other functions.
    
    Syntax:

        The basic syntax of a lambda function is:

            lambda arguments: expression 

        lambda: The keyword that signals you're creating a lambda function.
        arguments: A comma-separated list of zero or more arguments (just like in regular functions).
        expression: A single expression that the lambda function evaluates and returns. '''

#%%
# Example 1

square = lambda x: x * x

result = square(5)
print(result)

#%%
# Example 2

def square(n):
    return n*n

df = pd.DataFrame(data={'x':[1,2,3,4,5],'y':[6,7,8,9,10]})

df['x'] = df['x'].map(lambda x : x*x)
df['y'] = df['y'].map(square)

# The map function applies any function to each element in the numbers list, 
# resulting in a new list.

#%%
# Example 3

def even(n):
    if n%2 == 0:
        return True

def odd(n):
    if n%2 != 0:
        return True

df = pd.DataFrame(data={'x':[1,2,3,4,5],'y':[6,7,8,9,10]})

evens_x = list(filter(lambda x: x%2 == 0, df['x']))
odds_y = list(filter(lambda x: x%2 != 0, df['y']))

evens_x = list(filter(even, df['x']))
odds_y = list(filter(odd, df['y']))

# The filter function uses a function to test each element in the numbers list, 
# keeping only those that satisfy a condition.
