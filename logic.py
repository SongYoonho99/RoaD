'''핵심 함수 및 유틸 함수 모음 모듈'''
import api_client
from constants import Color

def center_window(window, width, height):
    '''창을 화면 정중앙에 띄우는 함수'''
    x = window.winfo_screenwidth() // 2 - width // 2
    y = window.winfo_screenheight() // 2 - height // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_temporarymessage(message, text, color=Color.FONT_RED):
    '''메시지를 띄우고 4초후에 없애는 함수'''
    message.config(fg=color, text=text)
    message.after(4000, lambda: message.config(text = ''))

def delaccount_check_user(obj, username, errormessage, delaccount_window):
    '''등록된 유저인지 확인 (True, False)'''
    if api_client.check_user_exists(obj, username):
        obj.delaccount_reconfirm_window(username, delaccount_window)
    else:
        show_temporarymessage(errormessage, 'ID not found')

def validate_signup(obj, username, language, dayword, word_category, errormessage, signup_window):
    '''회원가입 처리 함수'''
    # username 유효성 검사 (미작성 혹은 20자 이상일 경우)
    if not username or username == 'Username':
        show_temporarymessage(errormessage, 'Please enter username.')
        return
    if len(username) > 20:
        show_temporarymessage(errormessage, '20 characters max for username.')
        return

    # dayword 유효성 검사 (미작성 혹은 10 ~ 25사이의 자연수가 아닌 경우)
    try:
        dayword = int(dayword)
    except:
        show_temporarymessage(errormessage, 'Enter a number from 10 to 25.')
        return
    if not (10 <= dayword <= 25):
        show_temporarymessage(errormessage, 'Enter a number from 10 to 25.')
        return
    
    # 회원가입 api통신 전 데이터 가공
    language = 'K' if language == " korean" else 'J'
    if word_category == ' add yourself':
        word_category = 'add_yourself'
    else:
        word_category = 'word_' + word_category.strip()

    # 회원가입 api통신함수 호출 (상태코드 201이 성공)
    response = api_client.signup(obj, username, language, dayword, word_category)
    if response is None:
        obj.controller.show_overframe('Instance Connection Failure')
    elif response.status_code == 201:
        show_temporarymessage(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
        signup_window.destroy()
    else:
        show_temporarymessage(errormessage, response.json().get('message'))

def validate_delaccount(obj, input, username, errormessage, delaccount_window):
    '''계정 삭제 처리 함수'''
    if input == f'delete {username}':
        response = api_client.delaccount(obj, username)
        if response is None:
            obj.controller.show_overframe('Instance Connection Failure')
        elif response.status_code == 200:
            show_temporarymessage(obj.message_lbl, response.json().get('message'), Color.FONT_DEFAULT)
            delaccount_window.destroy()
        else:
            show_temporarymessage(errormessage, response.json().get('message'))
    else:
        show_temporarymessage(errormessage, 'Incorrect input.')