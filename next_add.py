import os
import re

def process_files(folder_path):
    # 第一步处理：在符合条件的行后添加 -next
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                # 检查是否是changeFigure/changeBg/BGM行
                if re.match(r'^(changeFigure|changeBg|bgm):.*;', line):
                    # 收集所有连续的change行
                    change_lines = []
                    j = i
                    while j < len(lines) and re.match(r'^(changeFigure|changeBg|bgm):.*;', lines[j].strip()):
                        change_lines.append(j)
                        j += 1
                    
                    # 检查下一行是否以 -fontSize=default; 结尾
                    if j < len(lines) and re.search(r' -fontSize=default;[\s]*$', lines[j]):
                        # 处理所有连续的change行
                        for idx in change_lines:
                            # 替换 ; 为 -next;
                            new_line = lines[idx].rstrip('\n').rstrip(';') + ' -next;\n'
                            new_lines.append(new_line)
                        # 添加fontSize行不变
                        new_lines.append(lines[j])
                        i = j + 1
                    else:
                        # 不满足条件，保持原样
                        new_lines.append(lines[i])
                        i += 1
                else:
                    new_lines.append(lines[i])
                    i += 1
            
            # 第二步处理：将连续的 -next -next 替换为 -next
            final_content = ''.join(new_lines)
            final_content = re.sub(r' -next -next', ' -next', final_content)

            # 第三步处理：移除 bgm:xxxx -next; 中的 -next
            final_content = re.sub(r'(bgm:[^;]*) -next;', r'\1;', final_content)
            
            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(final_content)

if __name__ == '__main__':
    folder_path = input('请输入文件夹路径: ')
    process_files(folder_path)
    print('处理完成!')