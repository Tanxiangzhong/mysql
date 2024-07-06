import tkinter as tk  
from tkinter import messagebox  
import mysql.connector  
  
# 数据库配置  
db_config = {  
    'host': 'localhost',  
    'user': 'root',  
    'password': '112233aabbCC',  
    'database': 'db_info'  
}  
  
# 数据库连接函数  
def create_db_connection():  
    return mysql.connector.connect(**db_config)  
  
# 注册新用户  
def register_user():  
    username = username_entry.get()  
    password = password_entry.get()  
  
    if not username.isalpha():  
        messagebox.showerror("错误", "用户名必须只包含英文字母。")  
        return  
  
    if not password:  
        messagebox.showerror("错误", "密码不能为空。")  
        return  
  
    conn = create_db_connection()  
    cursor = conn.cursor()  
  
    # 这里应该有一个更安全的密码存储方式，比如使用哈希  
    # 但为了简单起见，这里直接存储明文密码  
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"  
    cursor.execute(query, (username, password))  
    conn.commit()  
    conn.close()  
    messagebox.showinfo("成功", "注册成功！")  
  
# 用户登录  
def login_user():  
    username = username_login_entry.get()  
    password = password_login_entry.get()  
  
    conn = create_db_connection()  
    cursor = conn.cursor()  
  
    query = "SELECT * FROM users WHERE username = %s AND password = %s"  
    cursor.execute(query, (username, password))  
  
    result = cursor.fetchone()  
    if result:  
        messagebox.showinfo("成功", "登录成功！")  
    else:  
        messagebox.showerror("错误", "用户名或密码不正确。")  
  
    conn.close()  
  
# 创建GUI  
root = tk.Tk()  
root.title("用户注册与登录")  
  
# 注册部分  
username_label = tk.Label(root, text="用户名:")  
username_label.grid(row=0, column=0, pady=5)  
username_entry = tk.Entry(root)  
username_entry.grid(row=0, column=1, pady=5)  
  
password_label = tk.Label(root, text="密码:")  
password_label.grid(row=1, column=0, pady=5)  
password_entry = tk.Entry(root, show="*")  
password_entry.grid(row=1, column=1, pady=5)  
  
register_button = tk.Button(root, text="注册", command=register_user)  
register_button.grid(row=2, column=1, pady=5)  
  
# 登录部分  
tk.Label(root, text="").grid(row=3, column=0)  # 空白行  
  
username_login_label = tk.Label(root, text="用户名:")  
username_login_label.grid(row=4, column=0, pady=5)  
username_login_entry = tk.Entry(root)  
username_login_entry.grid(row=4, column=1, pady=5)  
  
password_login_label = tk.Label(root, text="密码:")  
password_login_label.grid(row=5, column=0, pady=5)  
password_login_entry = tk.Entry(root, show="*")  
password_login_entry.grid(row=5, column=1, pady=5)  
  
login_button = tk.Button(root, text="登录", command=login_user)  
login_button.grid(row=6, column=1, pady=5)  
  
root.mainloop()
