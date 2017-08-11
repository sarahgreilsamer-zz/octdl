
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def root():
    parameters = request.args.to_dict()
    return render_template('base.html', dictionary=str(parameters))

if __name__ == '__main__':
    app.run(debug=True)
