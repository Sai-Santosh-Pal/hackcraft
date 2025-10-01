from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random 
from perlin import PerlinNoise

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
    if key == 'q':
        application.quit()


def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        punch.play()
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)
    update_chunks()

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
            if key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])
            elif key == 'left mouse down':
                destroy(self)

# --- Chunked Terrain Generation ---
CHUNK_SIZE = 8
RENDER_DISTANCE = 1  # in chunks (so 5x5 chunks loaded around player)
MAX_HEIGHT = 10
perlin = PerlinNoise(seed=42)

loaded_chunks = {}

def chunk_key(x, z):
    return (x // CHUNK_SIZE, z // CHUNK_SIZE)

def generate_chunk(cx, cz):
    if (cx, cz) in loaded_chunks:
        return
    voxels = []
    for x in range(cx * CHUNK_SIZE, (cx + 1) * CHUNK_SIZE):
        for z in range(cz * CHUNK_SIZE, (cz + 1) * CHUNK_SIZE):
            height = int((perlin.noise(x * 0.1, z * 0.1) + 1) * (MAX_HEIGHT // 2))
            for y in range(height):
                Voxel(position=(x, y, z))
    loaded_chunks[(cx, cz)] = voxels

def unload_far_chunks(player_cx, player_cz):
    to_unload = []
    for (cx, cz) in loaded_chunks:
        if abs(cx - player_cx) > RENDER_DISTANCE or abs(cz - player_cz) > RENDER_DISTANCE:
            to_unload.append((cx, cz))
    for key in to_unload:
        for v in loaded_chunks[key]:
            destroy(v)
        del loaded_chunks[key]

def update_chunks():
    px, pz = int(player.x), int(player.z)
    pcx, pcz = px // CHUNK_SIZE, pz // CHUNK_SIZE
    # Load nearby chunks
    for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            generate_chunk(pcx + dx, pcz + dz)
    # Unload far chunks
    unload_far_chunks(pcx, pcz)

# Center player spawn
center_x = 0
center_z = 0
center_y = int((perlin.noise(center_x * 0.1, center_z * 0.1) + 1) * (MAX_HEIGHT // 2)) + 3
player = FirstPersonController()
player.position = (center_x, center_y, center_z)

player.gravity = 0.5
player.mouse_sensitivity = Vec2(40, 40)
player.jump_height = 2.5
player.speed = 6
player.jump_up_duration = 0.3

update_chunks()

app.run()