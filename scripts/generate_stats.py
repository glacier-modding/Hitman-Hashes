import json
import os
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style
from common_functions import *

def generate_statistics_table():
    input_directory = "paths"
    json_files = [os.path.join(input_directory, f) for f in sorted(os.listdir(input_directory)) if f.endswith(".json")]

    statistics = {}

    for json_file in json_files:
        file_type = os.path.basename(json_file).split('.')[0]
        with open(json_file, 'r') as f:
            data = json.load(f)
            total_resources = len(data)
            correct_paths = sum(1 for entry in data if entry['hash'] == ioi_hash(entry['path']))

            if file_type in statistics:
                total_resources += statistics[file_type]['total_resources']
                correct_paths += statistics[file_type]['correct_paths']

            statistics[file_type] = {
                'total_resources': total_resources,
                'correct_paths': correct_paths,
                'correct_percentage': (correct_paths / total_resources) * 100
            }

    value_matrix = []
    for file_type, stats in statistics.items():
        row = [
            file_type, 
            stats['total_resources'], 
            stats['correct_paths'], 
            f"{stats['correct_percentage']:.2f}%"
        ]
        value_matrix.append(row)

    writer = MarkdownTableWriter(
        table_name = "Statistics",
        headers = ["File Type", "Total Resources", "Correct Paths", "Correct Percentage"],
        value_matrix=value_matrix,
        column_styles = [
            Style(align="left"),
            Style(align="left"),
            Style(align="left"),
            Style(align="left"),
        ]
    )

    return writer.dumps()

statistics_table = generate_statistics_table()

with open("STATISTICS.md", "w", newline='\n') as f:
    f.write(statistics_table)
