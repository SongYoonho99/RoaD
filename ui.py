'''GUI 모듈'''
import tkinter as tk
from tkinter import ttk

import logic
import api_client
from constants import Color, Font

class LoginFrame(tk.Frame):
    '''로그인 화면을 구성하는 Frame 클래스'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.bind('<Button-1>', lambda e: self.focus_set())
        self.create_widgets()

        # 프로그램 시작 시 서버 상태 체크
        api_client.server_check(self)

    def create_widgets(self):
        '''로그인 화면에 필요한 위젯 생성 및 배치'''
        # 제목, 버전 라벨
        tk.Label(self, font=Font.TITLE, text='RoaD').pack(pady=(55, 0))
        tk.Label(self, font=Font.BODY, text='version 2.0').pack(pady=(5, 0))

        # 로그인 관련 위젯들을 담는 프레임
        login_frm = tk.Frame(self, bg=Color.DARK)
        login_frm.pack(expand=True)

        # ID 입력창
        username_ent = tk.Entry(
            login_frm, bg=Color.GREY, font=Font.ENTRY, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(padx=80, pady=(60, 50))
        username_ent.bind('<FocusIn>', self.clear_placeholder) 
        # TODO: self.self.username_ent.bind('<Return>', logic.signin())

        # 로그인 버튼
        tk.Button(
            login_frm, bg=Color.GREEN, font=Font.BUTTON, text='Log in', width=17,
            # TODO: command=lambda: logic.signin()
        ).pack(pady=(0, 4))

        # 안내, 오류 메시지 라벨
        self.message_lbl = tk.Label(login_frm, bg=Color.DARK, font=Font.CAPTION)
        self.message_lbl.pack(pady=(0, 20))

        # or 라벨
        tk.Label(login_frm, bg=Color.DARK, font=Font.BODY, text='OR').pack(pady=(0, 10))

        # 계정관리 프레임
        account_frm = tk.Frame(login_frm, bg=Color.DARK)
        account_frm.grid_columnconfigure(0, weight=1, uniform='col')
        account_frm.grid_columnconfigure(1, weight=1, uniform='col')
        account_frm.pack(pady=(0, 40))

        # 회원가입 라벨
        signup_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font.CAPTION, text='Sign up')
        signup_lbl.grid(row=0, column=0, padx=(0, 30))
        signup_lbl.bind('<Button-1>', lambda e: self.signup_window())

        # 계정삭제 라벨
        delaccount_lbl = tk.Label(account_frm, bg=Color.DARK, font=Font.CAPTION, text='Delete account')
        delaccount_lbl.grid(row=0, column=1, padx=(30, 0))
        delaccount_lbl.bind('<Button-1>', lambda e: self.delaccount_window())

    def clear_placeholder(self, event):
        '''Username이 적혀 있는 엔트리창 클릭 시 플레이스 홀더 제거'''
        if event.widget.get() == 'Username':
            event.widget.delete(0, len(event.widget.get()))

    def signup_window(self):
        '''계정 생성 창 위젯 생성 및 배치'''
        signup_window = tk.Toplevel(self, bg=Color.DARK)
        signup_window.title('Sign Up')
        signup_window.resizable(False, False)
        signup_window.bind(
            '<Button-1>', lambda e: signup_window.focus_set() if e.widget == signup_window else None
        )
        logic.center_window(signup_window, 480, 590)

        # 제목, 아이디 입력 라벨
        tk.Label(signup_window, bg=Color.DARK, font=Font.TITLE_SMALL, text='RoaD').pack(pady=40)
        tk.Label(
            signup_window, bg=Color.DARK, font=Font.EXPLAIN_BOLD, text='Enter your ID'
        ).pack(pady=(0, 20))

        # ID 입력창
        username_ent = tk.Entry(
            signup_window, bg=Color.GREY, font=Font.ENTRY, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(pady=(0, 40))
        username_ent.bind('<FocusIn>', self.clear_placeholder)

        # 계정 생성 상세설정 요소를 담는 프레임
        detail_frm = tk.Frame(signup_window, bg=Color.DARK)
        detail_frm.pack(pady=(0, 20))

        # 언어 선택 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='Language?'
        ).grid(row=0, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        language_cbx = ttk.Combobox(
            detail_frm, font=Font.BODY_BIG, state='readonly', values=[' korean', ' japanese'], width=8
        )
        ttk.Style().theme_use('clam')
        language_cbx.set(' korean')
        language_cbx.grid(row=0, column=1, sticky='e', pady=(0, 20))

        # 하루 단어 개수 설정 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='Words per day?'
        ).grid(row=1, column=0, sticky='w', pady=(0, 20))

        # 하루 단어 개수 설정 입력창
        dayword_ent = tk.Entry(
            detail_frm, bg=Color.BEIGE, font=Font.BODY_BIG, fg=Color.FONT_DARK,
            insertbackground=Color.FONT_DARK, justify='center', width=3
        )
        dayword_ent.insert(0, '12')
        dayword_ent.grid(row=1, column=1, sticky='e', pady=(0, 20))

        # 단어 카테고리 라벨
        tk.Label(
            detail_frm, bg=Color.DARK, font=Font.EXPLAIN, text='What word?'
        ).grid(row=2, column=0, sticky='w', pady=(0, 20))

        # 언어 선택 콤보박스
        word_category = api_client.take_word_category(self)
        word_category = word_category + [' add yourself']
        word_category_cbx = ttk.Combobox(
            detail_frm, font=Font.BODY_BIG, state='readonly',
            values=word_category, width=11
        )
        ttk.Style().theme_use('clam')
        word_category_cbx.set(word_category[0])
        word_category_cbx.grid(row=2, column=1, sticky='e', pady=(0, 20))

        # 계정 생성 버튼
        tk.Button(
            signup_window, bg=Color.GREEN, font=Font.BUTTON, text='Sign up', width=17,
            command=lambda: logic.validate_signup(
                self,
                username_ent.get(),
                language_cbx.get(),
                dayword_ent.get(),
                word_category_cbx.get(),
                signupmessage_lbl,
                signup_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        signupmessage_lbl = tk.Label(signup_window, bg=Color.DARK, font=Font.CAPTION)
        signupmessage_lbl.pack(expand=True)

    def delaccount_window(self):
        '''계정 삭제 창 위젯 생성 및 배치'''
        delaccount_window = tk.Toplevel(self, bg=Color.DARK)
        delaccount_window.title('Delete Account')
        delaccount_window.resizable(False, False)
        delaccount_window.bind(
            '<Button-1>', lambda e: delaccount_window.focus_set() if e.widget == delaccount_window else None
        )
        logic.center_window(delaccount_window, 480, 400)

        # 제목, 아이디 입력 라벨
        tk.Label(delaccount_window, bg=Color.DARK, font=Font.TITLE_SMALL, text='RoaD').pack(pady=40)
        tk.Label(
            delaccount_window, bg=Color.DARK, font=Font.EXPLAIN_BOLD, text='Enter ID to Delete'
        ).pack(pady=(0, 20))

        # ID 입력창
        username_ent = tk.Entry(
            delaccount_window, bg=Color.GREY, font=Font.ENTRY, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        username_ent.insert(0, 'Username')
        username_ent.pack(pady=(0, 40))
        username_ent.bind('<FocusIn>', self.clear_placeholder)

        # 계정 삭제 버튼
        tk.Button(
            delaccount_window, bg=Color.BEIGE, font=Font.BUTTON,
            fg=Color.FONT_DARK, text='Delect Account', width=17,
            command=lambda: logic.delaccount_check_user(
                self,
                username_ent.get(),
                delmessage_lbl,
                delaccount_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        delmessage_lbl = tk.Label(delaccount_window, bg=Color.DARK, font=Font.CAPTION)
        delmessage_lbl.pack(expand=True)

    def delaccount_reconfirm_window(self, username, delaccount_window):
        '''계정삭제 최종확인 창'''
        reconfirm_window = tk.Toplevel(delaccount_window, bg=Color.DARK)
        reconfirm_window.title('Delete Account Reconfirm')
        reconfirm_window.resizable(False, False)
        reconfirm_window.bind(
            '<Button-1>', lambda e: reconfirm_window.focus_set() if e.widget == reconfirm_window else None
        )
        logic.center_window(reconfirm_window, 400, 280)

        # 입력 문구 안내 라벨
        tk.Label(
            reconfirm_window, bg=Color.DARK, font=Font.EXPLAIN,
            text=f'To delete, please input\n"delete {username}"'
        ).pack(pady=25)

        # 입력 문구 입력창
        delete_ent = tk.Entry(
            reconfirm_window, bg=Color.GREY, font=Font.ENTRY, fg=Color.FONT_ENTRY,
            insertbackground=Color.FONT_ENTRY, justify='center'
        )
        delete_ent.pack(pady=(0, 25))

        # 최종 계정 삭제 버튼
        tk.Button(
            reconfirm_window, bg=Color.BEIGE, font=Font.BUTTON,
            fg=Color.FONT_DARK, text='Delete', width=10,
            command=lambda: logic.validate_delaccount(
                self, delete_ent.get(), username, delmessage_lbl, delaccount_window
            )
        ).pack(pady=(0, 4))

        # 오류메시지
        delmessage_lbl = tk.Label(reconfirm_window, bg=Color.DARK, font=Font.CAPTION)
        delmessage_lbl.pack()


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
                                 command=lambda: self.controller.show_frame(Overframe))
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


class Overframe(tk.Frame):
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
