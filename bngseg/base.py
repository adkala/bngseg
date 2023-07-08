from beamngpy import Vehicle
from beamngpy.sensors import Camera
from pathlib import Path
from tqdm import tqdm
import beamngpy
import time
import random
import datetime


def record_points_from_car(v: Vehicle, interval=1, countdown=True):
    """Record points in simulator given vehicle. Interval is in seconds."""
    points = []
    if countdown:
        for i in range(5, -1, -1):
            print("Starting in " + str(i) + "...")
            time.sleep(1)
    print("Press CTRL+C to stop recording...")
    try:
        while True:
            points.append(v.get_center_of_gravity())
            time.sleep(interval)
    except KeyboardInterrupt:
        return points


def generate_random_point(points, radius=4):  # not optimized
    """Generate random point within a given radius from any point within points list."""
    point = random.choice(points)
    offsets = (random.uniform(-radius, radius), random.uniform(-radius, radius), 0.5)
    rot_quat = beamngpy.quat.angle_to_quat((0, 0, random.uniform(-180, 180)))
    return (
        point[0] + offsets[0],
        point[1] + offsets[1],
        point[2] + offsets[2],
    ), rot_quat


def attach_cameras(
    camera_positions: list[
        tuple[
            tuple[float, float, float],
            tuple[float, float, float],
            tuple[float, float, float],
            float,
        ]
    ],
    bng,
    v: Vehicle,
    near_far_planes=(0.1, 1000),
    resolution=(224, 224),
):
    """Attach cameras to vehicle in BeamNG instance. `camera_positions` are tuples with position, direction, up, and fov [pos, dir, and up in (x, y, z) format, fov a number]."""
    cameras = []
    for i, (pos, dir, up, fov) in enumerate(camera_positions):
        camera = Camera(
            "camera" + str(i),
            bng,
            v,
            requested_update_time=-1.0,
            is_using_shared_memory=False,
            pos=pos,
            dir=dir,
            up=up,
            field_of_view_y=fov,
            near_far_planes=near_far_planes,
            resolution=resolution,
            is_render_annotations=True,
            is_render_instance=True,
            is_render_depth=True,
        )
        cameras.append(camera)
    return cameras


def generate_images(
    v: Vehicle,
    locations,
    cameras,
    annotated=False,
):
    """Generate images given vehicle, locations, and cameras. Set `annotated` to True if generating annotated images."""
    images = {}
    for i, (pos, dir) in tqdm(enumerate(locations), desc="Images:"):
        v.teleport(pos, rot_quat=dir)
        for j, cam in enumerate(cameras):
            base_image = cam.get_full_poll_request()[
                "colour" if not annotated else "annotation"
            ]
            name = "{}_{}".format(i, j)
            images[name] = base_image
    return images


def pair_images(base: dict, annotated: dict):
    """Pairs base and annotated images of same name. Key is name and value is image for both dicts."""
    images = {}
    for name in base:
        images[name] = {"base": base[name], "annotated": annotated[name]}
    return images


def save_images(paired_images, path: str = None):
    """Save images according to date and time. All images are going to be in a folder labeled ddmmYYYYHHMMSS (date, month, year, hours, minutes, seconds). All images are labeled using the scheme `{location #}_{camera #}_{b for base else a for annotated}`.

    In the same folder, info on location and camera setup can be found in the file `setup.txt`.

    The folder will be created in the present working directory (pwd). Specify where to save folder in `path` parameter relative to the pwd.

    `paired_images` should be output from `pair_images` function.
    """
    folder_name = datetime.now().strftime("%d%m%Y%H%M%S")
    if path:
        folder = Path(path) / folder_name
    else:
        folder = Path(folder_name)
    folder.mkdir(parents=True, exist_ok=True)
    for i in paired_images:
        paired_images[i]["base"].save(folder / (i + "_b.png"))
        paired_images[i]["annotated"].save(folder / (i + "_a.png"))
    return folder_name


def generate_paired_images_and_save(
    v: Vehicle, locations, cameras, path: str = None, verbose=True
):
    """Convenience function for generating paired images and saving."""
    base_images = generate_images(v, locations, cameras, verbose=verbose)
    input("Switch track for annotation mode. Press Enter when complete...")
    annotated_images = generate_images(
        v, locations, cameras, annotated=True, verbose=verbose
    )
    return save_images(pair_images(base_images, annotated_images), path=path)
