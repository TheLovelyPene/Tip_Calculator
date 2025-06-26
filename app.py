from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def tip_calculator():
    result = None
    error = None
    if request.method == 'POST':
        try:
            bill_amount = float(request.form['bill'])
            tip_percentage = float(request.form['tip'])
            num_people = int(request.form['num_people'])
            any_birthday = request.form.get('any_birthday') == 'yes'
            names = request.form.getlist('name')
            payment_methods = request.form.getlist('payment_method')
            birthdays = request.form.getlist('is_birthday') if any_birthday else ["no"] * num_people

            if bill_amount < 0 or not (0 <= tip_percentage <= 100):
                raise ValueError('Invalid bill or tip')
            if not (1 <= num_people <= 30):
                raise ValueError('Invalid number of people')

            tip_decimal = tip_percentage / 100
            tip_amount = bill_amount * tip_decimal
            total_bill = bill_amount + tip_amount

            person_details = []
            paying_people_count = 0
            for i in range(num_people):
                name = names[i] if names[i].strip() else f"Person {i+1}"
                payment_method = payment_methods[i]
                is_birthday = (birthdays[i] == 'yes') if any_birthday else False
                if not is_birthday:
                    paying_people_count += 1
                person_details.append({
                    'id': i+1,
                    'name': name,
                    'payment_method': payment_method,
                    'is_birthday': is_birthday
                })

            if paying_people_count > 0:
                bill_per_paying_person = total_bill / paying_people_count
                individual_bill_portion = bill_amount / paying_people_count
                individual_tip_portion = tip_amount / paying_people_count
            else:
                bill_per_paying_person = 0.0
                individual_bill_portion = 0.0
                individual_tip_portion = 0.0

            cash_total_owed = 0.0
            card_total_owed = 0.0
            for person in person_details:
                if not person['is_birthday']:
                    if person['payment_method'] == 'cash':
                        cash_total_owed += bill_per_paying_person
                    else:
                        card_total_owed += bill_per_paying_person

            result = {
                'bill_amount': bill_amount,
                'tip_percentage': tip_percentage,
                'tip_amount': tip_amount,
                'total_bill': total_bill,
                'num_people': num_people,
                'paying_people_count': paying_people_count,
                'person_details': person_details,
                'bill_per_paying_person': bill_per_paying_person,
                'individual_bill_portion': individual_bill_portion,
                'individual_tip_portion': individual_tip_portion,
                'cash_total_owed': cash_total_owed,
                'card_total_owed': card_total_owed,
                'any_birthday': any_birthday
            }
        except Exception as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)