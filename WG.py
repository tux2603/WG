import pyglet
from SpriteLibraries import Sprite


gameWindow = pyglet.window.Window(width=640, height=480, fullscreen=True)
fps_display = pyglet.window.FPSDisplay(window=gameWindow)
mainBatch = pyglet.graphics.Batch()
player = None
faceImage = None

updates = 0

# function to load the resources
def load():
    # images
    global faceImage

    # Sprites
    global player

    # Set the resource path
    pyglet.resource.path = ['resources']
    pyglet.resource.reindex()

    faceImage = pyglet.resource.image('images/face.png')
    player = Sprite(faceImage, batch=mainBatch)
    player.setSpeedAndDirection(1/60, 45)

@gameWindow.event
def on_draw():
    gameWindow.clear()
    fps_display.draw()
    print("Drawing stuff")
    mainBatch.draw()

def update(dt):
    global updates
    player.setSpeedAndDirection(10, updates)
    player.move()

    updates += 1
    pass


if __name__ == '__main__':
    load()
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()

    


