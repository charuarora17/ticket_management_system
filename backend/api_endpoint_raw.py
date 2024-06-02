from flask import Flask, jsonify
from datetime import datetime, timedelta
from models import db, Ticket
from flask import Flask, jsonify, request
from models import db, Ticket
import json

app = Flask(__name__)

# Endpoint to check unresolved tickets older than 3 days
@app.route('/notifications/unresolved_tickets', methods=['GET'])
def unresolved_tickets_notifications():
    try:
        # Calculate the datetime three days ago
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        
        unresolved_tickets = Ticket.query.filter(Ticket.is_open == True, Ticket.creation_date <= three_days_ago).all()
        notifications = []
        for ticket in unresolved_tickets:
            message = f"Ticket ID {ticket.ticket_id} created on {ticket.creation_date} is still unresolved."
            notifications.append(message)
        
        return jsonify({"notifications": notifications}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to receive ticket escalation notifications
@app.route('/notifications/escalated_tickets', methods=['POST'])
def escalated_tickets_notifications():
    try:
        data = json.loads(request.data)
        ticket_id = data.get('ticket_id')
        moderator_id = data.get('moderator_id')
        user_id = data.get('user_id') 

        ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
        
        if ticket:
            if ticket.is_escalated:
                # Assuming user_id is the user to be notified
                message = f"Ticket ID {ticket_id} has been escalated to you by moderator ID {moderator_id}. Please take appropriate action."
                
                # Send notification to the user
                # Code to send notification
                
                return jsonify({"message": message}), 200
            else:
                return jsonify({"message": "Ticket has not been escalated."}), 400
        else:
            return jsonify({"message": "Ticket not found."}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

from models import db, Flagged_Post, User

# Endpoint to handle flab BAN user
@app.route('/notifications/flagged_posts', methods=['POST'])
def handle_flagged_posts():
    try:
        data = request.json
        ticket_id = data.get('ticket_id')
        flagger_id = data.get('flagger_id')
        creator_id = data.get('creator_id')
        flagged_post = Flagged_Post.query.filter_by(ticket_id=ticket_id).first()
        
        if flagged_post:
            # Increment flag count if the flag is not approved or rejected
            if not flagged_post.is_approved and not flagged_post.is_rejected:
                flagged_post.flag_count += 1
                db.session.commit()
                
                # Check if flag count exceeds threshold
                threshold = 3
                if flagged_post.flag_count >= threshold:
                    user_to_ban = User.query.get(creator_id)
                    user_to_ban.is_banned = True
                    db.session.commit()
                    return jsonify({"message": f"User {creator_id} has been banned/silenced."}), 200
                else:
                    return jsonify({"message": f"Flag count for ticket {ticket_id} increased."}), 200
            else:
                return jsonify({"message": "Flag has already been processed."}), 400
        else:
            # Create a new flagged post entry
            new_flagged_post = Flagged_Post(ticket_id=ticket_id, flagger_id=flagger_id, creator_id=creator_id)
            db.session.add(new_flagged_post)
            db.session.commit()
            return jsonify({"message": "Flag recorded."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# WE HAVE TO CREATE A NEW ROW/DATATYPE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
    # to store it  maybe a variable is also enough
from models import db, Feedback

# Endpoint to submit feedback
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    try:
        # Parse the request data
        data = request.json
        
        # Extract feedback details from the request
        student_id = data.get('student_id')
        feedback_text = data.get('feedback_text')
        
        # Create a new feedback entry
        new_feedback = Feedback(student_id=student_id, feedback_text=feedback_text)
        db.session.add(new_feedback)
        db.session.commit()
        
        return jsonify({"message": "Feedback submitted successfully."}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500