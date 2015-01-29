from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3, LineSegs, TransparencyAttrib
from direct.task import Task
import pickle
import random


class BananaWorld(DirectObject):
    def __init__(self):
        hack = True  # using heading to identify which banana at which position
        # set to record movie
        self.record = True
        # make sure directory exists
        movie_name = '../movies/frames/GR_training2/GR_training2'
        use_eye_data = False
        use_lfp_data = False
        environ = 'original'
        #environ = 'circle'

        with open('../movies/data/GR_training2') as variable:
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
            lfp_data = []
            while True:
                try:
                    lfp_data.append(pickle.load(variable))
                except EOFError:
                    break

        if not use_eye_data:
            eye_data = []
            eye_ts = []
        num_bananas = len(banana_pos)
        #print test
        # hack! not using banana_h for heading, making that up. banana_h is now the
        # key to which banana is at which position, because not saving in any particular order

        if hack:
            banana_key = banana_h
            banana_h = [random.choice(range(360)) for i in range(num_bananas)]
        print banana_h
        print banana_key
        # make zero the start time, change to seconds (from milliseconds)
        self.avatar_ht = [(float(i) - start_time) / 1000 for i in avatar_ht]
        self.avatar_pt = [(float(i) - start_time) / 1000 for i in avatar_pt]
        self.banana_ts = [(float(i) - start_time) / 1000 for i in banana_ts]
        self.eye_ts = [(float(i) - start_time) / 1000 for i in eye_ts]
        # and now make it official...
        start_time = 0

        # non-time variables still need to be converted from strings
        #print(res)
        resolution = [int(i) for i in res]
        self.avatar_h = [float(i) for i in avatar_h]
        self.avatar_pos = [[float(j) for j in i] for i in avatar_pos]

        #print(gone_bananas[0])
        # bananarchy data and gobananas data slightly different here,
        # and gobananas also changed to accomodate over 99 bananas...
        if len(gone_bananas[0]) == 7:
            self.gone_bananas = [int(i[-1:]) for i in gone_bananas]
        elif len(gone_bananas[0]) == 8:
            self.gone_bananas = [int(i[-2:]) for i in gone_bananas]
        else:
            self.gone_bananas = [int(i[-3:]) for i in gone_bananas]
        if hack:
            self.banana_key = [int(i[-3:]) for i in banana_key]

        print self.gone_bananas
        self.lfp = []  # container for lfp traces
        self.lfp_data = []
        for data in lfp_data:
            float_data = [float(i) for i in data]
            self.lfp_data.append(float_data)
            self.lfp.append([])

        #print('gone', self.gone_bananas)
        #print('bananas', banana_pos)
        # Things that can affect camera:
        # options resolution resW resH
        base = ShowBase()
        lens = PerspectiveLens()
        # Fov is set in config for 60
        lens.setFov(60)
        # aspect ratio should be same as window size
        # this was for 800x600
        # field of view 60 46.8264...
        # aspect ratio 1.3333
        movie_res = [800, 600]
        # set aspect ratio to original game
        lens.setAspectRatio(1280.0 / 800.0)
        #lens.setAspectRatio(800.0 / 600.0)
        base.cam.node().setLens(lens)
        print('Fov', lens.getFov())
        print('Aspect Ratio', lens.getAspectRatio())
        # set near to be same as avatar's radius
        # affects how close you get to the bananas
        lens.setNear(0.1)
        #print('near camera', lens.getNear())
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
        # calibration not very good...
        fudge_factor_x = 50
        fudge_factor_y = 80

        self.eye_data = []
        for i in eye_data:
            x = (float(i[0]) * eye_factor[0]) + (base.win.getXSize() / 2) + fudge_factor_x
            y = (float(i[1]) * eye_factor[1]) - (base.win.getYSize() / 2) + fudge_factor_y
            self.eye_data.append((x, y))
            #print self.eye_data

        # container for eye trace
        self.eyes = []

        #print(len(self.eye_data))
        self.last_eye_ts = None
        if use_eye_data:
            self.last_eye = self.eye_data.pop(0)
            #print(len(self.eye_data))
            self.last_eye_ts = self.eye_ts.pop(0)
            self.gen_eye_pos = self.get_data(self.eye_data)
            self.gen_eye_ts = self.get_data(self.eye_ts)

        # need to adjust y position for lfp
        self.lfp_gain = 0.05
        # lfp_offset determines where each trace is on the y axis
        lfp_offset = -500  # bottom
        self.lfp_offset = []
        #self.lfp_offset = -100  # top of screen
        self.last_lfp = []
        self.gen_lfp = []
        for data in self.lfp_data:
            self.lfp_offset.append(lfp_offset)
            self.last_lfp.append([(data.pop(0) * self.lfp_gain) + lfp_offset])
            lfp_offset += 100
            self.gen_lfp.append(self.get_data(data))

        # last_lfp_x determines where on the x axis we start the lfp trace
        self.start_x_trace = 50

        points = self.avatar_pos.pop(0)
        base.cam.setPos(Point3(points[0], points[1], points[2]))
        base.cam.setH(self.avatar_h.pop(0))
        self.avatar_ht.pop(0)
        self.avatar_pt.pop(0)

        self.set_environment(environ)

        #load bananas
        # if we are not starting at the beginning of the trial, some of the bananas may
        # already be gone. Create them, and then stash them, so the index still refers to
        # the correct banana

        #bananas = range(len(banana_h))
        self.bananaModel = []

        for i, k in enumerate(self.banana_key):
            print('i', i)
            self.bananaModel.append(base.loader.loadModel('../goBananas/models/bananas/banana.bam'))
            self.bananaModel[i].setPos(
                Point3(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2])))
            self.bananaModel[i].setScale(0.5)
            self.bananaModel[i].setH(float(banana_h[i]))
            self.bananaModel[i].reparentTo(render)

        #print('start', start_time)
        for i, j in enumerate(self.banana_ts):
            if j < start_time:
                print('stashed')
                print(j)
                self.bananaModel[self.gone_bananas.pop(i)].stash()
                self.banana_ts.pop(i)

        if self.record:
            print('make movie', movie_name)
            self.movie_task = base.movie(movie_name, 150, 30, 'png', 4)

        #self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame

        #print('start', self.gameTask.game_time)
        #print('head start', self.avatar_ht[0])
        #print('increment', (1 / 60) * 1000000)

    def set_environment(self, environ):

        if environ == 'original':
            terrainModel = base.loader.loadModel('../goBananas/models/play_space/field.bam')
            skyModel = base.loader.loadModel('../goBananas/models/sky/sky.bam')
            skyModel.setPos(Point3(0, 0, 0))
            skyModel.setScale(1.6)
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
        elif environ == 'circle':
            terrainModel = base.loader.loadModel('../goBananas/models/new/round_courtyard2.bam')
            skyModel = base.loader.loadModel('../goBananas/models/new/sky_kahana.bam')
            skyModel.setPos(Point3(0, 0, -0.5))
            skyModel.setScale(Point3(2, 2, 4))

        terrainModel.setPos(Point3(0, 0, 0))
        terrainModel.reparentTo(render)
        #print 'terrain', terrainModel.getPos()
        skyModel.reparentTo(render)
        #print 'sky', skyModel.getPos()

        self.eye_spot = base.loader.loadModel("models/ball")
        #eye_texture = base.loader.loadTexture('textures/spotlight.png')
        #self.eye_spot.setTexture(eye_texture, 1)
        self.eye_spot.setScale(50)
        self.eye_spot.setTransparency(TransparencyAttrib.MAlpha)
        self.eye_spot.setColor(1, 1, 1, 0.3)

    def frame_loop(self, task):
        dt = task.time - task.last
        task.last = task.time
        #print('time', task.time)
        # check to see if anything has happened.
        if len(self.avatar_pt) > 0:
            self.update_avt_p(task.time)
        if len(self.avatar_ht) > 0:
            self.update_avt_h(task.time)
        if len(self.banana_ts) > 0 and self.banana_ts[0] < task.time - 0.5:
            self.update_banana()
        if self.last_eye_ts:
            self.update_eye(task.time)
        for ind, last_lfps in enumerate(self.last_lfp):
            self.update_LFP(dt, last_lfps, self.lfp[ind], self.lfp_offset[ind], self.gen_lfp[ind])
        return task.cont

    def get_data(self, data):
        for item in data:
            yield item

    def update_avt_h(self, t_time):
        while self.avatar_ht[0] < t_time:
            if len(self.avatar_ht) == 1:
                #print('avatar h done')
                break
            #print(self.avatar_ht[i])
            #print(task.game_time)
            #print('change direction')
            base.cam.setH(self.avatar_h.pop(0))
            self.avatar_ht.pop(0)

    def update_avt_p(self, t_time):
        while self.avatar_pt[0] < t_time:
            if len(self.avatar_pt) == 1:
                #print('avatar pos done')
                break
            #print('move')
            #print(self.avatar_pt[i])
            points = self.avatar_pos.pop(0)
            #print points
            base.cam.setPos(Point3(points[0], points[1], points[2]))
            self.avatar_pt.pop(0)

    def update_banana(self):
        #print(self.banana_ts[0])
        print('gone', self.gone_bananas[0])
        print self.avatar_pos[0]
        print('key', self.banana_key.index(self.gone_bananas[0]))
        print('gone_bananas', self.gone_bananas)
        now_banana = self.banana_key.index(self.gone_bananas[0])
        print('now banana', now_banana)
        self.gone_bananas.pop(0)
        print self.bananaModel[now_banana].getPos()
        self.bananaModel[now_banana].stash()
        self.banana_ts.pop(0)

    def update_LFP(self, dt, last_lfp, lfp_trace, offset, gen_lfp):
        # lfp data is taken at 1000Hz, and dt is the number of seconds since
        # the last frame was flipped, so plot number of points = dt * 1000
        lfp = LineSegs()
        lfp.setThickness(1.0)
        #print('points to plot', int(dt * 1000))
        #self.lfp_test += int(dt * 1000)
        #print('points so far', self.lfp_test)

        for i in range(int(dt * 1000)):
            try:
                last_lfp.append((next(gen_lfp) * self.lfp_gain) + offset)
                #last_lfp_x += 0.05
                # only plotting 200 data points at a time
                while len(last_lfp) > 3500:
                    last_lfp.pop(0)
            except StopIteration:
                #print('done with lfp')
                break

        if lfp_trace:
            lfp_trace[0].removeNode()
            lfp_trace.pop(0)
        lfp.moveTo(self.start_x_trace, 55, last_lfp[0])
        x = self.start_x_trace
        for i in last_lfp:
            x += .1
            lfp.drawTo(x, 55, i)
        node = pixel2d.attachNewNode(lfp.create())
        lfp_trace.append(node)

        # get rid of lfp trace from a while ago..
        #while len(self.lfp) > 50:
        #    self.lfp[0].removeNode()
        #    self.lfp.pop(0)

    def update_eye(self, t_time):
        #eye = LineSegs()
        #eye.setThickness(10.0)
        #print('last_eye', self.last_eye)

        group_eye = []
        while self.last_eye_ts < t_time:
            try:
                group_eye.append(next(self.gen_eye_pos))
                self.last_eye_ts = next(self.gen_eye_ts)
            except StopIteration:
                #make the next eye movement something crazy in the future
                self.last_eye_ts = t_time + 10000
                #print('break')
                taskMgr.remove('self.movie_task')
                break

        if group_eye:
            #eye.moveTo(self.last_eye[0], 55, self.last_eye[1])
            sum_x = 0
            sum_y = 0
            for i in group_eye:
                sum_x += i[0]
                sum_y += i[1]
            self.last_eye = [sum_x / len(group_eye), sum_y / len(group_eye)]

            self.eye_spot.setPos(self.last_eye[0], 55, self.last_eye[1])
            self.eye_spot.reparentTo(pixel2d)
            #if self.eyes:
            #    self.eyes[0].removeNode()
            #    self.eyes.pop(0)
            #eye.drawTo(self.last_eye[0], 55, self.last_eye[1])
            #node = pixel2d.attachNewNode(eye.create())
            #self.eyes.append(node)
        #print(self.eye_data[i][0])
        #print(self.eye_data.pop(i))

        # get rid of eye position from a while ago..
        #while len(self.eyes) > 1:
        #    self.eyes[0].removeNode()
        #    self.eyes.pop(0)


class StartError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

if __name__ == "__main__":
    BW = BananaWorld()
    run()
