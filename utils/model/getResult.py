import numpy as np
from PIL import Image
import streamlit as st

def predict(image,net,device,saveRoot):
        imagex = image.to(device)
        # TODO 加载数据后对模型进行训练
        result = net.forward(imagex)
        save(result[0][0], saveRoot)


def save(result,saveRoot):
    # delete a dimision
    cut = np.squeeze(result)
    # sigmoid
    """
    原评处理函数中没有sigmoid函数
    """
    cut = 1 / (1 + np.exp(-cut))
    cut = np.where(cut > 0.7, 1, 0)
    cut = (cut * 255).astype(np.uint8)
    # 图片存储
    cut.save(saveRoot)
    # cv2.imwrite(saveRoot, cut)
    return cut