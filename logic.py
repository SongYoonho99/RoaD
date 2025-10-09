def signup(username, language, word_per_day, word_category, errormessage):
    """ 회원가입 처리 함수"""

    # 회원가입 시 필요 항목을 다 채우지 않은 경우
    if not all([language, word_per_day, word_category]) or not username or username == "Username":
        errormessage.config(text="Please fill in all required fields.")
        errormessage.after(4000, lambda: errormessage.config(text = ''))

    else:
        pass