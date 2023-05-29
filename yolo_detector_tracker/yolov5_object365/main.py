import cv2
import torch
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.plots import Annotator, colors, save_one_box
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.dataloaders import LoadImages, LoadStreams

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

# data loader
if webcam:
    dataset = LoadStreams(source, img_size=img_sz, stride=stride, auto=pt, vid_stride=1)
    bs = len(dataset)

else:
    dataset = LoadImages(source, img_size=img_sz, stride=stride, auto=pt, vid_stride=1)

for frame_idx, batch in enumerate(dataset):
    # processing
    path, tranform_im, ori_im, vid_cap, s = batch
    tranform_im = torch.from_numpy(tranform_im).to(device)
    tranform_im = tranform_im.half() if half else tranform_im.float()
    tranform_im /= 255.0 
    tranform_im = torch.unsqueeze(tranform_im, 0)

    # inference
    preds = model(tranform_im, augment=False, visualize=False)
    results = non_max_suppression(preds, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

    # Process detections
    for i, det in enumerate(results):
        
        # annotator for plotting
        annotator = Annotator(ori_im, line_width=2, example=str(names))

        if det is not None and len(det): 
            det[:, :4] = scale_boxes(tranform_im.shape[2:], det[:, :4], ori_im.shape).round()

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

    final_img = annotator.result()
    if show_video:
        cv2.namedWindow("out", cv2.WINDOW_FREERATIO)
        cv2.resizeWindow("out", final_img.shape[1], final_img.shape[0])
        cv2.imshow("out", final_img)
        if cv2.waitKey(1) == ord('q'):
            exit()

    if save_video:
        frame = cv2.resize(final_img, img_sz, interpolation=cv2.INTER_AREA)
        out_writter.write(frame)