from __future__ import division
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties
from movie_data import MovieData
from panda3d.core import Point3, LineSegs, TransparencyAttrib
from direct.gui.OnscreenImage import OnscreenImage
from math import radians, cos, sin


class AvatarWorld(DirectObject):
    def __init__(self, datafile, record=True, distance_goal=None):
        DirectObject.__init__(self)

        movie_name = '../movies/frames/avatar/avatar'

        data = MovieData(datafile)
        # bring in data that we will use
        self.avatar_pos = [[j/2 for j in i] for i in data.avatar_pos]
        self.avatar_pt = data.avatar_pt
        self.fruit_status = data.fruit_status
        self.fruit_status_ts = data.fruit_status_ts
        self.fruit_pos = data.fruit_pos
        self.fruit_pos_ts = data.fruit_pos_ts
        self.trial_mark = data.trial_mark
        self.alpha = data.alpha
        # toggle to detect when a block of trials is finished
        self.block_done = False
        # print self.fruit_status
        # really should pull this from the config file (distance_goal)
        # everything is at 1/2 size
        if distance_goal:
            self.goal_radius = [i/2 for i in distance_goal]
        else:
            # total arbitrary guess
            self.goal_radius = [3/2, 3/2]
        # Things that can affect camera:
        # options resolution resW resH
        self.base = ShowBase()
        props = WindowProperties()
        # props.setSize(600, 600)
        self.base.win.requestProperties(props)

        border = LineSegs()
        border.setThickness(2.0)
        #corner = 600/100 * 5/6
        corner = 5.5
        # print corner
        # red
        border.setColor(1, 0, 0)
        border.moveTo(corner, 25, corner)
        border.drawTo(corner, 25, -corner)

        # purple
        border.setColor(1, 0, 1)
        border.moveTo(corner, 25, -corner)
        border.drawTo(-corner, 25, -corner)

        # white
        border.setColor(1, 1, 1)
        border.moveTo(-corner, 25, -corner)
        border.drawTo(-corner, 25, corner)

        # green
        border.setColor(0, 1, 0)
        border.moveTo(-corner, 25, corner)
        border.drawTo(corner, 25, corner)
        self.base.render.attachNewNode(border.create(True))

        imageObject = OnscreenImage(image='textures/lightpost.png',
                                    pos=(-0.9, 25, 0.9), scale=(0.06, 1, 0.08), color=(0.9, 0.9, 0.9, 0.8))
        imageObject.setTransparency(TransparencyAttrib.MAlpha)
        imageObject1 = OnscreenImage(image='textures/palm_tree.png',
                                    pos=(0.85, 25, 0.9), scale=0.09, color=(0.9, 0.9, 0.9, 0.8))
        imageObject1.setTransparency(TransparencyAttrib.MAlpha)
        imageObject2 = OnscreenImage(image='textures/transamerica_thumb.png',
                                    pos=(-0.9, 25, -0.9), scale=0.2, color=(0.9, 0.9, 0.9, 0.8))
        imageObject2.setTransparency(TransparencyAttrib.MAlpha)
        # background color doesn't show up anyway
        #base.setBackgroundColor(115 / 255, 115 / 255, 115 / 255)

        self.last_avt = self.avatar_pos.pop()
        #base.cam.setPos(Point3(points[0], points[1], points[2]))
        #base.cam.setH(self.avatar_h.pop(0))
        #self.avatar_ht.pop(0)
        self.avatar_pt.pop()
        # get last time stamp (first of list) for avatar to calculate length of movie
        # add half a second buffer.
        movie_length = self.avatar_pt[0] + 0.5
        print('movie length', movie_length)
        self.avatar_node = []
        self.avatar_color = [1, 1, 1]
        self.drawing_layer = 25
        self.alpha_circle_node = []

        self.fruitModel = {}
        # print('fruit', self.fruit_pos)

        for k, v in self.fruit_pos.iteritems():
            # print('i', i)
            # print('k', k)
            # print('v', v)
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
            # assume all fruit stashed to start
            self.fruitModel[k].stash()
            if k in data.alpha:
                # print 'set alpha'
                self.alpha_node_path = self.fruitModel[k]
                self.alpha_node_path.setTransparency(TransparencyAttrib.MAlpha)

        if record:
            self.movie_task = self.base.movie(movie_name, movie_length, 30, 'png', 4)

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
        if self.fruit_pos_ts:
            self.move_fruit(task.time)
        if self.fruit_status_ts:
            self.update_fruit(task.time)
        #if self.trial_mark and self.trial_mark[-1] <= task.time:
        #    self.move_fruit()
        return task.cont

    def update_avt_p(self, t_time):
        avt = LineSegs()
        avt.setThickness(5)
        avt.setColor(self.avatar_color[0], self.avatar_color[1], self.avatar_color[2])
        group_avatar = []
        while self.avatar_pt[-1] < t_time:
            group_avatar.append(self.avatar_pos.pop())
            # print points
            self.avatar_pt.pop()
            if not self.avatar_pt:
                break
        # print('positions', group_avatar)
        if group_avatar:
            avt.moveTo(self.last_avt[0], self.drawing_layer, self.last_avt[1])
            self.last_avt = group_avatar[0]
            for i in group_avatar:
                # print(i[0], i[1], i[2])
                avt.drawTo(i[0], self.drawing_layer, i[1])
            self.avatar_node.append(self.base.render.attachNewNode(avt.create()))

    def update_fruit(self, t_time):
        # print self.avatar_pos[-1]
        while self.fruit_status_ts[-1] < t_time:
            current_list = self.fruit_status.pop()
            # print current_list
            # print 'alpha', self.alpha
            # list goes: fruit name, what happens, how much
            if current_list[1] == 'alpha':
                self.alpha_node_path.setAlphaScale(float(current_list[2]))
                # if we are changing banana alpha to something less than 1, turn on circle
                if float(current_list[2]) == 0:
                    print 'make circle for invisible'
                    self.block_done = True
                    self.make_circle(1)
                    self.avatar_color = [0, 1, 1]
                elif float(current_list[2]) < 1:
                    print 'make circle for alpha'
                    self.make_circle(0)
            if current_list[1] == 'stash':
                if current_list[2] == 'True':
                    self.fruitModel[current_list[0]].stash()
                    # want if recall fruit turns off, circle goes away
                    # if another fruit turns off, and the next fruit to
                    # have an event is the alpha fruit, then
                    # circle appears
                    # this is almost certainly problematic for gobananas data
                    # with alpha fruit, maybe
                    # see what is next in line, if next is alpha and current is
                    # recall stashing,
                    # print self.fruit_status[-1]
                    # if stashing the recall fruit, erase the circle,
                    # return avatar line color to normal
                    if current_list[0] in self.alpha:
                        # print 'erase circle'
                        self.erase_circle()
                        self.avatar_color = [1, 1, 1]
                    # this is not true for newer data, but leaving it here for old data:
                    # no good way to tell the difference between an invisible recall fruit
                    # and a solid recall fruit, other than looking at timing. ugh. Brute force.
                    # can't use timing, self.fruit_status_ts[-1]
                    # if we are stashing a cherry, and the next thing to happen is alpha 1 and
                    # the next time stamp is not immediately, than must be invisible.
                    if current_list[0] not in self.alpha:
                        if self.fruit_status[-1][2] == '1':
                            # print 'next alpha?'
                            # print self.fruit_status_ts[-2] - self.fruit_status_ts[-1]
                            if self.fruit_status_ts[-2] - self.fruit_status_ts[-1] > 0.2:
                                print 'should only reach here with old data'
                                self.make_circle(1)
                                self.avatar_color = [0, 1, 1]
                else:
                    # print 'unstash'
                    self.fruitModel[current_list[0]].unstash()
                    # print self.fruitModel[current_list[0]].isStashed()
            self.fruit_status_ts.pop()
            if not self.fruit_status_ts:
                break

    def move_fruit(self, t_time):
        # did not reverse, since pain in the ass, and likely not many
        while self.fruit_pos_ts[0][0] < t_time:
            # whenever we draw fruit, make the drawing layer closer to the camera,
            # since otherwise which lines are on top is a bit random
            self.drawing_layer -= 0.01
            #print 'layer', self.drawing_layer
            ts, fruit = self.fruit_pos_ts.pop(0)
            # print('current time stamp', ts)
            position = self.fruit_pos[fruit]['position'].pop(0)
            # print('move fruit', fruit, position)
            self.fruitModel[fruit].setPos(
                Point3(float(position[0])/2, 25, float(position[1])/2))
            # print 'fruit pos ts', self.fruit_pos_ts
            # print 'time', t_time
            if not self.fruit_pos_ts:
                break

    def make_circle(self, radius_ind):
        alpha_circle = LineSegs()
        alpha_circle.setThickness(2.0)
        alpha_circle.setColor(1, 1, 0, 1)
        angle_radians = radians(360)
        alpha_pos = self.alpha_node_path.getPos()
        # print alpha_pos
        for i in range(50):
            a = angle_radians * i / 49
            y = self.goal_radius[radius_ind] * sin(a)
            x = self.goal_radius[radius_ind] * cos(a)
            alpha_circle.drawTo((x + alpha_pos[0], self.drawing_layer, y + alpha_pos[2]))
        self.alpha_circle_node.append(self.base.render.attachNewNode(alpha_circle.create()))

    def erase_circle(self):
        for i in self.alpha_circle_node:
            i.detachNode()
        if self.block_done:
            for i in self.avatar_node:
                i.detachNode()
            self.block_done = False

if __name__ == "__main__":
    AW = AvatarWorld()
    AW.base.run()
