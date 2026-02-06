# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "diagrams>=0.24",
# ]
# ///
"""Explore Graphviz layout engines with the diagrams library.

Generates the same AWS architecture diagram under every meaningful combination
of layout engine and engine-specific parameters.

Output structure:
    tmp/diagrams/{engine}/{variant}.png

Engines explored (7 of the 8 picture-producing engines, excluding patchwork):
    dot    – Hierarchical/layered (directed graphs)
    neato  – Spring model / stress majorization
    fdp    – Force-directed placement (Fruchterman-Reingold)
    sfdp   – Scalable force-directed (multilevel + Barnes-Hut)
    circo  – Circular layout (cyclic structures)
    twopi  – Radial layout (concentric rings from root)
    osage  – Array-based cluster packing

Usage:
    uv run https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/aws_diagrams_layout_examples.py
"""
import logging
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.network import ELB, CloudFront, Route53

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).resolve().parent / "diagrams"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Layout configurations — grouped by engine
#
# Each config:  name (becomes filename), engine, graph_attr overrides, description
# The description becomes the diagram title so you can tell them apart visually.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYOUT_CONFIGS = {
    # ══════════════════════════════════════════════════════════════════════════
    # DOT — hierarchical/layered directed graph layout
    #
    # Key attributes:
    #   rankdir    – TB|BT|LR|RL   direction of rank flow
    #   ranksep    – separation between ranks (inches)
    #   nodesep    – separation between nodes within a rank (inches)
    #   splines    – edge routing: spline|ortho|curved|polyline|line|false
    #   compound   – allow edges between clusters
    #   newrank    – single global ranking ignoring clusters
    #   clusterrank– local|global|none – cluster handling mode
    #   mclimit    – scale factor for mincross edge crossing minimizer
    #   ordering   – out|in – constrain left-to-right ordering of edges
    # ══════════════════════════════════════════════════════════════════════════
    "dot": [
        # ── Direction variants ────────────────────────────────────────────
        {
            "name": "rankdir_TB",
            "graph_attr": {"rankdir": "TB"},
            "description": "dot: rankdir=TB (top-to-bottom)",
        },
        {
            "name": "rankdir_LR",
            "graph_attr": {"rankdir": "LR"},
            "description": "dot: rankdir=LR (left-to-right)",
        },
        {
            "name": "rankdir_BT",
            "graph_attr": {"rankdir": "BT"},
            "description": "dot: rankdir=BT (bottom-to-top)",
        },
        {
            "name": "rankdir_RL",
            "graph_attr": {"rankdir": "RL"},
            "description": "dot: rankdir=RL (right-to-left)",
        },
        # ── Spline / edge routing variants ────────────────────────────────
        {
            "name": "splines_spline",
            "graph_attr": {"rankdir": "LR", "splines": "spline"},
            "description": "dot: splines=spline (default curved routing)",
        },
        {
            "name": "splines_ortho",
            "graph_attr": {"rankdir": "LR", "splines": "ortho"},
            "description": "dot: splines=ortho (right-angle routing)",
        },
        {
            "name": "splines_curved",
            "graph_attr": {"rankdir": "LR", "splines": "curved"},
            "description": "dot: splines=curved (curved arcs)",
        },
        {
            "name": "splines_polyline",
            "graph_attr": {"rankdir": "LR", "splines": "polyline"},
            "description": "dot: splines=polyline (straight segments)",
        },
        {
            "name": "splines_line",
            "graph_attr": {"rankdir": "LR", "splines": "line"},
            "description": "dot: splines=line (direct straight lines)",
        },
        {
            "name": "splines_false",
            "graph_attr": {"rankdir": "LR", "splines": "false"},
            "description": "dot: splines=false (no edges drawn)",
        },
        # ── Spacing variants ──────────────────────────────────────────────
        {
            "name": "tight_spacing",
            "graph_attr": {"rankdir": "LR", "nodesep": "0.25", "ranksep": "0.3"},
            "description": "dot: tight (nodesep=0.25 ranksep=0.3)",
        },
        {
            "name": "default_spacing",
            "graph_attr": {"rankdir": "LR", "nodesep": "0.70", "ranksep": "0.90"},
            "description": "dot: default (nodesep=0.70 ranksep=0.90)",
        },
        {
            "name": "loose_spacing",
            "graph_attr": {"rankdir": "LR", "nodesep": "1.5", "ranksep": "2.0"},
            "description": "dot: loose (nodesep=1.5 ranksep=2.0)",
        },
        {
            "name": "wide_ranks",
            "graph_attr": {"rankdir": "LR", "nodesep": "0.70", "ranksep": "3.0"},
            "description": "dot: wide ranks (ranksep=3.0)",
        },
        # ── Cluster handling ──────────────────────────────────────────────
        {
            "name": "newrank_true",
            "graph_attr": {"rankdir": "LR", "newrank": "true"},
            "description": "dot: newrank=true (global ranking ignores clusters)",
        },
        {
            "name": "compound_true",
            "graph_attr": {"rankdir": "LR", "compound": "true"},
            "description": "dot: compound=true (edges between clusters)",
        },
        # ── Ordering constraint ───────────────────────────────────────────
        {
            "name": "ordering_out",
            "graph_attr": {"rankdir": "LR", "ordering": "out"},
            "description": "dot: ordering=out (preserve edge order)",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # NEATO — spring model / stress majorization
    #
    # Key attributes:
    #   mode       – major|KK|sgd|hier|ipsep  optimization algorithm
    #   model      – shortpath|circuit|subset|mds  distance computation
    #   overlap    – true|false|scale|scalexy|compress|prism|voronoi|vpsc|ortho
    #   sep        – margin around nodes for overlap removal (inches or additive +N)
    #   esep       – margin around polygons for spline edge routing
    #   Damping    – force damping factor (0.0-1.0, default 0.99)
    #   epsilon    – convergence threshold (default 0.0001 * #nodes)
    #   maxiter    – iteration cap (default 200*#nodes for major, 600 for KK)
    #   defaultdist– distance for nodes in separate components (default sqrt(#nodes))
    #   diredgeconstraints – if true, edges point downward (like dot)
    #   inputscale – scale factor for input coordinates
    #   start      – random|self|... initial layout seed
    # ══════════════════════════════════════════════════════════════════════════
    "neato": [
        # ── Mode (optimization algorithm) variants ────────────────────────
        {
            "name": "mode_major",
            "graph_attr": {"mode": "major", "overlap": "false", "splines": "true"},
            "description": "neato: mode=major (stress majorization, default)",
        },
        {
            "name": "mode_KK",
            "graph_attr": {"mode": "KK", "overlap": "false", "splines": "true"},
            "description": "neato: mode=KK (Kamada-Kawai gradient descent)",
        },
        {
            "name": "mode_sgd",
            "graph_attr": {"mode": "sgd", "overlap": "false", "splines": "true"},
            "description": "neato: mode=sgd (stochastic gradient descent)",
        },
        # ── Model (distance computation) variants ─────────────────────────
        {
            "name": "model_shortpath",
            "graph_attr": {"model": "shortpath", "overlap": "false", "splines": "true"},
            "description": "neato: model=shortpath (shortest path distance, default)",
        },
        {
            "name": "model_circuit",
            "graph_attr": {"model": "circuit", "overlap": "false", "splines": "true"},
            "description": "neato: model=circuit (resistance model, emphasizes clusters)",
        },
        {
            "name": "model_subset",
            "graph_attr": {"model": "subset", "overlap": "false", "splines": "true"},
            "description": "neato: model=subset (separates high-degree nodes)",
        },
        {
            "name": "model_mds",
            "graph_attr": {"model": "mds", "overlap": "false", "splines": "true"},
            "description": "neato: model=mds (edge len as ideal distance)",
        },
        # ── Overlap removal strategies ────────────────────────────────────
        {
            "name": "overlap_true",
            "graph_attr": {"overlap": "true", "splines": "true"},
            "description": "neato: overlap=true (allow node overlaps)",
        },
        {
            "name": "overlap_false",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "neato: overlap=false (prism removal)",
        },
        {
            "name": "overlap_scale",
            "graph_attr": {"overlap": "scale", "splines": "true"},
            "description": "neato: overlap=scale (uniform scaling to remove overlaps)",
        },
        {
            "name": "overlap_scalexy",
            "graph_attr": {"overlap": "scalexy", "splines": "true"},
            "description": "neato: overlap=scalexy (separate x/y scaling)",
        },
        {
            "name": "overlap_compress",
            "graph_attr": {"overlap": "compress", "splines": "true"},
            "description": "neato: overlap=compress (smallest scale with no overlaps)",
        },
        {
            "name": "overlap_voronoi",
            "graph_attr": {"overlap": "voronoi", "splines": "true"},
            "description": "neato: overlap=voronoi (Voronoi-based removal)",
        },
        {
            "name": "overlap_vpsc",
            "graph_attr": {"overlap": "vpsc", "splines": "true"},
            "description": "neato: overlap=vpsc (quadratic optimization)",
        },
        {
            "name": "overlap_ortho",
            "graph_attr": {"overlap": "ortho", "splines": "true"},
            "description": "neato: overlap=ortho (axis-aligned constraint removal)",
        },
        {
            "name": "overlap_prism",
            "graph_attr": {"overlap": "prism", "splines": "true"},
            "description": "neato: overlap=prism (explicit prism algorithm)",
        },
        # ── Damping factor ────────────────────────────────────────────────
        {
            "name": "damping_low",
            "graph_attr": {"Damping": "0.5", "overlap": "false", "splines": "true"},
            "description": "neato: Damping=0.5 (heavy damping, faster settle)",
        },
        {
            "name": "damping_high",
            "graph_attr": {"Damping": "0.99", "overlap": "false", "splines": "true"},
            "description": "neato: Damping=0.99 (light damping, default)",
        },
        # ── Directed edge constraints (make neato more like dot) ──────────
        {
            "name": "diredge_true",
            "graph_attr": {
                "diredgeconstraints": "true", "overlap": "false", "splines": "true",
            },
            "description": "neato: diredgeconstraints=true (edges point downward)",
        },
        # ── Sep / spacing control ─────────────────────────────────────────
        {
            "name": "sep_small",
            "graph_attr": {"sep": "+2", "overlap": "false", "splines": "true"},
            "description": "neato: sep=+2 (small margin for overlap removal)",
        },
        {
            "name": "sep_large",
            "graph_attr": {"sep": "+20", "overlap": "false", "splines": "true"},
            "description": "neato: sep=+20 (large margin, very spread out)",
        },
        # ── Spline variants under neato ───────────────────────────────────
        {
            "name": "splines_curved",
            "graph_attr": {"overlap": "false", "splines": "curved"},
            "description": "neato: splines=curved",
        },
        {
            "name": "splines_polyline",
            "graph_attr": {"overlap": "false", "splines": "polyline"},
            "description": "neato: splines=polyline",
        },
        {
            "name": "splines_ortho",
            "graph_attr": {"overlap": "false", "splines": "ortho"},
            "description": "neato: splines=ortho (axis-aligned edges)",
        },
        {
            "name": "splines_line",
            "graph_attr": {"overlap": "false", "splines": "line"},
            "description": "neato: splines=line (straight lines)",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # FDP — force-directed placement (grid-variant Fruchterman-Reingold)
    #
    # Key attributes:
    #   K          – spring constant (default 0.3) — larger = more spread
    #   maxiter    – iteration limit (default 600)
    #   start      – initial layout seed
    #   overlap    – same options as neato
    #   sep        – margin for overlap removal
    #   splines    – same options; also supports "compound" (avoids clusters)
    # ══════════════════════════════════════════════════════════════════════════
    "fdp": [
        # ── Spring constant K variants ────────────────────────────────────
        {
            "name": "K_default",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "fdp: K=default (0.3)",
        },
        {
            "name": "K_0.1",
            "graph_attr": {"K": "0.1", "overlap": "false", "splines": "true"},
            "description": "fdp: K=0.1 (very tight spring, compact)",
        },
        {
            "name": "K_0.5",
            "graph_attr": {"K": "0.5", "overlap": "false", "splines": "true"},
            "description": "fdp: K=0.5 (slightly loose spring)",
        },
        {
            "name": "K_1.0",
            "graph_attr": {"K": "1.0", "overlap": "false", "splines": "true"},
            "description": "fdp: K=1.0 (loose spring, spread out)",
        },
        {
            "name": "K_2.0",
            "graph_attr": {"K": "2.0", "overlap": "false", "splines": "true"},
            "description": "fdp: K=2.0 (very loose, wide spacing)",
        },
        {
            "name": "K_5.0",
            "graph_attr": {"K": "5.0", "overlap": "false", "splines": "true"},
            "description": "fdp: K=5.0 (extreme spread)",
        },
        # ── Maxiter variants ──────────────────────────────────────────────
        {
            "name": "maxiter_50",
            "graph_attr": {"maxiter": "50", "overlap": "false", "splines": "true"},
            "description": "fdp: maxiter=50 (early stop, rough layout)",
        },
        {
            "name": "maxiter_600",
            "graph_attr": {"maxiter": "600", "overlap": "false", "splines": "true"},
            "description": "fdp: maxiter=600 (default, converged)",
        },
        {
            "name": "maxiter_2000",
            "graph_attr": {"maxiter": "2000", "overlap": "false", "splines": "true"},
            "description": "fdp: maxiter=2000 (extra refinement)",
        },
        # ── Overlap strategies under fdp ──────────────────────────────────
        {
            "name": "overlap_false",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "fdp: overlap=false (prism removal)",
        },
        {
            "name": "overlap_compress",
            "graph_attr": {"overlap": "compress", "splines": "true"},
            "description": "fdp: overlap=compress (smallest w/o overlaps)",
        },
        # ── Compound splines (fdp special) ────────────────────────────────
        {
            "name": "splines_compound",
            "graph_attr": {"overlap": "false", "splines": "compound"},
            "description": "fdp: splines=compound (edges avoid clusters too)",
        },
        {
            "name": "splines_curved",
            "graph_attr": {"overlap": "false", "splines": "curved"},
            "description": "fdp: splines=curved",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # SFDP — scalable force-directed (multilevel coarsening + Barnes-Hut)
    #
    # Key attributes:
    #   K              – spring constant (ideal edge length)
    #   repulsiveforce – power of repulsive force (default 1.0)
    #   beautify       – draw leaf nodes in a circle around root
    #   smoothing      – none|avg_dist|graph_dist|power_dist|rng|spring|triangle
    #   quadtree       – normal|fast|none  (Barnes-Hut approximation)
    #   levels         – number of coarsening levels (0 = single-level)
    #   overlap_shrink – enable compression pass
    #   rotation       – rotate final layout by degrees
    # ══════════════════════════════════════════════════════════════════════════
    "sfdp": [
        # ── Baseline ──────────────────────────────────────────────────────
        {
            "name": "default",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "sfdp: defaults",
        },
        # ── Spring constant K variants ────────────────────────────────────
        {
            "name": "K_0.3",
            "graph_attr": {"K": "0.3", "overlap": "false", "splines": "true"},
            "description": "sfdp: K=0.3 (tight spring)",
        },
        {
            "name": "K_1.0",
            "graph_attr": {"K": "1.0", "overlap": "false", "splines": "true"},
            "description": "sfdp: K=1.0 (moderate spring)",
        },
        {
            "name": "K_3.0",
            "graph_attr": {"K": "3.0", "overlap": "false", "splines": "true"},
            "description": "sfdp: K=3.0 (wide spring)",
        },
        # ── Repulsive force power ─────────────────────────────────────────
        {
            "name": "repulsive_0.5",
            "graph_attr": {"repulsiveforce": "0.5", "overlap": "false", "splines": "true"},
            "description": "sfdp: repulsiveforce=0.5 (weak repulsion)",
        },
        {
            "name": "repulsive_1.0",
            "graph_attr": {"repulsiveforce": "1.0", "overlap": "false", "splines": "true"},
            "description": "sfdp: repulsiveforce=1.0 (default)",
        },
        {
            "name": "repulsive_3.0",
            "graph_attr": {"repulsiveforce": "3.0", "overlap": "false", "splines": "true"},
            "description": "sfdp: repulsiveforce=3.0 (strong push-apart)",
        },
        # ── Smoothing variants ────────────────────────────────────────────
        {
            "name": "smooth_none",
            "graph_attr": {"smoothing": "none", "overlap": "false", "splines": "true"},
            "description": "sfdp: smoothing=none (no post-processing)",
        },
        {
            "name": "smooth_spring",
            "graph_attr": {"smoothing": "spring", "overlap": "false", "splines": "true"},
            "description": "sfdp: smoothing=spring",
        },
        {
            "name": "smooth_triangle",
            "graph_attr": {"smoothing": "triangle", "overlap": "false", "splines": "true"},
            "description": "sfdp: smoothing=triangle",
        },
        {
            "name": "smooth_rng",
            "graph_attr": {"smoothing": "rng", "overlap": "false", "splines": "true"},
            "description": "sfdp: smoothing=rng (relative neighborhood graph)",
        },
        {
            "name": "smooth_power_dist",
            "graph_attr": {"smoothing": "power_dist", "overlap": "false", "splines": "true"},
            "description": "sfdp: smoothing=power_dist",
        },
        # ── Quadtree scheme (Barnes-Hut approximation) ────────────────────
        {
            "name": "quadtree_normal",
            "graph_attr": {"quadtree": "normal", "overlap": "false", "splines": "true"},
            "description": "sfdp: quadtree=normal (default Barnes-Hut)",
        },
        {
            "name": "quadtree_fast",
            "graph_attr": {"quadtree": "fast", "overlap": "false", "splines": "true"},
            "description": "sfdp: quadtree=fast (optimized approximation)",
        },
        {
            "name": "quadtree_none",
            "graph_attr": {"quadtree": "none", "overlap": "false", "splines": "true"},
            "description": "sfdp: quadtree=none (exact forces, slow for large graphs)",
        },
        # ── Beautify (leaf nodes in circle) ───────────────────────────────
        {
            "name": "beautify_on",
            "graph_attr": {"beautify": "true", "overlap": "false", "splines": "true"},
            "description": "sfdp: beautify=true (leaves in circle around root)",
        },
        # ── Multi-level coarsening ────────────────────────────────────────
        {
            "name": "levels_0",
            "graph_attr": {"levels": "0", "overlap": "false", "splines": "true"},
            "description": "sfdp: levels=0 (single-level, no coarsening)",
        },
        {
            "name": "levels_5",
            "graph_attr": {"levels": "5", "overlap": "false", "splines": "true"},
            "description": "sfdp: levels=5 (multilevel coarsening)",
        },
        # ── Rotation ──────────────────────────────────────────────────────
        {
            "name": "rotation_90",
            "graph_attr": {"rotation": "90", "overlap": "false", "splines": "true"},
            "description": "sfdp: rotation=90 (rotated 90 degrees)",
        },
        # ── Overlap shrink ────────────────────────────────────────────────
        {
            "name": "overlap_shrink_on",
            "graph_attr": {
                "overlap_shrink": "true", "overlap": "false", "splines": "true",
            },
            "description": "sfdp: overlap_shrink=true (compression pass)",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # CIRCO — circular layout for cyclic structures
    #
    # Key attributes:
    #   mindist    – minimum separation between all nodes
    #   root       – center node(s) of the layout
    #   oneblock   – draw entire graph around a single circle
    #   overlap_scaling – scale factor for overlap reduction
    #   splines    – edge routing style
    # ══════════════════════════════════════════════════════════════════════════
    "circo": [
        # ── Baseline ──────────────────────────────────────────────────────
        {
            "name": "default",
            "graph_attr": {"splines": "true"},
            "description": "circo: defaults",
        },
        # ── Mindist variants ──────────────────────────────────────────────
        {
            "name": "mindist_0.5",
            "graph_attr": {"mindist": "0.5", "splines": "true"},
            "description": "circo: mindist=0.5 (tighter node spacing)",
        },
        {
            "name": "mindist_1.0",
            "graph_attr": {"mindist": "1.0", "splines": "true"},
            "description": "circo: mindist=1.0 (default)",
        },
        {
            "name": "mindist_2.0",
            "graph_attr": {"mindist": "2.0", "splines": "true"},
            "description": "circo: mindist=2.0 (wider spacing)",
        },
        {
            "name": "mindist_4.0",
            "graph_attr": {"mindist": "4.0", "splines": "true"},
            "description": "circo: mindist=4.0 (very wide)",
        },
        # ── Oneblock (single circle vs multiple) ─────────────────────────
        {
            "name": "oneblock_true",
            "graph_attr": {"oneblock": "true", "splines": "true"},
            "description": "circo: oneblock=true (all nodes on single circle)",
        },
        {
            "name": "oneblock_false",
            "graph_attr": {"oneblock": "false", "splines": "true"},
            "description": "circo: oneblock=false (biconnected components)",
        },
        # ── Spline variants under circo ───────────────────────────────────
        {
            "name": "splines_true",
            "graph_attr": {"splines": "true"},
            "description": "circo: splines=true (routed around nodes)",
        },
        {
            "name": "splines_curved",
            "graph_attr": {"splines": "curved"},
            "description": "circo: splines=curved",
        },
        {
            "name": "splines_line",
            "graph_attr": {"splines": "line"},
            "description": "circo: splines=line (straight lines)",
        },
        {
            "name": "splines_polyline",
            "graph_attr": {"splines": "polyline"},
            "description": "circo: splines=polyline",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # TWOPI — radial layout (concentric rings from root)
    #
    # Key attributes:
    #   root       – center node of the radial layout
    #   ranksep    – radial distance between concentric rings
    #   overlap    – overlap removal strategy
    #   splines    – edge routing style
    # ══════════════════════════════════════════════════════════════════════════
    "twopi": [
        # ── Baseline ──────────────────────────────────────────────────────
        {
            "name": "default",
            "graph_attr": {"splines": "true"},
            "description": "twopi: defaults",
        },
        # ── Ranksep (ring separation) variants ────────────────────────────
        {
            "name": "ranksep_0.5",
            "graph_attr": {"ranksep": "0.5", "splines": "true"},
            "description": "twopi: ranksep=0.5 (tight rings)",
        },
        {
            "name": "ranksep_1.0",
            "graph_attr": {"ranksep": "1.0", "splines": "true"},
            "description": "twopi: ranksep=1.0",
        },
        {
            "name": "ranksep_2.0",
            "graph_attr": {"ranksep": "2.0", "splines": "true"},
            "description": "twopi: ranksep=2.0 (wide rings)",
        },
        {
            "name": "ranksep_4.0",
            "graph_attr": {"ranksep": "4.0", "splines": "true"},
            "description": "twopi: ranksep=4.0 (very wide rings)",
        },
        # ── Overlap removal ───────────────────────────────────────────────
        {
            "name": "overlap_false",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "twopi: overlap=false (prism removal)",
        },
        {
            "name": "overlap_compress",
            "graph_attr": {"overlap": "compress", "splines": "true"},
            "description": "twopi: overlap=compress (minimal scaling)",
        },
        # ── Spline variants under twopi ───────────────────────────────────
        {
            "name": "splines_true",
            "graph_attr": {"overlap": "false", "splines": "true"},
            "description": "twopi: splines=true (routed around nodes)",
        },
        {
            "name": "splines_curved",
            "graph_attr": {"overlap": "false", "splines": "curved"},
            "description": "twopi: splines=curved",
        },
        {
            "name": "splines_line",
            "graph_attr": {"overlap": "false", "splines": "line"},
            "description": "twopi: splines=line (straight lines)",
        },
    ],

    # ══════════════════════════════════════════════════════════════════════════
    # OSAGE — array-based cluster packing
    #
    # Key attributes:
    #   pack       – margin around packed components (points)
    #   packmode   – node|clust|graph – what units to pack
    #   sortv      – integer key for sorting nodes/clusters within array
    #   splines    – edge routing style
    # ══════════════════════════════════════════════════════════════════════════
    "osage": [
        {
            "name": "default",
            "graph_attr": {},
            "description": "osage: defaults",
        },
        {
            "name": "pack_20",
            "graph_attr": {"pack": "20"},
            "description": "osage: pack=20 (tight packing)",
        },
        {
            "name": "pack_100",
            "graph_attr": {"pack": "100"},
            "description": "osage: pack=100 (loose packing)",
        },
        {
            "name": "packmode_node",
            "graph_attr": {"packmode": "node"},
            "description": "osage: packmode=node",
        },
        {
            "name": "packmode_clust",
            "graph_attr": {"packmode": "clust"},
            "description": "osage: packmode=clust",
        },
        {
            "name": "packmode_graph",
            "graph_attr": {"packmode": "graph"},
            "description": "osage: packmode=graph",
        },
    ],
}


def build_diagram(engine: str, config: dict) -> None:
    """Build and render the example architecture diagram with a given layout config.

    The diagram models a typical 3-tier web service on AWS:
      DNS -> CDN -> LB -> [Web Servers] -> [App Containers] -> DB + Cache
    """
    variant_name = config["name"]
    description = config["description"]
    extra_graph_attr = config.get("graph_attr", {})

    engine_dir = OUTPUT_DIR / engine
    engine_dir.mkdir(parents=True, exist_ok=True)
    filepath = str(engine_dir / variant_name)

    log.info("  %-30s -> %s/%s.png", variant_name, engine, variant_name)

    with Diagram(
        description,
        filename=filepath,
        show=False,
        outformat="png",
        graph_attr=extra_graph_attr,
    ) as diag:
        # Inject the layout engine onto the underlying graphviz.Digraph
        diag.dot.engine = engine

        # ── Build architecture ────────────────────────────────────
        dns = Route53("Route53\nDNS")
        cdn = CloudFront("CloudFront\nCDN")

        with Cluster("Web Tier"):
            lb = ELB("ALB")
            web1 = EC2("Web 1")
            web2 = EC2("Web 2")
            web3 = EC2("Web 3")

        with Cluster("App Tier"):
            app1 = ECS("App 1")
            app2 = ECS("App 2")
            worker = Lambda("Worker")

        with Cluster("Data Tier"):
            db_primary = RDS("Primary DB")
            db_replica = RDS("Read Replica")
            cache = Elasticache("Redis Cache")

        # ── Connections ───────────────────────────────────────────
        dns >> cdn >> lb
        lb >> [web1, web2, web3]
        web1 >> app1
        web2 >> app2
        web3 >> app1
        app1 >> db_primary
        app2 >> db_primary
        app1 >> cache
        app2 >> cache
        db_primary >> Edge(label="replication", style="dashed") >> db_replica
        worker >> db_primary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = sum(len(configs) for configs in LAYOUT_CONFIGS.values())
    log.info("Output directory: %s", OUTPUT_DIR)
    log.info("Generating %d layout variations across %d engines...\n", total, len(LAYOUT_CONFIGS))

    succeeded = []
    failed = []

    for engine, configs in LAYOUT_CONFIGS.items():
        log.info("[%s] — %d variants", engine.upper(), len(configs))

        for config in configs:
            full_name = f"{engine}/{config['name']}"
            try:
                build_diagram(engine, config)
                succeeded.append(full_name)
            except Exception:
                log.exception("  FAILED: %s", full_name)
                failed.append(full_name)

        log.info("")

    # ── Summary ───────────────────────────────────────────────────
    log.info("=" * 70)
    log.info("SUMMARY: %d succeeded, %d failed out of %d total", len(succeeded), len(failed), total)
    log.info("=" * 70)

    for engine in LAYOUT_CONFIGS:
        engine_dir = OUTPUT_DIR / engine
        pngs = sorted(engine_dir.glob("*.png"))
        total_kb = sum(p.stat().st_size for p in pngs) / 1024
        log.info("  %-10s %2d PNGs  (%6.0f KB total)", engine, len(pngs), total_kb)

    if failed:
        log.warning("\nFailed variants:")
        for name in failed:
            log.warning("  %s", name)

    log.info("\nBrowse results:  open %s", OUTPUT_DIR)


if __name__ == "__main__":
    main()
