import os
import cv2
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from types import MethodType
import time
from tqdm import tqdm

# load model
resnet = InceptionResnetV1(pretrained='vggface2').eval()
mtcnn = MTCNN(image_size=128, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60)
# get encoded features for all saved images
people_pictures = "./data/saved"
all_people_faces = {}

# helper function
def encode(img):
    # img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)
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

    while vdo.grab():
        _, img0 = vdo.retrieve()
        batch_boxes, cropped_images = mtcnn.detect_box(img0)

        start = time.time()
        if cropped_images is not None:
            for box, cropped in zip(batch_boxes, cropped_images):
                img_embedding = encode(cropped.unsqueeze(0))
                detect_dict = {}
                for k, v in all_people_faces.items():
                    detect_dict[k] = (v - img_embedding).norm().item()
                min_key = min(detect_dict, key=detect_dict.get)

                if detect_dict[min_key] >= 1.:
                    min_key = 'Undetected'
                
                x, y, x2, y2 = [int(x) for x in box]
                cv2.rectangle(img0, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img0, min_key, (x + 5, y + 10), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            print("Time Elapsed for Image Comparison: ", time.time() - start)
                
        ### display
        cv2.imshow("test", img0)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    detect(0)

'''
1000 images
Cropped + Feature Extractor: 600s

'''