TipEaseAbout This ProjectThe purpose of TipEase is to provide users with a quick, easy, and accurate tool for calculating tips and final bill totals. It simplifies the process of dining out or tipping for services by allowing users to split bills among multiple people, track payment methods (cash or card), and account for special cases like birthdays where a person might not contribute to the bill.How It Works (Core Logic)TipEase is a console-based Python application that follows these main logical steps:Initial Input Gathering:It first prompts the user to enter the total bill amount and the desired tip percentage. Robust input validation is in place to ensure these are valid numerical entries.Overall Calculation:Based on the bill amount and tip percentage, it calculates the total tip amount and the grand total bill (bill + tip).Split Setup and Individual Details:The program then asks for the total number of people splitting the bill (up to 30), with validation.It includes a preliminary question: "Is anyone celebrating a birthday today?" This acts as a global toggle.For each person, it prompts for their name, their preferred payment method (cash or card), and, if the global birthday toggle was 'yes', it asks if it's their birthday. Input is validated for each of these prompts.Individual Amount Calculation:The program determines the number of 'paying' people (excluding those celebrating a birthday).The total bill (including tip) is then divided equally among only the paying individuals to calculate each person's share.If everyone is a birthday person, it gracefully handles the case where no one pays.Display Results:Finally, TipEase presents a comprehensive summary:Overall Summary: Shows the original bill, tip percentage, calculated tip, and the grand total bill.Individual Breakdown: For each person, it lists their name, payment method, and the amount they need to pay. For card payments, it provides a detailed breakdown of their portion of the original bill and their portion of the tip. Birthday celebrants are clearly marked as not paying.Payment Method Summary: Provides a clear total amount to be collected in cash versus the total to be paid by card.How to Run ItTo run the TipEase project:Save the Code: Copy the Python code provided (from the tipease_python_code artifact) and save it in a file named tipease.py (or any other name ending with .py) on your computer.Open Terminal/Command Prompt: Navigate to the directory where you saved tipease.py using your terminal or command prompt.Execute the Script: Run the script using the Python interpreter:python tipease.py
Follow Prompts: The program will then guide you through the process by asking for the bill amount, tip percentage, number of people, and individual details.. Please enter a positive number.")
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
```

## Features

- **Input Validation**: Ensures bill amount is positive and tip percentage is between 0-100%
- **Error Handling**: Gracefully handles invalid numerical inputs
- **Clear Output**: Displays a formatted summary of the calculation
- **User-Friendly**: Provides clear prompts and instructions
