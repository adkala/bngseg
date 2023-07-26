import random
        
class CameraPosition:
    def __init__(self, pos, dir, up, fov=70, near_far_planes=(0.1, 1000), resolution=(224, 224), random=False):
        if random:
            if not (valid_random(pos) and valid_random(dir) and valid_random(up)):
                raise Exception("Coordinates not in valid format for random generation (lower_bound, upper_bound).")
        self.pos = pos
        self.dir = dir
        self.up = up
    
    def __call__(self):
        if random:
            pos = _generate_coor(*self.pos)
            dir = _generate_coor(*self.dir)
            up = _generate_coor(*self.up)
        return (pos, dir, up)

    def _valid_random(coor):
        return len(coor) == 2 and isinstance(coor[0], (tuple, list))

    def _generate_coor(lower, upper):
        return (random.uniform(lower[0], upper[0]), random.uniform(lower[1], upper[1]), random.uniform(lower[2], upper[2]))


class AnnotationCar:
    def __init__(self, car_model, camera_positions):
        self.car_model = car_model
        self.camera_positions = camera_positions


class AnnotationScenarioHistory:
    def __init__(self, base_map, annotated_map):
        self.base_map = base_map
        self.annotated_map = annotated_map
        self.locations = []

    def add(self, car, location, camera_positions):
        state = (car, location, camera_positions)
        self.locations.append(state)
        return state

    def save(self, path=None):
        if not path:
            prefix = ""
        else:
            prefix = path + r"\"
        path = prefix + ("%s_%s_%i" % (self.base_map, self.car, len(self.locations)))
        pickle.dump(self, path, protocol=0)
    
    def load(path):
        return pickle.load(path)


class AnnotationScenario:
    def __init__(self, base_map, annotated_map, cars: list[AnnotationCar], locations):
        self.base_map = base_map
        self.annotated_map = annotated_map
        self.cars = cars
        self.locations = locations
        
        self.history = AnnotationScenarioHistory(base_map, annotated_map)

        self.car_counter = 0
        self.loc_counter = 0

    def __iter__(self):
        return self

    def __next__():
        if self.loc_counter < len(locations):
            location = locations[self.loc_counter]
            self.loc_counter += 1
        else:
            self.loc_counter = 0
            self.car_counter += 1

        if self.car_counter < len(self.cars):
            return self.history.add(self.cars[car_counter].car_model, location, [cam() for cam in self.cars[car_counter].camera_positions])
        else:
            raise StopIteration