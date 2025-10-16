'''EC2인스턴스의 API 서버와 연결을 담당하는 모듈'''
import requests

EC2_IP = ''  # EC2 인스턴스 퍼블릭 IPv4 주소
base_URL = f'http://{EC2_IP}:5000/'  # 베이스 URL

def server_check(obj):
    '''프로그램 시작 시 서버 작동여부와 데이터베이스상태 확인'''
    try:
        URL = f'{base_URL}server_check'
        response = requests.get(URL)

        if response.status_code != 200:
            obj.controller.show_overframe(response.json().get('message'))
    except:
        obj.controller.show_overframe('Instance Connection Failure')

def check_user_exists(obj, username):
    '''username이 존재하는지 확인하는 함수'''
    payload = {'username': username}
    try:
        URL = f'{base_URL}check_user_exists'
        response = requests.post(URL, json=payload)

        if response.status_code == 200:
            return response.json().get('message')
        else:
            obj.controller.show_overframe(response.json().get('message'))
    except:
        obj.controller.show_overframe('Instance Connection Failure')

def take_word_category(obj):
    '''단어 카테고리명을 반환하는 함수'''
    try:
        URL = f'{base_URL}take_word_category'
        response = requests.get(URL)

        if response.status_code == 200:
            tables = response.json().get('word_tables')
            table_name = [f" {t[5:]}" for t in tables]
            return table_name
        else:
            obj.controller.show_overframe(response.json().get('message'))
            return []
    except:
        obj.controller.show_overframe('Instance Connection Failure')
        return []
    
def signup(obj, username, language, dayword, word_category):
    '''회원가입을 처리하는 함수'''
    payload = {
        'username': username, 'language': language, 'dayword': dayword, 'word_category': word_category
    }
    try:
        URL = f'{base_URL}signup'
        response = requests.post(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe('Instance Connection Failure')

def delaccount(obj, username):
    '''계정 삭제를 처리하는 함수'''
    payload = {'username': username}
    try:
        URL = f'{base_URL}delaccount'
        response = requests.delete(URL, json=payload)
        return response
    except:
        obj.controller.show_overframe('Instance Connection Failure')