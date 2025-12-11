# Connect Four Artificial Intelligence  
_A powerful AI-driven Connect Four implementation using Minimax, Alpha-Beta Pruning, and heuristic evaluation._

---

## What is Connect Four?

Connect Four (or *Four in a Line*) is a **two-player, perfect-information, zero-sum adversarial game**.

That means:

- The entire state of the game is visible at all times.  
- No randomness is involved.  
- One player’s advantage is exactly the opponent’s disadvantage.

The classic board contains **6 rows × 7 columns**, and the total number of possible states exceeds **4.5 trillion**.

### Rules  
Players alternate dropping pieces into columns.  
A piece always occupies the **lowest available position** in the chosen column.  
The first to connect **four pieces** in a line — horizontal, vertical, or diagonal — wins.

---

## How does this code work?

This project implements an **Intelligent Agent** capable of playing Connect Four at 3 difficulty levels:

| Level | Algorithm | Depth | Extras |
|-------|-----------|--------|--------|
| **Beginner** | Minimax | 2–3 | Simple heuristics |
| **Intermediate** | Minimax + Alpha-Beta | 4–5 | Intermediate heuristics |
| **Professional** | Alpha-Beta + Move Ordering + Time Limit | Dynamic (≈3s per move) | Advanced heuristics |

The agent explores possible future states recursively and selects the move with the best expected outcome.

---

## Project Structure

```
connect_four_ai/
│
├── GameObject/
│ ├── board.py → Board logic (moves, wins, validation)
│ └── agent.py → Decision interface for AI
│
├── SearchEngine/
│ ├── minimax.py → Basic minimax
│ └── alphabeta.py → Optimized minimax with pruning
│
├── Heuristic/
│ ├── basic.py → Beginner-level heuristic
│ ├── intermediate.py → Weighted pattern heuristic
│ └── advanced.py → Professional-level evaluation
│
├── Utils/
│ ├── utils.py → Constants and helper utilities
│ └── evaluator.py → Unified evaluation function
│
├── Interface/
│ └── render.py → Tkinter GUI
│
├── main.py → Terminal game
└── main_gui.py → Graphical game entry point

```

## Module Overview

### **1. GameObject/**
Responsible for the game's core mechanics.

- **board.py**
  - Creates and manages the board  
  - Detects wins and terminal states  
  - Applies and undoes moves  

- **agent.py**
  - Connects board logic with search algorithms  
  - Selects moves based on difficulty level  

---

### **2. SearchEngine/**
Implements decision-making algorithms.

- **minimax.py**  
  Basic minimax search — used in beginner mode.

- **alphabeta.py**  
  Minimax with alpha-beta pruning and:
  - Move ordering  
  - Time control  
  - Early cutoffs when branches become irrelevant  

---

### **3. Heuristic/**
Board evaluation functions used by the AI.

- **basic.py**  
  Simple priority on center-column and possible 3-in-a-rows.

- **intermediate.py**  
  Recognizes open patterns, weighted sequences, near-wins.

- **advanced.py**  
  Professional-level evaluation including:
  - Threat detection  
  - Fork creation  
  - Opponent blocking  
  - Centrality weighting  

---

### **4. Utils/**
General-purpose helper components.

- **utils.py**  
  Stores constants (e.g., `PLAYER_PIECE`, `AI_PIECE`).

- **evaluator.py**  
  Abstracts which heuristic to call for each difficulty level.

---

### **5. Interface /**
Tkinter graphical interface.

- **render.py**
  - Renders the board  
  - Handles mouse events  
  - Updates pieces and animations  
  - Displays end-game messages  
  - Calls the AI engine for moves  

---

### **6. main.py and main_gui.py**

- **main.py** → Text/terminal version  
- **main_gui.py** → Tkinter graphical version

---

## How to Run

### Terminal Version
```bash
python main.py
```

## Debug Info

The engine outputs:

- Chosen move
- Evaluation score
- Time spent per move
- Early cutoffs
- Terminal detections

