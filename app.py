'''사용자가 데이터에베이스에 접근하기 위한 서버'''
import os
import re
from functools import wraps

from flask import Flask, request, jsonify
import pymysql

# DB 접속 정보
HOST = ''
USER = os.getenv('')
PASSWORD = os.getenv('')
NAME = os.getenv('')

def get_connection():
    '''MySQL 데이터베이스 연결 객체 반환'''
    return pymysql.connect(host=HOST, user=USER, password=PASSWORD, database=NAME)

def _username_check(username):
    '''username이 users테이블에 있는지 확인 True, False 반환'''
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return True
            else:
                return False

def _check_exist_table(table):
    '''table 이름의 테이블이 있는지 확인 True, False 반환'''
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE %s;", (table,))
            if cursor.fetchone():
                return True
            else:
                return False

app = Flask(__name__)

def handle_server_errors(func):
    '''DB 관련 공통 예외 처리 데코레이터'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = get_connection()
            result = func(conn, *args, **kwargs)  # 원래 함수 실행
            conn.commit()
            return result
        except Exception as e:
            return jsonify({'message': 'server error'}), 500
        finally:
            if conn:
                conn.close()
    return wrapper

@app.route('/server_check', methods=['GET'])
@handle_server_errors
def server_check(conn):
    '''프로그램 시작 시 서버가 잘 작동하는지 확인'''
    with conn.cursor() as cursor:
        # users테이블 유무 확인
        cursor.execute("SHOW TABLES LIKE 'users';")
        has_users = cursor.fetchone() is not None
        # main테이블 유무 확인
        cursor.execute("SHOW TABLES LIKE 'main';")
        has_main = cursor.fetchone() is not None

        if not(has_users and has_main):
            return jsonify({'message': 'Missing users or main table'}), 503

    return jsonify({'message': 'ok'}), 200

@app.route('/check_user_exists', methods=['POST'])
@handle_server_errors
def check_user_exists(conn):
    '''username이 존재하는지 확인하는 함수'''
    data = request.get_json()
    username = data.get('username')
    with conn.cursor() as cursor:
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"message": True}), 200
        else:
            return jsonify({"message": False}), 200

@app.route('/take_word_category', methods=['GET'])
@handle_server_errors
def take_word_category(conn):
    '''단어 카테고리명을 반환하는 함수'''
    # 모든 테이블명 취득 후 word_가 붙은것만 리턴
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
    word_tables = [t for t in tables if t.startswith('word_')]

    return jsonify({'word_tables': word_tables}), 200

@app.route('/signup', methods=['POST'])
@handle_server_errors
def signup(conn):
    '''회원가입 함수'''
    # 입력받은 데이터 저장
    data = request.get_json()
    username = data.get('username')
    language = data.get('language')
    dayword = data.get('dayword')
    word_category = data.get('word_category')

    # word_category를 add yourself로 선택하면 False
    bool_add =  False if word_category == 'add_yourself' else True

    # 데이터 유효성 검사
    if not username or username == 'Username' or len(username) > 20:
        return jsonify({'message': 'username error'}), 400
    if language not in ['K', 'J']:
        return jsonify({'message': 'language error'}), 400
    if not(isinstance(dayword, int) and 10 <= dayword <= 25):
        return jsonify({'message': 'dayword error'}), 400
    if not _check_exist_table(word_category) and word_category != 'add_yourself':
        return jsonify({'message': 'word_category error'}), 400

    # username 중복 검사
    if _username_check(username):
        return jsonify({'message': 'The ID already exists.'}), 400

    with conn.cursor() as cursor:
        # users 테이블에 데이터 삽입
        cursor.execute("""
            INSERT INTO users 
            (username, language, num_word_oneday, word_category, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            """, (username, language, dayword, word_category)
        )
        if bool_add:
            # main 테이블에 데이터 삽입
            cursor.execute(f"""
                INSERT INTO main (username, number, word, status)
                SELECT 
                    %s AS username,
                    (@rownum := @rownum + 1) AS number,
                    w.word,
                    '-1' AS status
                FROM (
                    SELECT word FROM {word_category} ORDER BY RAND()
                ) AS w, (SELECT @rownum := 0) AS r;
                """, (username,)
            )

    return jsonify({"message": "Sign up successfully!"}), 201

@app.route('/delaccount', methods=['DELETE'])
@handle_server_errors
def delaccount(conn):
    '''계정 삭제 함수'''
    # 입력받은 데이터 저장
    data = request.get_json()
    username = data.get('username')

    with conn.cursor() as cursor:
        # main테이블에서 유저정보 삭세
        cursor.execute("DELETE FROM main WHERE username = %s", (username,))
        # users테이블에서 유저정보 삭세
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    
    return jsonify({'message': 'Deleted account.'}), 200

@app.route('/create_word_category', methods=['POST'])
@handle_server_errors
def create_word_category(conn):
    '''단어 테이블을 생성하는 함수'''
    # 데이터 취득
    data = request.get_json()
    table_name = data.get('table_name')
    words = data.get('words', [])

    # table_name, words 유효성 검사 
    # (존재해야하며 테이블명은 word_로 시작하고 그 이후는 알파벳으로 구성, 20자이내)
    if not table_name or not isinstance(words, list):
        return jsonify({'message': '잘못된 요청 데이터'}), 400
    if not re.fullmatch(r'word_[a-z]*', table_name) or len(table_name) > 20:
        return jsonify({'message': '잘못된 테이블명'}), 400

    # 단어테이블 작성
    with conn.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                number INT PRIMARY KEY AUTO_INCREMENT,
                word VARCHAR(20)
            );
        """)
        cursor.executemany(
            f"INSERT INTO {table_name} (word) VALUES (%s)", [(w,) for w in words]
        )

    return jsonify({'message': f'{table_name} 테이블 생성 및 {len(words)}개 단어 삽입 완료'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)