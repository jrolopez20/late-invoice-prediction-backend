from src import create_app

app = create_app()

if __name__ == "__main__":
    print("Starting Python Flask server for Late invoice prediction...")
    app.run(debug=True)