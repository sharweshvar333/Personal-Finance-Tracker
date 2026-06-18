import time

def timer(func):

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(
            f"\nExecution Time: {end - start:.4f} seconds"
        )

        return result

    return wrapper

def validate_input(func):

    def wrapper(*args, **kwargs):

        amount = args[0]

        if amount <= 0:

            print(
                "Error: Amount must be greater than 0"
            )

            return

        return func(*args, **kwargs)

    return wrapper