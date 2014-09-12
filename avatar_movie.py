from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from panda3d.core import Point3, LineSegs, TransparencyAttrib
from direct.task import Task
import pickle


class AvatarWorld(DirectObject):
    def __init__(self):
        # set to record movie
        #self.record = True
        self.record = False
        movie_name = '../movies/frames/avatar/avatar_1191'

        with open('../movies/data/JN_circle_array') as variable:
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
        # and now make it official
        start_time = 0

        # non-time variables still need to be converted from strings
        #print(res)
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
        # Things that can affect camera:
        # options resolution resW resH
        base = ShowBase()
        props = WindowProperties()
        props.setSize(600, 600)
        base.win.requestProperties(props)

        border = LineSegs()
        border.setThickness(2.0)
        corner = 600/100 * 5/6
        border.moveTo(corner, 25, corner)
        border.drawTo(corner, 25, -corner)
        border.drawTo(-corner, 25, -corner)
        border.drawTo(-corner, 25, corner)
        border.drawTo(corner, 25, corner)
        base.render.attachNewNode(border.create(True))
        #lens = PerspectiveLens()
        # Fov is set in config for 60
        #lens.setFov(60)
        # aspectratio should be same as window size
        # this was for 800x600
        # field of view 60 46.8264...
        # aspect ratio 1.3333
        #movie_res = [800, 600]
        #lens.setAspectRatio(800.0 / 600.0)
        #base.cam.node().setLens(lens)
        #print('Fov', lens.getFov())
        #print('Aspect Ratio', lens.getAspectRatio())
        # set near to be same as avatar's radius
        #lens.setNear(0.1)
        #print('near camera', lens.getNear())

        # background color doesn't show up anyway
        #base.setBackgroundColor(115 / 255, 115 / 255, 115 / 255)

        self.last_avt = self.avatar_pos.pop(0)
        #base.cam.setPos(Point3(points[0], points[1], points[2]))
        #base.cam.setH(self.avatar_h.pop(0))
        #self.avatar_ht.pop(0)
        self.avatar_pt.pop(0)

        bananas = range(len(banana_h))
        #print(bananas)
        self.bananaModel = []

        for i in bananas:
            #print(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2]))
            self.bananaModel.append(base.loader.loadModel('models/ball'))
            self.bananaModel[i].setPos(
                Point3(float(banana_pos[i][0]), 25, float(banana_pos[i][1])))
            #Point3(float(banana_pos[i][0]), float(banana_pos[i][1]), float(banana_pos[i][2])))
            self.bananaModel[i].setScale(0.5)
            self.bananaModel[i].setColor(1, 1, 0, 1)
            self.bananaModel[i].reparentTo(render)

        for i, j in enumerate(self.banana_ts):
            if j < start_time:
                #print('stashed')
                self.bananaModel[self.gone_bananas.pop(i)].stash()
                self.banana_ts.pop(i)

        if self.record:
            self.movie_task = base.movie(movie_name, 200, 30, 'png', 4)

        #self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame

        # start the clock at 1 second before the official start so has time to load
        self.gameTask.game_time = start_time - 100

    def frame_loop(self, task):
        dt = task.time - task.last
        task.last = task.time
        if len(self.avatar_pt) > 0:
            self.update_avt_p(task.time)
        if len(self.banana_ts) > 0 and self.banana_ts[0] < task.time:
            self.update_banana()
        return task.cont

    def update_avt_p(self, t_time):
        avt = LineSegs()
        avt.setThickness(5)
        avt.setColor(1, 1, 1)
        group_avatar = []
        while self.avatar_pt[0] < t_time:
            if len(self.avatar_pt) == 1:
                break
            #print('move')
            #print(self.avatar_pt[i])
            group_avatar.append(self.avatar_pos.pop(0))
            #print points
            self.avatar_pt.pop(0)
        #print('positions', group_avatar)
        if group_avatar:
            avt.moveTo(self.last_avt[0], 25, self.last_avt[1])
            self.last_avt = group_avatar[-1]
            for i in group_avatar:
                #print(i[0], i[1], i[2])
                avt.drawTo(i[0], 25, i[1])
            node = render.attachNewNode(avt.create())

    def update_banana(self):
        #print(self.banana_ts[0])
        #print('gone', self.gone_bananas[0])
        self.bananaModel[self.gone_bananas.pop(0)].stash()
        self.banana_ts.pop(0)


if __name__ == "__main__":
    AW = AvatarWorld()
    run()
