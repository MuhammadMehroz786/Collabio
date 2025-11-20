"""
Application Entry Point
Run this file to start the Flask server
"""
import os
from app import create_app, init_websocket
from app.extensions import socketio

# Create Flask app
app = create_app()

# Initialize WebSocket events
init_websocket(socketio)

if __name__ == '__main__':
    # Get configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    # Run with SocketIO
    socketio.run(
        app,
        host=host,
        port=port,
        debug=debug,
        use_reloader=debug,
        log_output=True,
        allow_unsafe_werkzeug=True  # Allow for development
    )
