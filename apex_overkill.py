# ApexKill Compilation GUI (PyQt6 - YoinxLab Style)
import json
import os
import subprocess
import glob
from datetime import datetime
from collections import defaultdict
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QSpinBox, QHBoxLayout, QFileDialog, QMessageBox, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
import sys

KILL_DATA_DIR = './json/updated_kills'


def load_all_kills():
    kills = []
    for path in glob.glob(os.path.join(KILL_DATA_DIR, '*.json')):
        with open(path, 'r') as f:
            kills.extend(json.load(f))
    return kills


def extract_clip_metadata(kills):
    clips = defaultdict(lambda: {
        'game_type': '',
        'character': '',
        'date': None,
        'kill_count': 0
    })
    for kill in kills:
        path = kill['video_path']
        clips[path]['kill_count'] += 1
        clips[path]['game_type'] = kill['game_type']
        clips[path]['character'] = kill['character_name']
        if not clips[path]['date']:
            try:
                filename = os.path.basename(path)
                date_part = filename.replace('Marvel Rivals_', '').replace('.mp4', '')
                clips[path]['date'] = datetime.strptime(date_part, '%m-%d-%Y_%H-%M-%S-%f')
            except:
                clips[path]['date'] = datetime.min
    return clips


def compile_videos(clips):
    with open('clips_to_merge.txt', 'w') as f:
        for clip in clips:
            f.write(f"file '{clip.replace('\\', '/')}" + "'\n")
    output_path, _ = QFileDialog.getSaveFileName(None, "Save Compilation", '', "MP4 Files (*.mp4)")
    if output_path:
        subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'clips_to_merge.txt', '-c', 'copy', output_path])
        QMessageBox.information(None, 'Success', f'Compilation created at:\n{output_path}')
    os.remove('clips_to_merge.txt')

def run_all_scripts():
    subprocess.run([sys.executable, 'run_all_scripts.py'])


class FilterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Highlight Compilation Filters")
        self.setStyleSheet("background-color: #111; color: #eee; font-size: 14px;")
        layout = QVBoxLayout()

        kills = load_all_kills()
        self.summary = extract_clip_metadata(kills)
        self.clips = []

        self.game_type_box = QComboBox()
        self.character_box = QComboBox()
        self.min_kills = QSpinBox()
        self.max_kills = QSpinBox()
        self.date_min = QDateTimeEdit()
        self.date_max = QDateTimeEdit()

        game_types = sorted(set(v['game_type'] for v in self.summary.values()))
        characters = sorted(set(v['character'] for v in self.summary.values()))
        kill_counts = sorted(set(v['kill_count'] for v in self.summary.values()))

        self.min_kills.setRange(min(kill_counts), max(kill_counts))
        self.max_kills.setRange(min(kill_counts), max(kill_counts))
        self.min_kills.setValue(min(kill_counts))
        self.max_kills.setValue(max(kill_counts))

        self.date_min.setDisplayFormat("MM/dd/yyyy HH:mm")
        self.date_max.setDisplayFormat("MM/dd/yyyy HH:mm")
        self.date_min.setCalendarPopup(True)
        self.date_max.setCalendarPopup(True)
        self.date_min.setDateTime(QDateTime.currentDateTime().addDays(-30))
        self.date_max.setDateTime(QDateTime.currentDateTime())

        self.game_type_box.addItems(game_types)
        self.character_box.addItems(characters)

        layout.addWidget(QLabel("Select Game Type:"))
        layout.addWidget(self.game_type_box)
        layout.addWidget(QLabel("Select Character:"))
        layout.addWidget(self.character_box)

        row = QHBoxLayout()
        row.addWidget(QLabel("Min Kills:"))
        row.addWidget(self.min_kills)
        row.addWidget(QLabel("Max Kills:"))
        row.addWidget(self.max_kills)
        layout.addLayout(row)

        layout.addWidget(QLabel("Earliest Video Date:"))
        layout.addWidget(self.date_min)
        layout.addWidget(QLabel("Latest Video Date:"))
        layout.addWidget(self.date_max)

        compile_button = QPushButton("Create Compilation")
        compile_button.clicked.connect(self.filter_and_compile)
        compile_button.setStyleSheet("padding: 10px; font-weight: bold; background-color: #222; border: 1px solid #444")
        layout.addWidget(compile_button)

        self.feedback_label = QLabel("Clips: 0 | Estimated Length: 0s")
        self.feedback_label.setStyleSheet("margin-top: 15px; font-weight: bold; color: #aaa;")
        layout.addWidget(self.feedback_label)

        self.setLayout(layout)
        self.resize(600, 350)
        self.attach_live_feedback_handlers()
        self.update_feedback()

    def update_feedback(self):
        selected_game_type = self.game_type_box.currentText()
        selected_character = self.character_box.currentText()
        min_k = self.min_kills.value()
        max_k = self.max_kills.value()
        dt_min = self.date_min.dateTime().toPyDateTime()
        dt_max = self.date_max.dateTime().toPyDateTime()

        filtered = [k for k, v in self.summary.items() if (
            v['game_type'] == selected_game_type and
            v['character'] == selected_character and
            min_k <= v['kill_count'] <= max_k and
            dt_min <= v['date'] <= dt_max)]

        total_seconds = len(filtered) * 15  # assuming each clip is ~15s
        self.feedback_label.setText(f"Clips: {len(filtered)} | Estimated Length: {total_seconds} seconds")

    def attach_live_feedback_handlers(self):
        self.game_type_box.currentTextChanged.connect(self.update_feedback)
        self.character_box.currentTextChanged.connect(self.update_feedback)
        self.min_kills.valueChanged.connect(self.update_feedback)
        self.max_kills.valueChanged.connect(self.update_feedback)
        self.date_min.dateTimeChanged.connect(self.update_feedback)
        self.date_max.dateTimeChanged.connect(self.update_feedback)

    def filter_and_compile(self):
        selected_game_type = self.game_type_box.currentText()
        selected_character = self.character_box.currentText()
        min_k = self.min_kills.value()
        max_k = self.max_kills.value()
        dt_min = self.date_min.dateTime().toPyDateTime()
        dt_max = self.date_max.dateTime().toPyDateTime()

        filtered = [k for k, v in self.summary.items() if (
            v['game_type'] == selected_game_type and
            v['character'] == selected_character and
            min_k <= v['kill_count'] <= max_k and
            dt_min <= v['date'] <= dt_max)]

        if not filtered:
            QMessageBox.warning(self, "No Clips", "No clips match the selected filters.")
            return

        compile_videos(filtered)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ApexKill Highlight Manager")
        self.setStyleSheet("background-color: #0f0f0f; color: #ffffff; font-size: 16px;")
        central = QWidget()
        layout = QVBoxLayout()

        title = QLabel("ApexKill Compilation Creator")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet("margin: 20px auto; text-align: center;")
        layout.addWidget(title)

        btn1 = QPushButton("Update Data")
        btn1.clicked.connect(run_all_scripts)
        btn2 = QPushButton("Create Compilation")
        btn2.clicked.connect(self.open_filter_window)
        btn3 = QPushButton("Exit")
        btn3.clicked.connect(QApplication.quit)

        for btn in (btn1, btn2, btn3):
            btn.setMinimumHeight(40)
            btn.setStyleSheet("margin: 10px; background-color: #222; border: 1px solid #555")
            layout.addWidget(btn)

        central.setLayout(layout)
        self.setCentralWidget(central)
        self.resize(500, 300)

    def open_filter_window(self):
        self.filter_window = FilterWindow()
        self.filter_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
