Some testing I've done with basic genetic algorithms and using pygame for visualization.

simulator.py contains most of the logic for the pygame application, while creatures.py defines how the creatures work and genetics.py contains breeding selection functions.

In the current version, creatures use a vector field to attempt to get close to the target.
<br>
The individuals are breeding using a tournament system, and exclude any members who either run into walls or run off the field.
