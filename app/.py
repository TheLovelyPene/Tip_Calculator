# Copyright (c) 2025 [Your Name]. All rights reserved.
# TipEase: Group Event Financial Management Platform
# Proprietary software - unauthorized copying, distribution, or use is prohibited.

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime, timedelta
import uuid
import json
import os
import qrcode
import base64
import io
import secrets
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # In production, use a secure secret key

# Simple in-memory storage (in production, use a database)
events = {}
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events_list():
    return render_template('events.html', events=events)

@app.route('/event/<event_id>')
def event_detail(event_id):
    event = events.get(event_id)
    if not event:
        return redirect(url_for('index'))
    return render_template('event_detail.html', event=event)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        try:
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
                'status': 'planning',  # planning, active, completed
                'comments': [],
                'party_fund': [],  # List of contributions from non-attendees
                'payment_methods': {
                    'cashapp': data.get('cashapp_tag', ''),
                    'venmo': data.get('venmo_username', ''),
                    'zelle': data.get('zelle_email', ''),
                    'stripe': data.get('stripe_enabled', False)
                }
            }
            
            events[event_id] = event
            return jsonify({'success': True, 'event_id': event_id})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    return render_template('create_event.html')

@app.route('/event/<event_id>/join', methods=['POST'])
def join_event(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        guest = {
            'id': str(uuid.uuid4()),
            'name': data.get('name'),
            'email': data.get('email', ''),
            'payment_method': data.get('payment_method', 'card'),
            'rsvp_status': 'confirmed',  # confirmed, maybe, declined
            'joined_at': datetime.now().isoformat(),
            'is_birthday': data.get('is_birthday', False),
            'budget': float(data.get('budget', 0))  # How much they can afford
        }
        
        event['guests'].append(guest)
        
        # Add a comment about joining
        comment = {
            'id': str(uuid.uuid4()),
            'author': guest['name'],
            'text': f"🎉 {guest['name']} is joining the event!",
            'timestamp': datetime.now().isoformat(),
            'type': 'join'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'guest': guest})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/comment', methods=['POST'])
def add_comment(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        comment = {
            'id': str(uuid.uuid4()),
            'author': data.get('author', 'Anonymous'),
            'text': data.get('text'),
            'timestamp': datetime.now().isoformat(),
            'type': 'comment'
        }
        
        event['comments'].append(comment)
        return jsonify({'success': True, 'comment': comment})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/contribute', methods=['POST'])
def contribute_to_party_fund(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        contribution = {
            'id': str(uuid.uuid4()),
            'contributor_name': data.get('contributor_name', 'Anonymous'),
            'amount': float(data.get('amount', 0)),
            'message': data.get('message', ''),
            'is_anonymous': data.get('is_anonymous', False),
            'timestamp': datetime.now().isoformat()
        }
        
        event['party_fund'].append(contribution)
        
        # Add a comment about the contribution
        display_name = 'Anonymous' if contribution['is_anonymous'] else contribution['contributor_name']
        comment = {
            'id': str(uuid.uuid4()),
            'author': display_name,
            'text': f"💝 Contributed ${contribution['amount']:.2f} to the party fund{(' - ' + contribution['message']) if contribution['message'] else ''}",
            'timestamp': datetime.now().isoformat(),
            'type': 'contribution'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'contribution': contribution})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/process_payment', methods=['POST'])
def process_payment(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        payment_method = data.get('payment_method')
        amount = float(data.get('amount', 0))
        contributor_name = data.get('contributor_name', 'Anonymous')
        message = data.get('message', '')
        is_anonymous = data.get('is_anonymous', False)
        
        # Get organizer's payment info
        organizer_payments = event.get('payment_methods', {})
        
        if payment_method == 'cashapp' and organizer_payments.get('cashapp'):
            # Generate Cash App payment link
            cashapp_tag = organizer_payments['cashapp']
            cashapp_link = f"https://cash.app/${cashapp_tag}/{amount}"
            
            contribution = {
                'id': str(uuid.uuid4()),
                'contributor_name': contributor_name,
                'amount': amount,
                'message': message,
                'is_anonymous': is_anonymous,
                'payment_method': 'cashapp',
                'payment_link': cashapp_link,
                'status': 'pending',
                'timestamp': datetime.now().isoformat()
            }
            
        elif payment_method == 'venmo' and organizer_payments.get('venmo'):
            # Generate Venmo payment link
            venmo_username = organizer_payments['venmo']
            venmo_link = f"https://venmo.com/{venmo_username}?txn=pay&amount={amount}"
            
            contribution = {
                'id': str(uuid.uuid4()),
                'contributor_name': contributor_name,
                'amount': amount,
                'message': message,
                'is_anonymous': is_anonymous,
                'payment_method': 'venmo',
                'payment_link': venmo_link,
                'status': 'pending',
                'timestamp': datetime.now().isoformat()
            }
            
        elif payment_method == 'zelle' and organizer_payments.get('zelle'):
            # Zelle uses email or phone number for transfers
            zelle_email = organizer_payments['zelle']
            contribution_id = str(uuid.uuid4())
            
            # Generate mobile deep links for popular banking apps
            mobile_links = {
                'chase': f"chase://pay?recipient={zelle_email}&amount={amount}",
                'bankofamerica': f"bofa://zelle?to={zelle_email}&amount={amount}",
                'wellsfargo': f"wellsfargo://zelle?recipient={zelle_email}&amount={amount}",
                'citibank': f"citi://zelle?to={zelle_email}&amount={amount}"
            }
            
            # Zelle doesn't have direct payment links, so we provide instructions
            zelle_instructions = f"Send ${amount:.2f} to {zelle_email} via Zelle"
            
            contribution = {
                'id': contribution_id,
                'contributor_name': contributor_name,
                'amount': amount,
                'message': message,
                'is_anonymous': is_anonymous,
                'payment_method': 'zelle',
                'payment_link': f"mailto:{zelle_email}?subject=Zelle Payment for Event&body=Hi! I'm sending ${amount:.2f} via Zelle for the event.",
                'payment_instructions': zelle_instructions,
                'mobile_links': mobile_links,
                'qr_code_url': f"/event/{event_id}/qr_code/{contribution_id}",
                'status': 'pending',
                'timestamp': datetime.now().isoformat()
            }
            
        else:
            return jsonify({'error': 'Payment method not configured for this event'}), 400
        
        event['party_fund'].append(contribution)
        
        # Add a comment about the payment
        display_name = 'Anonymous' if is_anonymous else contributor_name
        comment = {
            'id': str(uuid.uuid4()),
            'author': display_name,
            'text': f"💳 Paid ${amount:.2f} via {payment_method.title()}{(' - ' + message) if message else ''}",
            'timestamp': datetime.now().isoformat(),
            'type': 'payment'
        }
        event['comments'].append(comment)
        
        return jsonify({
            'success': True, 
            'contribution': contribution,
            'payment_link': contribution['payment_link']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/update_bill', methods=['POST'])
def update_bill(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        event['bill_amount'] = float(data.get('bill_amount', 0))
        event['tip_percentage'] = float(data.get('tip_percentage', 15))
        event['status'] = 'active'
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/calculate', methods=['POST'])
def calculate_tip(event_id):
    try:
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        bill_amount = event.get('bill_amount', 0)
        tip_percentage = event.get('tip_percentage', 15)
        guests = event.get('guests', [])
        
        if len(guests) == 0:
            return jsonify({'error': 'No guests to split the bill with'}), 400
        
        # Calculate totals
        tip_amount = bill_amount * (tip_percentage / 100)
        total_amount = bill_amount + tip_amount
        
        # Count paying people (exclude birthdays)
        paying_guests = [guest for guest in guests if not guest.get('is_birthday', False)]
        num_paying = len(paying_guests)
        
        if num_paying == 0:
            return jsonify({'error': 'At least one person must pay (not everyone can have a birthday!)'}), 400
        
        # Calculate total budget from paying guests
        total_budget = sum(guest.get('budget', 0) for guest in paying_guests)
        
        # Calculate total party fund contributions
        total_party_fund = sum(contribution.get('amount', 0) for contribution in event.get('party_fund', []))
        
        # Calculate proportional splits based on budgets
        individual_breakdowns = []
        for guest in guests:
            if guest.get('is_birthday', False):
                breakdown = {
                    'name': guest['name'],
                    'payment_method': guest['payment_method'],
                    'is_birthday': True,
                    'budget': guest.get('budget', 0),
                    'bill_amount': 0,
                    'tip_amount': 0,
                    'total_amount': 0,
                    'birthday_message': f"🎉 Happy Birthday {guest['name']}! Your meal is on the house!"
                }
            else:
                # Calculate proportional amount based on budget
                guest_budget = guest.get('budget', 0)
                if total_budget > 0:
                    budget_ratio = guest_budget / total_budget
                    bill_portion = bill_amount * budget_ratio
                    tip_portion = tip_amount * budget_ratio
                    total_portion = total_amount * budget_ratio
                else:
                    # If no budgets set, split equally
                    bill_portion = bill_amount / num_paying
                    tip_portion = tip_amount / num_paying
                    total_portion = total_amount / num_paying
                
                # Apply party fund to reduce individual shares
                if total_party_fund > 0:
                    # Reduce each person's share proportionally
                    reduction_ratio = min(total_party_fund / total_amount, 1.0)  # Cap at 100%
                    bill_portion = max(0, bill_portion * (1 - reduction_ratio))
                    tip_portion = max(0, tip_portion * (1 - reduction_ratio))
                    total_portion = max(0, total_portion * (1 - reduction_ratio))
                
                breakdown = {
                    'name': guest['name'],
                    'payment_method': guest['payment_method'],
                    'is_birthday': False,
                    'budget': guest_budget,
                    'bill_amount': bill_portion,
                    'tip_amount': tip_portion,
                    'total_amount': total_portion
                }
            individual_breakdowns.append(breakdown)
        
        # individual_breakdowns is now calculated above with proportional budgeting
        
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
            'num_people': len(guests),
            'num_paying': num_paying,
            'total_budget': total_budget,
            'total_party_fund': total_party_fund,
            'cash_total': cash_total,
            'card_total': card_total,
            'cash_tip_total': cash_tip_total,
            'rounded_cash_tip': rounded_cash_tip,
            'extra_per_cash_payer': extra_per_cash_payer,
            'total_cash_collected': total_cash_collected
        }
        
        # Update event status
        event['status'] = 'completed'
        
        return jsonify({
            'summary': summary,
            'individual_breakdowns': individual_breakdowns
        })
        
    except ValueError as e:
        return jsonify({'error': 'Invalid input: Please enter valid numbers'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events')
def api_events():
    return jsonify(list(events.values()))

@app.route('/event/<event_id>/qr_code/<contribution_id>')
def generate_qr_code(event_id, contribution_id):
    """Generate QR code for Zelle payment"""
    try:
        event = events.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        contribution = next((c for c in event['party_fund'] if c['id'] == contribution_id), None)
        if not contribution or contribution['payment_method'] != 'zelle':
            return jsonify({'error': 'Zelle contribution not found'}), 404
        
        # Create QR code with Zelle payment info
        qr_data = {
            'type': 'zelle_payment',
            'event_id': event_id,
            'contribution_id': contribution_id,
            'amount': contribution['amount'],
            'recipient': event['payment_methods']['zelle'],
            'message': contribution['message'] or f"Payment for {event['title']}"
        }
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'qr_code': f"data:image/png;base64,{img_str}",
            'payment_info': qr_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event/<event_id>/verify_payment/<contribution_id>', methods=['POST'])
def verify_payment(event_id, contribution_id):
    """Mark payment as verified (organizer confirms receipt)"""
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        contribution = next((c for c in event['party_fund'] if c['id'] == contribution_id), None)
        if not contribution:
            return jsonify({'error': 'Contribution not found'}), 404
        
        # Verify two-factor authentication
        verification_code = data.get('verification_code')
        if not verify_2fa(event_id, verification_code):
            return jsonify({'error': 'Invalid verification code'}), 401
        
        # Update payment status
        contribution['status'] = 'completed'
        contribution['verified_at'] = datetime.now().isoformat()
        contribution['verified_by'] = data.get('verifier_name', 'Organizer')
        
        # Add verification comment
        comment = {
            'id': str(uuid.uuid4()),
            'author': 'Organizer',
            'text': f"✅ Payment of ${contribution['amount']:.2f} verified and received",
            'timestamp': datetime.now().isoformat(),
            'type': 'verification'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'contribution': contribution})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event/<event_id>/receipt/<contribution_id>')
def generate_receipt(event_id, contribution_id):
    """Generate payment receipt"""
    try:
        event = events.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        contribution = next((c for c in event['party_fund'] if c['id'] == contribution_id), None)
        if not contribution:
            return jsonify({'error': 'Contribution not found'}), 404
        
        receipt = {
            'receipt_id': f"REC-{contribution_id[:8].upper()}",
            'event_title': event['title'],
            'event_date': event['date'],
            'contributor_name': contribution['contributor_name'],
            'amount': contribution['amount'],
            'payment_method': contribution['payment_method'],
            'payment_date': contribution['timestamp'],
            'verified_date': contribution.get('verified_at'),
            'message': contribution['message'],
            'organizer': event['organizer']
        }
        
        return jsonify({'receipt': receipt})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event/<event_id>/milestone', methods=['POST'])
def set_payment_milestone(event_id):
    """Set payment milestone/cap for the event"""
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        milestone = {
            'id': str(uuid.uuid4()),
            'target_amount': float(data.get('target_amount', 0)),
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        if 'milestones' not in event:
            event['milestones'] = []
        
        event['milestones'].append(milestone)
        
        # Add milestone comment
        comment = {
            'id': str(uuid.uuid4()),
            'author': 'Organizer',
            'text': f"🎯 Payment milestone set: ${milestone['target_amount']:.2f} - {milestone['description']}",
            'timestamp': datetime.now().isoformat(),
            'type': 'milestone'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'milestone': milestone})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def verify_2fa(event_id, code):
    """Verify two-factor authentication code"""
    # In a real app, this would check against a stored code
    # For demo purposes, we'll use a simple hash
    expected_code = hashlib.md5(f"event_{event_id}".encode()).hexdigest()[:6].upper()
    return code == expected_code

def get_2fa_code(event_id):
    """Generate 2FA code for an event"""
    return hashlib.md5(f"event_{event_id}".encode()).hexdigest()[:6].upper()

if __name__ == '__main__':
    app.run(debug=True, port=5000)