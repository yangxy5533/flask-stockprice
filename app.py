from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  #app.run(port=33507)
  port = int(os.environ.get('port', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
