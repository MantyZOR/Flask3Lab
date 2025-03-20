from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

# Инициализация приложения
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Секретный ключ для сессий
 
# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Страница для перенаправления
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

# Модель пользователя
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Простая "база данных" пользователей
users = {
    'user': User(1, 'user', 'qwerty')
}

# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if int(user.id) == int(user_id):
            return user
    return None

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Счетчик посещений
@app.route('/counter/')
def counter():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1
    return render_template('counter.html', visits=session.get('visits'))

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован - перенаправляем на главную
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Обработка формы входа
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        if username in users and users[username].password == password:
            login_user(users[username], remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            
            # Перенаправление на запрошенную страницу или на главную
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Секретная страница
@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True)
