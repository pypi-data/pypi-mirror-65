import tkinter

"""
tkinter.Misc
"""


def get_screen_width(misc: tkinter.Misc):
    """
    获取屏幕宽度像素
    :return:
    """
    return misc.winfo_screenwidth()


def get_screen_height(misc: tkinter.Misc):
    """
    获取屏幕高度像素
    :return:
    """
    return misc.winfo_screenheight()


def get_widget_width(misc: tkinter.Misc):
    """
    获取窗体宽度像素
    :return:
    """
    return misc.winfo_width()


def get_widget_height(misc: tkinter.Misc):
    """
    获取窗体高度像素
    :return:
    """
    return misc.winfo_height()


"""
tkinter.Wm
"""


def set_wm_state_max(wm: tkinter.Wm):
    """
    窗体最大化
    :param wm:
    :return:
    """
    wm.wm_state("zoomed")


def set_wm_state_min(wm: tkinter.Wm):
    """
    窗体最小化，通过set_wm_state_deiconify恢复
    :param wm:
    :return:
    """
    wm.wm_state("iconic")


def set_wm_state_normal(wm: tkinter.Wm):
    """
    窗体恢复正常
    :param wm:
    :return:
    """
    wm.wm_state("normal")


def set_wm_state_withdrawn(wm: tkinter.Wm):
    """
    窗体隐藏，通过set_wm_state_deiconify恢复
    :param wm:
    :return:
    """
    wm.wm_state("withdrawn")


def set_wm_state_deiconify(wm: tkinter.Wm):
    """
    激活窗体
    :param wm:
    :return:
    """
    wm.wm_deiconify()


def set_wm_tool(wm: tkinter.Wm, is_toolwindow=True):
    """
    是否设置工具栏样式
    :param wm:
    :param is_toolwindow:
    :return:
    """
    wm.attributes("-toolwindow", is_toolwindow)


def set_wm_topmost(wm: tkinter.Wm, is_topmost=True):
    """
    设置窗体置顶
    :param is_topmost:
    :return:
    """
    wm.attributes("-topmost", is_topmost)


def set_wm_alpha(wm: tkinter.Wm, alpha=0.5):
    """
    设置窗体透明度
    :param alpha:
    :return:
    """
    wm.attributes("-alpha", alpha)


def set_wm_resizable(wm: tkinter.Wm, resizable=False):
    """
    设置是否可以调整窗体大小，默认禁止
    :param wm:
    :param resizable:
    :return:
    """
    wm.resizable(resizable, resizable)


def set_wm_overrideredirect(wm: tkinter.Wm, ignore=True):
    """
    该窗体忽略窗口管理器的管理，会导致无边框，无标题，图标，最大，最小按钮
    :param wm:
    :param ignore:
    :return:
    """
    wm.overrideredirect(ignore)


"""
common
"""


def get_geometry(width: int, height: int, x: int = 0, y: int = 0):
    """
    获取geometry
    :param width:
    :param height:
    :param x:
    :param y:
    :return:
    """
    return str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y)


"""
window
"""


def set_window_center(window, width=None, height=None, dx=0, dy=20):
    """
    设置窗体居中
    :return:
    """
    if width is None:
        width = get_widget_width(window)
    if height is None:
        height = get_widget_height(window)
    x = int((get_screen_width(window) - width - dx * 2) / 2)
    y = int((get_screen_height(window) - height - dy * 2) / 2)
    window.geometry(get_geometry(width, height, x, y))


"""
tk
"""


def set_tk_center(tk: tkinter.Tk, dx=0, dy=20):
    """
    设置窗体居中
    :return:
    """
    width = get_widget_width(tk)
    height = get_widget_height(tk)
    x = int((get_screen_width(tk) - width - dx * 2) / 2)
    y = int((get_screen_height(tk) - height - dy * 2) / 2)

    tk.geometry(get_geometry(width, height, x, y))


"""
toplevel
"""


def set_toplevel_center(toplevel: tkinter.Toplevel):
    """
    设置窗体居中
    :return:
    """
    width = get_widget_width(toplevel)
    height = get_widget_height(toplevel)
    x = int((get_screen_width(toplevel) - width) / 2)
    y = int((get_screen_height(toplevel) - height) / 2)

    toplevel.geometry(get_geometry(width, height, x, y))


"""
messagebox
"""


def showinfo(title=None, message=None):
    "Show an info message"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.showinfo(title, message)
    win.destroy()
    return s


def showwarning(title=None, message=None):
    "Show a warning message"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.showwarning(title, message)
    win.destroy()
    return s


def showerror(title=None, message=None):
    "Show an error message"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.showerror(title, message)
    win.destroy()
    return s


def askquestion(title=None, message=None):
    "Ask a question"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.askquestion(title, message)
    win.destroy()
    return s


def askokcancel(title=None, message=None):
    "Ask if operation should proceed; return true if the answer is ok"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.askokcancel(title, message)
    win.destroy()
    return s


def askyesno(title=None, message=None):
    "Ask a question; return true if the answer is yes"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.askyesno(title, message)
    win.destroy()
    return s


def askyesnocancel(title=None, message=None):
    "Ask a question; return true if the answer is yes, None if cancelled."
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.askyesnocancel(title, message)
    win.destroy()
    return s


def askretrycancel(title=None, message=None):
    "Ask if operation should be retried; return true if the answer is yes"
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.messagebox as mb
    s = mb.askretrycancel(title, message)
    win.destroy()
    return s


"""
dialog
"""


def askinteger(title, prompt):
    '''get an integer from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is an integer
    '''
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.simpledialog as sd
    r = sd.askinteger(title, prompt)
    win.destroy()
    return r


def askfloat(title, prompt):
    '''get a float from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a float
    '''
    win = tkinter.Tk()
    win.withdraw()
    import tkinter.simpledialog as sd
    r = sd.askfloat(title, prompt)
    win.destroy()
    return r


def askstring(title, prompt):
    '''get a string from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a string
    '''
    win = tkinter.Tk()
    win.withdraw()
    win.geometry("+400+400")
    import tkinter.simpledialog as sd
    r = sd.askstring(title, prompt)
    win.destroy()
    return r


"""
canvas
"""

"""
tkinter_mtest
"""
# print(askyesnocancel("WYQ", "Hello!"))
# print(askstring("WYQ", "WYQString"))
