# Copyright (c) 2025 [Your Name]. All rights reserved.
# TipEase: Group Event Financial Management Platform
# Proprietary software - unauthorized copying, distribution, or use is prohibited.

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import uuid
import os
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'events'), exist_ok=True)

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
            'expected_budget': float(data.get('expected_budget', 0)),
            'capacity': data.get('capacity'),
            'created_at': datetime.now().isoformat(),
            'guests': [],
            'bill_amount': 0,
            'tip_percentage': 15,
            'status': 'planning',
        join_message = f"🎉 {guest['name']} joined the event!"
        if guest['message']:
            join_message += f" Message: \"{guest['message']}\""
        if guest['budget'] > 0:
            join_message += f" Pre-committed: ${guest['budget']:.2f}"
        
            'comments': [],
            'party_fund': [],
            'budget': float(data.get('budget', 0)),
            'dietary_restrictions': data.get('dietary_restrictions', ''),
            'commitment_level': 'high' if float(data.get('budget', 0)) >= 30 else 'medium' if float(data.get('budget', 0)) >= 15 else 'low',
            'payment_methods': {
                'paypal_email': data.get('paypal_email', ''),
                'cashapp_tag': data.get('cashapp_tag', ''),
                'venmo_username': data.get('venmo_username', ''),
                'zelle_email': data.get('zelle_email', '')
            },
            'media_gallery': [],  # For event day photos/videos
            'live_updates': [],   # Real-time event updates
            'check_ins': []       # Guest check-ins on event day
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
        'phone': data.get('phone', ''),
        'payment_method': data.get('payment_method', 'card'),
        'rsvp_status': 'confirmed',
        'joined_at': datetime.now().isoformat(),
        'is_birthday': data.get('is_birthday', False),
        'budget': float(data.get('budget', 0)),
        'message': data.get('message', ''),
        'dietary_restrictions': data.get('dietary_restrictions', ''),
        'commitment_level': 'high' if float(data.get('budget', 0)) >= 30 else 'medium' if float(data.get('budget', 0)) >= 15 else 'low',
        'avatar_color': data.get('avatar_color', '#FF6B6B'),  # Random color for avatar
        'checked_in': False,
        'check_in_time': None
    }
    event['guests'].append(guest)
    
    # Add join comment
    join_message = f"🎉 {guest['name']} joined the event!"
    if guest['message']:
        join_message += f" Message: \"{guest['message']}\""
    if guest['budget'] > 0:
        join_message += f" Pre-committed: ${guest['budget']:.2f}"
    
    comment = {
        'id': str(uuid.uuid4()),
        'author': guest['name'],
        'author_color': guest['avatar_color'],
        'text': join_message,
        'timestamp': datetime.now().isoformat(),
        'type': 'join'
    }
    event['comments'].append(comment)
    
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
            'author_color': data.get('author_color', '#667eea'),
            'text': data.get('text'),
            'timestamp': datetime.now().isoformat(),
            'type': 'comment'
        }
        
        event['comments'].append(comment)
        return jsonify({'success': True, 'comment': comment})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/check_in', methods=['POST'])
def check_in_guest(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        guest_name = data.get('guest_name')
        guest = next((g for g in event['guests'] if g['name'] == guest_name), None)
        
        if not guest:
            return jsonify({'error': 'Guest not found'}), 404
        
        if guest['checked_in']:
            return jsonify({'error': 'Already checked in'}), 400
        
        guest['checked_in'] = True
        guest['check_in_time'] = datetime.now().isoformat()
        
        # Add check-in to event updates
        check_in = {
            'id': str(uuid.uuid4()),
            'guest_name': guest_name,
            'guest_color': guest.get('avatar_color', '#FF6B6B'),
            'timestamp': datetime.now().isoformat(),
            'type': 'check_in'
        }
        event['check_ins'].append(check_in)
        
        # Add comment about check-in
        comment = {
            'id': str(uuid.uuid4()),
            'author': guest_name,
            'author_color': guest.get('avatar_color', '#FF6B6B'),
            'text': f"📍 {guest_name} has arrived at the event!",
            'timestamp': datetime.now().isoformat(),
            'type': 'check_in'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'check_in': check_in})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/event/<event_id>/upload_media', methods=['POST'])
def upload_media(event_id):
    try:
        event = events.get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        # Check if event is today (allow media uploads only on event day)
        event_date = datetime.fromisoformat(event['date']).date()
        today = datetime.now().date()
        
        if event_date != today:
            return jsonify({'error': 'Media uploads only allowed on event day'}), 403
        
        if 'media' not in request.files:
            return jsonify({'error': 'No media file provided'}), 400
        
        file = request.files['media']
        uploader_name = request.form.get('uploader_name', 'Anonymous')
        caption = request.form.get('caption', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Create secure filename
        filename = secure_filename(f"{event_id}_{uuid.uuid4().hex[:8]}.{file_extension}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'events', filename)
        
        # Save file
        file.save(file_path)
        
        # Create media entry
        media_item = {
            'id': str(uuid.uuid4()),
            'filename': filename,
            'original_name': file.filename,
            'uploader': uploader_name,
            'uploader_color': request.form.get('uploader_color', '#FF6B6B'),
            'caption': caption,
            'file_type': 'video' if file_extension in {'mp4', 'mov', 'avi'} else 'image',
            'file_size': os.path.getsize(file_path),
            'uploaded_at': datetime.now().isoformat(),
            'url': f"/static/uploads/events/{filename}"
        }
        
        event['media_gallery'].append(media_item)
        
        # Add comment about media upload
        media_type = '📹' if media_item['file_type'] == 'video' else '📸'
        comment_text = f"{media_type} {uploader_name} shared a {media_item['file_type']}"
        if caption:
            comment_text += f": \"{caption}\""
        
        comment = {
            'id': str(uuid.uuid4()),
            'author': uploader_name,
            'author_color': media_item['uploader_color'],
            'text': comment_text,
            'timestamp': datetime.now().isoformat(),
            'type': 'media',
            'media_id': media_item['id']
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'media': media_item})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/event/<event_id>/live_update', methods=['POST'])
def add_live_update(event_id):
    try:
        data = request.json or {}
        event = events.get(event_id)
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        update = {
            'id': str(uuid.uuid4()),
            'author': data.get('author', 'Organizer'),
            'author_color': data.get('author_color', '#FF6B6B'),
            'text': data.get('text'),
            'timestamp': datetime.now().isoformat(),
            'type': 'live_update'
        }
        
        event['live_updates'].append(update)
        
        # Also add to comments for main feed
        comment = {
            'id': str(uuid.uuid4()),
            'author': update['author'],
            'author_color': update['author_color'],
            'text': f"📢 Live Update: {update['text']}",
            'timestamp': datetime.now().isoformat(),
            'type': 'live_update'
        }
        event['comments'].append(comment)
        
        return jsonify({'success': True, 'update': update})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/events')
def api_events():
    return jsonify(list(events.values()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)