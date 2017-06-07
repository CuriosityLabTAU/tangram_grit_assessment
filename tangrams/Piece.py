import numpy as np
import copy


class Piece:
    JUMP = 4

    def __init__(self):
        self.x = []
        self.name = ['', '0', '']
        self.G = 0

    def print_me(self):
        print(self.name[0])
        print(self.name[1])
        print(self.name[2])
        print(self.x)

    def save_png(self):
        color = {
            'small triangle1': [255,0,0],
            'small triangle2': [255,255,0],
            'large triangle1': [255,0,255],
            'large triangle2': [0,255,0],
            'medium triangle': [0,0,255],
            'square': [0, 255, 255],
            'parrallelogram': [125, 0, 200]
        }

        filename = self.name[0] + "_" + self.name[1] + "_" + self.name[2] + ".png"
        bare = np.uint8(copy.deepcopy(self.x))
        bare[bare>0] = 1
        s = bare.shape
        img = np.zeros((9, 9, 4), 'uint8')
        img[0:s[0],0:s[1],0] = bare * color[self.name[0]][0]
        img[0:s[0],0:s[1],1] = bare * color[self.name[0]][1]
        img[0:s[0],0:s[1],2] = bare * color[self.name[0]][2]
        img[0:s[0],0:s[1],3] = bare * 255
        # self.to_image(img).save(filename, 'png')

    # @staticmethod
    # def to_image(img):
    #     s = np.array(img.shape)
    #     im = Image.fromarray(np.uint8(img))
    #     for k in range(0,3):
    #         s[0] *= 2
    #         s[1] *= 2
    #         im = im.resize([s[0], s[1]], Image.BILINEAR)
    #         s[0] *= 2
    #         s[1] *= 2
    #         im = im.resize([s[0], s[1]], Image.AFFINE)
    #
    #     return im

    def copy(self, target):
        target.name = self.name
        target.x = copy.deepcopy(self.x)
        target.G = self.G
        return target

    def rotate(self):
        p_list = [self]
        for i in range(1, 4):
            p_new = copy.deepcopy(self)
            p_new.x = np.rot90(self.x, i)
            found = False
            for q in p_list:
                if np.array_equal(p_new.x, q.x):
                    found = True
                    break
            if not found:
                p_new.name = [self.name[0], str(i*90), '']
                p_list.append(p_new)

        for r in p_list:
            p_new = copy.deepcopy(r)
            p_new.x = np.fliplr(r.x)
            found = False
            for q in p_list:
                if np.array_equal(p_new.x, q.x):
                    found = True
                    break
            if not found:
                p_new.name = [self.name[0], str(int(r.name[1])+180), '']
                p_list.append(p_new)

        return p_list

    def translate(self, I, J):
        t = copy.deepcopy(self)
        t.x = np.zeros([I,J])
        t_list = []
        for i in range(0,I-self.x.shape[0]+1, Piece.JUMP):
            for j in range(0, J-self.x.shape[1]+1, Piece.JUMP):
                t_new = copy.deepcopy(t)
                t_new.name = [t.name[0], t.name[1], str(i/Piece.JUMP) + " " + str(j/Piece.JUMP)]
                t_new.x[i:i+self.x.shape[0], j:j+self.x.shape[1]] = self.x
                t_list.append(t_new)

        return t_list

    def overlap(self, p):
        x = self.x + p.x
        return np.amax(x) > 5.01

    def unite(self, p):
        q = Piece()
        q.name[0] = self.name[0] + "+" + p.name[0]
        q.x = self.x + p.x
        return q

    def touch(self, p):
        x = self.x + p.x
        return len(np.where((x > 1) & (x < 5))[0]) > 0 and len(np.where(x > 5)[0]) == 0

    def base(self):
        a = np.transpose(np.argwhere(self.x > 0))
        x = self.x[np.min(a[0]):np.max(a[0])+1, np.min(a[1]):np.max(a[1])+1]
        return x

    def compare(self, p):
        return np.array_equal(self.x, p.x)

    def create(self, name, rot, pos):
        # create a piece according to parameters:
        # name is a string - 'small triangle1'
        # rot is a string - '90'
        # pos is a vector - [1, 2]

        self.name = [ name , rot, str(pos[0])+" "+str(pos[1]) ]
        if 'small triangle' in name:
            self.x = np.array([[1, 0, 0, 0, 0],
                               [1, 1, 0, 0, 0],
                               [1, 5, 1, 0, 0],
                               [1, 5, 5, 1, 0],
                               [1, 1, 1, 1, 1]])
            if rot == '90':
                self.x = np.rot90(self.x, 1)
            elif rot == '180':
                self.x = np.rot90(self.x,2)
            elif rot == '270':
                self.x = np.rot90(self.x,3)
        elif 'medium triangle' in name:
            self.x = np.array([[1,1,1,1,1,1,1,1,1],
                               [0,1,5,5,5,5,5,1,0],
                               [0,0,1,5,5,5,1,0,0],
                               [0,0,0,1,5,1,0,0,0],
                               [0,0,0,0,1,0,0,0,0]])
            if rot == '90':
                self.x = np.rot90(self.x, 1)
            elif rot == '180':
                self.x = np.rot90(self.x, 2)
            elif rot == '270':
                self.x = np.rot90(self.x, 3)
        elif 'large triangle' in name:
            self.x = np.array([[1,1,1,1,1,1,1,1,1],
                               [1,5,5,5,5,5,5,1,0],
                               [1,5,5,5,5,5,1,0,0],
                               [1,5,5,5,5,1,0,0,0],
                               [1,5,5,5,1,0,0,0,0],
                               [1,5,5,1,0,0,0,0,0],
                               [1,5,1,0,0,0,0,0,0],
                               [1,1,0,0,0,0,0,0,0],
                               [1,0,0,0,0,0,0,0,0]])
            if rot == '90':
                self.x = np.rot90(self.x, 1)
            elif rot == '180':
                self.x = np.rot90(self.x, 2)
            elif rot == '270':
                self.x = np.rot90(self.x, 3)
        elif 'square' in name:
            self.x = np.array([[1,1,1,1,1],
                               [1,5,5,5,1],
                               [1,5,5,5,1],
                               [1,5,5,5,1],
                               [1,1,1,1,1]])
        elif 'parrallelogram' in name:
            self.x = np.array([[0,0,0,0,1],
                               [0,0,0,1,1],
                               [0,0,1,5,1],
                               [0,1,5,5,1],
                               [1,5,5,5,1],
                               [1,5,5,1,0],
                               [1,5,1,0,0],
                               [1,1,0,0,0],
                               [1,0,0,0,0]])
            if rot == '90':
                self.x = np.rot90(self.x, 1)
            elif rot == '180':
                self.x = np.fliplr(self.x)
            elif rot == '270':
                self.x = np.fliplr(np.rot90(self.x, 1))

        temp_x = np.zeros([pos[0]*self.JUMP+self.x.shape[0], pos[1]*self.JUMP+self.x.shape[1]])
        temp_x[pos[0] * self.JUMP:pos[0]*self.JUMP+self.x.shape[0],pos[1] * self.JUMP:pos[1]*self.JUMP+self.x.shape[1]] = self.x
        self.x = temp_x


