import mcpi

from .object import Object
from .wall import Wall


class TownWall(Object):

    height = 3
    wall_space = 5
    thick = 1
    town = None

    def build(self):

        if self.town is None:
            raise RuntimeError("Town is not defined")

        # Create a wall around the town: 4 walls are needed

        # The height is the same always
        wall_init_y = self.position.y

        wall_width = self.town.houses * (self.town.house_width + self.town.space) - self.town.space \
                     + 2 * self.wall_space

        wall_length = self.town.house_length + 2 * self.wall_space

        # First wall
        wall1_init_x = self.position.x
        wall1_init_z = self.position.z
        wall_pos = mcpi.vec3.Vec3(wall1_init_x, wall_init_y, wall1_init_z)
        wall = Wall(self.block, wall_pos, self.server)
        wall.height = self.height
        wall.length = self.thick
        wall.width = wall_width + self.thick
        wall.build()

        # Second wall
        wall2_init_x = wall1_init_x + (self.thick-1)
        wall2_init_z = wall1_init_z + wall.width
        wall_pos = mcpi.vec3.Vec3(wall2_init_x, wall_init_y, wall2_init_z)
        wall = Wall(self.block, wall_pos, self.server)
        wall.height = self.height
        wall.length = -(wall_length+2*self.thick-1)
        wall.width = self.thick
        wall.build()

        # Third wall
        wall3_init_x = wall2_init_x + (wall.length-1)
        wall3_init_z = wall2_init_z
        wall_pos = mcpi.vec3.Vec3(wall3_init_x, wall_init_y, wall3_init_z)
        wall = Wall(self.block, wall_pos, self.server)
        wall.height = self.height
        wall.length = self.thick
        wall.width = -(wall_width+self.thick-1)
        wall.build()

        # Fourth wall
        wall4_init_x = wall3_init_x
        wall4_init_z = wall3_init_z + (wall.width-1)
        wall_pos = mcpi.vec3.Vec3(wall4_init_x, wall_init_y, wall4_init_z)
        wall = Wall(self.block, wall_pos, self.server)
        wall.height = self.height
        wall.length = wall_length + self.thick + self.thick
        wall.width = self.thick
        wall.build()
