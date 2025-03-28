import xml.etree.ElementTree as ET
import os
import glob
import re

# only remain 3 age groups
AGE_BUCKETS = {
    "0-15months": (0, 15),
    "15-20months": (15, 20),
    "20-60months": (20, 60)  # > 20 month will be 5 yr
}

def parse_age(age_str):
    """convert CHILDES format（P1Y08M）to months（20 months）"""
    match = re.match(r"P(\d+)Y(\d+)M", age_str)
    if match:
        years, months = int(match.group(1)), int(match.group(2))
        return years * 12 + months  # to months
    return None  # deal with non-num

def parse_chat_xml(xml_file):
    """anlysis individual XML file，get the age and conversation"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # get the age
    child = root.find(".//{http://www.talkbank.org/ns/talkbank}participant[@role='Target_Child']")
    age_str = child.get("age") if child is not None else None
    age_months = parse_age(age_str) if age_str else None

    if age_months is None:
        return None, None  # skip

    output = []

    # get conver
    for utterance in root.findall(".//{http://www.talkbank.org/ns/talkbank}u"):
        speaker = utterance.get("who")  #  (CHI / MOT)
        words = [w.text for w in utterance.findall(".//{http://www.talkbank.org/ns/talkbank}w") if w.text]
        if words:
            output.append(f"{speaker}: {' '.join(words)}")

    return age_months, "\n".join(output) + "\n\n"

def process_all_xml_files(directory, output_directory):
    """deal with all xml"""
    xml_files = glob.glob(os.path.join(directory, "**/*.xml"), recursive=True)
    categorized_data = {key: [] for key in AGE_BUCKETS}  # store in different ge group

    print(f"🔍 Found {len(xml_files)} XML files. Processing...")

    for xml_file in xml_files:
        try:
            age_months, text = parse_chat_xml(xml_file)
            if age_months is None or text is None:
                continue  # skip 

            # decide age group
            for category, (min_age, max_age) in AGE_BUCKETS.items():
                if min_age <= age_months < max_age:
                    categorized_data[category].append(text)
                    break  # get the age and exit

            print(f"✅ Processed: {xml_file} (Age: {age_months} months)")
        except Exception as e:
            print(f"⚠️ Error processing {xml_file}: {e}")

    # write in different age group 
    os.makedirs(output_directory, exist_ok=True)
    for category, texts in categorized_data.items():
        output_file = os.path.join(output_directory, f"childes_{category}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(texts)
        print(f"📁 Saved {len(texts)} records to {output_file}")

    print("🎉 All XML files processed and categorized!")

# set CHILDES data set
corpus_directory = "Desktop/data/CHILDES_xml/"  
output_directory = "Desktop/data/processed_childes_by_age/"  # out put

process_all_xml_files(corpus_directory, output_directory)
