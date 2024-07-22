# Graph Template for graph.txt

This template provides instructions for generating the contents of `graph.txt`, which defines a directed graph for visualizing learning paths or topic relationships on any subject. The resulting graph can be used with the LearningTechTree web application. It uses the DOT language, which is a graph description language. DOT is primarily used with Graphviz, a popular open-source graph visualization software. 

## Basic Structure

The `graph.txt` file should start with the following structure:

```
digraph SubjectName {
    rankdir=TB;
    node [shape=box, style="rounded,filled", color=black, fontname="Helvetica", fontsize=10, penwidth=2, width=2, height=0.5];
    edge [color=gray, arrowhead=open];

    // Node definitions and relationships will go here
}
```

Replace `SubjectName` with the name of your subject area (e.g., "DeepLearningPath", "WebDevelopment", "DataScience").

## Node and Edge Formatting

### Nodes (Topics)
Each node represents a topic or subtopic in your subject area. Define nodes using the following format:

```
TopicID [label="Topic Name\n(Optional Subtitle)"];
```

- `TopicID`: A unique identifier for the topic (no spaces, use CamelCase or snake_case)
- `label`: The displayed name of the topic, can include a subtitle on a new line

Example:
```
BasicMath [label="Basic Math\n(Algebra, Calculus)"];
```

### Edges (Relationships)
Edges represent relationships or dependencies between topics. Define them using the following format:

```
TopicID1 -> TopicID2;
```

This creates a directed edge from TopicID1 to TopicID2, indicating that TopicID1 is a prerequisite for TopicID2.

## Defining Topics and Subtopics

1. Start with high-level topics that form the foundation of your subject.
2. Break down each high-level topic into subtopics or more specific areas of study.
3. Consider the logical progression of learning when ordering your topics.

Example:
```
BasicMath [label="Basic Math"];
LinearAlgebra [label="Linear Algebra"];
ProbabilityStatistics [label="Probability &\nStatistics"];
```

## Creating Relationships

1. Identify prerequisites for each topic.
2. Create edges from prerequisite topics to their dependent topics.
3. Ensure that the graph remains acyclic (no circular dependencies).

Example:
```
BasicMath -> LinearAlgebra;
BasicMath -> ProbabilityStatistics;
LinearAlgebra -> MachineLearning;
ProbabilityStatistics -> MachineLearning;
```

## Graph Structure Examples

### Linear Progression
```
Topic1 -> Topic2;
Topic2 -> Topic3;
Topic3 -> Topic4;
```

### Branching Paths
```
RootTopic -> Branch1Topic1;
RootTopic -> Branch2Topic1;
Branch1Topic1 -> Branch1Topic2;
Branch2Topic1 -> Branch2Topic2;
```

### Converging Paths
```
Topic1 -> Topic3;
Topic2 -> Topic3;
Topic3 -> Topic4;
```

## Customization and Best Practices

1. Group related topics using the `rank` attribute:
   ```
   {rank=same; Topic1; Topic2; Topic3}
   ```
   This places Topic1, Topic2, and Topic3 at the same vertical level in the graph.

2. Keep the graph readable by limiting the number of edges coming into or out of a single node.

3. Use meaningful and concise labels for topics.

4. Consider using color coding for different categories of topics:
   ```
   node [fillcolor=lightblue, style="filled,rounded"];
   Category1Topic1 [fillcolor=lightgreen];
   Category2Topic1 [fillcolor=lightyellow];
   ```

## Using this Template with a Large Language Model

When using this template with a large language model to generate a `graph.txt` file for a specific subject:

1. Provide the model with the subject area and ask it to identify the main topics and subtopics.
2. Ask the model to organize these topics into a logical learning progression.
3. Request that the model create node definitions for each topic using the format provided in this template.
4. Ask the model to identify relationships between topics and create appropriate edges.
5. Have the model structure the output according to the basic structure provided at the beginning of this template.
6. Review the generated content and make any necessary adjustments for clarity and accuracy.

Remember to verify the logical flow and accuracy of the generated graph, as large language models may occasionally produce errors or inconsistencies.

# Quick prompt:
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