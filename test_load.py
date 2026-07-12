import torch
try:
    model = torch.jit.load("/home/kongnyuy/projects/finalYear/mediSightBackend/malaria_model_mobile.ptl")
    print("Model loaded successfully")
except Exception as e:
    print(f"Failed to load: {e}")
