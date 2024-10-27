# 导入jwt库，这是一个用于处理JSON Web Tokens的Python库  
import jwt
# 导入datetime库，用于处理日期和时间  
import datetime
# 从jwt库中导入exceptions，以便捕获与JWT相关的异常  
from jwt import exceptions
# 从django.conf中导入settings，这允许您访问Django项目的设置文件  
from django.conf import settings


# 定义一个函数，用于创建JWT token
def create_token(payload, timeout=20):
    """  
    :param payload: 字典，包含用户信息，例如：{'user_id':1,'username':'wupeiqi'}  
    :param timeout: token的过期时间，以分钟为单位，默认为20分钟（注意：在代码中实际是按小时处理的，可能需要修改以匹配描述）  
    :return: 返回生成的JWT token字符串  
    """
    # 定义JWT的头部信息，指定token类型和加密算法  
    headers = {
        'typ': 'jwt',  # token类型  
        'alg': 'HS256'  # 使用的加密算法，HS256表示HMAC SHA256  
    }

    # 在payload中添加'exp'字段，表示token的过期时间。这里使用datetime.now()获取当前UTC时间，并加上指定的超时时间（以小时为单位）
    payload['exp'] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=timeout)

    # 使用jwt.encode()函数生成token。传入payload、密钥（从Django设置中获取，并编码为utf-8）、算法和头部信息  
    result = jwt.encode(payload=payload, key=settings.SECRET_KEY.encode('utf-8'), algorithm="HS256", headers=headers)

    # 返回生成的token字符串  
    return result


# 定义一个函数，用于解析和验证JWT token，并获取其中的payload数据
def parse_payload(token):
    """  
    对传入的token进行验证，并尝试获取其中的payload数据  
    :param token: 要验证的JWT token字符串  
    :return: 如果验证成功，返回True和payload数据；如果验证失败，返回False和相应的错误信息  
    """
    try:
        # 使用jwt.decode()函数验证token，并获取payload数据。传入token、密钥（从Django设置中获取，并编码为utf-8）和允许的算法列表  
        verified_payload = jwt.decode(token, settings.SECRET_KEY.encode('utf-8'), algorithms=["HS256"])
        # 如果验证成功，返回True和payload数据  
        return True, verified_payload
    except exceptions.ExpiredSignatureError:
        # 如果token已过期，捕获该异常，并设置相应的错误信息  
        error = 'token已失效'
    except jwt.DecodeError:
        # 如果token解码失败（例如，由于格式错误），捕获该异常，并设置相应的错误信息  
        error = 'token认证失败'
    except jwt.InvalidTokenError:
        # 如果token无效（例如，由于被篡改），捕获该异常，并设置相应的错误信息  
        error = '非法的token'
        # 在出现异常的情况下，返回False和相应的错误信息
    return False, error