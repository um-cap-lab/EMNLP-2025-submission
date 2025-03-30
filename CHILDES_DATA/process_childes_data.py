# -*- coding: utf-8 -*-
# File   : preprocess_childes_data.py
# Date   : 2021-06-02

import os
import re
from nltk.corpus.reader.childes import CHILDESCorpusReader

def preprocess_childes_data(corpus_dir, output_dir):
    """
    Preprocess CHILDES data for filler-gap dependency study.
    """
    # Initialize CHILDESCorpusReader
    reader = CHILDESCorpusReader(corpus_dir, '.*.xml')

    # Iterate through files in the corpus
    for fileids in reader.fileids():
        # Extract utterances
        utterances = reader.utterances(fileids)
        processed_utterances = []

        for utterance in utterances:
            speaker = utterance['speaker']
            text = utterance['utterance']

            # Filter non-linguistic content
            text = re.sub(r'\[.*?\]', '', text)  # Remove annotations like [laughter], [noise]

            # Normalize punctuation and spacing
            text = re.sub(r'\s+', ' ', text.strip())
            text = text.replace("n't", " n’t")  # Preserve contractions

            # Filter by speaker (Target_Child and Mother)
            if speaker in ['Target_Child', 'Mother', 'Father']:
                processed_utterances.append(text)

        # Save processed utterances to output directory
        output_file = os.path.join(output_dir, f"{os.path.splitext(fileid)[0]}_processed.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(processed_utterances))

# Example usage
corpus_directory = "desktop/data/CHILDES_xml"
output_directory = "desktop/data/CHILDES_processed"
os.makedirs(output_directory, exist_ok=True)
preprocess_childes_data(corpus_directory, output_directory)
