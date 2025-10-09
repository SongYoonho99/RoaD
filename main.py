import tkinter as tk

from ui import LoginFrame, MenuFrame, TestFrame, ResultFrame, SettingsFrame
from db import create_users_table, create_record_table, create_main_table
from constants import Color

class App:
    """ 메인 애플리케이션 클래스 """

    def __init__(self):
        # 메인 Tk 객체
        self.root = tk.Tk()
        self.root.title("RoaD")
        self.root.minsize(1200, 700)
        self.root.state('zoomed')
        self.root.iconbitmap("resources/BI.ico")

        # Tk 옵션 설정
        self.root.option_add("*Background", Color.GREY)
        self.root.option_add("*Foreground", Color.FONT_DEFAULT)
        self.root.option_add("*TCombobox*Listbox*Background", Color.LIGHT_GREY)
        self.root.option_add('*TCombobox*Listbox*Foreground', Color.FONT_DARK)
        self.root.option_add('*TCombobox*Listbox*Font', 'Arial 16')

        # 모든 프레임을 담는 컨테이너 생성
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # 프레임 초기화
        self.frames = {}
        for F in (LoginFrame, MenuFrame, TestFrame, ResultFrame, SettingsFrame):
            frame = F(container, self)     # Frame 생성, controller=self
            self.frames[F] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        # 초기 화면 설정
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        """ 특정 프레임을 최상위로 표시 """

        self.frames[frame_class].tkraise()

    def run(self):
        """ 메인 이벤트 루프 실행 """

        self.root.mainloop()

if __name__ == "__main__":
    # 테이블 없을 시 생성
    create_users_table()
    create_record_table()
    create_main_table()

    # 앱 객체 생성 및 실행
    app = App()
    app.run()