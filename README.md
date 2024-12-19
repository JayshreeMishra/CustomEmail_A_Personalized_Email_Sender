# CustomEmail: A Personalized Email Sender

CustomEmail/
├── app/                            # Core web app logic
│   ├── __init__.py                 # Initialize Flask app and extensions
│   ├── routes.py                   # Define app routes
│   ├── templates/                  # HTML files for the web app
│   ├── static/                     # CSS, JS, images, etc.
│   ├── forms.py                    # Form handling with Flask-WTF
│   └── utils.py                    # Utility functions for the web app
│
├── ml/                             # ML-related components
│   ├── __init__.py                 # Init file for the ML module
│   ├── model.py                    # Code to load and use the ML model
│   ├── preprocess.py               # Preprocessing utilities
│   ├── training/                   # Scripts for training (optional)
│   │   ├── train.py                # Model training script
│   │   ├── config.yaml             # Configurations for training
│   │   └── artifacts/              # Saved models, encoders, etc.
│   └── tests/                      # Unit tests for ML functions
│
├── tests/                          # Tests for the entire project
│   ├── test_app.py                 # Tests for the web app
│   └── test_ml.py                  # Tests for the ML components
│
├── config/                         # Configuration files
│   ├── app_config.py               # Configs for Flask (debug mode, etc.)
│   ├── logging_config.py           # Logging settings
│   └── secrets.yaml                # Sensitive info (e.g., API keys)
|
├── database/
│   ├── __init__.py
│   ├── models.py              # Define MongoEngine or similar ORM models
│   └── queries.py             # Common database queries
|
├── docs/
│   ├── api_docs.md
│   └── usage.md
|
|
├── logs/                           # Logs for debugging
│   └── app.log
│
├── main.py                         # Entry point to run the Flask app
├── setup.py                        # Setup script for packaging
├── requirements.txt                # Python dependencies
└── README.md                       # Project overview



## WorkFlow
- Update config.yaml
-Update schema.yaml
- Update params.yaml
- Update the entity
- Update the configuration manager in src config
- Update the components
- Update the pipeline
- Update the main.py
- Update the app.py