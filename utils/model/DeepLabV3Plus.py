import onnxruntime
import numpy as np
import cv2 as cv

import streamlit as st
class ONNXModelDeepLabV3P():
    def __init__(self):
        onnx_path = r'./modelParameters/DeepLabV3Plus1_11_81552.onnx'
        self.onnx_session = onnxruntime.InferenceSession(onnx_path)
        self.input_name = self.get_input_name(self.onnx_session)
        self.output_name = self.get_output_name(self.onnx_session)
        print("input_name:{}".format(self.input_name))
        print("output_name:{}".format(self.output_name))

    def get_output_name(self, onnx_session):
        output_name = []
        for node in onnx_session.get_outputs():
            output_name.append(node.name)
        return output_name

    def get_input_name(self, onnx_session):
        input_name = []
        for node in onnx_session.get_inputs():
            input_name.append(node.name)
        return input_name

    def get_input_feed(self, input_name, image_numpy):
        input_feed = {}
        for name in input_name:
            input_feed[name] = image_numpy
        return input_feed

    def forward(self,image_numpy):
        input_feed = self.get_input_feed(self.input_name,image_numpy)
        pred = self.onnx_session.run(self.output_name,input_feed)
        return pred

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

@st.cache
def DeeplabV3Ppredict(image,saveRoot):
    Net = ONNXModelDeepLabV3P()
    imagef = cv.resize(image, (256, 256))
    img = np.asarray(imagef)
    imageArray = np.expand_dims(img, 0).repeat(3, axis=0)
    imageArray = np.expand_dims(imageArray, 0)

    images = (imageArray - np.min(imageArray)) / (np.max(imageArray) - np.min(imageArray))
    images = images.astype(np.float32)

    # TODO 加载数据后对模型进行训练
    results = Net.forward(images)

    squeezeInput = results[0][0]
    cut = np.squeeze(squeezeInput)
    cut = 1 / (1 + np.exp(-cut))
    cut = np.where(cut > 0.7, 1, 0)
    # TODO 生成RGB 三通道值
    cut = np.array(cut, dtype='uint8')
    predR = (cut * 218).astype(np.uint8)
    predG = (cut * 112).astype(np.uint8)
    predB = (cut * 214).astype(np.uint8)
    # # 生成图像
    predBGR = cv.merge((predB, predG, predR))
    imageArray = np.squeeze(imageArray)
    imageArray = np.transpose(imageArray, (1, 2, 0))
    resultA = cv.addWeighted(imageArray, 0.6, predBGR, 0.4, 0).astype(np.uint8)
    # 保存图像
    cv.imwrite(saveRoot, resultA)

    resultReshape = cv.resize(resultA, (800, 800), interpolation=cv.INTER_LINEAR)
    return resultReshape