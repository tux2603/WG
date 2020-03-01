import pyglet
import numpy as np
from SpriteLibraries import Sprite
from pyglet.window import key

GRAVITY = -2.0

gameWindow = pyglet.window.Window(width=800, height=600, fullscreen=False)
keyboard = key.KeyStateHandler()
fpsDisplay = None

# Sprite batches
backgroundBatch = None
terrainBatch = None
mainBatch = None
foregroundBatch = None

terrainData = (
    {
        "fileName": None,
        "batch": None,
        "blocksTop": False,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": False,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtBackground.png",
        "batch": terrainBatch,
        "blocksTop": False,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": False,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirt.png",
        "batch": terrainBatch,
        "blocksTop": False,
        "blocksBottom": True,
        "blocksLeft": True,
        "blocksRight": True,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtTop.png",
        "batch": terrainBatch,
        "blocksTop": True,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": False,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtLeft.png",
        "batch": terrainBatch,
        "blocksTop": False,
        "blocksBottom": False,
        "blocksLeft": True,
        "blocksRight": False,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtRight.png",
        "batch": terrainBatch,
        "blocksTop": False,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": True,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtTopLeft.png",
        "batch": terrainBatch,
        "blocksTop": True,
        "blocksBottom": False,
        "blocksLeft": True,
        "blocksRight": False,
        "buoyancy": 0.0
    },
    {
        "fileName": "dirtTopRight.png",
        "batch": terrainBatch,
        "blocksTop": True,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": True,
        "buoyancy": 0.0
    },
    {
        "fileName": "water.png",
        "batch": terrainBatch,
        "blocksTop": False,
        "blocksBottom": False,
        "blocksLeft": False,
        "blocksRight": False,
        "buoyancy": 0.45
    }
)

# Define sprites
player = None
plunger1 = None
plunger2 = None
door = None
ground = [[]]


# Define images
faceImage = None
cloudImage = None
doorImage = None
faceImage = None
gooieImage = None
ivyStalkImage = None
ivyImage = None
jellyImage = None
pixelImage = None
plungerImage = None
terrainImages = []

updates = 0

# function to load the resources


def load():
    # images
    global faceImage, cloudImage, doorImage, faceImage, gooieImage, ivyStalkImage, ivyImage, jellyImage, pixelImage, plungerImage, terrainImages

    # Sprites
    global player

    # Set the resource path
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    # Load the sprite data stuff
    faceImage = pyglet.resource.image('images/face.png')

    # Load in terrain images
    terrainImages.append(None)
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtBackground.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirt.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtTop.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtLeft.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtRight.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtTopLeft.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/dirtTopRight.png'))
    terrainImages.append(pyglet.resource.image(
        'images/terrainImages/water.png'))

    player = Sprite(faceImage, batch=mainBatch)
    player.setSpeedAndDirection(1/60, 45)

    # Displays a testing bar of different terrain images
    # TODO: Would terrain be better handled as one giant/multiple large textures rendered at level load?
    # for i in range(len(terrainImages)):
    #     if not terrainImages[i] is None:
    #         ground[0].append(Sprite(terrainImages[i], batch=(backgroundBatch if i != 8 else foregroundBatch), x = i * 32, y=0))

    player.y = 50


@gameWindow.event
def on_draw():
    gameWindow.clear()
    backgroundBatch.draw()
    terrainBatch.draw()
    mainBatch.draw()
    foregroundBatch.draw()

    fpsDisplay.draw()


def update(dt):
    global updates

    updatePlaying(dt)

    updates += 1


def updatePlaying(dt):
    # TODO: Update the monsters

    # TODO: Get player collision status
    onGround = player.y <= 0.2
    inWater = False
    collidedRight = False
    collidedLeft = False
    dontBounce = False
    hitHead = False

    blockBuoyancy = 0.0

    ##########################################################################
    ######       Update player velocities based on keyboard input       ######
    ##########################################################################

    # Move left
    if (keyboard[pyglet.window.key.LEFT] or keyboard[key.A]) and not collidedLeft:
        player.x -= 2

    # Moving right
    if (keyboard[key.RIGHT] or keyboard[key.D]) and not collidedRight:
        player.x += 2

    # Moving up/jumping
    if keyboard[key.UP] or keyboard[key.W] or keyboard[key.SPACE]:
        # mark that the player shouldn't bounce
        dontBounce = True
        if onGround:
            player.accelerate((0, 5))
        elif inWater:
            player.setVelocityY(2)

    # Moving down
    if keyboard[key.DOWN] or keyboard[key.S]:
        if inWater:
            player.setVelocityY(-2)

    # TODO Shoot plungers
    # TODO Rappel towards plungers
    # TODO Disappear plungers when you're done

    # float
    player.accelerate((0, blockBuoyancy))

    # If you're not on the ground, fall
    if not onGround:
        player.accelerate((0, -0.2))

    # If you are on the ground, bounce
    elif not dontBounce:
        player.setVelocity((player._velocity[0] / 5, player._velocity[1] / -5))

    # If you hit grass on the side of things, bounce
    if collidedLeft or collidedRight:
        player.setVelocity((-player._velocity[0] / 2, player._velocity[1]))

    # If you hit you're head... OUCH!
    if hitHead:
        player.setVelocity((player._velocity[0], -player._velocity[1] / 2))

    # TODO Make camera track the face, make the face and camera stay inside the world

    # Move the face
    player.move()

    # TODO Move the plungers

    # TODO Move the clouds

if __name__ == '__main__':
    # Set the window background color
    pyglet.gl.glClearColor(0.58823, 0.84313, 0.94117, 1.0)

    # Initialize game variables and stuff
    fpsDisplay = pyglet.window.FPSDisplay(window=gameWindow)

    gameWindow.push_handlers(keyboard)

    backgroundBatch = pyglet.graphics.Batch()
    terrainBatch = pyglet.graphics.Batch()
    mainBatch = pyglet.graphics.Batch()
    foregroundBatch = pyglet.graphics.Batch()

    # TODO Initialize the camera
    # TODO Set a cross hair for the mouse?

    load()
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
