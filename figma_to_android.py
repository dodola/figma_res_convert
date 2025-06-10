import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import re
from collections import defaultdict

# --- 配置Figma后缀到Android密度的映射 ---
# 可以根据需要自行扩展
DENSITY_MAP = {
    '': 'drawable-mdpi',       # e.g., 'image.png'
    '@1x': 'drawable-mdpi',    # e.g., 'image@1x.png'
    '@1.5x': 'drawable-hdpi',  # e.g., 'image@1.5x.png'
    '@2x': 'drawable-xhdpi',   # e.g., 'image@2x.png'
    '@3x': 'drawable-xxhdpi',  # e.g., 'image@3x.png'
    '@4x': 'drawable-xxxhdpi', # e.g., 'image@4x.png'
}

class FigmaToAndroidConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Figma to Android Converter")
        self.geometry("800x600")

        # --- 数据存储 ---
        self.source_dir = tk.StringVar()
        self.target_dir = tk.StringVar()
        self.image_groups = defaultdict(list)

        # --- UI 布局 ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- 左侧: 文件选择和分组列表 ---
        left_pane = ttk.Frame(main_frame)
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))

        source_frame = ttk.LabelFrame(left_pane, text="1. 选择 Figma 导出文件夹")
        source_frame.pack(fill="x", pady=(0, 10))

        ttk.Entry(source_frame, textvariable=self.source_dir, state="readonly").pack(side="left", fill="x", expand=True, padx=5, pady=5)
        ttk.Button(source_frame, text="浏览...", command=self.select_source_dir).pack(side="right", padx=5, pady=5)

        group_frame = ttk.LabelFrame(left_pane, text="2. 选择图片组")
        group_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(group_frame, columns=("files"), show="headings")
        self.tree.heading("files", text="识别出的图片组 (Group)")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_group_select)

        # --- 右侧: 重命名和导出 ---
        right_pane = ttk.Frame(main_frame, width=280)
        right_pane.pack(side="right", fill="y")
        right_pane.pack_propagate(False) # 防止面板缩放

        self.rename_frame = ttk.LabelFrame(right_pane, text="3. 设置新文件名和目标")
        self.rename_frame.pack(fill="x", pady=(25, 10))

        ttk.Label(self.rename_frame, text="新文件名 (不含后缀):").pack(fill="x", padx=10, pady=(10, 0))
        self.new_name_entry = ttk.Entry(self.rename_frame, state="disabled")
        self.new_name_entry.pack(fill="x", padx=10, pady=5)

        ttk.Label(self.rename_frame, text="Android res 文件夹:").pack(fill="x", padx=10, pady=(10, 0))
        self.target_entry = ttk.Entry(self.rename_frame, textvariable=self.target_dir, state="readonly")
        self.target_entry.pack(fill="x", padx=10, pady=5)
        ttk.Button(self.rename_frame, text="选择目标...", command=self.select_target_dir, state="disabled").pack(fill="x", padx=10, pady=5)

        self.export_button = ttk.Button(right_pane, text="🚀 导出选中组", command=self.export_files, state="disabled")
        self.export_button.pack(fill="x", pady=10, padx=10, ipady=10)

        self.status_label = ttk.Label(self, text="请先选择 Figma 导出文件夹", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=5)

    def select_source_dir(self):
        """选择包含Figma导出图片的源文件夹"""
        path = filedialog.askdirectory(title="选择 Figma 图片文件夹")
        if not path:
            return
        self.source_dir.set(path)
        self.status_label.config(text=f"已选择源文件夹: {path}")
        self.scan_and_group_files()

    def scan_and_group_files(self):
        """扫描文件夹并对图片进行分组"""
        self.image_groups.clear()
        self.tree.delete(*self.tree.get_children())
        
        source_path = self.source_dir.get()
        if not source_path:
            return

        # 正则表达式来匹配 'name@2x.png' 格式
        # (group1: name) (group2: @2x) (group3: .png)
        pattern = re.compile(r"(.+?)(@[\d.]+x)?(\.png|\.jpg|\.jpeg)$", re.IGNORECASE)

        for filename in os.listdir(source_path):
            match = pattern.match(filename)
            if match:
                base_name = match.group(1)
                self.image_groups[base_name].append(filename)

        if not self.image_groups:
            self.status_label.config(text="警告: 在所选文件夹中未找到符合命名规则的图片。")
            return

        for base_name in sorted(self.image_groups.keys()):
            self.tree.insert("", "end", text=base_name, values=(f"{len(self.image_groups[base_name])} 个文件",))

        self.status_label.config(text=f"扫描完成！找到 {len(self.image_groups)} 个图片组。")

    def on_group_select(self, event):
        """当用户在列表中选择一个组时触发"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        self.new_name_entry.config(state="normal")
        for widget in self.rename_frame.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.config(state="normal")
        
        self.export_button.config(state="normal")
        self.status_label.config(text="请输入新文件名并选择目标文件夹。")


    def select_target_dir(self):
        """选择Android项目的res文件夹作为目标"""
        path = filedialog.askdirectory(title="选择 Android 项目的 res 文件夹")
        if path and os.path.basename(path) == 'res':
            self.target_dir.set(path)
            self.status_label.config(text=f"已选择目标文件夹: {path}")
        elif path:
            messagebox.showwarning("目标文件夹无效", "请选择一个名为 'res' 的 Android 资源文件夹。")

    def export_files(self):
        """执行重命名和移动文件的操作"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("错误", "请先选择一个图片组。")
            return
        
        base_name = self.tree.item(selected_items[0])['text']
        new_name = self.new_name_entry.get().strip()
        target_res_dir = self.target_dir.get()

        if not new_name:
            messagebox.showerror("错误", "新文件名不能为空。")
            return
        
        if not re.match(r"^[a-z0-9_]+$", new_name):
            messagebox.showerror("错误", "新文件名不合法。请只使用小写字母、数字和下划线。")
            return

        if not target_res_dir:
            messagebox.showerror("错误", "请选择一个目标 res 文件夹。")
            return
            
        try:
            files_to_move = self.image_groups[base_name]
            file_extension = ".png" # 假设都为png

            for filename in files_to_move:
                # 提取后缀，例如 @2x
                scale_suffix = ''
                match = re.search(r"(@[\d.]+x)", filename)
                if match:
                    scale_suffix = match.group(1)
                
                # 如果找不到精确匹配，使用空字符串作为默认key
                density_folder_name = DENSITY_MAP.get(scale_suffix, DENSITY_MAP.get(''))
                
                # 创建目标文件夹
                final_dest_folder = os.path.join(target_res_dir, density_folder_name)
                os.makedirs(final_dest_folder, exist_ok=True)
                
                # 准备源文件和目标文件路径
                source_file_path = os.path.join(self.source_dir.get(), filename)
                destination_file_path = os.path.join(final_dest_folder, new_name + file_extension)

                # 复制和重命名文件
                shutil.copy(source_file_path, destination_file_path)
            
            messagebox.showinfo("成功", f"'{base_name}' 组已成功导出为 '{new_name}.png'！")
            self.status_label.config(text=f"导出成功: {new_name}.png")

        except Exception as e:
            messagebox.showerror("导出失败", f"发生错误: {e}")
            self.status_label.config(text=f"导出失败: {e}")


if __name__ == "__main__":
    app = FigmaToAndroidConverter()
    app.mainloop()
