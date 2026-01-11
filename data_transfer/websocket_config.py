from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS

def init_websocket(app):
    """Initialize WebSocket with Flask app"""
    CORS(app, resources={r"/*": {"origins": "*"}})
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    @socketio.on('connect', namespace='/alerts')
    def handle_connect():
        print('Client connected to alerts namespace')
        emit('connection_response', {'status': 'connected'})
    
    @socketio.on('disconnect', namespace='/alerts')
    def handle_disconnect():
        print('Client disconnected from alerts namespace')
    
    @socketio.on('acknowledge_alert', namespace='/alerts')
    def handle_acknowledge(data):
        print(f'Alert acknowledged: {data}')
        emit('alert_acknowledged', data, broadcast=True)
    
    return socketio
