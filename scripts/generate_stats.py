import json
import os
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style
from common_functions import *

def generate_badge_url(label, value, colour):
    label = label.replace(" ", "%20")
    return f"https://img.shields.io/badge/{label}-{value}-{colour}.svg"

def total_completion_colour(percentage):
    if percentage >= 90:
        return "green"
    elif 70 <= percentage < 90:
        return "yellow"
    else:
        return "red"

def generate_statistics_table():
    input_directory = "paths"
    json_files = [os.path.join(input_directory, f) for f in sorted(os.listdir(input_directory)) if f.endswith(".json")]

    statistics = {}
    total_resources_all = 0
    total_correct_all = 0

    for json_file in json_files:
        file_type = os.path.basename(json_file).split('.')[0]
        with open(json_file, 'r') as f:
            data = json.load(f)
            total_resources = len(data)
            correct_paths = sum(1 for entry in data if entry['hash'] == ioi_hash(entry['path']))
            hints = sum(1 for entry in data if entry.get('hint') and entry['hint'] != "")
            if file_type in statistics:
                total_resources += statistics[file_type]['total_resources']
                correct_paths += statistics[file_type]['correct_paths']
                hints += statistics[file_type]['hints']
            statistics[file_type] = {
                'total_resources': total_resources,
                'correct_paths': correct_paths,
                'correct_percentage': (correct_paths / total_resources) * 100,
                'hints': hints,
                'hint_percentage': (hints / total_resources) * 100
            }
            
            total_resources_all += total_resources
            total_correct_all += correct_paths

    value_matrix = []
    for file_type, stats in statistics.items():
        row = [
            file_type,
            stats['total_resources'],
            stats['correct_paths'],
            f"{stats['correct_percentage']:.2f}%",
            stats['hints'],
            f"{stats['hint_percentage']:.2f}%"
        ]
        value_matrix.append(row)

    writer = MarkdownTableWriter(
        headers = ["File Type", "Total Resources", "Correct Paths", "Correct Percentage", "Hints", "Hint Percentage"],
        value_matrix=value_matrix,
        column_styles = [
            Style(align="left"),
            Style(align="left"),
            Style(align="left"),
            Style(align="left"),
            Style(align="left"),
            Style(align="left")
        ]
    )
    
    total_completion_percentage = (total_correct_all / total_resources_all) * 100
    colour = total_completion_colour(total_completion_percentage)
    completion_badge_url = generate_badge_url("Total Completion", f"{total_completion_percentage:.2f}%25", colour)
    resources_badges_url = generate_badge_url("Total Resources", f"{total_resources_all:,}", "blue")

    return writer.dumps(), completion_badge_url, resources_badges_url

statistics_table, completion_badge_url, resources_badges_url = generate_statistics_table()

def add_statistics_table_to_readme(statistics_table):
    start_marker = "<!-- STATISTICS_TABLE_START -->"
    end_marker = "<!-- STATISTICS_TABLE_END -->"

    with open("README.md", "r") as f:
        content = f.read()

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index != -1 and end_index != -1:
        before_table = content[:start_index + len(start_marker)]
        after_table = content[end_index:]
        content = before_table + "\n" + statistics_table + after_table

    with open("README.md", "w") as f:
        f.write(content)


add_statistics_table_to_readme(statistics_table)

def add_badge_to_readme(badge_md):
    start_marker = "<!-- BADGES_START -->"
    end_marker = "<!-- BADGES_END -->"

    with open("README.md", "r") as f:
        content = f.read()

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    badges_str = "\n".join(badges_md)

    if start_index != -1 and end_index != -1:
        before_badge = content[:start_index + len(start_marker)]
        after_badge = content[end_index:]
        content = before_badge + "\n" + badges_str + "\n" + after_badge

    with open("README.md", "w") as f:
        f.write(content)

badges_md = [
    f"![Resources Badge]({resources_badges_url})",
    f"![Completion Badge]({completion_badge_url})"
]

add_badge_to_readme(badges_md)
