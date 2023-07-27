import random
import pickle

class HistoryState:
    def __init__(self, car, location, camera_positions):
        self.car = car
        self.location = location
        self.camera_positions = camera_positions

    def __getstate__(self):
        return (self.car, self.location, self.camera_positions)

    def __setstate__(self, i):
        self.car = i[0]
        self.location = i[1]
        self.camera_positions = i[2]

    def __repr__(self):
        return str(self.__getstate__())

class CameraPosition:
    def __init__(self, pos, dir, up, fov=70, near_far_planes=(0.1, 1000), resolution=(224, 224), random=False):
        if random:
            raise Exception("Random camera positions currently not supported.")
        self.pos = pos
        self.dir = dir
        self.up = up
        self.fov = fov
        self.near_far_planes = near_far_planes
        self.resolution = resolution
        self.random = random
            
    
    def __call__(self):
        return (self.pos, self.dir, self.up, self.fov, self.near_far_planes, self.resolution)

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
        state = HistoryState(car, location, camera_positions)
        self.locations.append(state)
        return state

    def save(self, path=None):
        if not path:
            prefix = ""
        else:
            prefix = path + "\\"
        path = prefix + ("%s_%i.bin" % (self.base_map, len(self.locations)))
        with open(path, 'wb') as fp:
            pickle.dump(self, fp, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load(path):
        with open(path, 'rb') as fp:
            return pickle.load(fp)
        

class AnnotationScenario:
    def __init__(self, base_map, annotated_map, cars: list[AnnotationCar], locations):
        self.base_map = base_map
        self.annotated_map = annotated_map
        self.cars = cars
        self.locations = locations

        self.history = AnnotationScenarioHistory(base_map, annotated_map)
        
        car_counter = 0
        loc_counter = 0
        
        while car_counter < len(self.cars):
            self.history.add(self.cars[car_counter].car_model, locations[loc_counter], [cam() for cam in self.cars[car_counter].camera_positions])
            
            if loc_counter < len(locations) - 1:
                loc_counter += 1
            else:
                loc_counter = 0
                car_counter += 1

