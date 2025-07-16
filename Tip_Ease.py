# --- TipEase: Simple Tip Calculator ---
# Copyright (c) 2025 [Your Name]. All rights reserved.
#
# This program calculates the tip amount and the total bill based on user input.
# It now includes features for splitting the bill among multiple people,
# tracking payment methods (cash/card), a birthday toggle for non-payment,
# individual names, detailed card payment specifics, and a clear payment summary.
# Final touches for improved user experience have been applied.
#
# Proprietary software - unauthorized copying, distribution, or use is prohibited.

def calculate_tip():
    """
    Prompts the user for bill amount, tip percentage, number of people,
    individual names, payment methods, and birthday status.
    Then calculates and displays the overall tip and total,
    along with individual amounts to pay, payment methods,
    and a summary of cash vs. card totals.
    Ensures robust input validation and clear output.
    """
    print("--- Welcome to TipEase! ---")
    print("Let's calculate your tip and total bill, and split it!")
    print("\n--- Getting Bill and Tip Details ---") # Added introductory line

    # --- 1. Gather Initial Inputs (Bill Amount & Tip Percentage) ---
    bill_amount = 0.0
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

    tip_percentage = 0.0
    while True:
        try:
            tip_percentage_str = input("Enter the desired tip percentage (e.g., 15 for 15%): ")
            tip_percentage = float(tip_percentage_str)
            # Ensure percentage is within a reasonable range (0 to 100)
            if not (0 <= tip_percentage <= 100):
                print("Tip percentage must be between 0 and 100. Please try again.")
            else:
                break # Exit loop if input is valid
        except ValueError:
            print("Invalid input. Please enter a numerical value for the percentage.")

    # Convert tip percentage to a decimal for calculation (e.g., 15% -> 0.15)
    tip_decimal = tip_percentage / 100

    # --- 2. Calculate Overall Tip and Total ---
    tip_amount = bill_amount * tip_decimal
    total_bill = bill_amount + tip_amount

    # --- 3. Gather Split Bill & Individual Payment Inputs ---
    print("\n--- Setting Up the Split ---") # Added introductory line
    num_people = 0
    while True:
        try:
            num_people_str = input("How many people are splitting the bill (1-30)? ")
            num_people = int(num_people_str)
            if not (1 <= num_people <= 30):
                print("Please enter a number between 1 and 30.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a whole number for the number of people.")

    # Ask if anyone is celebrating a birthday upfront
    any_birthday = False
    while True:
        any_birthday_str = input("Is anyone celebrating a birthday today? (yes/no): ").strip().lower()
        if any_birthday_str in ['yes', 'no']:
            any_birthday = (any_birthday_str == 'yes')
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    person_details = []
    paying_people_count = 0

    print("\n--- Enter Details for Each Person ---") # Added introductory line
    for i in range(num_people):
        person_info = {}
        person_info['id'] = i + 1

        # Prompt for person's name
        person_info['name'] = input(f"Person {i + 1}: What is their name? (e.g., John): ").strip()
        if not person_info['name']: # Default name if left blank
            person_info['name'] = f"Person {i + 1}"

        # Get payment method (cash/card)
        while True:
            payment_method = input(f"{person_info['name']}: Paying by cash or card? (cash/card): ").strip().lower()
            if payment_method in ['cash', 'card']:
                person_info['payment_method'] = payment_method
                break
            else:
                print("Invalid input. Please enter 'cash' or 'card'.")

        # Get birthday status only if 'any_birthday' was true
        if any_birthday:
            while True:
                is_birthday_str = input(f"{person_info['name']}: Is it their birthday? (yes/no): ").strip().lower()
                if is_birthday_str in ['yes', 'no']:
                    person_info['is_birthday'] = (is_birthday_str == 'yes')
                    if not person_info['is_birthday']:
                        paying_people_count += 1 # Only count if not birthday
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        else:
            # If no one is celebrating a birthday, everyone pays
            person_info['is_birthday'] = False
            paying_people_count += 1 # Everyone contributes

        person_details.append(person_info)

    # --- 4. Calculate Individual Amounts ---
    bill_per_paying_person = 0.0
    individual_bill_portion = 0.0 # Portion of the original bill for each paying person
    individual_tip_portion = 0.0  # Portion of the total tip for each paying person

    if paying_people_count > 0:
        bill_per_paying_person = total_bill / paying_people_count
        individual_bill_portion = bill_amount / paying_people_count
        individual_tip_portion = tip_amount / paying_people_count
    else:
        # This case happens if everyone is having a birthday and no one is paying
        print("\nEveryone is celebrating a birthday! The total bill is $0 for those paying.")

    # --- 5. Display Results ---
    print("\n--- Overall Calculation Summary ---")
    print(f"Original Bill: ${bill_amount:.2f}")
    print(f"Tip Percentage: {tip_percentage:.0f}%")
    print(f"Calculated Tip: ${tip_amount:.2f}")
    print(f"Total Bill (including tip): ${total_bill:.2f}")
    print(f"Number of people splitting: {num_people}")
    print(f"Number of people actually paying: {paying_people_count}")
    print("----------------------------------\n")

    print("--- Individual Breakdown ---")
    cash_total_owed = 0.0
    card_total_owed = 0.0

    for person in person_details:
        person_name = person['name']
        person_id = person['id']
        payment_method = person['payment_method']
        is_birthday = person['is_birthday']

        amount_to_pay = 0.0
        status = ""

        if is_birthday:
            amount_to_pay = 0.0 # Birthday means no payment
            status = "(Birthday - Not Paying)"
        else:
            amount_to_pay = bill_per_paying_person
            if payment_method == 'cash':
                cash_total_owed += amount_to_pay
            else: # card
                card_total_owed += amount_to_pay

        print(f"{person_name} (Person {person_id}):")
        print(f"  Payment Method: {payment_method.capitalize()}")

        if is_birthday:
            print(f"  Amount to Pay: ${amount_to_pay:.2f} {status}")
        elif payment_method == 'card':
            # Detailed breakdown for card payments
            print(f"  Total to Pay: ${amount_to_pay:.2f}")
            print(f"    - Bill Portion: ${individual_bill_portion:.2f}")
            print(f"    - Tip Portion:  ${individual_tip_portion:.2f}")
        else: # cash payment
            print(f"  Amount to Pay: ${amount_to_pay:.2f}")
        print("-" * 20) # Separator for readability

    print("\n--- Payment Method Summary ---")
    print(f"Total to collect in Cash: ${cash_total_owed:.2f}")
    print(f"Total to collect by Card: ${card_total_owed:.2f}")
    print("------------------------------\n")

    print("Thank you for using TipEase! Have a great day!") # Final goodbye message

# Call the main function to run the tip calculator when the script is executed.
if __name__ == "__main__":
    calculate_tip()
