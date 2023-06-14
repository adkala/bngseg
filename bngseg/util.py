from beamngpy import BeamNGpy, Scenario, Vehicle

def quick_start(home_dir, user_dir, ip = 'localhost', port = '64526'):
    '''Convenience function for starting BeamNG server and simulator. Returns created BeamNG.* instance.'''
    bng = BeamNGpy('localhost', 64526, home=home_dir, user=user_dir)
    bng.open()
    return bng

def quick_scenario(bng, map, car_model, start_pos, start_rot_quat=(0,0,0,0), scenario_name="quick"):
    '''Convenience function for creating scenario. Returns scenario and spawned car.'''
    scenario = Scenario(map, scenario_name)
    car0 = Vehicle('car0', model=car_model)
    scenario.add_vehicle(car0, pos=start_pos, rot_quat=start_rot_quat)

    scenario.make(bng)
    bng.scenario.load(scenario)
    bng.scenario.start()

    return scenario, car0

