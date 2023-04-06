import os
import dash
import dash_bootstrap_components as dbc
from template import main_layout
from flask import Response
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
import cv2
from types import MethodType

# flask setting
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

# load model
resnet = InceptionResnetV1(pretrained='vggface2').eval()
mtcnn = MTCNN(image_size=224, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60)

# get encoded features for all saved images
people_pictures = "./data/saved/"
all_people_faces = {}

# helper function
def encode(img):
    res = resnet(torch.Tensor(img))
    return res

def detect_box(self, img, save_path=None):
    # Detect faces
    batch_boxes, batch_probs, batch_points = self.detect(img, landmarks=True)
    # Select faces
    if not self.keep_all:
        batch_boxes, batch_probs, batch_points = self.select_boxes(
            batch_boxes, batch_probs, batch_points, img, method=self.selection_method
        )
    # Extract faces
    faces = self.extract(img, batch_boxes, save_path)
    return batch_boxes, faces
mtcnn.detect_box = MethodType(detect_box, mtcnn)

# feature extraction for all saved images 
for file in os.listdir(people_pictures):
    person_face, extension = file.split(".")
    img = cv2.imread(f'{people_pictures}/{person_face}.jpg')
    cropped = mtcnn(img)
    if cropped is not None:
        all_people_faces[person_face] = encode(cropped)[0, :]
print(f"Stored Image Features: {len(all_people_faces)}")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        _, image = self.video.read()

        # face matching
        batch_boxes, cropped_images = mtcnn.detect_box(image)
        if cropped_images is not None:
            for box, cropped in zip(batch_boxes, cropped_images):
                x, y, x2, y2 = [int(x) for x in box]
                img_embedding = encode(cropped.unsqueeze(0))
                detect_dict = {}
                for k, v in all_people_faces.items():
                    detect_dict[k] = (v - img_embedding).norm().item()
                min_key = min(detect_dict, key=detect_dict.get)

                if detect_dict[min_key] >= 0.8:
                    min_key = 'Undetected'
                cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(image, min_key, (x + 5, y + 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )

@server.route('/video_feed')
def video_feed():
    return Response(
        gen(VideoCamera()),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

app.layout = main_layout.layout
if __name__ == '__main__':
    app.run_server(debug=False, port=5000, host='0.0.0.0')