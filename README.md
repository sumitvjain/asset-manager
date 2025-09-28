# 🎬 Asset Manager

A Python-based **Asset Manager** designed for VFX/Animation pipelines.  
It provides a simple interface to browse, organize, and preview assets such as images, sequences, and videos.  

The project uses **PySide2 (Qt for Python)** for the UI and supports customizable project configurations via JSON.

---

## 🚀 Features
- 📂 Drag-and-drop support for files and folders  
- 🖼️ Thumbnail previews of supported media files (`exr`, `jpg`, `jpeg`, `png`, `mov`)  
- 📑 Project-based extension filtering (customizable per project)  
- ⚡ Zoom in/out functionality on the preview tab  
- 🔄 Undo/Redo, Copy/Paste, and Remove asset actions  
- ⚙️ Preferences dialog to update project configurations  
- 📝 Config file auto-generated on first launch  

---

## 📦 Requirements
- Python **3.8+**  
- [PySide2](https://pypi.org/project/PySide2/)  
- [platformdirs](https://pypi.org/project/platformdirs/)  

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Setup
When first run, the application will:
1. Create a hidden directory inside your **Documents folder** (`~/.app/`)  
2. Generate a default `config.json` file with 10 sample projects  

---

## ▶️ Run the App
```bash
python main.py
```

---

## 📝 Example: Default Config File (`config.json`)
```json
{
    "proj_01": {
        "name": "Project_01",
        "extension": {
            "exr": false,
            "jpeg": true,
            "jpg": true,
            "png": false,
            "mov": false
        }
    },
    "proj_02": {
        "name": "Project_02",
        "extension": {
            "exr": false,
            "jpeg": true,
            "jpg": true,
            "png": false,
            "mov": false
        }
    }
}
```

---

## 📂 Project Structure
```
asset-manager/
│── config/
│   ├── constant.py        # Centralized constants
│   ├── setup_config.py    # Ensures config.json exists
│
│── model/                 # Data and logic layer
│── view/                  # UI layer (PySide2 widgets)
│── controller/            # Business logic and signal-slot connections
│
│── style.qss              # UI styling
│── main.py                # Entry point
│── requirements.txt
│── README.md
```

---

## 🖥️ Example Workflow
1. Launch the app → it creates the default config at `~/Documents/.app/config.json`  
2. Drag and drop a folder with assets into the UI  
3. The **Tree widget** displays the folder structure → click an item to view thumbnails  
4. Right-click thumbnails to access options:  
   - **Load in Viewer**  
   - **Compare** (two items)  
   - **Remove**  

---

## 👨‍💻 Author
**Sumit Saktepar**  
Pipeline TD / Python Developer  
