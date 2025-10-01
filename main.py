from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random 

app = Ursina()

block_id = 0
blocks = [
    load_texture('assets/grass.png'),
    load_texture('assets/grass.png'), # so that when i click 1 it selects grass from the hotbar
    load_texture('assets/stone.png'),
    load_texture('assets/lava.png'),
    load_texture('assets/gold.png'),
]

hotbar = [0, ['grass','stone','lava','gold']]

punch = Audio('assets/punch', autoplay=False)

sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/sky.jpg'),
    scale=500,
    double_sided=True
)

hand = Entity(
    parent=camera.ui,
    model='assets/block',
    texture=blocks[block_id],
    scale=0.2,
    rotation=Vec3(-10, -10, 10),
    position=Vec2(0.6, -0.6)
)

def update_hotbar():
    # Remove previous hotbar items
    for e in camera.ui.children[:]:
        if hasattr(e, 'is_hotbar_item') and e.is_hotbar_item:
            destroy(e)

    selected_block = hotbar[0]
    for i in range(1, len(hotbar[1])+1):
        item = Entity(
            parent=camera.ui,
            model='quad',
            texture=load_texture(f'block_icons/{hotbar[1][i-1]}.png'),
            scale=0.1,
            color=color.white if i == selected_block + 1 else color.gray,
            position=Vec2(-0.35 + i * 0.15, -0.4)
        )
        item.is_hotbar_item = True

update_hotbar()

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        if key != '0': 
            hotbar[0] = block_id - 1
            hand.texture = blocks[block_id]
            print(hotbar)
            update_hotbar()


def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=blocks[0]):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.hsv(0, 0, random.uniform(0.9, 1.0)),
            # highlight_color=color.lime,
            scale=0.5
        )

    def input(self, key):
        # update_hotbar()
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == 'right mouse down':
                destroy(self)

for z in range(16):
    for x in range (16):
        voxel = Voxel(position=(x,0,z)) #random.randrange(0,2)

player = FirstPersonController()

player.gravity = 0.5
player.mouse_sensitivity = Vec2(40, 40)
player.jump_height = 2.5
player.speed = 6
player.jump_up_duration = 0.3

app.run()