import pygame
import math

# Start pygame so we can open a window and draw things
pygame.init()

# Size of our window (width x height in pixels)
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

# This helps control how fast our simulation runs (frames per second)
clock = pygame.time.Clock()

# A special number used in physics to calculate gravity between objects
G = 6.67430e-11  # Gravitational constant

# Real distances in space are HUGE (millions of km), so we shrink them down
# to fit nicely on our small screen using these scale numbers
SCALE = 6e-11        # Normal zoomed-out view
ZOOM_SCALE = 1e-9    # Zoomed-in view (makes things look bigger/closer)

# Each "tick" of our simulation pretends that 1 day has passed in real life
DT = 86400  # number of seconds in 1 day

# This tells us whether we are currently zoomed in or not
zoomed = False


# This class represents one space object (like a planet or the sun)
class Body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y          # Starting position (x, y)
        self.vx, self.vy = vx, vy      # Starting speed (velocity) in x and y directions
        self.mass = mass               # How heavy the object is
        self.radius = radius           # How big the circle looks on screen (just for drawing)
        self.color = color             # What color the planet is drawn in
        self.trail = []                # Stores past positions so we can draw a trail behind the planet

    def update_position(self, bodies):
        # We start with zero force, then add up the pull from every other planet/sun
        fx = fy = 0

        for other in bodies:
            if other != self:  # Don't calculate gravity with itself
                # Find the distance between this body and the other body
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx*dx + dy*dy)  # Straight-line distance

                if r > 0:
                    # Formula: F = G * (m1 * m2) / r^2
                    # This tells us how strong the pull of gravity is
                    f = G * self.mass * other.mass / (r*r)

                    # Split that force into x and y directions (like an arrow pointing toward the other body)
                    fx += f * dx / r
                    fy += f * dy / r

        # Formula: a = F / m  (based on F = ma)
        # This tells us how much we should speed up because of gravity
        ax = fx / self.mass
        ay = fy / self.mass

        # Update our speed using the acceleration (speed changes over time)
        self.vx += ax * DT
        self.vy += ay * DT

        # Update our position using our new speed (position changes over time)
        self.x += self.vx * DT
        self.y += self.vy * DT

        # Pick the right zoom level to use when converting real-world position to screen pixels
        current_scale = ZOOM_SCALE if zoomed else SCALE

        # Save this position to our trail list so we can draw a line showing where we've been
        self.trail.append((int(self.x * current_scale + WIDTH//2), int(self.y * current_scale + HEIGHT//2)))

        # Only keep the last 200 trail points, so the trail doesn't get too long
        if len(self.trail) > 200:
            self.trail.pop(0)

    def draw(self, screen):
        # Draw the trail (the path the planet has traveled) as a thin gray line
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)

        # Pick the right zoom level for drawing
        current_scale = ZOOM_SCALE if zoomed else SCALE

        # Convert the real-world x, y position into a pixel position on the screen
        # (WIDTH//2 and HEIGHT//2 puts the center of the screen at position 0,0 in space)
        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)

        # Draw the planet as a filled circle
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


# Create all our space objects: the Sun and the planets
# Each one gets: starting x, starting y, starting vx, starting vy, mass, drawing size, color
bodies = [
    Body(0, 0, 0, 0, 1.989e30, 8, (255, 255, 0)),        # Sun  (1.989e30 kg, 8 pixel radius (not used in calculations, just visual))
    Body(5.79e10, 0, 0, 47360, 3.301e23, 2, (169, 169, 169)),   # Mercury
    Body(1.082e11, 0, 0, 35020, 4.867e24, 3, (255, 165, 0)),    # Venus
    Body(1.496e11, 0, 0, 29780, 5.972e24, 4, (0, 100, 255)),    # Earth
    Body(279e11, 0, 0, 24077, 6.39e23, 3, (255, 100, 0)),       # Mars
    Body(7.786e11, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Jupiter
    Body(1.432e12, 0, 0, 9680, 5.683e26, 5, (250, 200, 100)),   # Saturn
    Body(2.867e12, 0, 0, 6810, 8.681e25, 4, (100, 200, 255)),   # Uranus
    Body(4.515e12, 0, 0, 5430, 1.024e26, 4, (0, 0, 255)),       # Neptune
    Body(5.906e12, 0, 0, 4670, 1.309e22, 2, (150, 100, 50)),    # Pluto
]

# This keeps our program running until we close the window
running = True

while running:
    # Check for any events, like closing the window or pressing a key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Stop the loop so the program can close

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoomed = not zoomed  # Pressing "Z" switches between zoomed in/out

            # Whenever any key is pressed, clear all the trails so they redraw fresh
            for body in bodies:
                body.trail = []

    # Clear the screen by painting it all black before drawing the new frame
    screen.fill((0, 0, 0))

    # For every planet/sun: calculate its new position, then draw it
    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)

    # Show everything we just drew on the screen
    pygame.display.flip()

    # Limit the simulation to 60 frames per second so it doesn't run too fast
    clock.tick(60)

# Close the pygame window properly when the loop ends
pygame.quit() 