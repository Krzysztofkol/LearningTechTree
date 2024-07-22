import os
import re
from flask import Flask, render_template, request, jsonify, url_for
import json
import pygraphviz as pgv
import logging
app = Flask(__name__, template_folder='.')
SUBJECTS_FOLDER = 'subjects'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
def get_available_subjects():
    return [d for d in os.listdir(SUBJECTS_FOLDER) if os.path.isdir(os.path.join(SUBJECTS_FOLDER, d))]
def get_subject_path(subject):
    return os.path.join(SUBJECTS_FOLDER, subject)
def get_graph_file(subject):
    return os.path.join(get_subject_path(subject), 'graph.txt')
def get_progress_file(subject):
    return os.path.join(get_subject_path(subject), 'progress.json')
def read_graph_file(subject):
    try:
        with open(get_graph_file(subject), 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Graph file not found for subject: {subject}")
        return ""
    except IOError:
        logger.error(f"Error reading graph file for subject: {subject}")
        return ""
def parse_graph_file(subject):
    graph_content = read_graph_file(subject)
    nodes = set()

    # Extract nodes from node definitions
    node_matches = re.findall(r'^\s*(\w+)\s*\[', graph_content, re.MULTILINE)
    nodes.update(node_matches)

    # Extract nodes from edge definitions
    edge_matches = re.findall(r'(\w+)\s*->\s*(\w+)', graph_content)
    nodes.update([node for edge in edge_matches for node in edge])

    # Remove 'node' and 'edge' if they exist
    nodes.discard('node')
    nodes.discard('edge')

    logger.debug(f"Extracted nodes for {subject}: {nodes}")
    if not nodes:
        logger.error(f"No valid nodes found in the graph file for {subject}")
    return list(nodes)  # Convert set to list before returning

def generate_default_progress(subject):
    node_names = parse_graph_file(subject)
    if not node_names:
        logger.error(f"No valid nodes found for {subject}. Cannot generate progress.")
        return {}
    progress = {node: False for node in node_names}
    logger.info(f"Generated default progress for {subject}: {progress}")
    save_progress(subject, progress)
    return progress

def is_progress_consistent_with_graph(progress, subject):
    current_nodes = set(parse_graph_file(subject))
    progress_nodes = set(progress.keys())
    logger.debug(f"Checking consistency for {subject}:")
    logger.debug(f"  Current nodes: {current_nodes}")
    logger.debug(f"  Progress nodes: {progress_nodes}")
    return current_nodes == progress_nodes

def load_progress(subject):
    progress_file = get_progress_file(subject)
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)
            if not is_progress_consistent_with_graph(progress, subject):
                logger.info(f"Progress file for {subject} is inconsistent with the current graph. Regenerating.")
                return generate_default_progress(subject)
            logger.info(f"Loaded existing progress for {subject}: {progress}")
            return progress
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {progress_file}")
            return generate_default_progress(subject)
    else:
        logger.info(f"Progress file not found for subject: {subject}. Creating default progress.")
        return generate_default_progress(subject)

def save_progress(subject, progress):
    progress_file = get_progress_file(subject)
    try:
        with open(progress_file, 'w') as f:
            json.dump(progress, f)
        logger.info(f"Saved progress for {subject}: {progress}")
    except IOError:
        logger.error(f"Error writing to {progress_file}")

def get_all_predecessors(graph, node):
    predecessors = set()
    for edge in graph.edges():
        if edge[1] == node:
            predecessors.add(edge[0])
            predecessors.update(get_all_predecessors(graph, edge[0]))
    return predecessors
def generate_graph(subject, progress):
    app.logger.info(f"Generating graph for subject: {subject}")
    graph = pgv.AGraph(string=read_graph_file(subject))
    graph.node_attr['shape'] = 'box'
    graph.node_attr['style'] = 'rounded,filled'
    graph.node_attr['fontname'] = 'Helvetica'
    graph.node_attr['fontsize'] = '10'
    graph.node_attr['height'] = '0.5'
    graph.node_attr['width'] = '2'
    graph.graph_attr['rankdir'] = 'TB'
    graph.graph_attr['splines'] = 'polyline'
    graph.graph_attr['overlap'] = 'false'
    graph.graph_attr['pack'] = 'true'
    graph.graph_attr['packmode'] = 'clust'
    # First pass: identify and color completed nodes
    completed_nodes = set()
    for node in graph.nodes():
        node_name = node.name
        if progress.get(node_name, False):
            completed_nodes.add(node_name)
            node.attr['fillcolor'] = 'lightgreen'
            app.logger.info(f"Node {node_name} colored green (completed)")
    # Second pass: identify and color yellow nodes
    for node in graph.nodes():
        node_name = node.name
        if node_name not in completed_nodes:
            predecessors = get_all_predecessors(graph, node_name)
            if all(pred in completed_nodes for pred in predecessors):
                node.attr['fillcolor'] = 'yellow'
                app.logger.info(f"Node {node_name} colored yellow (ready)")
            else:
                node.attr['fillcolor'] = 'lightgrey'
                app.logger.info(f"Node {node_name} colored light grey (not ready)")
        node.attr['id'] = node_name
        node.attr['href'] = f'javascript:void(0);'
        node.attr['onclick'] = f'updateTopic("{node_name}");'
    return graph
def calculate_progress_percentage(progress):
    # Filter out 'node' and 'edge' entries
    valid_progress = {k: v for k, v in progress.items() if k not in ['node', 'edge']}
    total = len(valid_progress)
    completed_count = sum(1 for state in valid_progress.values() if state)
    if total == 0:
        return 0  # Avoid division by zero
    percentage = (completed_count / total) * 100
    return round(percentage, 0)

@app.route('/')
def index():
    subjects = get_available_subjects()
    if not subjects:
        return "No subjects available", 404
    selected_subject = request.args.get('subject', subjects[0])
    if selected_subject not in subjects:
        return f"Subject {selected_subject} not found", 404
    
    logger.info(f"Rendering index page for subject: {selected_subject}")
    progress = load_progress(selected_subject)
    logger.info(f"Loaded progress for {selected_subject}: {progress}")
    
    if not progress:
        return f"Error: Unable to generate progress for {selected_subject}", 500
    
    graph = generate_graph(selected_subject, progress)
    graph_file = f'static/{selected_subject}_graph.png'
    graph.draw(graph_file, format='png', prog='dot')
    
    map_file = f'static/{selected_subject}_graph.map'
    graph.draw(map_file, format='cmapx', prog='dot')
    
    try:
        with open(map_file) as f:
            image_map = f.read()
    except IOError:
        logger.error(f"Error reading {map_file}")
        image_map = ""
    
    logger.info(f"Generated graph: {graph_file}")
    logger.debug(f"Generated image map: {image_map}")
    
    progress_percentage = calculate_progress_percentage(progress)
    
    return render_template('frontend.html',
                           graph_file=url_for('static', filename=f'{selected_subject}_graph.png'),
                           image_map=image_map,
                           progress=json.dumps(progress),
                           subjects=subjects,
                           selected_subject=selected_subject,
                           progress_percentage=progress_percentage)
                           
@app.route('/update', methods=['POST'])
def update():
    app.logger.info(f"Received update request: {request.json}")
    data = request.json
    subject = data['subject']
    topic = data['topic']
    completed = data['completed']
    progress = load_progress(subject)
    progress[topic] = completed
    save_progress(subject, progress)
    app.logger.info(f"Updated topic: {topic}, Completed: {completed} for subject: {subject}")
    app.logger.info(f"Current progress for {subject}: {progress}")
    graph = generate_graph(subject, progress)
    graph_file = f'static/{subject}_graph.png'
    graph.draw(graph_file, format='png', prog='dot')
    map_file = f'static/{subject}_graph.map'
    graph.draw(map_file, format='cmapx', prog='dot')
    try:
        with open(map_file) as f:
            image_map = f.read()
    except IOError:
        app.logger.error(f"Error reading {map_file}")
        image_map = ""
    app.logger.info(f"Generated updated graph: {graph_file}")
    app.logger.info(f"Generated updated image map: {image_map}")
    progress_percentage = calculate_progress_percentage(progress)
    return jsonify(success=True,
                   graph_file=url_for('static', filename=f'{subject}_graph.png'),
                   image_map=image_map,
                   progress=progress,
                   progress_percentage=progress_percentage)
if __name__ == '__main__':
    app.run(debug=True, port=9696)