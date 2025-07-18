from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def simple_ui():
    result = None
    error = None
    if request.method == 'POST':
        try:
            bill_amount = float(request.form.get('bill_amount', 0))
            tip_percentage = float(request.form.get('tip_percentage', 15))
            people = []
            num_people = int(request.form.get('num_people', 1))
            for i in range(num_people):
                name = request.form.get(f'name_{i}', f'Person {i+1}')
                payment_method = request.form.get(f'payment_method_{i}', 'cash')
                is_birthday = request.form.get(f'is_birthday_{i}') == 'on'
                budget = float(request.form.get(f'budget_{i}', 0))
                people.append({
                    'name': name,
                    'payment_method': payment_method,
                    'is_birthday': is_birthday,
                    'budget': budget
                })
            # Use the same logic as /calculate
            api_url = request.url_root.rstrip('/') + '/calculate'
            api_resp = requests.post(api_url, json={
                'bill_amount': bill_amount,
                'tip_percentage': tip_percentage,
                'num_people': num_people,
                'people': people
            })
            if api_resp.ok:
                result = api_resp.json()
            else:
                error = api_resp.text
        except Exception as e:
            error = str(e)
    return render_template('simple_ui.html', result=result, error=error)

@app.route('/calculate', methods=['POST'])
def calculate_tip():
    try:
        data = request.json
        
        # Get basic inputs
        bill_amount = float(data.get('bill_amount', 0))
        tip_percentage = float(data.get('tip_percentage', 15))
        num_people = int(data.get('num_people', 1))
        
        # Get people data
        people = data.get('people', [])
        
        if len(people) != num_people:
            return jsonify({'error': 'Number of people does not match people data'}), 400
        
        # Calculate totals
        tip_amount = bill_amount * (tip_percentage / 100)
        total_amount = bill_amount + tip_amount
        
        # Count paying people (exclude birthdays)
        paying_people = [person for person in people if not person.get('is_birthday', False)]
        num_paying = len(paying_people)
        
        if num_paying == 0:
            return jsonify({'error': 'At least one person must pay (not everyone can have a birthday!)'}), 400
        
        # --- Budget logic ---
        total_budget = sum(float(person.get('budget', 0)) for person in paying_people)
        use_budget = total_budget > 0
        
        # Create individual breakdowns
        individual_breakdowns = []
        for person in people:
            if person.get('is_birthday', False):
                breakdown = {
                    'name': person['name'],
                    'payment_method': person['payment_method'],
                    'is_birthday': True,
                    'budget': float(person.get('budget', 0)),
                    'bill_amount': 0,
                    'tip_amount': 0,
                    'total_amount': 0,
                    'birthday_message': f"🎉 Happy Birthday {person['name']}! Your meal is on the house!"
                }
            else:
                person_budget = float(person.get('budget', 0))
                if use_budget:
                    budget_ratio = person_budget / total_budget if total_budget > 0 else 1/num_paying
                    bill_portion = bill_amount * budget_ratio
                    tip_portion = tip_amount * budget_ratio
                    total_portion = total_amount * budget_ratio
                else:
                    bill_portion = bill_amount / num_paying
                    tip_portion = tip_amount / num_paying
                    total_portion = total_amount / num_paying
                breakdown = {
                    'name': person['name'],
                    'payment_method': person['payment_method'],
                    'is_birthday': False,
                    'budget': person_budget,
                    'bill_amount': bill_portion,
                    'tip_amount': tip_portion,
                    'total_amount': total_portion
                }
            individual_breakdowns.append(breakdown)
        
        # Calculate payment method totals
        cash_total = sum(b['total_amount'] for b in individual_breakdowns if b['payment_method'] == 'cash')
        card_total = sum(b['total_amount'] for b in individual_breakdowns if b['payment_method'] == 'card')
        cash_tip_total = sum(b['tip_amount'] for b in individual_breakdowns if b['payment_method'] == 'cash')
        # Suggest a rounded tip (nearest $1)
        rounded_cash_tip = round(cash_tip_total + 0.5)
        extra_per_cash_payer = 0
        num_cash_payers = sum(1 for b in individual_breakdowns if b['payment_method'] == 'cash' and not b['is_birthday'])
        if num_cash_payers > 0:
            extra_per_cash_payer = max(0, (rounded_cash_tip - cash_tip_total) / num_cash_payers)
        total_cash_collected = cash_total - cash_tip_total + rounded_cash_tip
        # Create summary
        summary = {
            'bill_amount': bill_amount,
            'tip_percentage': tip_percentage,
            'tip_amount': tip_amount,
            'total_amount': total_amount,
            'num_people': num_people,
            'num_paying': num_paying,
            'total_budget': total_budget,
            'cash_total': cash_total,
            'card_total': card_total,
            'cash_tip_total': cash_tip_total,
            'rounded_cash_tip': rounded_cash_tip,
            'extra_per_cash_payer': extra_per_cash_payer,
            'total_cash_collected': total_cash_collected
        }
        
        return jsonify({
            'summary': summary,
            'individual_breakdowns': individual_breakdowns
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid input: Please enter valid numbers'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Visit: http://127.0.0.1:5001/")
app.run(debug=True, port=5001)