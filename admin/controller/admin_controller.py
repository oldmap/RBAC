#! coding: utf8

from admin import app, db
from flask import request, render_template, url_for, flash, redirect, jsonify, session, abort
from flask_login import login_required, login_user, logout_user
from admin.model.User import User, Operation, Role, Blog
from admin.controller.Auth import custom_auth

# from flask.ext import restful


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # print(request.form)
        username = request.form['username']
        password = request.form['password']
        # user = User.query.filter(User.username == username).filter(User.password == password).first_or_404()
        user = User.query.filter_by(username=username, password=password).first_or_404()
        # print(user)
        if user is None:
            error = '用户名或密码不正确，请重新输入'
        else:
            # session['logged_in'] = True
            login_user(user)
            flash('登陆成功')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were Logged out.')
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    return render_template('base.html')


# 获取用户列表页
@app.route('/users/', methods=['GET',])
@login_required
def users():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    user_list = User.query.all()
    return render_template('users.html', user_list=user_list)


# POST 添加新用户 GET 获取所有用户
@app.route('/api/users/', methods=['GET', 'POST'])
@login_required
def api_users():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)

    if request.method == 'POST':
        data = dict()
        data['username'] = request.form.get('username', type=str, default=None)
        data['email'] = request.form.get('email', type=str, default=None)
        data['password'] = request.form.get('password', type=str, default=None)
        data['is_admin'] = request.form.get('is_admin', type=int, default=None)
        data['status'] = request.form.get('status', type=int, default=None)

        data['roles'] = []
        roles_ids_string = request.form.get('roles', default=None)
        if roles_ids_string:
            roles_ids = roles_ids_string.split(',')
            for role_id in roles_ids:
                role = Role.query.filter_by(id=role_id).first()
                data['roles'].append(role)
        try:
            user = User(**data)
            # print(user)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '添加成功'
    else:
        data = []
        user_list = User.query.all()
        for user in user_list:
            u = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password,
                'is_admin': user.is_admin,
                'status': user.status,
                'roles': user.roles.__str__(),
            }
            data.append(u)
        return jsonify(data)


# GET 获取指定ID用户 PUT 更新用户  DELETE 删除用户
@app.route('/api/user/<int:user_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_user(user_id):
    is_auth = custom_auth(session.get('user_id'), request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    if request.method == 'PUT':
        users = User.query.filter_by(id=user_id)
        user = User.query.filter_by(id=user_id).first_or_404()
        data = {}
        roles = []
        for k in request.form:
            if k == 'roles':
                roles_ids_string = request.form.get(k, default=None)
                roles_ids = roles_ids_string.split(',')
                for role_id in roles_ids:
                    role = Role.query.filter_by(id=role_id).first()
                    roles.append(role)
                continue
            else:
                data[k] = request.form.get(k, default=None)
        try:
            users.update(data)
            user.roles = roles
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '更新成功'
    elif request.method == 'DELETE':
        user = User.query.filter_by(id=user_id).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return '删除成功'
    else:
        user = User.query.filter_by(id=user_id).first_or_404()
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'is_admin': user.is_admin,
            'status': user.status,
            'roles': user.roles.__str__(),
        }
        return jsonify(data)


@app.route('/operations/', methods=['GET', ])
@login_required
def operations():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    operation_list = Operation.query.all()
    return render_template('operations.html', operation_list=operation_list)


# POST 添加新用户 GET 获取所有用户
@app.route('/api/operations/', methods=['GET', 'POST'])
@login_required
def api_operations():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    if request.method == 'POST':
        data = dict()
        data['name'] = request.form.get('name', type=str, default=None)
        data['method'] = request.form.get('method', type=str, default=None)
        data['uri'] = request.form.get('uri', type=str, default=None)

        data['roles'] = []
        roles_ids_string = request.form.get('roles', default=None)
        if roles_ids_string:
            # print(roles_ids_string)
            roles_ids = roles_ids_string.split(',')
            for role_id in roles_ids:
                role = Role.query.filter_by(id=role_id).first()
                data['roles'].append(role)
        try:
            operation = Operation(**data)
            # print(operation)
            db.session.add(operation)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '添加成功'
    else:
        data = []
        operation_list = Operation.query.all()
        for operation in operation_list:
            operation_obj = {
                'id': operation.id,
                'name': operation.name,
                'method': operation.method,
                'uri': operation.uri,
                'roles': operation.roles.__str__(),
            }
            data.append(operation_obj)
        return jsonify(data)


# GET 获取指定ID用户 PUT 更新用户  DELETE 删除用户
@app.route('/api/operation/<int:operation_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_operation(operation_id):
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)

    if request.method == 'PUT':
        operations = Operation.query.filter_by(id=operation_id)
        operation = Operation.query.filter_by(id=operation_id).first_or_404()
        data = {}
        roles = []
        for k in request.form:
            if k == 'roles':
                roles_ids_string = request.form.get(k, default=None)
                roles_ids = roles_ids_string.split(',')
                for role_id in roles_ids:
                    role = Role.query.filter_by(id=role_id).first()
                    roles.append(role)
                continue
            else:
                data[k] = request.form.get(k, default=None)
        try:
            operations.update(data)
            operation.roles = roles
            db.session.add(operation)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '更新成功'
    elif request.method == 'DELETE':
        operation = Operation.query.filter_by(id=operation_id).first_or_404()
        db.session.delete(operation)
        db.session.commit()
        return '删除成功'
    else:
        operation = Operation.query.filter_by(id=operation_id).first_or_404()
        data = {
            'id': operation.id,
            'name': operation.name,
            'method': operation.method,
            'uri': operation.uri,
            'roles': operation.roles.__str__(),
        }
        return jsonify(data)


@app.route('/roles/', methods=['GET', ])
@login_required
def roles():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    role_list = Role.query.all()
    return render_template('roles.html', role_list=role_list)


@app.route('/api/roles/', methods=['GET', 'POST'])
@login_required
def api_roles():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)

    if request.method == 'POST':
        data = dict()
        data['name'] = request.form.get('name', type=str, default=None)
        data['status'] = request.form.get('status', type=int, default=None)

        data['users'] = []
        data['operations'] = []

        # 多个用户
        user_ids_string = request.form.get('users', default=None)

        if user_ids_string:
            users_ids = user_ids_string.split(',')
            for user_id in users_ids:
                user = User.query.filter_by(id=user_id).first()
                data['users'].append(user)
        # 多个权限
        operation_ids_string = request.form.get('operations', default=None)
        if operation_ids_string:
            # print(operation_ids_string)
            operations_ids = operation_ids_string.split(',')
            for operation_id in operations_ids:
                operation = Operation.query.filter_by(id=operation_id).first()
                data['operations'].append(operation)
        # print(data)
        try:
            role = Role(**data)
            # print(role)
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '添加角色成功'
    else:
        data = []
        roles = Role.query.all()
        # print(roles)
        for role in roles:
            role_obj = {
                'id': role.id,
                'name': role.name,
                'status': role.status,
                'users': role.users.__str__(),
                'operations': role.operations.__str__()
            }
            data.append(role_obj)
        # print(data)
        return jsonify(data)


# GET 获取指定ID PUT 更新  DELETE 删除
@app.route('/api/role/<int:role_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_role(role_id):
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)

    if request.method == 'PUT':
        roles = Role.query.filter_by(id=role_id)
        role = Role.query.filter_by(id=role_id).first_or_404()

        data = {}
        users = []
        operations = []

        for k in request.form:
            if k == 'users':
                users_ids_string = request.form.get(k, default=None)
                users_ids = users_ids_string.split(',')
                for user_id in users_ids:
                    user = User.query.filter_by(id=user_id).first()
                    users.append(user)
            elif k == 'operations':
                operations_ids_string = request.form.get(k, default=None)
                operations_ids = operations_ids_string.split(',')
                for operation_id in operations_ids:
                    operation = Operation.query.filter_by(id=operation_id).first()
                    operations.append(operation)
            else:
                data[k] = request.form.get(k, default=None)
        try:
            roles.update(data)
            role.users = users
            role.operations = operations
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '更新成功'
    elif request.method == 'DELETE':
        role = Role.query.filter_by(id=role_id).first_or_404()
        db.session.delete(role)
        db.session.commit()
        return '删除成功'
    else:
        role = Role.query.filter_by(id=role_id).first_or_404()
        data = {
            'id': role.id,
            'name': role.name,
            'method': role.status,
            'users': role.users.__str__(),
            'operations': role.operations.__str__(),
        }
        return jsonify(data)


@app.route('/blogs/', methods=['GET', ])
@login_required
def blogs():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    blog_list = Blog.query.all()
    return render_template('blogs.html', blog_list=blog_list)


@app.route('/api/blogs/', methods=['GET', 'POST'])
@login_required
def api_blogs():
    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        abort(403)
    if request.method == 'POST':
        data = dict()
        data['title'] = request.form.get('title', type=str, default=None)
        data['content'] = request.form.get('content', type=int, default=None)
        data['author_id'] = request.form.get('author_id', type=int, default=None)
        try:
            blog = Blog(**data)
            db.session.add(blog)
            db.session.commit()
        except Exception as e:
            # print(e)
            return e.__str__()
        else:
            return '添加成功'
    else:
        data = []
        blogs = Blog.query.all()
        # print(blogs)
        for blog in blogs:
            blog_obj = {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'author': blog.author.__str__(),
            }
            data.append(blog_obj)
        # print(data)
        return jsonify(data)


# GET 获取指定ID PUT 更新  DELETE 删除
@app.route('/api/blog/<int:blog_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_blog(blog_id):

    user_id = session.get('user_id')
    is_auth = custom_auth(user_id, request.method, request.url_rule)
    if not is_auth:    # 无权限情况
        # 功能模块，无权限访问的情况下会继续验证
        blog = Blog.query.filter_by(id=blog_id).first_or_404()
        if not int(blog.author_id) == int(user_id):
            print(blog.author_id, user_id)
            abort(403)

    if request.method == 'PUT':
        blogs = Blog.query.filter_by(id=blog_id)
        data = {}
        for k in request.form:
            data[k] = request.form.get(k, default=None)
        try:
            blogs.update(data)
            db.session.commit()
        except Exception as e:
            #print(e)
            return e.__str__()
        else:
            return '更新成功'
    elif request.method == 'DELETE':
        blog = Blog.query.filter_by(id=blog_id).first_or_404()
        db.session.delete(blog)
        db.session.commit()
        return '删除成功'
    else:
        blog = Blog.query.filter_by(id=blog_id).first_or_404()
        data = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'author': blog.author.__str__(),
        }
        return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
