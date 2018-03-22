#! coding: utf8

from admin.model.User import User, Operation


def custom_auth(user_id, method, uri):
    # print(user_id, method, uri)
    # 获取用户的角色列表

    user = User.query.filter_by(id=user_id).first()
    if user.is_admin:
        return True

    try:
        user_role = set(User.query.filter_by(id=user_id).first().roles)
        # 通过 method + uri 拼接查询除一个role
        operation_role = set(Operation.query.filter_by(method=method, uri=uri).first().roles)
        if user_role & operation_role:
            return True
    except Exception as e:
        print(e)
        return False





