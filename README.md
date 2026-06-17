This project is a simple physics-based simulation of our solar system, built using Python and the Pygame library. It models the gravitational pull between the Sun and each planet using Newton's law of universal gravitation, so the orbits you see aren't pre-scripted; they emerge naturally from the same physics that governs real planetary motion.
Each planet starts with its real-world mass, distance from the Sun, and orbital velocity (scaled down so everything fits on screen), and on every frame the simulation recalculates the gravitational force between every pair of bodies, updates their velocities and positions accordingly, and renders them with a fading trail showing their path through space.
Features:

Realistic gravity simulation using G = 6.674×10⁻¹¹ and Newton's gravitational formula
All 8 planets plus Pluto, with accurate relative masses, distances, and orbital speeds
Orbital trails that visualize each planet's path
Toggleable zoom (press Z) to switch between a wide solar-system view and a closer view
Built entirely with Python's standard math library and Pygame, no external physics engine