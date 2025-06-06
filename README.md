# ASCII_Arms
**ASCII Arms** is a modular CLI based damage simulation system, built with Python. 
It simulates interactions between game entities, items, and spells using customizable data from JSON configuration files. 
This tool is useful for prototyping game mechanics, balancing combat systems, or serving as a backend module in larger game engines.

---

## 🛠 Requirements
- Python 3.13 or higher
- Git (optional, if cloning the repo)

## 💻 Installation

1. **Clone repository**
   ```bash
   git clone <repository-url>
   ```
   ```bash
   cd ASCII_Arms
   ```
2. **Create virtual environment (recommended)**
   ```bash
    python -m venv .venv
   ```
   **Windows**
   ```bash
   .\.venv\Scripts\Activate.bat
   ```
   **Mac OS / Linux**
   ```bash
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   python -m pip install .
   ```
4. **Run game**
   
   _RUN GAME AS MODULE:_ **-m**

   **Windows**
   ```bash
   Use run.bat
   ```

   **Terminal**
   ```bash
   python -m src.ascii_arms.main
   ```