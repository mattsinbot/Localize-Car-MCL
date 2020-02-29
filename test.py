class test(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set(self, nx, ny, nz):
        self.x = nx
        self.y = ny
        self.z = nz

    def __repr__(self):
        return "x={}, y={}, z={}".format(self.x, self.y, self.z)


if __name__=="__main__":
    test_arr = [test() for _ in range(10)]
    test_arr[0].set(10, 63, 48)
    test_arr[1].set(54, 98, 15)
    test_arr[5].set(78, 22, 45)

    for i in range(len(test_arr)):
        print(test_arr[i])
