# %%
import os
import xml.etree.ElementTree as ET
import json
import glob


uv_path = "D:\embed_doc\h743\h743tool\STM32H743VIT6_DEMO_25M XTAL\LCD_1.14inch\MDK-ARM\STM32H743VIT6.uvprojx"
# cmds_path = os.path.dirname(uv_path)
cmds_path = "D:\embed_doc\h743\h743tool\STM32H743VIT6_DEMO_25M XTAL\LCD_1.14inch"


def find_uvprojx(directory):
    # 使用glob模块搜索指定目录及其子目录中的所有.uvprojx文件
    uvprojx_files = glob.glob(os.path.join(directory, '**', '*.uvprojx'), recursive=True)
    print(f'find {uvprojx_files}')
    return uvprojx_files


# 调用函数并打印找到的.txt文件列表
uvprojx_files = find_uvprojx(os.getcwd())
uvprojx_files = sorted(uvprojx_files, key=lambda x: x.count(os.sep))
for file in uvprojx_files:
    uv_path = os.path.abspath(file)
    print(f'process {uv_path}')
    break


# 解析 XML 文件
tree = ET.parse(uv_path)
root = tree.getroot()

# 打印根元素的标签
print(f'Root element: {root.tag}')

cmds = []
# directory
file_json = {"arguments":["-c","-D__GNUC__"],"directory":os.path.dirname(uv_path).replace('\\', '/')}
# head files
headers = root.findall('.//IncludePath')
for header in headers:
    if header.text is not None:
        paths = header.text.replace('\\', '/').split(';')
        paths = [path.strip() for path in paths]
        # 打印每个路径
        for path in paths:
            path = "-I"+path
            print(path)
            file_json["arguments"].append(path)
# macro
macros = root.findall('.//Define')
for macro in macros:
    if macro.text is not None:
        defines = macro.text.split(',')
        for d in defines:
            d = "-D" + d
            print(d)
            file_json["arguments"].append(d)


all_subchildren = root.findall('.//File')
for file_element in all_subchildren:
    # 获取 <FileName>, <FileType>, <FilePath> 子元素的值
    file_name = file_element.find('FileName').text
    file_type = file_element.find('FileType').text
    file_path = file_element.find('FilePath').text.replace('\\', '/')
    absolute_file_path = os.path.abspath(file_path)
    if file_type == "1":
        # print("FileName:", file_name)
        # print("FileType:", file_type)
        print("FilePath:", file_path)
        # print("FilePath (Absolute):", absolute_file_path)
        file_json["file"] = file_path
        cmds.append(file_json.copy())

with open('compile_commands.json', 'w') as f:
    json.dump(cmds, f, indent=4)

print("compile_commands.json 文件已创建")
