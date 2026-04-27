import os
from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from urllib.parse import urlparse
from models import db
from config import Config


def _create_database_if_not_exists(app_config):
    """Creates the database specified in the SQLAlchemy URI if it doesn't exist."""
    try:
        db_uri = app_config['SQLALCHEMY_DATABASE_URI']

        # Skip if not MySQL
        if not db_uri or not db_uri.startswith('mysql'):
            return

        # ✅ FIX: urlparse can't handle 'mysql+mysqlconnector://' scheme
        # Strip the driver part so it becomes 'mysql://' which urlparse understands
        parse_uri = db_uri.replace('mysql+mysqlconnector://', 'mysql://') \
                          .replace('mysql+pymysql://', 'mysql://') \
                          .replace('mysql+mysqldb://', 'mysql://')

        parsed_uri = urlparse(parse_uri)

        db_name = parsed_uri.path.lstrip('/')
        host = parsed_uri.hostname
        user = parsed_uri.username
        password = parsed_uri.password
        port = parsed_uri.port or 3306

        print(f"🔍 Connecting to MySQL at {host}:{port} as '{user}'...")

        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        cursor = mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        cursor.close()
        mydb.close()
        print(f"✅ Database '{db_name}' verified/created.")

    except mysql.connector.Error as err:
        print(f"❌ Database creation/verification failed: {err}")
        print(f"   Host: {host}, User: {user}")
        print("   👉 Check your DB_HOST, DB_USER, DB_PASSWORD in config.py or environment variables.")
        exit(1)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Create/verify DB BEFORE db.init_app() tries to connect
    _create_database_if_not_exists(app.config)

    # Initialize Extensions
    CORS(app, supports_credentials=True)
    db.init_app(app)

    # Ensure storage folders exist
    os.makedirs(app.config['SCREENSHOT_FOLDER'], exist_ok=True)

    # Register Blueprints
    from routes.register_routes import register_routes
    register_routes(app)

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    @app.route("/")
    def home():
        return jsonify({
            "status": "online",
            "message": "ISMS API Server Running 🚀",
            "version": "1.0.0"
        })

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Database Tables Verified/Created")

        from models import Admin
        super_admin = Admin.query.filter_by(username="superadmin").first()

        if not super_admin:
            print("🌱 Seeding default Superadmin...")
            super_admin = Admin(
                username="superadmin",
                email="superadmin@isms.com",
                role="superadmin",
                status="Offline",
                custom_id="SA/IN/24/0001",
                domain="Management",
                designation="HR Head"
            )
            super_admin.set_password("123")
            db.session.add(super_admin)
            db.session.commit()
            print("✅ Default Superadmin Created")
        else:
            if super_admin.designation != "HR Head" or super_admin.domain != "Management":
                print("🔄 Updating Superadmin details...")
                super_admin.designation = "HR Head"
                super_admin.domain = "Management"
                db.session.commit()
                print("✅ Superadmin details updated")

    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)