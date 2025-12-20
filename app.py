import os
import webbrowser, urllib.parse
from flask import Flask, request, session,render_template,redirect, url_for

# Initialize the Flask application
app = Flask(__name__)
# Set a secret key for session management (required for Flask sessions)
app.secret_key = 'super_secret_tictactoe_key' 

   



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

# Run the Flask application







if __name__ == '__main__':
    # --- FIX FOR DEPLOYMENT ---
    # 1. Get port from environment variables (provided by Render)
    # 2. Default to 5000 if not found (good for local development)
    port = int(os.environ.get("PORT", 5000))
    
    # 3. Bind to '0.0.0.0' to listen on all public interfaces
    #    (This is crucial for web hosts like Render)
    # 4. Set debug=False for production deployments
    app.run(host='0.0.0.0', port=port, debug=False)
