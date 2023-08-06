import time
from functools import wraps

class timeify(object):

    def __init__(self, return_time=None):
        """
        timeify simplifies measurement of functions
        run time with "@timeify()" decorator. Sample usage:

        @timeify()
        def squared(x):
            return x ** 2
        
        squared_numbers = squared([i for i in range(100)])
        >> Function squared took 3 seconds!

        if passed True, then function returns time in seconds:
        @timeify(True)
        def squared(x):
            return x ** 2
        >> answer, run_time = squared([i for i in range(100)])

        Inputs:
        =======
        return_time (bool): if return run_time as a result
        Outputs:
        ========
        None
        """
        
        self.return_time = return_time
        
    def __call__(self, func_to_timeify):
        """
        Wraps decorator and passes arguments to it.
        """

        @wraps(func_to_timeify)
        def timeified(*args, **kwargs):
            """
            Measures execution time of a function
            Inputs:
            ========
            function_to_timeify (function): function to measure execution time

            Outputs:
            ========
            answer (): answer from the timeified function
            """

            start_time = time.perf_counter()
            value = func_to_timeify(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"Function {func_to_timeify.__name__} took {run_time:.4f} seconds!")

            if self.return_time:
                return value, run_time
            else:
                return value

        return timeified