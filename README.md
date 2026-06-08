# ⚽ Football Tactical AI

An AI-powered football match analyzer that detects players from video, analyzes team tactics, and generates counter-strategies using Computer Vision and a Large Language Model.

## 🎯 What It Does

Football Tactical AI combines two AI domains into one pipeline:

1. **Computer Vision** detects and tracks players, identifies teams, and analyzes formations
2. **Large Language Model** generates tactical counter-strategies based on the detected setup

The result: feed in match data, get back coaching-style recommendations on how to beat the opponent.

## 🧠 How It Works

\\\
Video Input
    |
    v
[1] Detection (YOLOv8)        -> finds players & ball
    |
    v
[2] Tracking (ByteTrack)      -> assigns IDs, follows players across frames
    |
    v
[3] Team Classification       -> K-means on jersey colors splits into 2 teams
    |
    v
[4] Tactical Analysis         -> computes formation, possession, attack side
    |
    v
[5] Strategy Generation (LLM) -> TinyLlama generates counter-strategy
    |
    v
[6] Report Output             -> saves a tactical analysis report
\\\

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Object Detection | YOLOv8 (Ultralytics) |
| Multi-Object Tracking | ByteTrack (Supervision) |
| Team Classification | K-means (scikit-learn) |
| Strategy Generation | TinyLlama (Hugging Face, runs locally) |
| Video Processing | OpenCV |
| Language | Python 3.10+ |

## 🚀 Getting Started

### Installation

\\\ash
# Clone the repository
git clone https://github.com/philipmk42/football-tactical-ai.git
cd football-tactical-ai

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
\\\

### Usage

\\\ash
# Run in demo mode (no video required)
python main.py --demo

# Run on a real match video
python main.py --video data/input_videos/match.mp4
\\\

## 📊 Sample Output

Given an opponent playing a **4-3-3 formation with 64% possession**, attacking through the right wing, the system generates:

\\\
RECOMMENDED COUNTER-STRATEGY

1. Defensive Block: Organize defenders in a compact shape to deny
   space in the final third and force long balls.

2. Pressure: Press the opposition midfield and use counter-pressing
   to win the ball back quickly.

3. Advanced Passing: Use long balls to the flanks and through the
   center to create chances for forwards.

4. Counter-Attacking: Exploit the opponent's high possession by
   breaking quickly through their defensive line.
\\\

Full reports are saved to \data/reports/\.

## 📁 Project Structure

\\\
football-tactical-ai/
├── detection/          # YOLO object detection
├── trackers/           # Multi-object tracking (ByteTrack)
├── team_assigner/      # Team classification (K-means)
├── analysis/           # Tactical analysis (formation, possession)
├── strategy/           # LLM-based strategy generation
├── reporting/          # Report file generation
├── utils/              # Video utilities
├── models/             # YOLO model weights
├── data/               # Input videos & output reports
├── main.py             # Pipeline entry point
└── requirements.txt    # Dependencies
\\\

## 🎓 Key Engineering Decisions

- **Local LLM (TinyLlama)**: Runs fully offline with no API keys or costs, optimized for CPU inference on standard hardware.
- **Modular pipeline**: Each stage (detection, tracking, analysis, strategy) is an independent, testable module.
- **Caching**: Detection results are cached to avoid reprocessing during development.

## 🔮 Future Improvements

- [ ] Custom YOLO model trained specifically on football footage
- [ ] RAG integration to ground strategies in a real tactics database
- [ ] Annotated video output with player overlays
- [ ] Web interface for uploading and analyzing matches

## 👤 Author

**Philip M K**
GitHub: [@philipmk42](https://github.com/philipmk42)
