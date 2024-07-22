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

### Usage

Before using be sure to install dependencies following the `Installation` section.

To run the app, you can use `start-app-script.bat`

You can add as many roadmaps as you want. To add a roadmap on a subject `Subject`:

1. create folder `Subject` in the main directory,
2. create empty file `graph.txt` in the newly created `Subject` folder,
3. generate the graph by using prompt from `graph-template.md`,
4. place the graph into `graph.txt` file
5. run the app or refresh page to make the app generate the `progress.json`

If you want to remove a roadmap on `Subject`, just remove the `Subject` folder.

### Installation

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

# Roadmap generation prompt:

Here is prompt for roadmap generation. I highly recommend Claude-3.5-Sonnet on https://claude.ai/ or ChatGPT-4o-Classic on https://chatgpt.com/g/g-YyyyMT9XH-chatgpt-classic.

"""
# Context:
Here is format template:
# Template:
## Basic structure:
```
digraph SubjectName {
    rankdir=TB;
    node [shape=box, style="rounded,filled", color=black, fontname="Helvetica", fontsize=10, penwidth=2, width=2, height=0.5];
    edge [color=gray, arrowhead=open];
    // Node definitions and relationships will go here
}
```
## Graph Structure Examples:
### Linear Progression:
```
Topic1 -> Topic2;
Topic2 -> Topic3;
Topic3 -> Topic4;
```
### Branching Paths:
```
RootTopic -> Branch1Topic1;
RootTopic -> Branch2Topic1;
Branch1Topic1 -> Branch1Topic2;
Branch2Topic1 -> Branch2Topic2;
```
### Converging Paths:
```
Topic1 -> Topic3;
Topic2 -> Topic3;
Topic3 -> Topic4;
```
# Topics list:
```
Introduction to Linear Modeling in Python
Statistical Thinking in Python (Part 1)
Statistical Thinking in Python (Part 2)
A/B Testing in Python
Foundations of Inference in Python
Generalized Linear Models in Python
Statistical Simulation in Python
Monte Carlo Simulations in Python
Case Studies in Statistical Thinking
Discrete Event Simulation in Python
Performing Experiments in Python
Practicing Statistics Interview Questions in Python
``
# Task:
I want to learn about statistics from `Topics list`. Generate learning dependency graph in DOT language using described format template. Maximize concurrency without violating dependencies. Never use quotation marks. Use floors ("_") instead of spaces (" "). Lets 1. understand task and mental contrast potential issues, 2. make detailed to-do list, 3. devise detailed plan to complete task. Then lets take deep breath, carry out plan, and do task step-by-step.
"""