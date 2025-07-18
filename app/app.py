# Copyright (c) 2025 [Your Name]. All rights reserved.
# TipEase: Group Event Financial Management Platform
# Proprietary software - unauthorized copying, distribution, or use is prohibited.

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# In-memory storage for demo
events = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events_list():
    return render_template('events.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        data = request.json or {}
        event_id = str(uuid.uuid4())
        event = {
            'id': event_id,
            'title': data.get('title', 'Dinner Event'),
            'description': data.get('description', ''),
            'date': data.get('date'),
            'time': data.get('time'),
            'location': data.get('location', ''),
            'organizer': data.get('organizer', 'Anonymous'),
            'created_at': datetime.now().isoformat(),
            'guests': [],
            'bill_amount': 0,
            'tip_percentage': 15,
            'status': 'planning',
            'comments': [],
            'party_fund': [],
            'payment_methods': {}
        }
        events[event_id] = event
        return jsonify({'success': True, 'event_id': event_id})
    return render_template('create_event.html')

@app.route('/event/<event_id>')
def event_detail(event_id):
    event = events.get(event_id)
    if not event:
        return redirect(url_for('index'))
    return render_template('event_detail.html', event=event)

@app.route('/event/<event_id>/join', methods=['POST'])
def join_event(event_id):
    data = request.json or {}
    event = events.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    guest = {
        'id': str(uuid.uuid4()),
        'name': data.get('name'),
        'email': data.get('email', ''),
        'payment_method': data.get('payment_method', 'card'),
        'rsvp_status': 'confirmed',
        'joined_at': datetime.now().isoformat(),
        'is_birthday': data.get('is_birthday', False),
        'budget': float(data.get('budget', 0))
    }
    event['guests'].append(guest)
    return jsonify({'success': True, 'guest': guest})

@app.route('/event/<event_id>/calculate', methods=['POST'])
def calculate_bill(event_id):
    event = events.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404

    bill_amount = event.get('bill_amount', 0)
    tip_percentage = event.get('tip_percentage', 15)
    guests = event.get('guests', [])
    num_paying = sum(1 for g in guests if not g.get('is_birthday', False))

    tip_amount = bill_amount * (tip_percentage / 100)
    total_amount = bill_amount + tip_amount

    if num_paying == 0:
        return jsonify({'error': 'No paying guests'}), 400

    bill_per_person = bill_amount / num_paying
    tip_per_person = tip_amount / num_paying
    total_per_person = total_amount / num_paying

    breakdown = []
    for guest in guests:
        if guest.get('is_birthday', False):
            breakdown.append({
                'name': guest['name'],
                'is_birthday': True,
                'bill': 0,
                'tip': 0,
                'total': 0
            })
        else:
            breakdown.append({
                'name': guest['name'],
                'is_birthday': False,
                'bill': bill_per_person,
                'tip': tip_per_person,
                'total': total_per_person
            })

    return jsonify({
        'bill_amount': bill_amount,
        'tip_percentage': tip_percentage,
        'tip_amount': tip_amount,
        'total_amount': total_amount,
        'breakdown': breakdown
    })

@app.route('/event/<event_id>/update_bill', methods=['POST'])
def update_bill(event_id):
    event = events.get(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    data = request.json or {}
    bill_amount = data.get('bill_amount', 0)
    tip_percentage = data.get('tip_percentage', 15)
    
    event['bill_amount'] = float(bill_amount)
    event['tip_percentage'] = float(tip_percentage)
    
    return jsonify({'success': True, 'message': 'Bill updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)