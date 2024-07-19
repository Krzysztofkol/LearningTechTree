import os
import re
from flask import Flask, render_template, request, jsonify
import json
import pygraphviz as pgv

app = Flask(__name__)

PROGRESS_FILE = 'progress.json'
GRAPH_FILE = 'graph.txt'

if not os.path.exists('static'):
    os.makedirs('static')

def read_graph_file():
    try:
        with open(GRAPH_FILE, 'r') as file:
            return file.read()
    except FileNotFoundError:
        app.logger.error(f"Graph file not found: {GRAPH_FILE}")
        return ""
    except IOError:
        app.logger.error(f"Error reading graph file: {GRAPH_FILE}")
        return ""

def parse_graph_file():
    graph_content = read_graph_file()
    topic_ids = re.findall(r'(\w+)\s*\[label=', graph_content)
    return topic_ids

def generate_default_progress(topic_ids):
    progress = {topic: False for topic in topic_ids}
    save_progress(progress)
    return progress

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            app.logger.error(f"Error decoding JSON from {PROGRESS_FILE}")
            return generate_default_progress(parse_graph_file())
    else:
        app.logger.info(f"{PROGRESS_FILE} not found. Creating default progress.")
        return generate_default_progress(parse_graph_file())

def save_progress(progress):
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f)
    except IOError:
        app.logger.error(f"Error writing to {PROGRESS_FILE}")

def get_direct_successors(graph, node):
    return [edge[1] for edge in graph.edges() if edge[0] == node]

def generate_graph(progress):
    app.logger.info("Generating graph")
    graph = pgv.AGraph(string=read_graph_file())
    graph.node_attr['shape'] = 'box'
    graph.node_attr['style'] = 'rounded,filled'
    graph.node_attr['fontname'] = 'Helvetica'
    graph.node_attr['fontsize'] = '10'
    graph.node_attr['height'] = '0.5'
    graph.node_attr['width'] = '2'

    # First pass: identify completed nodes and their direct successors
    completed_nodes = set()
    yellow_nodes = set()
    for node in graph.nodes():
        node_name = node.name
        if progress.get(node_name, False):
            completed_nodes.add(node_name)
            successors = get_direct_successors(graph, node)
            for successor in successors:
                if not progress.get(successor, False):
                    yellow_nodes.add(successor)

    # Second pass: color the nodes
    for node in graph.nodes():
        node_name = node.name
        if node_name in completed_nodes:
            node.attr['fillcolor'] = 'lightgreen'
        elif node_name in yellow_nodes:
            node.attr['fillcolor'] = 'yellow'
        else:
            node.attr['fillcolor'] = 'lightgrey'
        node.attr['id'] = node_name
        node.attr['href'] = f'javascript:void(0);'
        node.attr['onclick'] = f'updateTopic("{node_name}");'
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
    
    try:
        with open(map_file) as f:
            image_map = f.read()
    except IOError:
        app.logger.error(f"Error reading {map_file}")
        image_map = ""

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
    
    try:
        with open(map_file) as f:
            image_map = f.read()
    except IOError:
        app.logger.error(f"Error reading {map_file}")
        image_map = ""

    app.logger.info(f"Generated updated graph: {graph_file}")
    app.logger.info(f"Generated updated image map: {image_map}")
    return jsonify(success=True, graph_file=f'/static/graph.png', image_map=image_map, progress=progress)

if __name__ == '__main__':
    app.run(debug=True, port=9696)