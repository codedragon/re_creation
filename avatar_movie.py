from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from movie_data import MovieData
from panda3d.core import Point3, LineSegs, TransparencyAttrib
from math import radians, cos, sin


class AvatarWorld(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        # set to record movie
        self.record = True
        #self.record = False
        movie_name = '../movies/frames/avatar/avatar_1191'

        data = MovieData()
        # bring in data that we will use
        self.avatar_pos = [[j/2 for j in i] for i in data.avatar_pos]
        self.avatar_pt = data.avatar_pt
        self.fruit_status = data.fruit_status
        self.fruit_status_ts = data.fruit_status_ts
        self.fruit_pos = data.fruit_pos
        self.trial_mark = data.trial_mark
        self.alpha = data.alpha

        # really should pull this from the config file (distance_goal)
        # everything is at 1/2 size
        self.goal_radius = 3/2
        # Things that can affect camera:
        # options resolution resW resH
        self.base = ShowBase()
        props = WindowProperties()
        props.setSize(600, 600)
        self.base.win.requestProperties(props)

        border = LineSegs()
        border.setThickness(2.0)
        #corner = 600/100 * 5/6
        corner = 5.5
        print corner
        border.moveTo(corner, 25, corner)
        border.drawTo(corner, 25, -corner)
        border.drawTo(-corner, 25, -corner)
        border.drawTo(-corner, 25, corner)
        border.drawTo(corner, 25, corner)
        self.base.render.attachNewNode(border.create(True))

        # background color doesn't show up anyway
        #base.setBackgroundColor(115 / 255, 115 / 255, 115 / 255)

        self.last_avt = self.avatar_pos.pop()
        #base.cam.setPos(Point3(points[0], points[1], points[2]))
        #base.cam.setH(self.avatar_h.pop(0))
        #self.avatar_ht.pop(0)
        self.avatar_pt.pop()
        self.avatar_node = []
        self.alpha_circle_node = []

        self.fruitModel = {}
        print('fruit', self.fruit_pos)

        for k, v in self.fruit_pos.iteritems():
            #print('i', i)
            print('k', k)
            #print('v', v)
            if 'banana' in k:
                self.fruitModel[k] = self.base.loader.loadModel('models/ball')
                self.fruitModel[k].setScale(0.5)
                self.fruitModel[k].setColor(1, 1, 0, 1)
            elif 'cherry' in k:
                self.fruitModel[k] = self.base.loader.loadModel('models/ball')
                self.fruitModel[k].setScale(0.5)
                self.fruitModel[k].setColor(1, 0, 0, 1)
            # position = self.fruit_pos[k]['position'].pop(0)
            # print position
            heading = v['head']
            #print heading
            # self.fruitModel[k].setPos(
            #     Point3(float(position[0]), float(position[1]), float(position[2])))

            self.fruitModel[k].setH(float(heading))
            self.fruitModel[k].reparentTo(self.base.render)
            # assume all bananas stashed to start
            #self.fruitModel[k].stash()
            if k in data.alpha:
                print 'set alpha'
                self.alpha_node_path = self.fruitModel[k]
                self.alpha_node_path.setTransparency(TransparencyAttrib.MAlpha)

        if self.record:
            self.movie_task = self.base.movie(movie_name, 200, 30, 'png', 4)

        #self.accept("space", base.taskMgr.add, [self.frame_loop, "frame_loop"])
        self.gameTask = taskMgr.add(self.frame_loop, "frame_loop")

        self.gameTask.last = 0         # Task time of the last frame

        # start the clock at 1 second before the official start so has time to load
        #self.gameTask.game_time = start_time - 100

    def frame_loop(self, task):
        #dt = task.time - task.last
        #task.last = task.time
        if self.avatar_pt:
            self.update_avt_p(task.time)
        else:
            # if we aren't moving the avatar anymore, assume done
            print 'done'
            return task.done
        if self.fruit_status_ts:
            self.update_fruit(task.time)
        if self.trial_mark and self.trial_mark[-1] < task.time:
            self.move_fruit()
        return task.cont

    def update_avt_p(self, t_time):
        avt = LineSegs()
        avt.setThickness(5)
        avt.setColor(1, 1, 1)
        group_avatar = []
        while self.avatar_pt[-1] < t_time:
            group_avatar.append(self.avatar_pos.pop())
            #print points
            self.avatar_pt.pop()
            if not self.avatar_pt:
                break
        #print('positions', group_avatar)
        if group_avatar:
            avt.moveTo(self.last_avt[0], 25, self.last_avt[1])
            self.last_avt = group_avatar[0]
            for i in group_avatar:
                #print(i[0], i[1], i[2])
                avt.drawTo(i[0], 25, i[1])
            self.avatar_node.append(self.base.render.attachNewNode(avt.create()))
        if self.trial_mark[-1] < t_time:
            print 'remove node'
            for i in self.avatar_node:
                i.detachNode()
            #old_color = avt.getVertexColor(-1)
            #print old_color
            #old_color[0] += 0.2
            #avt.setColor(old_color)

    def update_fruit(self, t_time):
        # print self.avatar_pos[-1]
        while self.fruit_status_ts[-1] < t_time:
            current_list = self.fruit_status.pop()
            print current_list
            # list goes: fruit name, what happens, how much
            if current_list[1] == 'alpha':
                self.alpha_node_path.setAlphaScale(float(current_list[2]))
                #if float(current_list[2]) < 1:
            if current_list[1] == 'stash':
                if current_list[2] == 'True':
                    self.fruitModel[current_list[0]].stash()
                    # want if recall fruit turns off, circle goes away
                    # if another fruit turns off, and the next fruit to
                    # have an event is the alpha fruit, then
                    # circle appears
                    # this is almost certainly problematic for gobananas data
                    # with alpha fruit, maybe
                    print self.fruit_status[-1]
                    if current_list[0] in self.alpha:
                        print 'erase circle'
                        self.erase_circle()
                    elif self.fruit_status[-1][0] in self.alpha:
                        print 'make circle'
                        self.make_circle()
                else:
                    print 'unstash'
                    self.fruitModel[current_list[0]].unstash()
            #         print self.fruitModel[current_list[0]].isStashed()
            self.fruit_status_ts.pop()
            if not self.fruit_status_ts:
                break

    def move_fruit(self):
        print 'move fruit'
        for k, v in self.fruit_pos.iteritems():
            print('k', k)
            print ('position', v['position'][0])
            # we did not reverse the lists in the dictionary, since pain in the ass, and
            # they are likely to be short. so taking from the front
            position = v['position'].pop(0)
            #print('popped this position', position)
            position = [float(x)/2 for x in position]
            print position
            self.fruitModel[k].setPos(
                Point3(float(position[0]), 25, float(position[1])))
            #print('after pop', self.fruit_pos)

        self.trial_mark.pop()

    def make_circle(self):
        alpha_circle = LineSegs()
        alpha_circle.setThickness(2.0)
        alpha_circle.setColor(1, 1, 0, 1)
        angle_radians = radians(360)
        alpha_pos = self.alpha_node_path.getPos()
        print alpha_pos
        for i in range(50):
            a = angle_radians * i / 49
            y = self.goal_radius * sin(a)
            x = self.goal_radius * cos(a)
            alpha_circle.drawTo((x + alpha_pos[0], 25, y + alpha_pos[2]))
        self.alpha_circle_node.append(self.base.render.attachNewNode(alpha_circle.create()))

    def erase_circle(self):
        for i in self.alpha_circle_node:
            i.detachNode()

if __name__ == "__main__":
    AW = AvatarWorld()
    AW.base.run()
