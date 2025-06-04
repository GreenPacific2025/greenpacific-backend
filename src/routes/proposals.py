from flask import Blueprint, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import json
from datetime import datetime
import os

proposals_bp = Blueprint('proposals', __name__)

# Email configuration - you'll need to update these with real SMTP settings
SMTP_SERVER = "smtp.gmail.com"  # or your email provider's SMTP server
SMTP_PORT = 587
EMAIL_ADDRESS = "greenpacificcleaningservices@gmail.com"  # Update with your email
EMAIL_PASSWORD = "ameh hazx jkyi uioq"    # Update with your app password
BUSINESS_EMAIL = "bgulum@greenpacificcleaning.ca"  # Update with business email

def send_email(to_email, subject, html_content, attachments=None):
    """Send email with optional attachments"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Add attachments if provided
        if attachments:
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment['data'])
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {attachment["filename"]}'
                )
                msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

def create_client_email_content(client_info, package_info):
    """Create HTML email content for client confirmation"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #1e40af; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .package-info {{ background-color: #f0f9ff; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
            .logo {{ max-width: 200px; height: auto; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Green Pacific Cleaning & Facility Care</h1>
            <p>Thank you for choosing our professional cleaning services!</p>
        </div>
        
        <div class="content">
            <h2>Dear {client_info.get('name', '')},</h2>
            
            <p>We have successfully received your signed cleaning service agreement. Thank you for choosing Green Pacific Cleaning & Facility Care for your healthcare facility cleaning needs.</p>
            
            <div class="package-info">
                <h3>Service Agreement Details:</h3>
                <p><strong>Client:</strong> {client_info.get('name', '')} ({client_info.get('title', '')})</p>
                <p><strong>Facility:</strong> {client_info.get('company', 'New West Eyes')}</p>
                <p><strong>Email:</strong> {client_info.get('email', '')}</p>
                <p><strong>Phone:</strong> {client_info.get('phone', '')}</p>
                <p><strong>Contract Length:</strong> {client_info.get('contractLength', '')}</p>
                <p><strong>Start Date:</strong> {client_info.get('startDate', '')}</p>
                <p><strong>Selected Package:</strong> {package_info.get('name', 'Custom Package')}</p>
                <p><strong>Monthly Investment:</strong> ${package_info.get('monthlyApprox', 0):,}</p>
            </div>
            
            <h3>Next Steps:</h3>
            <ul>
                <li>Initial facility assessment and team assignment</li>
                <li>Service commencement with enhanced monitoring</li>
                <li>First quarterly quality assurance inspection</li>
                <li>Ongoing partnership and service optimization</li>
            </ul>
            
            <p>We will contact you within 24 hours to schedule the initial facility assessment and begin the transition process.</p>
            
            <p>Your signed contract is attached to this email for your records.</p>
            
            <p>If you have any questions, please don't hesitate to contact us:</p>
            <p><strong>Burak Gulum</strong><br>
            Phone: 604 440 3569<br>
            Email: burak@greenpacificcleaning.com</p>
        </div>
        
        <div class="footer">
            <p>Green Pacific Cleaning & Facility Care<br>
            Professional Healthcare Cleaning Services<br>
            Where patient safety meets professional excellence</p>
        </div>
    </body>
    </html>
    """

def create_business_email_content(client_info, package_info):
    """Create HTML email content for business notification"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #059669; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .client-info {{ background-color: #f0fdf4; padding: 15px; border-radius: 8px; margin: 20px 0; }}
            .urgent {{ background-color: #fef3c7; padding: 10px; border-radius: 5px; border-left: 4px solid #f59e0b; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎉 New Proposal Accepted!</h1>
            <p>A client has signed a cleaning service agreement</p>
        </div>
        
        <div class="content">
            <div class="urgent">
                <strong>Action Required:</strong> Contact client within 24 hours to schedule initial assessment
            </div>
            
            <div class="client-info">
                <h3>Client Information:</h3>
                <p><strong>Name:</strong> {client_info.get('name', '')}</p>
                <p><strong>Title:</strong> {client_info.get('title', '')}</p>
                <p><strong>Company:</strong> {client_info.get('company', 'New West Eyes')}</p>
                <p><strong>Email:</strong> {client_info.get('email', '')}</p>
                <p><strong>Phone:</strong> {client_info.get('phone', '')}</p>
                <p><strong>Contract Length:</strong> {client_info.get('contractLength', '')}</p>
                <p><strong>Desired Start Date:</strong> {client_info.get('startDate', '')}</p>
                <p><strong>Submission Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="client-info">
                <h3>Package Details:</h3>
                <p><strong>Package:</strong> {package_info.get('name', 'Custom Package')}</p>
                <p><strong>Description:</strong> {package_info.get('subtitle', '')}</p>
                <p><strong>Monthly Value:</strong> ${package_info.get('monthlyApprox', 0):,}</p>
                <p><strong>Annual Value:</strong> ${package_info.get('annualApprox', 0):,}</p>
            </div>
            
            <h3>Immediate Actions:</h3>
            <ul>
                <li>Call client at {client_info.get('phone', '')} to confirm receipt</li>
                <li>Schedule initial facility assessment</li>
                <li>Prepare team assignment and service schedule</li>
                <li>Send welcome package and service guidelines</li>
            </ul>
            
            <p>The signed contract with client signature is attached to this email.</p>
        </div>
    </body>
    </html>
    """

@proposals_bp.route('/submit', methods=['POST'])
def submit_proposal():
    """Handle proposal submission with email notifications"""
    try:
        data = request.get_json()
        
        client_info = data.get('clientInfo', {})
        package_info = data.get('packageInfo', {})
        signature_data = data.get('signatureData', '')
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if not client_info.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare signature attachment (decode base64)
        attachments = []
        if signature_data:
            try:
                # Remove data URL prefix if present
                if signature_data.startswith('data:image/png;base64,'):
                    signature_data = signature_data.replace('data:image/png;base64,', '')
                
                signature_bytes = base64.b64decode(signature_data)
                attachments.append({
                    'filename': f"signed_contract_{client_info.get('name', 'client').replace(' ', '_')}.png",
                    'data': signature_bytes
                })
            except Exception as e:
                print(f"Error processing signature: {str(e)}")
        
        # Send email to client
        client_email_sent = send_email(
            to_email=client_info['email'],
            subject="Green Pacific Cleaning - Service Agreement Confirmation",
            html_content=create_client_email_content(client_info, package_info),
            attachments=attachments
        )
        
        # Send email to business
        business_email_sent = send_email(
            to_email=BUSINESS_EMAIL,
            subject=f"🎉 New Proposal Accepted - {client_info.get('name', 'Unknown Client')}",
            html_content=create_business_email_content(client_info, package_info),
            attachments=attachments
        )
        
        # Store submission data (you could save to database here)
        submission_data = {
            'timestamp': datetime.now().isoformat(),
            'client_info': client_info,
            'package_info': package_info,
            'emails_sent': {
                'client': client_email_sent,
                'business': business_email_sent
            }
        }
        
        # Save to file for now (in production, use database)
        submissions_file = '/tmp/proposal_submissions.json'
        submissions = []
        if os.path.exists(submissions_file):
            try:
                with open(submissions_file, 'r') as f:
                    submissions = json.load(f)
            except:
                submissions = []
        
        submissions.append(submission_data)
        
        with open(submissions_file, 'w') as f:
            json.dump(submissions, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Proposal submitted successfully',
            'emails_sent': {
                'client': client_email_sent,
                'business': business_email_sent
            }
        })
        
    except Exception as e:
        print(f"Error processing proposal submission: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@proposals_bp.route('/submissions', methods=['GET'])
def get_submissions():
    """Get all proposal submissions (for business dashboard)"""
    try:
        submissions_file = '/tmp/proposal_submissions.json'
        if os.path.exists(submissions_file):
            with open(submissions_file, 'r') as f:
                submissions = json.load(f)
            return jsonify({'submissions': submissions})
        else:
            return jsonify({'submissions': []})
    except Exception as e:
        print(f"Error retrieving submissions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@proposals_bp.route('/test-email', methods=['POST'])
def test_email():
    """Test email functionality"""
    try:
        data = request.get_json()
        test_email = data.get('email', 'test@example.com')
        
        success = send_email(
            to_email=test_email,
            subject="Green Pacific Cleaning - Email Test",
            html_content="<h1>Email Test Successful!</h1><p>Your email configuration is working correctly.</p>"
        )
        
        return jsonify({'success': success, 'message': 'Test email sent' if success else 'Test email failed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

