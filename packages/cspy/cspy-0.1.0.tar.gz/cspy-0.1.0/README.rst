cspy
====

A collection of algorithms for the (resource) Constrained Shortest Path
(CSP) problem.

The CSP problem was popularised by `Inrich 2005`_. 
It was initially introduced as a subproblem for the bus
driver scheduling problem, and has since then widely studied in a
variety of different settings including: the vehicle routing problem
with time windows (VRPTW), the technician routing and scheduling
problem, the capacitated arc-routing problem, on-demand transportation
systems, and, airport ground movement; among others.

More generally, in the applied column generation framework, particularly
in the scheduling related literature, the CSP problem is commonly
employed to generate columns.

Therefore, this library is of interest to the operational research
community, students and academics alike, that wish to solve an instance
of the CSP problem.

Algorithms
----------

Currently, the algorithms implemented include:

-  Monodirectional forward labeling algorithm;
-  Monodirectional backward labeling algorithm;
-  Bidirectional labeling algorithm with static halfway point;
-  Bidirectional labeling algorithm with dynamic halfway point `Tilk et al 2017`_;
-  Heuristic Tabu search;
-  Greedy elimination procedure;
-  Greedy Randomised Adaptive Search Procedure (GRASP). Adapted from
   `Ferone et al 2019`_;
- Particle Swarm Optimization with combined Local and Global Expanding Neighborhood Topology (PSOLGET) (`Marinakis et al 2017`_).


The first algorithm `BiDirectional`, is the only *exact* algorithm in the library.
This means that it provides an exact (optimal) solution to the resource CSP problem.
For this reason, it sometimes takes longer than the others.
The remaining algorithms are metaheuristics,
i.e. they provide fast and approximate solutions to the CSP problem.


Features
--------

- Generic resource extension functions (`Inrich 2005`_) (not restricted to additive resources);
- Generic resource consumptions (not restricted to non-negative values).

Prerequisites
-------------

Conceptual background and input formatting is discussed in the
`docs`_.

Examples
--------

For complex examples see:

`vrpy`_: (under development) external vehicle routing framework which uses cspy to solve
different variants of the vehicle routing problem using column generation.

`jpath`_ : Simple example showing the necessary graph adptations and the use of
custom resource extension functions. Also discussed below.

`cgar`_: Complex example using cspy for column generation applied to the aircraft
recovery problem.

All of can be found under `examples`_.

.. _examples: https://github.com/torressa/cspy/tree/master/examples/
.. _vrpy: https://github.com/Kuifje02/vrpy
.. _jpath: https://github.com/torressa/cspy/tree/master/examples/jpath
.. _cgar: https://github.com/torressa/cspy/blob/master/examples/cgar/

Contributing
------------

Feel free to contribute to this project either by either working trough
some of issues flagged as help wanted, or raise a new issue with any
bugs/improvements.

If you have a question or need help, feel free to raise an
`issue`_ explaining it.


.. _Tilk et al 2017: https://www.sciencedirect.com/science/article/pii/S0377221717302035
.. _Inrich 2005: https://www.researchgate.net/publication/227142556_Shortest_Path_Problems_with_Resource_Constraints
.. _Marinakis et al 2017: https://www.sciencedirect.com/science/article/pii/S0377221717302357z
.. _Ferone et al 2019: https://www.tandfonline.com/doi/full/10.1080/10556788.2018.1548015
.. _docs: https://cspy.readthedocs.io/en/latest/how_to.html
.. _issue: https://github.com/torressa/cspy/issues
