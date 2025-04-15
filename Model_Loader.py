"""
Filename: Model_Loader.py
Purpose: Loads custom torch models into a dictionary
"""

import torch
import os
from Predictor import NeuralNet, CNN


class Loader:
    def __init__(self, models_dir: str, device: torch.device=torch.device('cpu'), from_dicts: bool=True):
        """Loads all the models in the model_path directory into a dictionary.

        Args:
            models_dir (str): Directory containing torch models/model-dicts. 
            device (torch.device): the device to load the models onto
            from_dicts (bool, optional): Whether the saved models are state dictionaries or full models. Defaults to True.
        """

        self.models = None # stores the all the loaded models
        self.models_dir= os.path.join(models_dir)

        if from_dicts: 
            self.models = self.load_from_dicts(self.models_dir, device)
        else:
            self.models = self.load_full_models(self.models_dir, device)


    def load_from_dicts(self, models_dir: str, device) -> dict:
        """Loads models from state dictionaries

        Args:
            models_dir (str): Directory containing saved model dictionary files.
        
        Returns: Dictionary with model dimensions separated by "-" as keys and models as values
        """
        res = {}

        for filename in os.listdir(models_dir):
            load_path = os.path.join(models_dir, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            if "cnn" in filename:
                # load model
                model = CNN()
            else:
                hidden_widths = [int(width) for width in filename_no_ext.rstrip("-dict").split("-")]
                model = NeuralNet(input_size=28*28, hidden_widths=hidden_widths, num_classes=10)

            # load model state dictionary
            model.load_state_dict(torch.load(load_path, weights_only=True))
            model = model.to(device)
            model.eval()
            # add model to dict
            key = filename_no_ext.rstrip("-dict")
            res[key] = model

        return res
    

    def load_full_models(self, models_dir: str, device: torch.device) -> dict:
        """Loads full models from save files.

        Args:
            models_dir (str): Directory containing saved model files.
            device (torch.device): the device to load models to.

        Returns: Dictionary with model dimensions separated by "-" as keys and models as values
        """

        res = {}

        for filename in os.listdir(models_dir):
            load_path = os.path.join(models_dir, filename)
            filename_no_ext = os.path.splitext(filename)[0]
            model = torch.load(load_path, map_location=device, weights_only=False)
            model.eval()
            # add model to dict
            key = filename_no_ext.rstrip("-dict")
            res[key] = model

        return res



            
