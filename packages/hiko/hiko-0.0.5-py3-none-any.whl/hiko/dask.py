from functools import wraps

class daskify(object):

    def __init__(self, address=None):
        """
        daskify simplifies mapping functions to iterables.
        Instead of writing Dask code, just decorate function
        with "@daskify()". Sample usage:
        
        @daskify()
        def squared(x):
            return x ** 2
        
        squared_numbers = squared([i for i in range(100)])

        Inputs:
        =======
        address (string): cluster address for
        Dask cluster setup. For example, "127.0.0.1:8786"
        Outputs:
        ========
        None
        """
        
        self.address = address
        
    def __call__(self, func_to_daskify):
        """
        Wraps decorator and passes arguments to it.
        """

        @wraps(func_to_daskify)
        def daskified(*args, **kwargs):
            """
            Maps function to an iterable. Does that in parallel
            via Dask
            Inputs:
            ========
            function_to_daskify (function): function we want to run
            in parallel
            self.address (string): address to start Dask cluster (if provided)

            Outputs:
            ========
            answer (list): computed list with results from Dask
            """
            from dask.distributed import Client
            c = Client(self.address) if self.address else Client()
            answer = c.gather(c.map(func_to_daskify, *args))
            c.close()
            return answer

        return daskified