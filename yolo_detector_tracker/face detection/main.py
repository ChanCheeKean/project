import os
import time
import cv2
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from tqdm import tqdm
from types import MethodType
from tensorflow.keras.models import load_model

# load model
resnet = InceptionResnetV1(pretrained='vggface2').eval()
mtcnn = MTCNN(image_size=224, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60)
faceq_model = load_model('./weights/FaceQnet_v1.h5')

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
start = time.time()
for file in tqdm(os.listdir(people_pictures)):

    try:
        person_face, extension = file.split(".")
        img = cv2.imread(f'{people_pictures}/{person_face}.jpg')
        cropped = mtcnn(img)
        if cropped is not None:
            all_people_faces[person_face] = encode(cropped)[0, :]
    except Exception as e:
        print(f"Failed: {file} with Error: {e}")

print("Time Elapsed for Saved Images Processing: ", time.time() - start)
print(f"Stored Image Features: {len(all_people_faces)}")

def detect(cam=0):
    vdo = cv2.VideoCapture(cam)

    q_score_max = 0
    while vdo.grab():
        _, img0 = vdo.retrieve()
        batch_boxes, cropped_images = mtcnn.detect_box(img0)
        test_img = img0

        if cropped_images is not None:
            for box, cropped in zip(batch_boxes, cropped_images):
                x, y, x2, y2 = [int(x) for x in box]

                # for quality assessment
                q_score = faceq_model.predict(
                    np.expand_dims(cv2.resize(img0[y:y2, x:x2, :], (224, 224)), 0)
                )
                img_embedding = encode(cropped.unsqueeze(0))
                detect_dict = {}
                for k, v in all_people_faces.items():
                    detect_dict[k] = (v - img_embedding).norm().item()
                min_key = min(detect_dict, key=detect_dict.get)

                if detect_dict[min_key] >= 0.8:
                    min_key = 'Undetected'
                
                cv2.rectangle(img0, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img0, min_key, (x + 5, y + 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                print(q_score)
                if q_score > q_score_max:
                    q_score_max = q_score

        ### display
        cv2.imshow("test", test_img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    detect(0)