#!/usr/bin/env python3
"""
Main deployment file for RAG Chat Application
This file serves as the entry point for cloud deployment
"""

import os
import sys
from pathlib import Path
from flask import send_from_directory

# Add src directory to Python path
PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / 'src'
sys.path.insert(0, str(SRC_PATH))

# Import the Flask app from src
from app import app, initialize_system

# Configure Flask for serving static files
app.static_folder = str(PROJECT_ROOT / 'public')
app.template_folder = str(PROJECT_ROOT / 'view')

# Add routes for serving frontend files
@app.route('/', methods=["GET"])

def serve_index():
    """Serve the main HTML file"""
    return send_from_directory(str(PROJECT_ROOT / 'view'), 'chatbot_interface.html')

@app.route('/public/<path:filename>')
def serve_static(filename):
    """Serve CSS and other static files"""
    return send_from_directory(str(PROJECT_ROOT / 'public'), filename)

@app.route('/view/<path:filename>')
def serve_views(filename):
    """Serve HTML files from view directory"""
    return send_from_directory(str(PROJECT_ROOT / 'view'), filename)

# Health check for deployment
@app.route('/health')
def health():
    """Simple health check for deployment platforms"""
    return {"status": "ok", "message": "RAG Chat API is running"}

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RAG Chat Application - Deployment Mode")
    print("=" * 60)
    
    # Get port from environment (for cloud deployment)
    port = int(os.environ.get("PORT", 10000))
    
    if initialize_system():
        print(f"\n🎉 Server ready! Starting on port {port}")
        print(f"📡 Will be available at deployment URL")
        print("=" * 60 + "\n")
        
        # Run in production mode
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=False,  # Disable debug in production
            threaded=True
        )
    else:
        print("\n❌ Failed to initialize RAG system. Server not started.")
        print("📋 Please check your configuration and try again.")
        sys.exit(1)#!/usr/bin/env python3
"""
Main deployment file for RAG Chat Application
This file serves as the entry point for cloud deployment
"""

import os
import sys
from pathlib import Path
from flask import send_from_directory

# Add src directory to Python path
PROJECT_ROOT = Path(__file__).parent
SRC_PATH = PROJECT_ROOT / 'src'
sys.path.insert(0, str(SRC_PATH))

# Import the Flask app from src
from app import app, initialize_system

# Configure Flask for serving static files
app.static_folder = str(PROJECT_ROOT / 'public')
app.template_folder = str(PROJECT_ROOT / 'view')

# HTML entry point (can be overridden by env var)
MAIN_HTML = os.getenv("MAIN_HTML", "chatbot_interface.html")

# === Routes ===
@app.route('/', methods=["GET"])
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory(str(PROJECT_ROOT / 'view'), MAIN_HTML)

@app.route('/public/<path:filename>', methods=["GET"])
def serve_static(filename):
    """Serve CSS, JS, and other static files"""
    return send_from_directory(str(PROJECT_ROOT / 'public'), filename)

@app.route('/view/<path:filename>', methods=["GET"])
def serve_views(filename):
    """Serve HTML templates from view directory"""
    return send_from_directory(str(PROJECT_ROOT / 'view'), filename)

@app.route('/health', methods=["GET"])
def health():
    """Simple health check for deployment platforms"""
    return {"status": "ok", "message": "RAG Chat API is running"}

# === Entry Point ===
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 RAG Chat Application - Deployment Mode")
    print("=" * 60)

    port = int(os.environ.get("PORT", 10000))  # default port for local/cloud

    if initialize_system():
        print(f"\n🎉 Server ready! Starting on port {port}")
        print(f"📡 Access: http://localhost:{port}/")
        print("=" * 60 + "\n")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    else:
        print("\n❌ Failed to initialize RAG system. Server not started.")
        print("📋 Please check your configuration and try again.")
        sys.exit(1)
