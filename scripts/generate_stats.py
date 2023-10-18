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
    game_statistics = {game: {'total_resources': 0, 'correct_paths': 0} for game in GAME_FLAGS}

    for json_file in json_files:
        file_type = os.path.basename(json_file).split('.')[0]
        with open(json_file, 'r') as f:
            data = json.load(f)
            for entry in data:
                for game, flag in GAME_FLAGS.items():
                    if entry['gameFlags'] & flag:
                        game_statistics[game]['total_resources'] += 1
                        if entry['hash'] == ioi_hash(entry['path']):
                            game_statistics[game]['correct_paths'] += 1
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
    resources_badge_url = generate_badge_url("Total Resources", f"{total_resources_all:,}", "blue")

    game_badge_urls = {}
    for game, stats in game_statistics.items():
        total_game_resources = stats['total_resources']
        total_game_correct = stats['correct_paths']
        game_completion_percentage = (total_game_correct / total_game_resources) * 100 if total_game_resources else 0
        colour = total_completion_colour(game_completion_percentage)
        game_badge_url = generate_badge_url(f"{game.capitalize()} Completion", f"{game_completion_percentage:.2f}%25", colour)
        game_badge_urls[game] = game_badge_url

    return writer.dumps(), completion_badge_url, resources_badge_url, game_badge_urls

def add_to_readme(start_marker, end_marker, addition_str):
    with open("README.md", "r") as f:
        content = f.read()

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index != -1 and end_index != -1:
        before_section = content[:start_index + len(start_marker)]
        after_section = content[end_index:]
        content = before_section + "\n" + addition_str + after_section

    with open("README.md", "w", newline="\n") as f:
        f.write(content)

def add_statistics_table_to_readme(statistics_table):
    add_to_readme("<!-- STATISTICS_TABLE_START -->", "<!-- STATISTICS_TABLE_END -->", statistics_table)

def add_badges_to_readme(badges_md):
    badges_str = "\n".join(badges_md) + "\n"
    add_to_readme("<!-- BADGES_START -->", "<!-- BADGES_END -->", badges_str)

statistics_table, completion_badge_url, resources_badges_url, game_badge_urls = generate_statistics_table()

badges_md = [
    f"![Resources Badge]({resources_badges_url})",
    f"![Completion Badge]({completion_badge_url})"
]

for game, badge_url in game_badge_urls.items():
    badges_md.append(f"![{game.capitalize()} Badge]({badge_url})")

add_badges_to_readme(badges_md)
add_statistics_table_to_readme(statistics_table)
