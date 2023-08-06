#!/usr/bin/env python
import csv
import os
import re
import sys


def export_to_csv(nodes, output_dir):
    nodes_path = os.path.join(output_dir, "nodes.csv")
    edges_path = os.path.join(output_dir, "edges.csv")
    node_path_exists = os.path.exists(nodes_path)
    edge_path_exists = os.path.exists(edges_path)

    edges = set(
        (node["videoId"], child) for node in nodes for child in node["relatedVideos"]
    )
    with open(edges_path, "a", newline="") as out:
        csv_out = csv.writer(out, delimiter="\t")
        if not edge_path_exists:
            csv_out.writerow(["origin", "target"])
        for origin, target in edges:
            csv_out.writerow([origin, target])

    with open(nodes_path, "a", newline="") as out:
        csv_out = csv.writer(out, delimiter="\t")
        if not node_path_exists:
            csv_out.writerow(nodes[0].keys())
        for node in nodes:
            del node["relatedVideos"]
            del node["description"]
            csv_out.writerow(node.values())


def filter_text(text, encoding="ascii"):
    if encoding == "smart":
        text = re.sub(r"<[^>]*>", " ", text)
        text = re.sub(r"\[[^\]]*\]", " ", text)
        text = re.sub(r"[^a-zA-ZäöüÄÖÜß\s]*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
    else:
        text = text.encode(encoding, "ignore").decode()
    return text
