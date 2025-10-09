""" 상수 모듈 """

class Color:
    """ UI에서 사용하는 색상 상수 클래스 """

    # 위젯 색상
    GREY = "#3C3A38"
    DARK = "#262421"
    GREEN = '#5d9948'
    LIGHT_GREY = "#D9D6D2"
    
    # 텍스트 색상
    FONT_DEFAULT = "#FFFFFF"
    FONT_DARK = "#262421"
    FONT_ENTRY = "#9E9D9C"  # Entry 내부 텍스트 및 커서 색상
    FONT_WARNING = '#F27E7E' # 경고 메시지 색상

class Font:
    """ UI에서 사용하는 글꼴 상수 클래스 """

    TITLE = ("Arial", 80, "bold")
    TITLE_SMALL = ("Arial", 50, "bold")
    EXPLAIN_BOLD = BUTTON = ('Arial', 20, 'bold')
    EXPLAIN = ENTRY = ("Arial", 20)
    BODY_BIG = ("Arial", 16)
    BODY = ("Arial", 14)
    CAPTION = ("Arial", 12)
    