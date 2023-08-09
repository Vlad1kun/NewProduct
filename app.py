from flask import Flask, render_template, request
from asyncio import run
from freeGPT import gpt3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    user_input = request.form['message']

    async def process_user_input():
        try:
            resp = await getattr(gpt3, 'Completion')().create(prompt=user_input)
            return resp
        except Exception as e:
            return str(e)

    response = run(process_user_input())

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
