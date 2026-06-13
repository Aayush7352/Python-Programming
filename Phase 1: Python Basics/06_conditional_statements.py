def main():
    score = int(input("Enter your score (0-100): "))

    # if-elif-else ladder
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(f"Score: {score}, Grade: {grade}")

    # Ternary operator
    status = "Pass" if score >= 60 else "Fail"
    print(f"Status: {status}")

    # Nested conditions
    if score >= 60:
        if score >= 90:
            print("Excellent work!")
        elif score >= 80:
            print("Good job!")
        else:
            print("You passed.")
    else:
        print("Better luck next time.")

    # Match-case (Python 3.10+)
    print("\n=== Match-Case ===")
    command = input("Enter a command (start/stop/restart): ")
    match command.lower():
        case "start":
            print("Starting the system...")
        case "stop":
            print("Stopping the system...")
        case "restart":
            print("Restarting the system...")
        case _:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
