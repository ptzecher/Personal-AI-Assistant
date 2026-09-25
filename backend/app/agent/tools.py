def calculator(args: list[float], operation: str):

    """
    Performs a mathematical operation on a list of numbers.

    Args:
        args: The numbers to perform the operation on.
        operation: The operation to perform.
                   Supported operations are:
                   add, subtract, multiply, divide.

    Returns:
        The result of the calculation.
    """
    print(f"CALCULATOR TOOL CALLED: {operation=} {args=}")

    if not args:
        raise ValueError("args cannot be empty")

    if operation == "add":
        return sum(args)

    elif operation == "multiply":
        result = 1

        for x in args:
            result *= x

        return result

    elif operation == "divide":
        result = args[0]

        for x in args[1:]:
            if x == 0:
                raise ValueError("Cannot divide by zero")

            result /= x

        return result

    elif operation == "subtract":
        return args[0] - sum(args[1:])

    else:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )





