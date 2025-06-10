

# Figma to Android Drawable Converter

一个简洁的桌面GUI工具，旨在帮助 Android 开发者快速、高效地将 Figma 导出的多密度图片资源，转换为符合 Android 项目规范的 `drawable` 文件夹结构。

---

## 💡 它解决了什么问题？

Figma 是一个流行的UI设计工具，当设计师导出适用于不同屏幕密度的图片资源时，通常会得到一组带有 `@2x`, `@3x` 等后缀的文件。例如：

```
/downloads
├── icon_profile.png         (mdpi)
├── icon_profile@2x.png      (xhdpi)
├── icon_profile@3x.png      (xxhdpi)
├── button_bg.png
├── button_bg@2x.png
└── button_bg@3x.png
```

手动将这些文件重命名并分类到 Android 项目的 `drawable-mdpi`, `drawable-xhdpi`, `drawable-xxhdpi` 等文件夹中是一项重复且容易出错的工作。

本工具通过一个简单的图形界面，将这个过程自动化，让您只需几次点击即可完成转换。

## ✨ 功能特性

* **自动分组**: 智能扫描源文件夹，并根据文件名前缀（如 `icon_profile`）自动对图片进行分组。
* **批量重命名**: 为整组图片（例如 `icon_profile` 的所有密度版本）指定一个符合 Android 规范的新名称（如 `ic_profile`）。
* **自动目录映射**: 根据 Figma 的后缀（`@1.5x`, `@2x`, `@3x` 等）自动将文件放置到正确的 `drawable-*dpi` 文件夹。
* **文件夹创建**: 如果目标 `drawable` 文件夹不存在，工具会自动创建。
* **简单易用**: 直观的图形用户界面，无需复杂的命令行操作。
* **跨平台**: 基于 Python 和 Tkinter 构建，可在 Ubuntu, macOS 和 Windows 上运行。

## 🖥️ 系统要求 (Ubuntu)

在运行此工具之前，请确保您的 Ubuntu 系统已安装以下环境：

1.  **Python 3**: Ubuntu 通常会预装。可以通过 `python3 --version` 命令检查。
2.  **Tkinter 库**: Python 的标准 GUI 库。如果缺失，可通过以下命令安装：
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk
    ```

## 🚀 如何使用

1.  **保存脚本**: 将 `figma2android.py` 代码保存到您电脑的任意位置。
2.  **运行工具**: 打开终端，进入脚本所在的目录，并执行以下命令：
    ```bash
    python3 figma2android.py
    ```
3.  **选择源文件夹**: 点击界面左上角的 **“浏览...”** 按钮，选择您从 Figma 导出并存放所有图片资源的文件夹。
4.  **选择图片组**: 工具会自动扫描并分组。在左侧的列表中，点击您想要处理的图片组（例如 `Polygon 2`）。
5.  **输入新文件名**: 在右侧的 **“新文件名”** 输入框中，填写该组图片在 Android 项目中希望使用的新名称。**注意**：名称只能包含小写字母、数字和下划线（例如 `ic_polygon_2`）。
6.  **选择目标文件夹**: 点击 **“选择目标...”** 按钮，导航到您的 Android 项目，并选择 `res` 文件夹。工具会自动验证所选的是否为 `res` 文件夹。
7.  **导出**: 点击 **“🚀 导出选中组”** 按钮。工具将自动完成所有重命名、创建文件夹和移动文件的操作。
8.  **完成!** 您会收到一个成功提示。现在，您可以去您的 Android 项目中查看 `drawable-*dpi` 文件夹，新的资源已经准备就绪。

## ⚙️ 文件命名约定和配置

本工具依赖于 Figma 导出的标准命名约定。默认的后缀和 Android 密度文件夹映射关系如下：

| Figma 文件后缀 | 对应 Android Drawable 文件夹 |
| :------------- | :----------------------------- |
| `[name].png`     | `drawable-mdpi`                |
| `[name]@1x.png`  | `drawable-mdpi`                |
| `[name]@1.5x.png`| `drawable-hdpi`                |
| `[name]@2x.png`  | `drawable-xhdpi`               |
| `[name]@3x.png`  | `drawable-xxhdpi`              |
| `[name]@4x.png`  | `drawable-xxxhdpi`             |

**高级定制**: 如果您的 Figma 导出设置不同，可以直接在 `figma2android.py` 脚本中修改 `DENSITY_MAP` 字典来调整这个映射关系。

```python
# 位于脚本顶部的配置字典
DENSITY_MAP = {
    '': 'drawable-mdpi',
    '@1x': 'drawable-mdpi',
    '@1.5x': 'drawable-hdpi',
    '@2x': 'drawable-xhdpi',
    '@3x': 'drawable-xxhdpi',
    '@4x': 'drawable-xxxhdpi',
}
```

## 📄 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)。
