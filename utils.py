""" 유틸리티 함수 모듈 """

import tkinter as tk

def center_window(window: tk.Toplevel | tk.Tk, width: int, height: int):
    """ Toplevel창을 화면 정중앙에 띄우는 함수 """

    x = window.winfo_screenwidth() // 2 - width // 2
    y = window.winfo_screenheight() // 2 - height // 2
    window.geometry(f"{width}x{height}+{x}+{y}")