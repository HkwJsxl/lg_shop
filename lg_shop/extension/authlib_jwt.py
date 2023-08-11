from django.conf import settings

from authlib.jose import jwt, JoseError

from users.models import UserInfo


def generate_token(user_id, email):
    """
    生成authlib加密后的token
    :param user_id: 用户id
    :param email: 用户邮箱
    :return:
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 待签名的数据负载
    data = {'user_id': user_id, "email": email}
    # 生成token
    token = jwt.encode(header=header, payload=data, key=settings.SECRET_KEY)
    return token


def validate_token(token):
    """
    校验authlib签名函数
    :param token: 加密后的token
    :return: user对象或None
    """
    try:
        data = jwt.decode(token, settings.SECRET_KEY)
    except JoseError:
        return None
    else:
        # 拿到解密后的数据
        user_id = data.get("user_id")
        email = data.get("email")
        # 数据库校验
        try:
            user = UserInfo.objects.get(pk=user_id, email=email)
        except UserInfo.DoesNotExist:
            return None
        else:
            return user


def generate_access_token(openid):
    """
    加密函数
    :param openid: 加密的数据
    :return: 加密后的数据
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 待签名的数据负载
    data = {"openid": openid}
    # 生成token
    token = jwt.encode(header=header, payload=data, key=settings.SECRET_KEY)
    return token


def check_access_token(openid):
    """
    校验authlib签名函数
    :param openid: 加密后的token
    :return: user对象或None
    """
    try:
        data = jwt.decode(openid, settings.SECRET_KEY)
    except JoseError:
        return None
    else:
        # 拿到解密后的数据
        return data.get("openid")
