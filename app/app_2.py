from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        
        # Calculate per person amounts
        bill_per_person = bill_amount / num_paying
        tip_per_person = tip_amount / num_paying
        total_per_person = total_amount / num_paying
        
        # Create individual breakdowns
        individual_breakdowns = []
        for person in people:
            if person.get('is_birthday', False):
                breakdown = {
                    'name': person['name'],
                    'payment_method': person['payment_method'],
                    'is_birthday': True,
                    'bill_amount': 0,
                    'tip_amount': 0,
                    'total_amount': 0,
                    'birthday_message': f"🎉 Happy Birthday {person['name']}! Your meal is on the house!"
                }
            else:
                breakdown = {
                    'name': person['name'],
                    'payment_method': person['payment_method'],
                    'is_birthday': False,
                    'bill_amount': bill_per_person,
                    'tip_amount': tip_per_person,
                    'total_amount': total_per_person
                }
            individual_breakdowns.append(breakdown)
        
        # Calculate payment method totals
        cash_total = sum(b['total_amount'] for b in individual_breakdowns if b['payment_method'] == 'cash')
        card_total = sum(b['total_amount'] for b in individual_breakdowns if b['payment_method'] == 'card')
        
        # Create summary
        summary = {
            'bill_amount': bill_amount,
            'tip_percentage': tip_percentage,
            'tip_amount': tip_amount,
            'total_amount': total_amount,
            'num_people': num_people,
            'num_paying': num_paying,
            'bill_per_person': bill_per_person,
            'tip_per_person': tip_per_person,
            'total_per_person': total_per_person,
            'cash_total': cash_total,
            'card_total': card_total
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
    print("Visit: http://127.0.0.1:5000/")
    app.run(debug=True, host='127.0.0.1', port=5000)
   