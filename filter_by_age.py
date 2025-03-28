import xml.etree.ElementTree as ET
import os
import glob
import re

# 只保留 3 个年龄段
AGE_BUCKETS = {
    "0-15months": (0, 15),
    "15-20months": (15, 20),
    "20-60months": (20, 60)  # 20 个月以上到 5 岁
}

def parse_age(age_str):
    """将 CHILDES 年龄格式（P1Y08M）转换为月龄（20 个月）"""
    match = re.match(r"P(\d+)Y(\d+)M", age_str)
    if match:
        years, months = int(match.group(1)), int(match.group(2))
        return years * 12 + months  # 转换为总月数
    return None  # 处理缺失年龄数据

def parse_chat_xml(xml_file):
    """解析单个 XML 文件，提取儿童年龄和对话"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 获取儿童年龄
    child = root.find(".//{http://www.talkbank.org/ns/talkbank}participant[@role='Target_Child']")
    age_str = child.get("age") if child is not None else None
    age_months = parse_age(age_str) if age_str else None

    if age_months is None:
        return None, None  # 跳过无法解析年龄的文件

    output = []

    # 提取对话
    for utterance in root.findall(".//{http://www.talkbank.org/ns/talkbank}u"):
        speaker = utterance.get("who")  # 说话人 (CHI 或 MOT)
        words = [w.text for w in utterance.findall(".//{http://www.talkbank.org/ns/talkbank}w") if w.text]
        if words:
            output.append(f"{speaker}: {' '.join(words)}")

    return age_months, "\n".join(output) + "\n\n"

def process_all_xml_files(directory, output_directory):
    """递归处理所有 XML 文件，并按照年龄段分类保存"""
    xml_files = glob.glob(os.path.join(directory, "**/*.xml"), recursive=True)
    categorized_data = {key: [] for key in AGE_BUCKETS}  # 存储不同年龄段的文本

    print(f"🔍 Found {len(xml_files)} XML files. Processing...")

    for xml_file in xml_files:
        try:
            age_months, text = parse_chat_xml(xml_file)
            if age_months is None or text is None:
                continue  # 跳过无效数据

            # 确定年龄段
            for category, (min_age, max_age) in AGE_BUCKETS.items():
                if min_age <= age_months < max_age:
                    categorized_data[category].append(text)
                    break  # 找到对应年龄段后退出

            print(f"✅ Processed: {xml_file} (Age: {age_months} months)")
        except Exception as e:
            print(f"⚠️ Error processing {xml_file}: {e}")

    # 写入不同年龄段的文件
    os.makedirs(output_directory, exist_ok=True)
    for category, texts in categorized_data.items():
        output_file = os.path.join(output_directory, f"childes_{category}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(texts)
        print(f"📁 Saved {len(texts)} records to {output_file}")

    print("🎉 All XML files processed and categorized!")

# 设置 CHILDES 数据集路径
corpus_directory = "Desktop/data/CHILDES_xml/"  
output_directory = "Desktop/data/processed_childes_by_age/"  # 输出目录

process_all_xml_files(corpus_directory, output_directory)