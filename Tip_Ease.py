# --- TipEase: Simple Tip Calculator ---
#
# This program calculates the tip amount and the total bill based on user input.
# It covers the essential core features for the first version of TipEase.

def calculate_tip():
    """
    Prompts the user for bill amount and tip percentage,
    then calculates and displays the tip and total bill.
    """
    print("--- Welcome to TipEase! ---")
    print("Let's calculate your tip and total bill.")

    # 1. Gather Inputs
    # Get the bill amount from the user.
    # Use a loop to ensure valid numerical input.
    while True:
        try:
            bill_amount_str = input("Enter the total bill amount (e.g., 50.75): $")
            bill_amount = float(bill_amount_str)
            if bill_amount < 0:
                print("Bill amount cannot be negative. Please enter a positive number.")
            else:
                break # Exit loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a numerical value for the bill.")

    # Get the tip percentage from the user.
    # Use a loop to ensure valid numerical input.
    while True:
        try:
            tip_percentage_str = input("Enter the desired tip percentage (e.g., 15 for 15%): ")
            tip_percentage = float(tip_percentage_str)
            if not (0 <= tip_percentage <= 100): # Ensure percentage is within a reasonable range
                print("Tip percentage must be between 0 and 100. Please try again.")
            else:
                break # Exit loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a numerical value for the percentage.")

    # Convert tip percentage to a decimal for calculation (e.g., 15% -> 0.15)
    tip_decimal = tip_percentage / 100

    # 2. Calculate Tip
    # Calculate the tip amount.
    tip_amount = bill_amount * tip_decimal

    # 3. Calculate Total
    # Calculate the total bill including the tip.
    total_bill = bill_amount + tip_amount

    # 4. Display Results
    print("\n--- Calculation Summary ---")
    print(f"Original Bill: ${bill_amount:.2f}") # .2f formats to two decimal places
    print(f"Tip Percentage: {tip_percentage:.0f}%") # .0f formats to no decimal places
    print(f"Calculated Tip: ${tip_amount:.2f}")
    print(f"Total Bill: ${total_bill:.2f}")
    print("---------------------------\n")

# Call the function to run the tip calculator when the script is executed.
if __name__ == "__main__":
    calculate_tip()
