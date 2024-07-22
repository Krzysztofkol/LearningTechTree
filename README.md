# LearningTechTree

Simple web app for learning roadmaps, inspired by Learney.me and World of Tanks' tech tree.

### Folder structure:
```
LearningTechTree/
├── subjects/
│   ├── Deep Learning/
│   │   ├── graph.txt
│   │   └── progress.json
│   ├── Discrete Mathematics/
│   │   ├── graph.txt
│   │   └── progress.json
│   └── Large Language Models/
│       ├── graph.txt
│       └── progress.json
├── static/
│   ├── Large Language Models_graph.map
│   ├── Large Language Models_graph.png
│   ├── Discrete Mathematics_graph.png
│   ├── graph.map
│   ├── graph.png
│   ├── Deep Learning_graph.png
│   ├── Discrete Mathematics_graph.map
│   └── Deep Learning_graph.map
├── backend.py
├── frontend.html
├── graph-template.md
├── requirements.txt
├── README.md
└── start-app-script.bat
```

### Dependencies

Be sure to install packages from `requirements.txt` file. Navigate to the directory in command line and run:

```
pip install requirements.txt -r
```

You need to have installed the following programs:
- Microsoft Visual C++ 14.0 or greater: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#latest-microsoft-visual-c-redistributable-version
- graphviz: https://graphviz.org/download/

You also need to confirm graphviz installation and set environment variables (preferably system variables instead of user variables):

1. **Check Graphviz Installation**:
    - Open Command Prompt and check if Graphviz is installed:
      ```sh
      dot -version
      ```
    - If Graphviz is not installed, download and install it from [Graphviz Download](https://graphviz.org/download/).

2. **Set Environment Variables**:
    - Open Environment Variables settings.
    - Add the Graphviz `bin` directory to `PATH`:
      - Example: `C:\Program Files\Graphviz\bin`.
    - Set `INCLUDE` and `LIB` variables to point to Graphviz directories:
      - Example `INCLUDE`: `C:\Program Files\Graphviz\include`.
      - Example `LIB`: `C:\Program Files\Graphviz\lib`.
	- Add Microsoft Visual C++ 14.0 or greater directory to `PATH`: 
      - Example: `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\14.40.33807\bin\HostX86\x64\cl.exe`.

3. **Re-attempt Pygraphviz Installation**:
    - Open a new Command Prompt.
    - Run:
      ```sh
      pip install pygraphviz
      ```