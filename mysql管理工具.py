import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import mysql.connector

conn = None

# 创建MySQL连接
def create_mysql_connection(host, user, password, database=None):
    try:
        if database:
            conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        else:
            conn = mysql.connector.connect(host=host, user=user, password=password)
        messagebox.showinfo('成功', '成功连接到MySQL服务器')
        return conn
    except mysql.connector.Error as err:
        error_code = 'ERROR1001'
        error_message = f'创建MySQL连接时出错（{error_code}）: {err}'
        messagebox.showerror('错误', error_message)
        return None

# 登录窗口
def show_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("登录MySQL")

    ttk.Label(login_window, text="服务器地址:").pack(pady=(10, 5))
    host_entry = ttk.Entry(login_window, width=40)
    host_entry.pack(pady=5)
    
    ttk.Label(login_window, text="用户名:").pack(pady=5)
    user_entry = ttk.Entry(login_window, width=40)
    user_entry.pack(pady=5)
    
    ttk.Label(login_window, text="密码:").pack(pady=5)
    password_entry = ttk.Entry(login_window, show='*', width=40)
    password_entry.pack(pady=5)
    
    ttk.Label(login_window, text="数据库:").pack(pady=5)
    database_entry = ttk.Entry(login_window, width=40)
    database_entry.pack(pady=10)

    def login():
        host = host_entry.get()
        user = user_entry.get()
        password = password_entry.get()
        database = database_entry.get()
        global conn
        conn = create_mysql_connection(host, user, password, database)
        if conn:
            login_button.config(state=tk.DISABLED)
            logout_button.config(state=tk.NORMAL)
            execute_query_button.config(state=tk.NORMAL)
            list_databases_button.config(state=tk.NORMAL)
            create_database_button.config(state=tk.NORMAL)
            delete_database_button.config(state=tk.NORMAL)
            list_tables_button.config(state=tk.NORMAL)
            manage_table_button.config(state=tk.NORMAL)
            login_window.destroy()

    ttk.Button(login_window, text="登录", command=login).pack(pady=10)

# 注册窗口
def show_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("注册MySQL用户")

    ttk.Label(register_window, text="服务器地址:").pack(pady=(10, 5))
    host_entry = ttk.Entry(register_window, width=40)
    host_entry.pack(pady=5)
    
    ttk.Label(register_window, text="管理员用户名:").pack(pady=5)
    admin_user_entry = ttk.Entry(register_window, width=40)
    admin_user_entry.pack(pady=5)
    
    ttk.Label(register_window, text="管理员密码:").pack(pady=5)
    admin_password_entry = ttk.Entry(register_window, show='*', width=40)
    admin_password_entry.pack(pady=5)
    
    ttk.Label(register_window, text="新用户名:").pack(pady=5)
    new_user_entry = ttk.Entry(register_window, width=40)
    new_user_entry.pack(pady=5)
    
    ttk.Label(register_window, text="新密码:").pack(pady=10)
    new_password_entry = ttk.Entry(register_window, show='*', width=40)
    new_password_entry.pack(pady=10)

    def register():
        host = host_entry.get()
        admin_user = admin_user_entry.get()
        admin_password = admin_password_entry.get()
        new_user = new_user_entry.get()
        new_password = new_password_entry.get()
        
        conn = create_mysql_connection(host, admin_user, admin_password)
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"CREATE USER '{new_user}'@'%' IDENTIFIED BY '{new_password}'")
                cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{new_user}'@'%' WITH GRANT OPTION")
                conn.commit()
                messagebox.showinfo('成功', f'用户 {new_user} 创建成功')
                register_window.destroy()
            except mysql.connector.Error as err:
                error_code = 'ERROR1002'
                error_message = f'创建用户时出错（{error_code}）: {err}'
                messagebox.showerror('错误', error_message)
            cursor.close()
            conn.close()

    ttk.Button(register_window, text="注册", command=register).pack(pady=10)

# 注销MySQL
def logout_mysql():
    global conn
    if conn:
        try:
            conn.close()
            messagebox.showinfo('成功', '成功注销MySQL连接')
            login_button.config(state=tk.NORMAL)
            logout_button.config(state=tk.DISABLED)
            execute_query_button.config(state=tk.DISABLED)
            list_databases_button.config(state=tk.DISABLED)
            create_database_button.config(state=tk.DISABLED)
            delete_database_button.config(state=tk.DISABLED)
            list_tables_button.config(state=tk.DISABLED)
            manage_table_button.config(state=tk.DISABLED)
            conn = None
        except mysql.connector.Error as err:
            error_code = 'ERROR1003'
            error_message = f'注销MySQL连接时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)

# 执行SQL查询
def execute_query():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    query = simpledialog.askstring("输入SQL查询", "请输入SQL查询:")
    if query:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if cursor.description:
                results = cursor.fetchall()
                show_query_results(results)
                cursor.close()
            else:
                conn.commit()
                messagebox.showinfo('成功', '操作成功')
        except mysql.connector.Error as err:
            error_code = 'ERROR1004'
            error_message = f'执行SQL查询时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)

# 显示查询结果
def show_query_results(results):
    result_window = tk.Toplevel(root)
    result_window.title("查询结果")

    tree = ttk.Treeview(result_window)
    tree['columns'] = tuple(range(1, len(results[0]) + 1))
    tree['show'] = 'headings'

    for i in range(1, len(results[0]) + 1):
        tree.heading(i, text=f"列 {i}")

    for row in results:
        tree.insert('', tk.END, values=row)

    tree.pack(expand=tk.YES, fill=tk.BOTH)

# 列出所有数据库
def list_databases():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        show_query_results(databases)
        cursor.close()
    except mysql.connector.Error as err:
        error_code = 'ERROR1005'
        error_message = f'列出数据库时出错（{error_code}）: {err}'
        messagebox.showerror('错误', error_message)

# 创建新数据库
def create_database():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    db_name = simpledialog.askstring("输入数据库名称", "请输入要创建的数据库名称:")
    if db_name:
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {db_name}")
            messagebox.showinfo('成功', f'数据库 {db_name} 创建成功')
            cursor.close()
        except mysql.connector.Error as err:
            error_code = 'ERROR1006'
            error_message = f'创建数据库时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)

# 删除数据库
def delete_database():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    db_name = simpledialog.askstring("输入数据库名称", "请输入要删除的数据库名称:")
    if db_name:
        cursor = conn.cursor()
        try:
            cursor.execute(f"DROP DATABASE {db_name}")
            messagebox.showinfo('成功', f'数据库 {db_name} 删除成功')
            cursor.close()
        except mysql.connector.Error as err:
            error_code = 'ERROR1007'
            error_message = f'删除数据库时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)

# 列出所有表
def list_tables():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if not tables:
            messagebox.showinfo('提示', '数据库中没有表')
        else:
            show_query_results(tables)
        cursor.close()
    except mysql.connector.Error as err:
        error_code = 'ERROR1008'
        error_message = f'列出表时出错（{error_code}）: {err}'
        messagebox.showerror('错误', error_message)


# 管理表数据
def manage_table():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return

    database_name = simpledialog.askstring("输入数据库名称", "请输入要操作的数据库名称:")
    if database_name:
        try:
            cursor = conn.cursor()
            cursor.execute(f"USE {database_name}")
        except mysql.connector.Error as err:
            error_code = 'ERROR1009'
            error_message = f'选择数据库时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)
            return

        table_name = simpledialog.askstring("输入表名称", "请输入要管理的表名称:")
        if table_name:
            manage_window = tk.Toplevel(root)
            manage_window.title(f"管理表 {table_name}")

            def add_data():
                add_window = tk.Toplevel(manage_window)
                add_window.title(f"添加数据到 {table_name}")

                columns = []
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                for column in cursor.fetchall():
                    columns.append(column[0])

                entries = {}
                for column in columns:
                    ttk.Label(add_window, text=column).pack(pady=(10, 5))
                    entry = ttk.Entry(add_window, width=40)
                    entry.pack(pady=5)
                    entries[column] = entry

                def submit_add():
                    values = [entries[column].get() for column in columns]
                    placeholders = ', '.join(['%s'] * len(values))
                    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    try:
                        cursor.execute(query, values)
                        conn.commit()
                        messagebox.showinfo('成功', f'数据成功添加到 {table_name}')
                        add_window.destroy()
                    except mysql.connector.Error as err:
                        error_code = 'ERROR1010'
                        error_message = f'添加数据时出错（{error_code}）: {err}'
                        messagebox.showerror('错误', error_message)

                ttk.Button(add_window, text="提交", command=submit_add).pack(pady=10)

            def delete_data():
                id_column = simpledialog.askstring("输入ID列名称", "请输入ID列的名称（通常是主键）:")
                if id_column:
                    id_value = simpledialog.askstring("输入ID值", f"请输入要删除的记录的 {id_column} 值:")
                    if id_value:
                        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
                        try:
                            cursor = conn.cursor()
                            cursor.execute(query, (id_value,))
                            conn.commit()
                            messagebox.showinfo('成功', f'记录成功从 {table_name} 删除')
                        except mysql.connector.Error as err:
                            error_code = 'ERROR1011'
                            error_message = f'删除数据时出错（{error_code}）: {err}'
                            messagebox.showerror('错误', error_message)

            def update_data():
                id_column = simpledialog.askstring("输入ID列名称", "请输入ID列的名称（通常是主键）:")
                if id_column:
                    id_value = simpledialog.askstring("输入ID值", f"请输入要修改的记录的 {id_column} 值:")
                    if id_value:
                        columns = []
                        cursor = conn.cursor()
                        cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                        for column in cursor.fetchall():
                            columns.append(column[0])

                        updates = {}
                        for column in columns:
                            new_value = simpledialog.askstring("输入新值", f"请输入列 {column} 的新值:")
                            if new_value:
                                updates[column] = new_value

                        set_clause = ', '.join([f"{col} = %s" for col in updates.keys()])
                        values = list(updates.values()) + [id_value]
                        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
                        try:
                            cursor.execute(query, values)
                            conn.commit()
                            messagebox.showinfo('成功', f'记录成功更新在 {table_name}')
                        except mysql.connector.Error as err:
                            error_code = 'ERROR1012'
                            error_message = f'更新数据时出错（{error_code}）: {err}'
                            messagebox.showerror('错误', error_message)

            ttk.Button(manage_window, text="添加数据", command=add_data).pack(pady=10)
            ttk.Button(manage_window, text="删除数据", command=delete_data).pack(pady=10)
            ttk.Button(manage_window, text="修改数据", command=update_data).pack(pady=10)

# 进入指定数据库
def enter_database():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return
    
    database_name = simpledialog.askstring("输入数据库名称", "请输入要连接的数据库名称:")
    if database_name:
        try:
            cursor = conn.cursor()
            cursor.execute(f"USE {database_name}")
            messagebox.showinfo('成功', f'成功连接到数据库 {database_name}')
            list_tables_button.config(state=tk.NORMAL)
            manage_table_button.config(state=tk.NORMAL)
        except mysql.connector.Error as err:
            error_code = 'ERROR1013'
            error_message = f'连接数据库时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)

# 删除表中数据
def delete_table_data():
    global conn
    if not conn:
        messagebox.showerror('错误', '请先登录MySQL')
        return

    database_name = simpledialog.askstring("输入数据库名称", "请输入要操作的数据库名称:")
    if database_name:
        try:
            cursor = conn.cursor()
            cursor.execute(f"USE {database_name}")
        except mysql.connector.Error as err:
            error_code = 'ERROR1014'
            error_message = f'选择数据库时出错（{error_code}）: {err}'
            messagebox.showerror('错误', error_message)
            return

        table_name = simpledialog.askstring("输入表名称", "请输入要操作的表名称:")
        if table_name:
            condition = simpledialog.askstring("输入条件", "请输入删除条件（例如：id=1）:")
            if condition:
                try:
                    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
                    conn.commit()
                    messagebox.showinfo('成功', f'表 {table_name} 中符合条件的数据已删除')
                except mysql.connector.Error as err:
                    error_code = 'ERROR1015'
                    error_message = f'删除数据时出错（{error_code}）: {err}'
                    messagebox.showerror('错误', error_message)

# 创建主窗口
root = tk.Tk()
root.title('MySQL管理工具')

# 创建菜单栏
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="退出", command=root.quit)
menu_bar.add_cascade(label="文件", menu=file_menu)

tool_menu = tk.Menu(menu_bar, tearoff=0)
tool_menu.add_command(label="登录MySQL", command=show_login_window)
tool_menu.add_command(label="注册MySQL用户", command=show_register_window)
tool_menu.add_command(label="进入指定数据库", command=enter_database)
tool_menu.add_command(label="删除表中数据", command=delete_table_data)
menu_bar.add_cascade(label="工具", menu=tool_menu)

root.config(menu=menu_bar)

# 创建按钮
login_button = ttk.Button(root, text='登录MySQL', command=show_login_window)
login_button.pack(pady=10)

logout_button = ttk.Button(root, text='注销MySQL', command=logout_mysql, state=tk.DISABLED)
logout_button.pack(pady=10)

execute_query_button = ttk.Button(root, text='执行SQL查询', command=execute_query, state=tk.DISABLED)
execute_query_button.pack(pady=10)

list_databases_button = ttk.Button(root, text='列出所有数据库', command=list_databases, state=tk.DISABLED)
list_databases_button.pack(pady=10)

create_database_button = ttk.Button(root, text='创建新数据库', command=create_database, state=tk.DISABLED)
create_database_button.pack(pady=10)

delete_database_button = ttk.Button(root, text='删除数据库', command=delete_database, state=tk.DISABLED)
delete_database_button.pack(pady=10)

list_tables_button = ttk.Button(root, text='列出所有表', command=list_tables, state=tk.DISABLED)
list_tables_button.pack(pady=10)

manage_table_button = ttk.Button(root, text='管理表数据', command=manage_table, state=tk.DISABLED)
manage_table_button.pack(pady=10)

# 创建文本框
result_text = scrolledtext.ScrolledText(root, width=100, height=20, wrap=tk.WORD)
result_text.pack(pady=10)

# 运行主循环
root.mainloop()
