def sqrt_newton_raphson(number, tolerance=1e-10):
    if number < 0:
        raise ValueError("Cannot compute square root of a negative number")
    if number == 0:
        return 0

    guess = number / 2.0  # initial guess

    while True:
        new_guess = 0.5 * (guess + number / guess)
        if abs(new_guess - guess) < tolerance:
            break
        guess = new_guess

    return new_guess


# Example usage
if __name__ == "__main__":
    num = float(input("\nEnter a number: "))
    result = sqrt_newton_raphson(num)
    print(f"\nThe square root of {num} is approximately {result}\n")