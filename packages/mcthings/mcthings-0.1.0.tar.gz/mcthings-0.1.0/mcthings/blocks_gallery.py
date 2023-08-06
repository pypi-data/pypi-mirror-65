import mcpi

from .object import Object


class BlocksGallery(Object):

    MAX_BLOCK_NUMBER = 247

    def build(self):
        """
        Show all possible block types in a line
        :return:
        """

        for i in range(1, self.MAX_BLOCK_NUMBER):
            self.server.setBlock(self.position.x + i, self.position.y,
                                 self.position.z, mcpi.block.Block(i))
