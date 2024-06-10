# diagram.py
import ast
import contextvars
import os
import sys
from collections import Counter
from inspect import signature
from typing import List, Tuple

from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.custom import Custom

sys.path.append(".")
sys.path.append("..")

class CallGraphAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.call_graph = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                self.call_graph.append((self.current_function, node.func.id))
            elif isinstance(node.func, ast.Attribute):
                self.call_graph.append((self.current_function, node.func.attr))

        self.generic_visit(node)

    def get_call_graph(self):
        return self.call_graph


def analyze_file(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    walk_tree = [x.name for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]
    analyzer = CallGraphAnalyzer()
    analyzer.visit(tree)
    return analyzer.get_call_graph(), walk_tree

graph_attr = {"fontsize": "45", "bgcolor": "transparent"}

with Diagram(
    "LSTM",
    show=False,
    filename=os.path.abspath("./docs/img/LSTM"),
    graph_attr=graph_attr,
):
    with Cluster("main()"):
        tf_icon = os.path.abspath("./docs/img/source_img/tf.png")
        tf_results_icon = os.path.abspath("./docs/img/source_img/tf.png")

        tf_icon = Custom("make_classification", icon_path=tf_icon)
        tf_results = Custom("Make Results", icon_path=tf_results_icon)

        Python("make_data") >> Python("make_ragged") >> tf_icon >> tf_results

with Diagram(
    "Utilities",
    show=False,
    filename=os.path.abspath("./docs/img/Utils"),
    graph_attr=graph_attr,
):
    with Cluster("do_utils()"):
        (
            Python("Classy\ngenerate_sample()")
            >> Python("f()")
            >> Python("g()")
            >> Python("h()")
        )

source_code_fpaths = ["src/dswb/lstm/pipeline/main.py"]

skip = ["randint", "len", "max", "print", "list", "set", "enumerate", "constant", "Input", "add"]
for file_path in source_code_fpaths:
    call_graph, walker = analyze_file(file_path)
    callers = {x[0] for x in call_graph}
    callees = {x[1] for x in call_graph}

    highest = callers.difference(callees)
    assert len(highest) == 1
    highest = list(highest)[0]

    sl = [y for x, y in call_graph if x == highest and y not in skip]
    sec_l = []
    for k,v in Counter(sl).items():
        if v == 1:
            sec_l.append(k)
        else:
            for i in range(v):
                sec_l.append(f"{k}_{i}")
    fp = "/".join(file_path.split("/")[2:])
    fpath_out_name = fp.replace("/", "_").split(".")[0]
    with Diagram(
        highest,
        show=False,
        filename=os.path.abspath(f"./docs/img/generated/{fpath_out_name}"),
        graph_attr=graph_attr,
    ):
        clusters = []
        seen = []
        for s, se in zip(sl, sec_l):
            with Cluster(se, direction="BT"):
                if s in seen:
                    cluster = [Python("...")]
                
                else:
                    cluster = [Python(y) for x, y in call_graph if x in s and y not in skip]
                    # cluster = [ll[i] >> ll[i+1] for i in range(len(ll)-1)]
                    # cluster = [ll[i] for i in range(len(ll))]
                    # cluster = cluster[::-1]                   
                    pass

            seen.append(s)
            clusters.append(cluster)
        
        for i in range(len(clusters)-1):
            if not len(clusters[i]):
                med_idx = len(clusters[i+1]) // 2
                clusters[i] >> clusters[i+1][med_idx]

            else:
                med_idx_0 = len(clusters[i]) // 2
                med_idx_1 = len(clusters[i+1]) // 2

                clusters[i][med_idx_0] >> clusters[i+1][med_idx_1]