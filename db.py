""" 데이터 베이스 관련 모듈 """

import os

import pymysql

# 환경변수에서 DB 접속 정보 가져오기
DB_HOST: str = os.getenv("ROAD_DB_HOST")
DB_USER: str = os.getenv("ROAD_DB_USER")
DB_PASSWORD: str = os.getenv("ROAD_DB_PASSWORD")
DB_NAME: str = os.getenv("ROAD_DB_NAME")
DB_PORT: int = int(os.getenv("ROAD_DB_PORT"))

def get_connection():
    """ MySQL 데이터베이스 연결 객체 반환 """

    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def create_users_table():
    """ 유저 테이블(users) 생성 """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(20) PRIMARY KEY,
                    language ENUM('korean', 'japanese') NOT NULL,
                    num_word_oneday INT NOT NULL,
                    word_category VARCHAR(50),
                    created_at DATETIME NOT NULL
                );
            """)
        conn.commit()
    finally:
        conn.close()

def create_record_table():
    """ 기록 테이블(record) 생성 """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS record (
                    username VARCHAR(20) NOT NULL,
                    start_time DATETIME NOT NULL,
                    end_time DATETIME NOT NULL,
                    PRIMARY KEY (username, start_time)
                );
            """)
        conn.commit()
    finally:
        conn.close()

def create_main_table():
    """ 메인 테이블(main) 생성 """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS main (
                    username VARCHAR(20) NOT NULL,
                    number INT NOT NULL,
                    word VARCHAR(20) NOT NULL,
                    status CHAR(2) NOT NULL,
                    PRIMARY KEY (username, number)
                );
            """)
        conn.commit()
    finally:
        conn.close()


def signup(username):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, created_at) VALUES (%s, NOW())"
            cursor.execute(sql, (username,))
        conn.commit()
    finally:
        conn.close()