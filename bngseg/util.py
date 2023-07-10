from beamngpy import BeamNGpy, Scenario, Vehicle
import pickle
import matplotlib.pyplot as plt


def quick_start(home_dir, user_dir, ip="localhost", port="64526"):
    """Convenience function for starting BeamNG server and simulator. Returns created BeamNG.* instance."""
    bng = BeamNGpy("localhost", 64526, home=home_dir, user=user_dir)
    bng.open()
    return bng


def quick_scenario(
    bng,
    map,
    car_model,
    start_pos,
    start_rot_quat=(0, 0, 0, 0),
    scenario_name="quick",
    new_scenario=True,
):
    """Convenience function for creating scenario. Returns scenario and spawned car."""
    scenario = Scenario(map, scenario_name)
    car0 = Vehicle("car0", model=car_model)
    scenario.add_vehicle(car0, pos=start_pos, rot_quat=start_rot_quat)

    if new_scenario:
        scenario.make(bng)
    bng.scenario.load(scenario)
    bng.scenario.start()

    return scenario, car0


def serialize_points(points: list, path="points.bin"):
    with open(path, "wb") as outp:
        pickle.dump(points, outp, pickle.HIGHEST_PROTOCOL)


def deserialize_points(path="points.bin"):
    with open(path, "rb") as inp:
        return pickle.load(inp)


def save_image_generation_info(camera_positions, car_positions, path):
    with open(path, "w") as f:
        f.write("# camera positions\n")
        for pos, i in enumerate(camera_positions):
            f.write("%i: %s\n" % (i, str(pos)))
        f.write("\n# locations")
        for pos, i in enumerate(car_positions):
            f.write("%i: %s\n" % (i, str(pos)))


def poll_and_show_images(camera):
    images = camera.get_full_poll_request()
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(images["colour"])
    ax[1].imshow(images["annotation"])
    plt.show()
