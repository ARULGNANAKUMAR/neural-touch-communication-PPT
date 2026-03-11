import sys
import sqlite3
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg

# -------------------------
# FAST DB LOAD
# -------------------------
def load_data():
    try:
        conn = sqlite3.connect("ai_memory.db")
        df = pd.read_sql_query("SELECT * FROM samples", conn)
        conn.close()
        return df.tail(200)
    except:
        return pd.DataFrame()

# -------------------------
# ULTRA FAST UI
# -------------------------
class JarvisFast(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ JARVIS ULTRA CORE")
        self.resize(1100, 700)
        self.setStyleSheet("background-color: black; color: cyan;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        self.title = QLabel("JARVIS REAL-TIME AI CORE")
        self.title.setFont(QFont("Orbitron", 18))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Status
        self.status = QLabel("Initializing...")
        self.status.setFont(QFont("Consolas", 11))
        layout.addWidget(self.status)

        # Graph
        self.graph = pg.PlotWidget()
        self.graph.setBackground('k')
        self.graph.showGrid(x=True, y=True)
        layout.addWidget(self.graph)

        self.temp_line = self.graph.plot(pen=pg.mkPen('c', width=2))
        self.pulse_line = self.graph.plot(pen=pg.mkPen('y', width=2))
        self.reward_line = self.graph.plot(pen=pg.mkPen('m', width=2))

        # Insight
        self.insight = QLabel("AI Insight: ---")
        layout.addWidget(self.insight)

        # Timer (FAST refresh)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ai)
        self.timer.start(800)  # <--- faster refresh

        self.update_ai()

    # -------------------------
    def update_ai(self):
        df = load_data()

        if df.empty:
            self.status.setText("Collecting AI data...")
            return

        temp = df["temperature"].values
        pulse = df["pulse"].values
        reward = df["reward"].values

        self.temp_line.setData(temp)
        self.pulse_line.setData(pulse)
        self.reward_line.setData(reward)

        self.status.setText(
            f"Samples: {len(df)} | Avg Temp: {np.mean(temp):.1f}°C | Avg Pulse: {np.mean(pulse):.0f}"
        )

        # Insight logic
        trend = np.polyfit(range(len(temp)), temp, 1)[0]

        if trend > 0.05:
            msg = "⚠ Heat rising"
        elif trend < -0.05:
            msg = "❄ Cooling trend"
        else:
            msg = "Stable condition"

        self.insight.setText("AI Insight: " + msg)

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = JarvisFast()
    ui.show()
    sys.exit(app.exec_())
