import os
import re

def process_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 第一步处理：所有 changeFigure/changeBg 行末尾添加 -next
            content = re.sub(
                r'^(changeFigure|changeBg):([^;]*);',  # 匹配 changeFigure:xxx; 或 changeBg:xxx;
                r'\1:\2 -next;',  # 替换为 changeFigure:xxx -next; 或 changeBg:xxx -next;
                content,
                flags=re.MULTILINE  # 确保 ^ 匹配每行开头
            )
          
            # 第二步处理：将连续的 -next -next 替换为 -next
            content = re.sub(r' -next -next', ' -next', content)
            
            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)

if __name__ == '__main__':
    folder_path = input('请输入文件夹路径: ')
    process_files(folder_path)
    print('处理完成!')