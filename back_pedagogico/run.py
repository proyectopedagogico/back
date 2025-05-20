import os
from app import create_app # Import the application factory from the app package

# Get the configuration to use from the FLASK_CONFIG environment variable
# If not set, default to 'development'
config_name = os.getenv('FLASK_CONFIG') or 'development'

# Create the application instance using the factory and the specified configuration
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    # host='0.0.0.0' makes the server accessible from any IP address on the network
    # The debug mode will be taken from the app's configuration (config.py)
    app.run(host='0.0.0.0')

