from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3, LineSegs
from direct.task import Task
import pickle


class BananaWorld(DirectObject):
    def __init__(self):

        with open('../movies/data/bananarchy_movie_1') as variable:
            res = pickle.load(variable)
            start_time = int(pickle.load(variable))
            if start_time == 0:
                message = """This data is for a single frame, please use a time_stamp
                      rather than zero for the starting time"""
                raise StartError(message)
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
            #print('before', avatar_pos)
            avatar_ht = pickle.load(variable)
            avatar_pt = pickle.load(variable)
            banana_ts = pickle.load(variable)
            eye_data = pickle.load(variable)
            eye_ts = pickle.load(variable)
            lfp_data = pickle.load(variable)

        # make zero the start time, change to seconds (from milliseconds)
        self.avatar_ht = [(float(i) - start_time) / 1000 for i in avatar_ht]
        self.avatar_pt = [(float(i) - start_time) / 1000 for i in avatar_pt]
        self.banana_ts = [(float(i) - start_time) / 1000 for i in banana_ts]
        self.eye_ts = [(float(i) - start_time) / 1000 for i in eye_ts]

        # non-time variables still need to be converted from strings
        print(res)
        resolution = [int(i) for i in res]
        self.avatar_h = [float(i) for i in avatar_h]
        self.avatar_pos = [[float(j) for j in i] for i in avatar_pos]

        #print(gone_bananas[0])
        # bananarchy data and gobananas data slightly different here
        if len(gone_bananas[0]) == 7:
            self.gone_bananas = [int(i[-1:]) for i in gone_bananas]
        else:
            self.gone_bananas = [int(i[-2:]) for i in gone_bananas]

        self.lfp_data = [float(i) for i in lfp_data]
        #print('size lfp', len(self.lfp_data))

        #print('gone', self.gone_bananas)
        #print('bananas', banana_pos)
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
        movie_res = [800, 600]
        lens.setAspectRatio(800.0 / 600.0)
        base.cam.node().setLens(lens)
        print('Fov', lens.getFov())
        print('Aspect Ratio', lens.getAspectRatio())
        # set near to be same as avatar's radius
        lens.setNear(0.1)
        print('near camera', lens.getNear())
        #base.cam.setPos(0, 0, 1)
        #print('x', base.win.getXSize())
        #print('y', base.win.getYSize())
        # when doing the calibration task I used the orthographic lens with normal render,
        # so the origin was in the center, but when using pixel2d the origin is in the top
        # left corner, so we must move the coordinate system to the right and down by half
        # the screen
        #
        eye_factor = [movie_res[0]/resolution[0], movie_res[1]/resolution[1]]
        #print('eye factor', eye_factor)
        self.eye_data = []
        for i in eye_data:
            x = (float(i[0]) * eye_factor[0]) + (base.win.getXSize() / 2)
            y = (float(i[1]) * eye_factor[1]) - (base.win.getYSize() / 2)
            self.eye_data.append((x, y))
            #print self.eye_data

        # for eye trace and lfp trace
        self.eyes = []
        self.lfp = []
        #print(len(self.eye_data))
        self.last_eye = self.eye_data.pop(0)
        #print(len(self.eye_data))
        self.last_eye_ts = self.eye_ts.pop(0)
        self.gen_eye_pos = self.get_data(self.eye_data)
        self.gen_eye_ts = self.get_data(self.eye_ts)

        # need to adjust y position for lfp
        self.lfp_gain = 0.1
        self.lfp_offset = -500
        self.last_lfp = (self.lfp_data.pop(0) * self.lfp_gain) + self.lfp_offset
        self.gen_lfp = self.get_data(self.lfp_data)
        self.last_lfp_x = 100
        self.lfp_test = 1

        points = self.avatar_pos.pop(0)
        base.cam.setPos(Point3(points[0], points[1], points[2]))
        base.cam.setH(self.avatar_h.pop(0))
        self.avatar_ht.pop(0)
        self.avatar_pt.pop(0)

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
            self.bananaModel[i].setPos(
                Point3(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2])))
            self.bananaModel[i].setScale(0.5)
            self.bananaModel[i].setH(float(banana_h[i]))
            self.bananaModel[i].reparentTo(render)

        for i, j in enumerate(self.banana_ts):
            if j < start_time:
                self.bananaModel[self.gone_bananas.pop(i)].stash()
                self.banana_ts.pop(i)

        #self.movie_task = base.movie('../movies/frames/movie_14_2_12', 5, 30, 'png', 4)

        #self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame

        # start the clock at 1 second before the official start so has time to load
        self.gameTask.game_time = start_time - 100
        #print('start', self.gameTask.game_time)
        #print('head start', self.avatar_ht[0])
        #print('increment', (1 / 60) * 1000000)

    def frame_loop(self, task):
        dt = task.time - task.last
        task.last = task.time
        #print('time', task.time)
        # check to see if anything has happened.
        if len(self.avatar_pt) > 0:
            self.update_avt_p(task.time)
        if len(self.avatar_ht) > 0:
            self.update_avt_h(task.time)
        if len(self.banana_ts) > 0 and self.banana_ts[0] < task.time:
            self.update_banana()
        self.update_eye(task.time)
        self.update_LFP(dt)
        return task.cont

    def get_data(self, data):
        for item in data:
            yield item

    def update_avt_h(self, t_time):
        while self.avatar_ht[0] < t_time:
            if len(self.avatar_ht) == 1:
                break
            #print(self.avatar_ht[i])
            #print(task.game_time)
            #print('change direction')
            base.cam.setH(self.avatar_h.pop(0))
            self.avatar_ht.pop(0)

    def update_avt_p(self, t_time):
        while self.avatar_pt[0] < t_time:
            if len(self.avatar_pt) == 1:
                break
            #print('move')
            #print(self.avatar_pt[i])
            points = self.avatar_pos.pop(0)
            #print points
            base.cam.setPos(Point3(points[0], points[1], points[2]))
            self.avatar_pt.pop(0)

    def update_banana(self):
        #print(self.banana_ts[0])
        #print('gone', self.gone_bananas[0])
        self.bananaModel[self.gone_bananas.pop(0)].stash()
        self.banana_ts.pop(0)

    def update_LFP(self, dt):
        # lfp data is taken at 1000Hz, and dt is the number of seconds since
        # the last frame was flipped, so plot number of points = dt * 1000
        lfp = LineSegs()
        lfp.setThickness(2.0)
        lfp.moveTo(self.last_lfp_x, 55, self.last_lfp)
        #print('points to plot', int(dt * 1000))
        self.lfp_test += int(dt * 1000)
        #print('points so far', self.lfp_test)
        for i in range(int(dt * 1000)):
            try:
                self.last_lfp = (next(self.gen_lfp) * self.lfp_gain) + self.lfp_offset
                self.last_lfp_x += 0.05
                lfp.drawTo(self.last_lfp_x, 55, self.last_lfp)
            except StopIteration:
                #print('done with lfp')
                break

        node = pixel2d.attachNewNode(lfp.create())
        self.lfp.append(node)
        # get rid of lfp trace from a while ago..
        while len(self.lfp) > 500:
            self.lfp[0].removeNode()
            self.lfp.pop(0)

    def update_eye(self, t_time):
        eye = LineSegs()
        eye.setThickness(2.0)
        #print('last_eye', self.last_eye)
        eye.moveTo(self.last_eye[0], 55, self.last_eye[1])
        while self.last_eye_ts < t_time:
            try:
                self.last_eye = next(self.gen_eye_pos)
                self.last_eye_ts = next(self.gen_eye_ts)
                eye.drawTo(self.last_eye[0], 55, self.last_eye[1])
            except StopIteration:
                self.last_eye_ts = t_time + 10000
                #print('break')
                #taskMgr.remove('self.movie_task')
                break
        node = pixel2d.attachNewNode(eye.create())
        self.eyes.append(node)
        #print(self.eye_data[i][0])
        #print(self.eye_data.pop(i))

        # get rid of eye position from a while ago..
        while len(self.eyes) > 10:
            self.eyes[0].removeNode()
            self.eyes.pop(0)

class StartError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

if __name__ == "__main__":
    BW = BananaWorld()
    run()
