from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3
from panda3d.core import globalClock
from math import pi, sin, cos
from direct.task import Task
import pickle


class BananaWorld(DirectObject):
    def __init__(self):

        with open('../play_data/pickle_data') as input:
            banana_pos = pickle.load(input)
            #print(banana_pos)
            banana_h = pickle.load(input)
            #print(banana_h)
            gone_bananas = pickle.load(input)
            #print(gone_bananas)
            avatar_h = float(pickle.load(input))
            #print(avatar_h)
            apl = pickle.load(input)
            #print(avatar_pos)

        avatar_pos = Point3(float(apl[0]), float(apl[1]), float(apl[2]))
        #config =
        #data_file =
        #time_stamp =
        # using log.txt in this directory (gobananas), Yummy banana09
        #avatar_head = -23.0306647431 
        #avatar_pos = Point3(-0.499429, 4.01372, 1)
        #banana_pos = Point3(-0.461612, 4.1383, 1)
        #banana_h = 35

        # using giz_bananarchy.txt in this directory Yummy banana4
        #avatar_h = 32.6150996909
        #avatar_pos = Point3(-2.53202, 3.98558, 1)
        #banana_pos = Point3(-2.88193, 4.38051, 1)
        #banana_h = -418

        # Things that can affect camera:
        # options resolution resW resH
        base = ShowBase()
        lens = PerspectiveLens()
        # Fov is set in config for 60
        lens.setFov(60)
        # aspectratio should be same as window size
        # this was for 800x600
        # field of view 60 46.8264...
        # aspect ratio 1.3333
        lens.setAspectRatio(800.0 / 600.0)
        base.cam.node().setLens(lens)
        print lens.getFov()
        print lens.getAspectRatio()
        # set near to be same as avatar's radius
        lens.setNear(0.1)
        print 'near camera', lens.getNear()
        #base.cam.setPos(0, 0, 1)
        base.cam.setPos(avatar_pos)
        base.cam.setH(avatar_h)
        #self.smiley = base.loader.loadModel('smiley')
        #self.smiley.setPos(Point3(0, 6, 0))
        #self.smiley.reparentTo(render)
        #print 'smiley', self.smiley.getPos()
        terrainModel = base.loader.loadModel('../goBananas/models/towns/play_field.bam')
        terrainModel.setPos(Point3(0, 0, 0))
        terrainModel.reparentTo(render)
        #print 'terrain', terrainModel.getPos()
        skyModel = base.loader.loadModel('../goBananas/models/sky/sky.bam')
        skyModel.setPos(Point3(0, 0, 0))
        skyModel.setScale(1.6)
        skyModel.reparentTo(render)
        #print 'sky', skyModel.getPos()
        treeModel = base.loader.loadModel('../goBananas/models/trees/palmTree.bam')
        treeModel.setPos(Point3(13, 13, 0))
        treeModel.setScale(0.0175)
        treeModel.reparentTo(render)
        skyscraper = base.loader.loadModel('../goBananas/models/skyscraper/skyscraper.bam')
        skyscraper.setPos(Point3(-13, -13, 0))
        skyscraper.setScale(0.3)
        skyscraper.reparentTo(render)
        stLightModel = base.loader.loadModel('../goBananas/models/streetlight/streetlight.bam')
        stLightModel.setPos(Point3(-13, 13, 0))
        stLightModel.setScale(0.75)
        stLightModel.reparentTo(render)
        windmillModel = base.loader.loadModel('../goBananas/models/windmill/windmill.bam')
        windmillModel.setPos(Point3(13, -13, 0))
        windmillModel.setScale(0.2)
        windmillModel.setH(45)
        windmillModel.reparentTo(render)
        j = 0
        for i in banana_h:
            bananaModel = base.loader.loadModel('../goBananas/models/bananas/banana.bam')
            #print(j)
            #print(banana_pos[j])
            #print(banana_pos[j+1])
            #print(banana_pos[j+2])
            bananaModel.setPos(Point3(float(banana_pos[j]), float(banana_pos[j+1]), float(banana_pos[j+2])))
            j += 3
            bananaModel.setScale(0.5)
            bananaModel.setH(float(i))
            bananaModel.reparentTo(render)
        #coffeeModel = base.loader.loadModel('./db_models/stores/Coffee_Shop.bam')
        #coffeeModel.setPos(Point3(14.2, -2.7, 0))
        # uncomment if you want to spin around
        #base.taskMgr.add(self.frame_loop, "frame_loop")

        dt = globalClock.getDt()

    def move(self, dt):
        """
        Moves the object based on its current direction, speed,
        and the given dt. dt is in seconds.
        """
        self.setH(self.getH() + dt*self.getTurningSpeed())
        self.setPos(self.getPos() + self.direction()*dt*self.getLinearSpeed())

    def frame_loop(self, task):
        angleDegrees = task.time * 10.0
        angleRadians = angleDegrees * (pi / 180)
        base.cam.setPos(1 * sin(angleRadians), -1.0 * cos(angleRadians), 2)
        base.cam.setHpr(angleDegrees, 0, 0)
        #self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        #self.camera.setHpr(angleDegrees, 0, 0)

        return task.cont
if __name__ == "__main__":
    BW = BananaWorld()
    run()
