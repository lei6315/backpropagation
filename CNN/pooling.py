import numpy as np
import matplotlib.pyplot as plt
import cv2

class AvgPooling(object):
    def __init__(self, shape, ksize=2, stride=2):
        self.input_shape = shape
        self.ksize = ksize
        self.stride = stride
        self.output_channels = shape[-1]
        self.integral = np.zeros(shape)
        # self.index = np.zeros(shape)
        self.output_shape = [shape[0], int(shape[1] / self.stride),
                             int(shape[2] / self.stride), self.output_channels]
    def gradient(self, eta):
        next_eta = np.repeat(eta, self.stride, axis=1)
        next_eta = np.repeat(next_eta, self.stride, axis=2)
        # next_eta = next_eta*self.index
        return next_eta/(self.ksize*self.ksize)

    def forward(self, x):
        out = np.zeros([x.shape[0], x.shape[1] // self.stride, x.shape[2] // self.stride, self.output_channels])

        for b in range(x.shape[0]):
            for c in range(self.output_channels):
                for i in range(0, x.shape[1], self.stride):
                    for j in range(0, x.shape[2], self.stride):
                        out[b, i // self.stride, j // self.stride, c] = np.mean(
                            x[b, i:i + self.ksize, j:j + self.ksize, c])
                        
        return out


class MaxPooling(object):
    def __init__(self, shape, ksize=2, stride=2):
        self.input_shape = shape
        self.ksize = ksize
        self.stride = stride
        self.output_channels = shape[-1]
        self.index = np.zeros(shape)
        self.output_shape = [shape[0], shape[1] // self.stride,
                             shape[2] // self.stride, self.output_channels]

    def forward(self, x):
        out = np.zeros([x.shape[0], x.shape[1] // self.stride,
                        x.shape[2] // self.stride, self.output_channels])
        self.index = np.zeros(self.input_shape)
        for b in range(x.shape[0]):
            for c in range(self.output_channels):
                for i in range(0, x.shape[1], self.stride):
                    for j in range(0, x.shape[2], self.stride):
                        out[b, i // self.stride, j // self.stride, c] = np.max(
                            x[b, i:i + self.ksize, j:j + self.ksize, c])
                        index = np.argmax(
                            x[b, i:i + self.ksize, j:j + self.ksize, c])
                        self.index[b, i+int(index // self.stride),
                                   j + index % self.stride, c] = 1
        return out

    def gradient(self, eta):
        return np.repeat(np.repeat(eta, self.stride, axis=1), self.stride, axis=2) * self.index


if __name__ == "__main__":
    img = cv2.imread('15.png')
    # img=img[:400,:600]
    img2=img
    # img2 = cv2.imread('test.jpg')
    print(img.shape)
    img = np.array([img, img2]).reshape(
        [2, img.shape[0], img.shape[1], img.shape[2]])

    pool = MaxPooling(img.shape, 4, 4)
    img1 = pool.forward(img)
    img2 = pool.gradient(img1)
    # print(img[1, :, :, 1])
    # print(img1[1, :, :, 1])
    # print(img2[1, :, :, 1])
    # print(map(lambda x:int(x),img1[0]))
    print(img1[0].shape)
    plt.imshow(img1[0]/256)
    plt.show()
