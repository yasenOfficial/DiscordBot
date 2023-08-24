from deepface import DeepFace
import cv2
import matplotlib as plt

obj = DeepFace.analyze(img_path = "test.jpg", actions = ['age', 'gender', 'race', 'emotion'])
print(obj)


# selected_elements = {
#     'age', 
#     'dominant_gender', 
#     'dominant_race', 
#     'dominant_emotion'
# }

# for record in data:
#     print("Record:")
#     for key, value in record.items():
#         if key in selected_elements:
#             print(f"{key}: {value}")

