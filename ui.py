""" GUI 모듈 """

import tkinter as tk
from tkinter import ttk

from logic import signup
from constants import Color, Font
from utils import center_window

class LoginFrame(tk.Frame):
    """로그인 화면을 구성하는 Tkinter Frame 클래스"""

    def __init__(self, parent, controller):
        """ 로그인 프레임 초기화 """

        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """로그인 화면에 필요한 위젯 생성 및 배치"""

        # 제목 라벨
        title_lbl = tk.Label(self, font=Font.TITLE, text="RoaD")
        title_lbl.pack(pady=(80, 0))

        # 버전 라벨
        version_lbl = tk.Label(self, font=Font.BODY, text="version 2.0")
        version_lbl.pack(pady=(0, 10))

        # 로그인 관련 위젯들을 담는 프레임
        login_frm = tk.Frame(self, bg=Color.DARK)
        login_frm.pack(expand=True)

        # ID 입력창
        self.username_ent = tk.Entry(
            login_frm,
            bg=Color.GREY,
            font=Font.ENTRY,
            fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY,
            justify='center'
        )
        self.username_ent.insert(0, 'Username')
        self.username_ent.bind('<FocusIn>', self.clear_placeholder)
        self.bind_all("<Button-1>", self.restore_placeholder)
        self.username_ent.pack(padx=80, pady=(60, 50))

        # 로그인 버튼
        login_btn = tk.Button(
            login_frm,
            bg=Color.GREEN,
            font=Font.BUTTON,
            text='Log in',
            width=17
        )
        self.username_ent.bind('<Return>', self.login_enter)
        login_btn.pack(pady=(0, 4))

        # 안내, 오류 메시지 라벨
        self.message_lbl = tk.Label(
            login_frm,
            bg=Color.DARK,
            font=Font.CAPTION
        )
        self.message_lbl.pack(pady=(0, 20))

        # or 라벨
        or_lbl = tk.Label(login_frm, bg=Color.DARK, font=Font.BODY, text='OR')
        or_lbl.pack(pady=(0, 10))

        # 계정관리 프레임
        account_frm = tk.Frame(login_frm, bg=Color.DARK)
        account_frm.grid_columnconfigure(0, weight=1, uniform='col')
        account_frm.grid_columnconfigure(1, weight=1, uniform='col')
        account_frm.pack(pady=(0, 40))

        # 회원가입 라벨
        signup_lbl = tk.Label(
            account_frm,
            bg=Color.DARK,
            font=Font.CAPTION,
            text='Sign up'
        )
        signup_lbl.bind("<Button-1>", lambda e: self.open_signup_window())
        signup_lbl.grid(row=0, column=0, padx=(0, 30))

        # 계정삭제 라벨
        delaccount_lbl = tk.Label(
            account_frm,
            bg=Color.DARK,
            font=Font.CAPTION,
            text='Delete account'
        )
        delaccount_lbl.bind("<Button-1>", lambda e: self.open_delaccount_window())
        delaccount_lbl.grid(row=0, column=1, padx=(30, 0))

    def clear_placeholder(self, event):
        """ 엔트리창 클릭 시 플레이스 홀더 제거 """

        if event.widget.get() == 'Username':
            event.widget.delete(0, len(event.widget.get()))

    def restore_placeholder(self, event):
        """ username 엔트리창이 빈 상태로 포커스가 빠지면 플레이스 홀더 다시 입력 """

        if event.widget != self.username_ent and self.username_ent.get() == "":
            self.username_ent.insert(0, 'Username')
            self.focus_set()

    def login_enter(self, event):
        """ username입력창에 포커스를 둔 후 엔터키를 눌러도 로그인 가능하게 하는 함수 """

        pass

    def open_signup_window(self):
        """ 계정 생성 창 위젯 생성 및 배치 """

        signup_window = tk.Toplevel(self, bg=Color.DARK)
        signup_window.title("Sign Up")
        signup_window.resizable(False, False)
        center_window(signup_window, 500, 590)

        # 제목 라벨
        title_lbl = tk.Label(signup_window, bg=Color.DARK, font=Font.TITLE_SMALL, text='RoaD')
        title_lbl.pack(pady=40)

        # 아이디 입력 라벨
        explain_lbl = tk.Label(
            signup_window,
            bg=Color.DARK,
            font=Font.EXPLAIN_BOLD,
            text='Enter your ID'
        )
        explain_lbl.pack(pady=(0, 20))

        # ID 입력창
        username_ent = tk.Entry(
            signup_window,
            bg=Color.GREY,
            font=Font.ENTRY,
            fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY,
            justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.bind('<FocusIn>', self.clear_placeholder)
        username_ent.pack(pady=(0, 40))

        # 계정 생성 상세설정 요소를 담는 프레임
        detail_frm = tk.Frame(signup_window, bg=Color.DARK)
        detail_frm.pack(pady=(0, 20))

        # 언어 선택 라벨
        language_lbl = tk.Label(detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='Language?')
        language_lbl.grid(row=0, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        language_cbx = ttk.Combobox(
            detail_frm,
            font=Font.BODY_BIG,
            values=[" korean", " japanese"],
            state='readonly',
            width=7
        )
        ttk.Style().theme_use('clam')
        language_cbx.set(" korean")
        language_cbx.grid(row=0, column=1, sticky='e', pady=(0, 20))

        # 하루 단어 개수 설정 라벨
        word_per_day_lbl = tk.Label(detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='Words per day?')
        word_per_day_lbl.grid(row=1, column=0, sticky='w', pady=(0, 20))

        # 하루 단어 개수 설정 입력창
        word_per_day_ent = tk.Entry(
            detail_frm,
            bg=Color.LIGHT_GREY,
            font=Font.BODY_BIG,
            fg=Color.FONT_DARK,
            insertbackground=Color.FONT_ENTRY,
            justify='center',
            width=3
        )
        word_per_day_ent.insert(0, '12')
        word_per_day_ent.grid(row=1, column=1, sticky='e', pady=(0, 20))

        # 단어 카테고리 라벨
        word_category_lbl = tk.Label(detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='What word?')
        word_category_lbl.grid(row=2, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        word_category_cbx = ttk.Combobox(
            detail_frm,
            font=Font.BODY_BIG,
            values=[" Add yourself", " middle school", " high school"],
            state='readonly',
            width=11
        )
        ttk.Style().theme_use('clam')
        word_category_cbx.set(" Add yourself")
        word_category_cbx.grid(row=2, column=1, sticky='e', pady=(0, 20))

        # 계정 생성 버튼
        signup_button = tk.Button(
            signup_window,
            bg=Color.GREEN,
            font=Font.BUTTON,
            text='Sign up',
            width=17,
            command=lambda: signup(
                username_ent.get(),
                language_cbx.get(),
                word_per_day_ent.get(),
                word_category_cbx.get(),
                self.errormessage
            )
        )
        signup_button.pack(pady=(0, 4))

        # 오류메시지
        self.errormessage = tk.Label(
            signup_window,
            bg=Color.DARK,
            font=Font.CAPTION,
            fg=Color.FONT_WARNING
        )
        self.errormessage.pack()

    def open_delaccount_window(self):
        """ 계정 삭제 창 위젯 생성 및 배치 """

        delaccount_window = tk.Toplevel(self)
        delaccount_window.title("Delete Account")
        delaccount_window.resizable(False, False)
        center_window(delaccount_window, 450, 400)









class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E0F7FA")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="메뉴 화면", font=("Arial", 16, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(30, 10))

        btn_test = tk.Button(self, text="테스트 시작",
                             command=lambda: self.controller.show_frame(TestFrame))
        btn_test.grid(row=1, column=0, padx=20, pady=10)

        btn_settings = tk.Button(self, text="설정",
                                 command=lambda: self.controller.show_frame(SettingsFrame))
        btn_settings.grid(row=1, column=1, padx=20, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FFF3E0")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 길이가 긴 텍스트 예시
        text = ("이것은 테스트 화면 예시입니다. 텍스트가 길면 자동으로 줄바꿈이 되도록 "
                "wraplength를 설정했습니다.")
        lbl_text = tk.Label(self, text=text, wraplength=400, justify="center")
        lbl_text.grid(row=0, column=0, columnspan=2, pady=30)

        btn_result = tk.Button(self, text="결과 보기",
                               command=lambda: self.controller.show_frame(ResultFrame))
        btn_result.grid(row=1, column=0, padx=20, pady=10)

        btn_menu = tk.Button(self, text="메뉴로 돌아가기",
                             command=lambda: self.controller.show_frame(MenuFrame))
        btn_menu.grid(row=1, column=1, padx=20, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


class ResultFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#E8F5E9")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="결과 화면", font=("Arial", 16, "bold"))
        lbl_title.grid(row=0, column=0, pady=30)

        btn_menu = tk.Button(self, text="메뉴로 돌아가기",
                             command=lambda: self.controller.show_frame(MenuFrame))
        btn_menu.grid(row=1, column=0, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)


class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#FBE9E7")
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        lbl_title = tk.Label(self, text="설정 화면", font=("Arial", 16, "bold"))
        lbl_title.grid(row=0, column=0, pady=30)

        btn_menu = tk.Button(self, text="메뉴로 돌아가기",
                             command=lambda: self.controller.show_frame(MenuFrame))
        btn_menu.grid(row=1, column=0, pady=10)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
