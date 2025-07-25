import requests
import configparser
import argparse
import json
import os
import lark_oapi as lark
from lark_oapi.api.authen.v1 import *

def GET_USER_ACCESS_TOKEN(login_code=None, app_access_token=None, config_file=None):
    if config_file is None:
        config_file = 'feishu-config.ini'

    # 确保配置文件存在
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            pass

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    # 确保 TOKEN 部分存在
    if not config.has_section('TOKEN'):
        config.add_section('TOKEN')

    # 确保 ID 部分存在
    if not config.has_section('ID'):
        config.add_section('ID')

    # 从配置文件获取参数
    app_id = config.get('ID', 'app_id', fallback=None)
    app_secret = config.get('ID', 'app_secret', fallback=None)

    if not app_id or not app_secret:
        raise ValueError("app_id 或 app_secret 未在配置文件中找到。请先提供这些值。")

    # 创建 lark client
    client = lark.Client.builder() \
        .app_id(app_id) \
        .app_secret(app_secret) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request = CreateOidcAccessTokenRequest.builder() \
        .request_body(CreateOidcAccessTokenRequestBody.builder()
            .grant_type("authorization_code")
            .code(login_code)
            .build()) \
        .build()

    # 发起请求
    response = client.authen.v1.oidc_access_token.create(request)

    # 处理失败返回
    if not response.success():
        error_msg = f"获取用户访问令牌失败，代码：{response.code}，消息：{response.msg}，日志ID：{response.get_log_id()}"
        print(error_msg)
        return None, None

    # 处理业务结果
    access_token = response.data.access_token
    refresh_token = response.data.refresh_token

    # 更新配置文件
    if access_token:
        config.set('TOKEN', 'user_access_token', str(access_token))
        if refresh_token:
            config.set('TOKEN', 'refresh_token', str(refresh_token))
        with open(config_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    return access_token, refresh_token


def GET_USER_ACCESS_TOKEN_CMD():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login_code', help='登录预授权码')
    parser.add_argument('--config_file', default='feishu-config.ini', help='config file path')
    args = parser.parse_args()

    # 获取登录码，优先从命令行参数获取，没有则从配置文件获取
    login_code = args.login_code
    config_file = args.config_file

    if not login_code:
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        login_code = config.get('TOKEN', 'login_code', fallback=None)

        if not login_code:
            raise ValueError("login_code is required either in command line argument or in the configuration file.")

    # 调用 GET_USER_ACCESS_TOKEN 函数，获取 user_access_token
    user_access_token, refresh_token = GET_USER_ACCESS_TOKEN(login_code, config_file=config_file)
    
    # 打印结果
    print(f'user_access_token: {user_access_token}')
    print(f'refresh_token: {refresh_token}')


# 主函数
if __name__ == "__main__":
    GET_USER_ACCESS_TOKEN_CMD()
