# find-duplicate-image

Description for each module
 * find.py: the main function detect wish finds duplicated image for onr url
 * app.py: use flask HTTP request to enable Microservices for find.py
 * process.py: test for app.py and enable multi-threading

Step 1: enable flask server
 * pip install Flask (python3: pip3 install Flask)
 * export FLASK_APP=app.py

Step 2: run flask in development mode
 * export FLASK_ENV=development
 * flask run (deflaut Running on http://127.0.0.1:5000/)

Step 3: run main module
 * python process.py (python3: python3 process.py)
