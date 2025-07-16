# TipEase: Group Event Financial Management Platform

A comprehensive web application designed to solve the problem of "broke people at group events" by providing transparent, flexible, and accessible tools for managing shared expenses and ensuring everyone can contribute fairly.

## 🚀 Development Journey

This project evolved through several phases, each building upon the previous to create a more comprehensive solution:

### Phase 1: Simple Tip Calculator (`Tip_Ease.py`)
- **Goal**: Basic tip calculation with bill splitting
- **Features**: Command-line interface, birthday person detection, payment method tracking
- **Learning**: Core calculation logic and user input validation

### Phase 2: Web Interface (`html/tip_calculator.html`)
- **Goal**: Move from command-line to web interface
- **Features**: Static HTML with JavaScript calculations
- **Learning**: Frontend development and user experience design

### Phase 3: Flask Web Application (`app/app.py`)
- **Goal**: Full-stack web application with advanced features
- **Features**: Event management, payment processing, QR codes, 2FA, party funds
- **Learning**: Backend development, API design, security implementation

### Current State: Production-Ready MVP
The application now serves as a complete solution for group event finances, addressing the core problem of financial friction at social gatherings.

## 🎯 Core Problem Solved

The primary challenge is the financial friction and awkwardness that arises when individuals at group events struggle to contribute their share, leading to some people overpaying, underpaying, or feeling excluded. TipEase creates a transparent, flexible, and accessible system for collective payment.

## ✨ Key Features

### Event Creation & Management
- Create events with details (name, date, location, description)
- Invite and track attendees
- Real-time event status updates

### Comprehensive Bill Splitting & Individual Accountability
- Accurate calculation of individual shares including tip
- Handle non-paying members (e.g., birthday person)
- Track payment methods (cash/card) for internal reconciliation
- Assign names to individual contributions for clear accountability

### Flexible Payment Facilitation
- Support for multiple digital payment platforms:
  - PayPal
  - CashApp
  - Venmo
  - Zelle (with QR code generation)
- QR code generation for quick digital transfers
- Mobile deep links to banking apps

### Payment Verification & Security
- Two-factor authentication (2FA) for payment verification
- Secure payment status tracking
- Professional receipt generation with unique IDs

### Financial Transparency & Tracking
- Real-time payment status tracking
- Professional receipt generation
- Milestone tracking for fundraising goals
- Party fund for non-attendee contributions

### Party Fund (Non-Attendee Contributions)
- System for non-attendees to contribute to shared funds
- Anonymous contribution options
- Contribution tracking and transparency

## 🚀 Getting Started

### Quick Start (Recommended)
For the full web application with all features:

```bash
cd Tip_Calculator/app
pip install -r requirements.txt
python app.py
```

The application will be available at `http://localhost:5000`

### Alternative Versions

**Simple Command-Line Calculator:**
```bash
python Tip_Ease.py
```

**Static Web Calculator:**
Open `html/tip_calculator.html` in your browser

**Basic Flask Test:**
```bash
python app.py  # Runs on port 5001
```

### Prerequisites
- Python 3.7+
- Flask 2.3.3
- qrcode[pil] 7.4.2
- Pillow 10.0.1

## 📁 Project Structure

```
Tip_Calculator/
├── Tip_Ease.py              # Phase 1: Command-line calculator
├── app.py                   # Basic Flask test (port 5001)
├── html/
│   ├── tip_calculator.html  # Phase 2: Static web interface
│   └── tip_calculator_2.html
├── app/                     # Phase 3: Full web application
│   ├── app.py              # Main Flask application (port 5000)
│   ├── requirements.txt    # Dependencies
│   ├── templates/          # HTML templates
│   └── ADVANCED_ZELLE_FEATURES.md
└── templates/              # Legacy templates
```

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS/JavaScript
- **Payment Processing**: Multiple platform integrations
- **Security**: Two-factor authentication
- **QR Codes**: Dynamic generation for payments
- **Dependencies**: See `app/requirements.txt`

## 📱 Usage

### For Event Organizers
1. Create an event with details and payment methods
2. Share the event link with attendees
3. Set payment milestones and track contributions
4. Verify payments using 2FA
5. Generate receipts for contributors

### For Attendees
1. Join events via shared links
2. View your individual payment amount
3. Choose your preferred payment method
4. Complete payment using QR codes or direct links
5. Receive payment receipts

### For Contributors (Non-Attendees)
1. Access event party fund
2. Make anonymous or named contributions
3. Choose payment method
4. Add personal messages to contributions

## 🔒 Security Features

- Two-factor authentication for payment verification
- Secure payment status tracking
- Input validation and error handling
- Professional receipt generation with audit trails

## 🎯 MVP Scope

This MVP addresses core pain points in group event finances:
- **Event Management**: Foundation for group financial activities
- **Bill Splitting**: Ensures fairness and clarity in shared expenses
- **Payment Flexibility**: Removes barriers for various payment preferences
- **Security**: Builds trust through verification systems
- **Transparency**: Provides clear financial tracking and accountability
- **Inclusivity**: Allows non-attendees to contribute

## 🚀 Future Enhancements

- Recurring events
- Advanced budgeting tools
- Direct payment integrations
- Social features and notifications
- Advanced reporting and analytics
- Dispute resolution systems

## 📄 License

This project is designed to make group events more financially accessible and transparent for everyone involved.

---

**TipEase**: Making group finances simple, transparent, and inclusive. 🎉
