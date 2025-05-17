from flask import Flask, render_template, send_from_directory 
import os 
  
app = Flask(__name__, template_folder='.', static_folder='frontend/static')  
  
@app.route("/")  
def web():  
    return render_template('frontend/index.html')  


@app.route("/scripts/<path:filename>")
def serve_scripts(filename):
    return send_from_directory(os.path.join("frontend", "scripts"), filename)

if __name__ == "__main__":  
    app.run(debug=True, host="0.0.0.0", port='80') 