from flask import Flask, render_template, request, jsonify
import json
import os
import pygraphviz as pgv

app = Flask(__name__)

PROGRESS_FILE = 'progress.json'

if not os.path.exists('static'):
    os.makedirs('static')

DOT_SCRIPT = """
digraph DeepLearningPath {
    rankdir=LR;
    node [shape=box, style="rounded,filled", color=black, fillcolor=lightblue2, fontname="Helvetica", fontsize=12, penwidth=2];
    edge [color=gray, arrowhead=open];
    BasicMath [label="Basic Math (Algebra, Calculus)"];
    BasicProgramming [label="Basic Programming (Python)"];
    LinearAlgebra [label="Linear Algebra"];
    ProbabilityStatistics [label="Probability & Statistics"];
    DataStructures [label="Data Structures"];
    Algorithms [label="Algorithms"];
    NumericalComputing [label="Numerical Computing (Numpy)"];
    DataPreprocessing [label="Data Preprocessing"];
    MLBasics [label="Machine Learning Basics"];
    NeuralNetworks [label="Neural Networks"];
    DeepLearningFrameworks [label="Deep Learning Frameworks (TensorFlow, PyTorch)"];
    CNNs [label="Convolutional Neural Networks (CNNs)"];
    RNNs [label="Recurrent Neural Networks (RNNs)"];
    GANs [label="Generative Adversarial Networks (GANs)"];
    RL [label="Reinforcement Learning"];
    NLP [label="Natural Language Processing (NLP)"];
    AdvancedDL [label="Advanced Deep Learning Topics"];
    ModelDeployment [label="Model Deployment"];
    EthicsAI [label="Ethics in AI"];
    BasicMath -> LinearAlgebra;
    BasicMath -> ProbabilityStatistics;
    BasicProgramming -> DataStructures;
    BasicProgramming -> NumericalComputing;
    BasicProgramming -> DataPreprocessing;
    LinearAlgebra -> NumericalComputing;
    LinearAlgebra -> MLBasics;
    ProbabilityStatistics -> MLBasics;
    DataStructures -> Algorithms;
    Algorithms -> MLBasics;
    NumericalComputing -> MLBasics;
    MLBasics -> NeuralNetworks;
    DataPreprocessing -> NeuralNetworks;
    NeuralNetworks -> DeepLearningFrameworks;
    NeuralNetworks -> CNNs;
    NeuralNetworks -> RNNs;
    NeuralNetworks -> GANs;
    NeuralNetworks -> RL;
    NeuralNetworks -> NLP;
    DeepLearningFrameworks -> CNNs;
    DeepLearningFrameworks -> RNNs;
    DeepLearningFrameworks -> GANs;
    DeepLearningFrameworks -> RL;
    DeepLearningFrameworks -> NLP;
    CNNs -> AdvancedDL;
    RNNs -> AdvancedDL;
    GANs -> AdvancedDL;
    RL -> AdvancedDL;
    NLP -> AdvancedDL;
    AdvancedDL -> ModelDeployment;
    AdvancedDL -> EthicsAI;
    ModelDeployment -> EthicsAI;
}
"""

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

def generate_graph(progress):
    app.logger.info("Generating graph")
    graph = pgv.AGraph(string=DOT_SCRIPT)
    graph.node_attr['shape'] = 'box'
    graph.node_attr['style'] = 'rounded,filled'
    graph.node_attr['fontname'] = 'Helvetica'
    graph.node_attr['fontsize'] = '12'
    graph.node_attr['height'] = '0.5'  # Set a fixed height for nodes
    graph.node_attr['width'] = '2'     # Set a minimum width for nodes
    
    for node in graph.nodes():
        node_name = node.name
        app.logger.info(f"Processing node: {node_name}")
        if progress.get(node_name, False):
            node.attr['fillcolor'] = 'lightgreen'
        else:
            node.attr['fillcolor'] = 'lightblue2'
        node.attr['id'] = node_name
        node.attr['href'] = f'javascript:void(0);'
        node.attr['onclick'] = f'updateTopic("{node_name}");'
        
        # Calculate accurate node dimensions
        label_width = len(node.attr['label']) * 0.1  # Estimate width based on label length
        node.attr['width'] = max(2, label_width)  # Ensure minimum width of 2
        
        app.logger.info(f"Node {node_name} attributes: {node.attr}")
    
    return graph

@app.route('/')
def index():
    app.logger.info("Rendering index page")
    progress = load_progress()
    app.logger.info(f"Loaded progress: {progress}")
    graph = generate_graph(progress)
    graph_file = 'static/graph.png'
    graph.draw(graph_file, format='png', prog='dot')
    map_file = 'static/graph.map'
    graph.draw(map_file, format='cmapx', prog='dot')
    with open(map_file) as f:
        image_map = f.read()
    app.logger.info(f"Generated graph: {graph_file}")
    app.logger.info(f"Generated image map: {image_map}")
    return render_template('index.html', graph_file=f'/{graph_file}', image_map=image_map, progress=json.dumps(progress))

@app.route('/update', methods=['POST'])
def update():
    app.logger.info(f"Received update request: {request.json}")
    data = request.json
    topic = data['topic']
    completed = data['completed']
    progress = load_progress()
    progress[topic] = completed
    save_progress(progress)
    app.logger.info(f"Updated topic: {topic}, Completed: {completed}")
    app.logger.info(f"Current progress: {progress}")
    graph = generate_graph(progress)
    graph_file = 'static/graph.png'
    graph.draw(graph_file, format='png', prog='dot')
    map_file = 'static/graph.map'
    graph.draw(map_file, format='cmapx', prog='dot')
    with open(map_file) as f:
        image_map = f.read()
    app.logger.info(f"Generated updated graph: {graph_file}")
    app.logger.info(f"Generated updated image map: {image_map}")
    return jsonify(success=True, graph_file=f'/static/graph.png', image_map=image_map, progress=progress)

if __name__ == '__main__':
    app.run(debug=True, port=9696)