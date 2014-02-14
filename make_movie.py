from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3
from direct.task import Task
import pickle


class BananaWorld(DirectObject):
    def __init__(self):

        with open('../play_data/pickle_data') as variable:
            start_time = int(pickle.load(variable))
            if start_time == 0:
                print('This movie starts from the beginning of the file.'
                      'Is this really what you intended?')
            banana_pos = pickle.load(variable)
            #print(banana_pos)
            banana_h = pickle.load(variable)
            #print(banana_h)
            gone_bananas = pickle.load(variable)
            #print(gone_bananas)
            #print(int(gone_bananas[0][-2:]))
            avatar_h = pickle.load(variable)
            #print(avatar_h)
            avatar_pos = pickle.load(variable)
            #print('before', self.avatar_pos)
            avatar_ht = pickle.load(variable)
            avatar_pt = pickle.load(variable)
            banana_ts = pickle.load(variable)
            eye_data = pickle.load(variable)
            eye_ts = pickle.load(variable)

        self.avatar_ht = [float(i) for i in avatar_ht]
        self.avatar_pt = [float(i) for i in avatar_pt]
        self.avatar_h = [float(i) for i in avatar_h]
        self.avatar_pos = [[float(j) for j in i] for i in avatar_pos]
        self.banana_ts = [float(i) for i in banana_ts]
        self.gone_bananas = [int(i[-2:]) for i in gone_bananas]
        self.eye_data = [[float(j) for j in i] for i in eye_data]
        self.eye_ts = [float(i) for i in eye_ts]
        print(self.eye_ts)
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

        points = self.avatar_pos.pop(0)
        base.cam.setPos(Point3(points[0], points[1], points[2]))
        base.cam.setH(self.avatar_h.pop(0))
        self.avatar_ht.pop(0)
        self.avatar_pt.pop(0)

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

        # if we are not starting at the beginning of the trial, some of the bananas may
        # already be gone. Create them, and then stash them, so the index still refers to
        # the correct banana

        bananas = range(len(banana_h))
        self.bananaModel = []

        for i in bananas:
            #print('i', i)
            self.bananaModel.append(base.loader.loadModel('../goBananas/models/bananas/banana.bam'))
            self.bananaModel[i].setPos(Point3(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2])))
            self.bananaModel[i].setScale(0.5)
            self.bananaModel[i].setH(float(banana_h[i]))
            self.bananaModel[i].reparentTo(render)

        for i, j in enumerate(self.banana_ts):
            if j < start_time:
                self.bananaModel[self.gone_bananas.pop(i)].stash()
                self.banana_ts.pop(i)

        #self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame
        #dt = globalClock.getDt()
        # start the clock at 1 second before the official start so has time to load
        self.gameTask.game_time = start_time - 100
        #print('start', self.gameTask.game_time)
        #print('head start', self.avatar_ht[0])
        #print('increment', (1 / 60) * 1000000)

    def frame_loop(self, task):
        #print('loop')
        # assume 60 Hz for original game, so draw everything that happens every 1/60 of a second.
        # time is in microseconds
        task.game_time += (1 / 60) * 1000
        #print(task.game_time)
        # check to see if anything has happened.
        i = 0
        while i < len(self.avatar_ht):
            #print(self.avatar_ht[i])
            #print(task.game_time)
            if self.avatar_ht[i] < task.game_time:
                #print('change direction')
                base.cam.setH(self.avatar_h.pop(i))
                self.avatar_ht.pop(i)
            else:
                #print('break')
                break

        while i < len(self.avatar_pt):
            if self.avatar_pt[i] < task.game_time:
                #print('move')
                #print(self.avatar_pt[i])
                points = self.avatar_pos.pop(i)
                #print points
                base.cam.setPos(Point3(points[0], points[1], points[2]))
                #base.cam.setPos(Point3(self.avatar_pos.pop(i), self.avatar_pos.pop(i+1), self.avatar_pos.pop(i+2)))
                self.avatar_pt.pop(i)
            else:
                #print('break2')
                break

        while i < len(self.banana_ts):
            if self.banana_ts[i] < task.game_time:
                #print('ok')
                #print(self.banana_ts[i])
                #print(task.game_time)
                #print(self.gone_bananas[i])
                self.bananaModel[self.gone_bananas.pop(i)].stash()
                self.banana_ts.pop(i)
            else:
                break

        while i < len(self.eye_ts):
            if self.eye_ts[i] < task.game_time:
                print(self.eye_data[i][0])
                print(self.eye_data.pop(i))
                self.eye_ts.pop(i)
            else:
                break

        #dt = task.time - task.last
        #task.last = task.time
        # look to see what happened during actual game.
        return task.cont

if __name__ == "__main__":
    BW = BananaWorld()
    run()
