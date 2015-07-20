from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import PerspectiveLens, Point3, LineSegs, TransparencyAttrib
from movie_data import MovieData
from collections import deque


class BananaWorld(DirectObject):
    def __init__(self, movie_data_file, record, use_eye_data=False, use_lfp_data=False):
        DirectObject.__init__(self)
        self.record = record
        # make sure directory exists
        movie_name = '../movies/frames/game/game'
        # environ = 'original'
        environ = 'circle'

        data = MovieData(movie_data_file, use_eye_data)

        # Things that can affect camera:
        # options resolution resW resH
        self.base = ShowBase()
        lens = PerspectiveLens()
        # Fov is set in config for 60
        lens.setFov(60)
        # aspect ratio should be same as window size
        # this was for 800x600
        # field of view 60 46.8264...
        # aspect ratio 1.3333
        movie_res = [800, 600]
        # set aspect ratio to original game
        #print resolution
        lens.setAspectRatio(data.resolution[0] / data.resolution[1])
        #print lens.getAspectRatio()
        #lens.setAspectRatio(800.0 / 600.0)
        self.base.cam.node().setLens(lens)
        # print('Fov', lens.getFov())
        # print('Aspect Ratio', lens.getAspectRatio())
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
        # covert resolution
        eye_factor = [movie_res[0]/data.resolution[0], movie_res[1]/data.resolution[1]]
        # print('move_res', movie_res)
        # print('actual movie res', self.base.win.getXSize(), self.base.win.getYSize())
        # print('data_res', data.resolution)
        # print('eye factor', eye_factor)
        # calibration not very good...
        #fudge_factor_x = 50
        #fudge_factor_y = 80
        fudge_factor_x = 0
        fudge_factor_y = 60
        self.eye_data = deque()
        self.last_eye_ts = None
        # since for eye_data we are looping and adding to the end of the list,
        # but then we will be pulling from the front of the list, we have a queue,
        # so let's use deque. (Other data was reversed in movie_data).
        if use_eye_data:
            for i in data.raw_eye_data:
                x = (float(i[0]) * eye_factor[0]) + (self.base.win.getXSize() / 2) + fudge_factor_x
                y = (float(i[1]) * eye_factor[1]) - (self.base.win.getYSize() / 2) + fudge_factor_y
                self.eye_data.append((x, y))
            #print self.eye_data
            # container for eye trace
            self.eyes = []
            #print(len(self.eye_data))
            # make generators for eye data
            self.last_eye = self.eye_data.popleft()
            #print(len(self.eye_data))
            # time stamps are all reversed, so can use normal pop and then assign directly,
            # like other time variables
            self.last_eye_ts = data.eye_ts.pop()
            self.eye_ts = data.eye_ts

        # need to adjust y position for lfp
        self.lfp_gain = 0.05
        # lfp_offset determines where each trace is on the y axis
        lfp_offset = -500  # bottom
        self.lfp_offset = []
        #self.lfp_offset = -100  # top of screen
        self.last_lfp = []
        self.gen_lfp = []
        # make a generator for lfp data
        # this code is a little silliness, and I'm popping a giant list from the wrong end
        # when I start plotting lfp again, fix this!
        if use_lfp_data:
            for data in data.lfp_data:
                self.lfp_offset.append(lfp_offset)
                self.last_lfp.append([(data.pop(0) * self.lfp_gain) + lfp_offset])
                lfp_offset += 100
                # self.gen_lfp.append(get_data(data))

        # last_lfp_x determines where on the x axis we start the lfp trace
        self.start_x_trace = 50

        # bring in data we care about.
        self.avatar_pos = data.avatar_pos
        self.avatar_pt = data.avatar_pt
        self.avatar_h = data.avatar_h
        self.avatar_ht = data.avatar_ht
        self.fruit_status = data.fruit_status
        self.fruit_status_ts = data.fruit_status_ts
        self.fruit_pos = data.fruit_pos
        self.fruit_pos_ts = data.fruit_pos_ts
        self.trial_mark = data.trial_mark

        print 'fruit pos timestamps', self.fruit_pos_ts
        # initialize other variables
        self.eye_spot = None

        # set starting point for avatar
        points = self.avatar_pos.pop()
        self.base.cam.setPos(Point3(points[0], points[1], points[2]))
        self.base.cam.setH(self.avatar_h.pop())
        self.avatar_ht.pop()
        self.avatar_pt.pop()

        # get last time stamp (first of list) for avatar to calculate length of movie
        # add half a second buffer.
        movie_length = self.avatar_ht[0] + 0.8
        print('movie length', movie_length)
        self.set_environment(environ)

        #load bananas
        # if we are not starting at the beginning of the trial, some of the bananas may
        # already be gone. Create them, and then stash them, so the index still refers to
        # the correct banana

        self.fruitModel = {}
        # print('fruit', self.fruit_pos)

        for k, v in self.fruit_pos.iteritems():
            #print('i', i)
            # print('k', k)
            #print('v', v)
            if 'banana' in k:
                self.fruitModel[k] = self.base.loader.loadModel('../goBananas/models/bananas/banana.bam')
                self.fruitModel[k].setScale(0.5)
            elif 'cherry' in k:
                self.fruitModel[k] = self.base.loader.loadModel('../goBananas/models/fruit/cherries.egg')
                self.fruitModel[k].setScale(0.08)
            # position = self.fruit_pos[k]['position'].pop(0)
            # print position
            heading = v['head']
            #print heading
            # self.fruitModel[k].setPos(
            #     Point3(float(position[0]), float(position[1]), float(position[2])))

            self.fruitModel[k].setH(float(heading))
            self.fruitModel[k].reparentTo(self.base.render)
            # assume all fruit stashed to start
            self.fruitModel[k].stash()
            if k in data.alpha:
                print 'set alpha', data.alpha
                self.alpha_node_path = self.fruitModel[k]
                self.alpha_node_path.setTransparency(TransparencyAttrib.MAlpha)

        if self.record:
            print('make movie', movie_name)
            self.movie_task = self.base.movie(movie_name, movie_length, 30, 'png', 4)

        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame

        #print('trialmarks', self.trial_mark)
        #print('start', self.gameTask.game_time)
        #print('head start', self.avatar_ht[-1])
        #print('increment', (1 / 60) * 1000000)

    def set_environment(self, environ):

        if environ == 'original':
            terrainModel = self.base.loader.loadModel('../goBananas/models/play_space/field.bam')
            skyModel = self.base.loader.loadModel('../goBananas/models/sky/sky.bam')
            skyModel.setPos(Point3(0, 0, 0))
            skyModel.setScale(1.6)
            treeModel = self.base.loader.loadModel('../goBananas/models/trees/palmTree.bam')
            treeModel.setPos(Point3(13, 13, 0))
            treeModel.setScale(0.0175)
            treeModel.reparentTo(self.base.render)
            skyscraper = self.base.loader.loadModel('../goBananas/models/skyscraper/skyscraper.bam')
            skyscraper.setPos(Point3(-13, -13, 0))
            skyscraper.setScale(0.3)
            skyscraper.reparentTo(self.base.render)
            stLightModel = self.base.loader.loadModel('../goBananas/models/streetlight/streetlight.bam')
            stLightModel.setPos(Point3(-13, 13, 0))
            stLightModel.setScale(0.75)
            stLightModel.reparentTo(self.base.render)
        elif environ == 'circle':
            terrainModel = self.base.loader.loadModel('../goBananas/models/play_space/round_courtyard.bam')
            skyModel = self.base.loader.loadModel('../goBananas/models/sky/sky_kahana2.bam')
            skyModel.setPos(Point3(0, 0, -0.5))
            skyModel.setScale(Point3(2, 2, 4))

        terrainModel.setPos(Point3(0, 0, 0))
        terrainModel.reparentTo(self.base.render)
        #print 'terrain', terrainModel.getPos()
        skyModel.reparentTo(self.base.render)
        #print 'sky', skyModel.getPos()

        self.eye_spot = self.base.loader.loadModel("models/ball")
        #eye_texture = base.loader.loadTexture('textures/spotlight.png')
        #self.eye_spot.setTexture(eye_texture, 1)
        self.eye_spot.setScale(50)
        self.eye_spot.setTransparency(TransparencyAttrib.MAlpha)
        self.eye_spot.setColor(1, 1, 1, 0.3)

    def frame_loop(self, task):
        dt = task.time - task.last
        task.last = task.time
        #print('time', task.time)
        #print('trial marker', self.trial_mark[-1])
        # check to see if anything has happened.
        # there is a position and heading for every time stamp for the avatar.
        if self.avatar_pt:
            self.update_avt_p(task.time)
        else:
            # if we aren't moving the avatar anymore, assume done
            print 'done'
            return task.done
        if self.avatar_ht:
            self.update_avt_h(task.time)
        if self.fruit_pos_ts:
            self.move_fruit(task.time)
        if self.fruit_status_ts:
            self.update_fruit(task.time)
        # if len(self.banana_ts) > 0 and self.banana_ts[0] < task.time - 0.5:
        #    self.update_banana()
        if self.last_eye_ts:
            self.update_eye(task.time)
        #if self.trial_mark and self.trial_mark[-1] < task.time:
        #    self.move_fruit()
        for ind, last_lfps in enumerate(self.last_lfp):
            self.update_LFP(dt, last_lfps, self.lfp[ind], self.lfp_offset[ind], self.gen_lfp[ind])
        return task.cont

    def update_avt_h(self, t_time):
        while self.avatar_ht[-1] < t_time:
            self.base.cam.setH(self.avatar_h.pop())
            self.avatar_ht.pop()
            if not self.avatar_ht:
                break

    def update_avt_p(self, t_time):
        # print('avatar', self.avatar_pt[-1], 'time', t_time)
        while self.avatar_pt[-1] < t_time:
            points = self.avatar_pos.pop()
            # print points
            self.base.cam.setPos(Point3(points[0], points[1], points[2]))
            self.avatar_pt.pop()
            if not self.avatar_pt:
                break

    def update_fruit(self, t_time):
        # print self.avatar_pos[-1]
        while self.fruit_status_ts[-1] < t_time:
            current_list = self.fruit_status.pop()
            # print current_list
            # list goes: fruit name, what happens, how much
            if current_list[1] == 'alpha':
                if float(current_list[2]) < 1:
                    self.alpha_node_path.setAlphaScale(float(current_list[2]))
            if current_list[1] == 'stash':
                if current_list[2] == 'True':
                    self.fruitModel[current_list[0]].stash()
                else:
                    # print 'unstash'
                    self.fruitModel[current_list[0]].unstash()
            #         print self.fruitModel[current_list[0]].isStashed()
            self.fruit_status_ts.pop()
            if not self.fruit_status_ts:
                break

    def move_fruit(self, t_time):
        # did not reverse, since pain in the ass, and likely not many
        # print 'position', self.fruit_pos_ts[0][0]
        # print 'delete' self.fruit_pos_ts
        # print 'time', t_time
        while self.fruit_pos_ts[0][0] < t_time:
            ts, fruit = self.fruit_pos_ts.pop(0)
            # print('current time stamp', ts)
            position = self.fruit_pos[fruit]['position'].pop(0)
            # print('move fruit', fruit, position)
            self.fruitModel[fruit].setPos(
                Point3(float(position[0]), float(position[1]), float(position[2])))
            # print('next timestamp', self.fruit_pos_ts[0])
            if not self.fruit_pos_ts:
                break

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
        node = self.base.pixel2d.attachNewNode(lfp.create())
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
        # get eye movements since the last frame
        while self.last_eye_ts < t_time:
            try:
                group_eye.append(self.eye_data.popleft())
                self.last_eye_ts = self.eye_ts.pop()
            except StopIteration:
                #make the next eye movement something crazy in the future
                self.last_eye_ts = t_time + 10000
                #print('break')
                taskMgr.remove('self.movie_task')
                break

        if group_eye:
            # plotting the average
            # have to sum in a loop, because tuples in a list
            #eye.moveTo(self.last_eye[0], 55, self.last_eye[1])
            sum_x = 0
            sum_y = 0
            for i in group_eye:
                sum_x += i[0]
                sum_y += i[1]
            self.last_eye = [sum_x / len(group_eye), sum_y / len(group_eye)]
            self.eye_spot.setPos(self.last_eye[0], 55, self.last_eye[1])
            self.eye_spot.reparentTo(self.base.pixel2d)


class StartError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

if __name__ == "__main__":
    BW = BananaWorld()
    BW.base.run()
