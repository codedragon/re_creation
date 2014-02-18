from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3, Vec4
from panda3d.core import Spotlight, AmbientLight
from direct.task import Task
import pickle


class BananaWorld(DirectObject):
    def __init__(self):

        with open('../play_data/pickle_data') as variable:
            start_time = pickle.load(variable)
            banana_pos = pickle.load(variable)
            #print(banana_pos)
            banana_h = pickle.load(variable)
            #print(banana_h)
            gone_bananas = pickle.load(variable)
            #print(gone_bananas)
            #print(int(gone_bananas[0][-2:]))
            self.avatar_h = float(pickle.load(variable)[-1])
            #print(avatar_h)
            apl = pickle.load(variable)[-1]
            #print(avatar_pos)

        self.avatar_pos = Point3(float(apl[0]), float(apl[1]), float(apl[2]))
        #print(self.avatar_pos)
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
        base.cam.setPos(self.avatar_pos)
        base.cam.setH(self.avatar_h)
        #self.smiley = base.loader.loadModel('smiley')
        #self.smiley.setPos(Point3(0, 6, 0))
        #self.smiley.reparentTo(render)
        #print 'smiley', self.smiley.getPos()
        terrainModel = base.loader.loadModel('../goBananas/models/towns/field.bam')
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

        # get rid of bananas already gone
        ind = range(len(banana_h))
        for i in gone_bananas:
            ind.pop(int(i[-2:]))

        for i in ind:
            #print('go', i)
            bananaModel = base.loader.loadModel('../goBananas/models/bananas/banana.bam')
            bananaModel.setPos(Point3(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2])))
            bananaModel.setScale(0.5)
            bananaModel.setH(float(banana_h[i]))
            bananaModel.reparentTo(render)

        # Create Ambient Light
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

        self.spot = Spotlight("spot")
        self.spot.setColor(Vec4(1, 1, 1, 1))
        self.lens = PerspectiveLens()
        self.lens.setFov(10)
        self.spot.setLens(self.lens)
        self.spotNP = render.attachNewNode(self.spot)
        render.setLight(self.spotNP)
        self.spotNP.setPos(self.avatar_pos)
        print('spotlight position', self.avatar_pos)
        self.spotNP.setHpr(90, 5, 90)

        # hit the space bar if you want to spin around
        self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        
    def frame_loop(self, task):
        # spin in a circle
        angleDegrees = task.time * 10.0
        base.cam.setHpr(self.avatar_h + angleDegrees, 0, 0)
        return task.cont

if __name__ == "__main__":
    BW = BananaWorld()
    run()
