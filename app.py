import argparse

from flask import Flask, request, jsonify, render_template, send_file, flash
import torch
# import numpy as np
# import os
# from torchvision import transforms
# from models.experimental import attempt_load
# #from utils.plots import plot_one_box
import os
from detect import  run,main

app = Flask(__name__)


# 定义路由
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 从表单中获取上传的文件
        f = request.files['file']
        global filename
        filename = f.filename
        global file_path 
        
        # 将文件保存到服务器本地
        file_path = os.path.join(os.getcwd(), filename)

        print(file_path)
        f.save(file_path)
        # 返回文件路径
        # return file_path
    return render_template('index1.html')

#检测函数
@app.route('/det', methods=['GET','POST'])
def my_flask_function():
    #print('测试一下！')
    opt = parse_opt()
    main(opt)


    # return jsonify({'message': 'Hello from Flask!'})
    return render_template('123.html')

# 检测结果显示
def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

@app.route('/sh', methods=['GET', 'POST'])
def hello_world():
    img_path = 'runs\\detect\\exp\\' + str(filename)
    img_stream = return_img_stream(img_path)
    return render_template('showimage.html', img_stream=img_stream)

# 检测图片的

def parse_opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('--weights', nargs='+', type=str, default= 'yolov5s.pt', help='model path or triton URL')
    #parser.add_argument('--source', type=str, default=0, help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--source', type=str, default= file_path, help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default= 'models/yolov5s.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--project', default= 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    #print_args(vars(opt))
    args = parser.parse_args(args=[])
    print(args)
    return opt

# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
