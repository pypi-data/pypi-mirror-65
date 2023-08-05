import yaml
from gibson2.core.physics.robot_locomotors import Turtlebot
from gibson2.core.simulator import Simulator
from gibson2.core.physics.scene import BuildingScene, StadiumScene
from gibson2.utils.utils import parse_config
import pytest
import pybullet as p
import numpy as np
import os
import gibson2

class Demo(object):
    def __init__(self):
        self.download_assets()
        
    def download_assets(self):
        if not os.path.exists(gibson2.assets_path):
            os.system('wget https://storage.googleapis.com/gibsonassets/assets_gibson_v2.tar.gz -O /tmp/assets_gibson_v2.tar.gz')
            os.system('tar -zxf /tmp/assets_gibson_v2.tar.gz --directory {}'.format(os.path.dirname(gibson2.assets_path)))

        if not os.path.exists(gibson2.dataset_path):
            os.makedirs(gibson2.dataset_path)
        if not os.path.exists(os.path.join(gibson2.dataset_path, 'Rs')):
            os.system('wget https://storage.googleapis.com/gibson_scenes/Rs.tar.gz -O /tmp/Rs.tar.gz')
            os.system('tar -zxf /tmp/Rs.tar.gz --directory {}'.format(gibson2.dataset_path))
        if not os.path.exists(os.path.join(gibson2.assets_path, 'turtlebot_p2p_nav_house.yaml')):
            os.system('wget https://storage.googleapis.com/gibson_scenes/turtlebot_p2p_nav_house.yaml \
            -O {}/turtlebot_p2p_nav_house.yaml'.format(gibson2.assets_path))


    def run_demo(self):
        config = parse_config(os.path.join(gibson2.assets_path,'turtlebot_p2p_nav_house.yaml'))
        
        s = Simulator(mode='gui', image_width=700, image_height=700)
        scene = BuildingScene('Rs')
        s.import_scene(scene)
        turtlebot = Turtlebot(config)
        s.import_robot(turtlebot)
        
        for i in range(1000):
            turtlebot.apply_action([0.1,0.5])
            s.step()

        s.disconnect()

if __name__ == "__main__":
    Demo().run_demo()