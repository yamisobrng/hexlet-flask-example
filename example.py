import uuid, os, psycopg2
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from validator import validate
from user_repository import UserRepository

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://alexeygladkov@127.0.0.1:5433/alexeygladkov'
)

conn = psycopg2.connect(DATABASE_URL)

repo = UserRepository(conn)


@app.route("/")
def index():
    return 'Hello World!'


@app.get("/users")
def users_index():
    repo = UserRepository(conn)
    query = request.args.get('query', '')
    users = repo.get_content()
    filtered_users = [user for user in users if query in user['name']]
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'users/index.html',
        users=filtered_users,
        search=query,
        messages=messages
    )


@app.post('/users')
def users_post():
    repo = UserRepository(conn)
    name = request.form.get('name')
    email = request.form.get('email')
    user = {
        'name': name,
        'email': email,
    }
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors
        ), 422
    repo.save(user)
    flash('User was added successfully', 'success')
    return redirect(url_for('users_index'), code=302)


@app.route('/users/<id>')
def users_show(id):
    app.logger.info('Вывод страницы users/show.html с id')
    repo = UserRepository(conn)
    user = repo.find(id)
    return render_template(
        'users/show.html',
        user=user
    )

@app.route('/users/<id>/edit')
def users_edit(id):
    repo = UserRepository(conn)
    user = repo.find(id)
    errors = {}
    return render_template(
        'users/edit.html',
        user=user,
        errors=errors
    )


@app.route('/users/<id>/patch', methods=['POST'])
def users_patch(id):
    data = request.form.to_dict()
    repo = UserRepository(conn)
    user = repo.find(id)
    errors = validate(data)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors
        )
    for key, value in data.items():
        user[key] = value
    repo.save(user)
    flash('User has been edited', 'success')
    return redirect(
        url_for('users_index'),
    )


@app.route('/users/<id>/delete', methods=["POST"])
def users_delete(id):
    repo = UserRepository(conn)
    repo.destroy(id)
    flash('User has been deleted', 'success')
    return redirect(
        url_for('users_index')
    )



@app.route('/users/new')
def users_new():
    user = {
        'id': '',
        'name': '',
        'email': ''
    }

    errors = {}
    app.logger.info('Вывод страницы с пользователям')
    return render_template(
        'users/new.html',
        user=user,
        errors=errors
    )