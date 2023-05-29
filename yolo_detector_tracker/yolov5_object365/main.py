import cv2
import torch
import numpy as np
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.plots import Annotator, colors, save_one_box
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.dataloaders import LoadImages, LoadStreams
from yolov5.utils.augmentations import letterbox

# model config
half = False
img_sz = [640, 640]
device = 'cpu'
classes = list(range(80))
conf_thres = 0.5
iou_thres = 0.5
max_det = 1000
line_thickness = 2
agnostic_nms = False
dnn = True

# source
source = './test.mp4'
webcam = source.isnumeric() or source.endswith('.txt')

# output config
show_video = True
save_video = False
output_file_name = 'test_output.avi'
out_writter = cv2.VideoWriter(
    output_file_name, 
    cv2.VideoWriter_fourcc('M','J','P','G'), 30, img_sz
)

# load model
# use FP16 half-precision inference, use OpenCV DNN for ONNX inference
model_name = "yolov5m_Objects365.pt"
data = 'data/Objects365.yaml'
model = DetectMultiBackend(model_name, device=device, dnn=dnn, data=data, fp16=half)
stride, names, pt = model.stride, model.names, model.pt

# import threading
# class FreshestFrame(threading.Thread):
#     def __init__(self, capture, name='FreshestFrame'):
#         self.capture = capture
#         assert self.capture.isOpened()
#         # this lets the read() method block until there's a new frame
#         self.cond = threading.Condition()
#         # this allows us to stop the thread gracefully
#         self.running = False
#         # keeping the newest frame around
#         self.frame = None
#         # passing a sequence number allows read() to NOT block
#         # if the currently available one is exactly the one you ask for
#         self.latestnum = 0
#         # this is just for demo purposes        
#         self.callback = None
#         super().__init__(name=name)
#         self.start()

#     def start(self):
#         self.running = True
#         super().start()

#     def release(self, timeout=None):
#         self.running = False
#         self.join(timeout=timeout)
#         self.capture.release()

#     def run(self):
#         counter = 0
#         while self.running:
#             # block for fresh frame
#             (rv, img) = self.capture.read()
#             assert rv
#             counter += 1
#             # publish the frame
#             with self.cond: # lock the condition for this operation
#                 self.frame = img if rv else None
#                 self.latestnum = counter
#                 self.cond.notify_all()
#             if self.callback:
#                 self.callback(img)

#     def read(self, wait=True, seqnumber=None, timeout=None):
#         # with no arguments (wait=True), it always blocks for a fresh frame
#         # with wait=False it returns the current frame immediately (polling)
#         # with a seqnumber, it blocks until that frame is available (or no wait at all)
#         # with timeout argument, may return an earlier frame;
#         #   may even be (0,None) if nothing received yet
#         with self.cond:
#             if wait:
#                 if seqnumber is None:
#                     seqnumber = self.latestnum+1
#                 if seqnumber < 1:
#                     seqnumber = 1
#                 rv = self.cond.wait_for(lambda: self.latestnum >= seqnumber, timeout=timeout)
#                 if not rv:
#                     return (self.latestnum, self.frame)
#             return (self.latestnum, self.frame)
# video_loader = cv2.VideoCapture('rtsp://service:​Thales1$8o8@192.168.100.108:554/live')
# video_loader = FreshestFrame(video_loader)

video_loader = cv2.VideoCapture(source)

while True:
    _, image = video_loader.read()
    # s = np.stack([letterbox(x, img_sz, stride=stride, auto=True)[0].shape for x in image])
    im = cv2.resize(image, img_sz, interpolation = cv2.INTER_AREA)
    im = torch.from_numpy(im).to(device)
    im = im.half() if half else im.float()
    im /= 255.0 
    im = torch.unsqueeze(im, 0)
    im = torch.permute(im, (0, 3, 1, 2))
    preds = model(im, augment=False, visualize=False)
    results = non_max_suppression(preds, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

    # Process detections
    for i, det in enumerate(results):
        
        # annotator for plotting
        annotator = Annotator(image, line_width=2, example=str(names))

        if det is not None and len(det): 
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], image.shape).round()
            for j, (output) in enumerate(det):
                bbox = output[0:4]
                conf = output[4]
                cls = output[5]
                annotator.box_label(bbox, f'{names[int(cls)]} {conf:.2f}', color=colors(int(cls), True))

            # for deepsort
            # outputs = deep_tracker.update(det.cpu(), ori_im)
            # if len(outputs) > 0:
            #     for j, (output) in enumerate(outputs):
            #         bbox = output[0:4]
            #         id = output[4]
            #         cls = output[5]
            #         conf = output[6]
            #         annotator.box_label(bbox, f'{id} {names[int(cls)]} {conf:.2f}', color=colors(int(cls), True))


    if show_video:
        cv2.namedWindow("out", cv2.WINDOW_FREERATIO)
        cv2.resizeWindow("out", image.shape[1], image.shape[0])
        cv2.imshow("out", image)
        if cv2.waitKey(1) == ord('q'):
            exit()
    
    if save_video:
        frame = cv2.resize(image, img_sz, interpolation=cv2.INTER_AREA)
        out_writter.write(frame)

# # data loader
# if webcam:
#     dataset = LoadStreams(source, img_size=img_sz, stride=stride, auto=pt, vid_stride=1)
#     bs = len(dataset)

# else:
#     dataset = LoadImages(source, img_size=img_sz, stride=stride, auto=pt, vid_stride=1)

# for frame_idx, batch in enumerate(dataset):
#     # processing
#     path, tranform_im, ori_im, vid_cap, s = batch
#     tranform_im = torch.from_numpy(tranform_im).to(device)
#     tranform_im = tranform_im.half() if half else tranform_im.float()
#     tranform_im /= 255.0 
#     tranform_im = torch.unsqueeze(tranform_im, 0)

#     # inference
#     preds = model(tranform_im, augment=False, visualize=False)
#     results = non_max_suppression(preds, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

#     # Process detections
#     for i, det in enumerate(results):
        
#         # annotator for plotting
#         annotator = Annotator(ori_im, line_width=2, example=str(names))

#         if det is not None and len(det): 
#             det[:, :4] = scale_boxes(tranform_im.shape[2:], det[:, :4], ori_im.shape).round()

#             for j, (output) in enumerate(det):
#                 bbox = output[0:4]
#                 conf = output[4]
#                 cls = output[5]
#                 annotator.box_label(bbox, f'{names[int(cls)]} {conf:.2f}', color=colors(int(cls), True))

#             # for deepsort
#             # outputs = deep_tracker.update(det.cpu(), ori_im)
#             # if len(outputs) > 0:
#             #     for j, (output) in enumerate(outputs):
#             #         bbox = output[0:4]
#             #         id = output[4]
#             #         cls = output[5]
#             #         conf = output[6]
#             #         annotator.box_label(bbox, f'{id} {names[int(cls)]} {conf:.2f}', color=colors(int(cls), True))

#     final_img = annotator.result()
#     if show_video:
#         cv2.namedWindow("out", cv2.WINDOW_FREERATIO)
#         cv2.resizeWindow("out", final_img.shape[1], final_img.shape[0])
#         cv2.imshow("out", final_img)
#         if cv2.waitKey(1) == ord('q'):
#             exit()

#     if save_video:
#         frame = cv2.resize(final_img, img_sz, interpolation=cv2.INTER_AREA)
#         out_writter.write(frame)