from Utils import *

def compare_code_lines(code1, code2)->tuple[int,int]:
    """
    比较两段代码的相同行数，输出第一个不相同的行及总共相同的行数。
    如果全部相同，则返回提示信息。
    
    :param code1: 第一段代码，字符串形式。
    :param code2: 第二段代码，字符串形式。
    :return: 第一个不相同的行的信息（如果有）及总共相同的行数。
    """
    # 将两段代码按行分割成列表
    lines1 = code1.strip().split('\n')
    lines2 = code2.strip().split('\n')
    
    # 初始化相同行数计数器
    same_count = 0
    
    # 初始化不同行的信息
    first_diff_line = 0
    
    # 遍历所有行
    max_len = max(len(lines1), len(lines2))
    for i in range(max_len):
        if i < len(lines1) and i < len(lines2) and lines1[i] == lines2[i]:
            # 如果当前行相同，增加相同行数
            same_count += 1
        elif not first_diff_line:
            # 如果找到第一个不相同的行，记录该行的信息
            first_diff_line = i+1
    
    return same_count, first_diff_line

def recompareAll(contestID):
    subjects = CFSubject.load_list_from_json(contestID)
    for subject in subjects:
        same_count, first_diff_line = compare_code_lines(subject.acceptedCode, subject.rejectedCode)
        lineCount_code1 = len(subject.acceptedCode.split('\n'))
        lineCount_code2 = len(subject.rejectedCode.split('\n'))
        max_lineCount = max(lineCount_code1,lineCount_code2)
        if (first_diff_line > 0 and max_lineCount - same_count <= thresh_diff_lines):
            # TODO: remove this case
            pass
        subject.errorLine = first_diff_line
    CFSubject.save_list_to_json(subjects,contestID)

def test():
    # 示例用法
    code1 = """def hello_world():
        print("Hel
        lo, World!")
        return 42"""

    code2 = """def hello_world():
        print("Hello, World!")
        return 42
        hi"""

    print(compare_code_lines(code1, code2))

if __name__ == "__main__":
    recompareAll(1915)

