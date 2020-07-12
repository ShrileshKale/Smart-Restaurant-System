from flask import Config
import os

class DevelopmentConfig(Config):
	MONGODB_DATABASE = 'scp_db'
	MONGODB_HOST= '127.0.0.1'
	MONGODB_PORT = 27017
	MONGODB_USERNAME = 'scp_user'
	MONGODB_PASSWORD = 'scp_password_123'

	SECRET_KEY = "SCP_2O19quTDhgP"