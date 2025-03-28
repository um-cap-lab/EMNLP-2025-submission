import xml.etree.ElementTree as ET
import os
import glob

def parse_chat_xml(xml_file):
    """parse the XML file and extract the conversation"""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # get the age of the child
    child = root.find(".//{http://www.talkbank.org/ns/talkbank}participant[@role='Target_Child']")
    age = child.get("age") if child is not None else "Unknown"

    output = [f"Child Age: {age}\n"]  # only keep the age of the child

    # get the conversation
    for utterance in root.findall(".//{http://www.talkbank.org/ns/talkbank}u"):
        speaker = utterance.get("who")  # speaker (CHI & MOT)
        words = [w.text for w in utterance.findall(".//{http://www.talkbank.org/ns/talkbank}w") if w.text]
        if words:
            output.append(f"{speaker}: {' '.join(words)}")

    return "\n".join(output) + "\n\n"  #make sure each conversation is separated by a new line

def process_all_xml_files(directory, output_file):
    """recursive process all XML files in the directory"""
    xml_files = glob.glob(os.path.join(directory, "**/*.xml"), recursive=True)

    print(f"🔍 Found {len(xml_files)} XML files. Processing...")

    with open(output_file, "w", encoding="utf-8") as f:
        for xml_file in xml_files:
            try:
                result = parse_chat_xml(xml_file)
                f.write(result)
                print(f"✅ Processed: {xml_file}")
            except Exception as e:
                print(f"⚠️ Error processing {xml_file}: {e}")

    print(f"🎉 All XML files processed! Output saved to: {output_file}")

# path to CHILDES data index(can process all the xml files)
corpus_directory = "Desktop/data/CHILDES_xml/"  
output_file = "Desktop/data/processed_childes_data.txt"  # all the processed data will be saved in this file

process_all_xml_files(corpus_directory, output_file)