import time


def eval_and_time_function(some_function, *args, **kwargs):
    """
    Measures the time it takes to run a function, prints the function name, result,
    and execution time, and returns the result along with the execution time.

    Parameters:
        some_function (callable): The function to be executed.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        tuple: (result, elapsed_time) where:
               - result is the output of some_function.
               - elapsed_time is the time taken to execute the function, in seconds.
    """
    # Start the timer
    start_time = time.time()

    # Execute the function
    result = some_function(*args, **kwargs)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print the function name, result, and execution time
    function_name = some_function.__name__
    print(f"Function Name: {function_name}")
    print(f"Function Result: {result}")
    print(f"Execution Time: {elapsed_time:.4f} seconds")
    print()

    return result, elapsed_time

