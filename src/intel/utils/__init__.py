import  sys
import torch
import yaml
import torch.nn as nn
from src.intel.exception import CustomException
from torch.optim.lr_scheduler import StepLR
from src.intel.constants import *

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise CustomException(e, sys) from e

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)

def my_fit_method(epochs, lr, model, train_data_loader, val_loader, opt_func=torch.optim.SGD,grad_clip=GRAD_CLIP):
    history = []
    optimizer = opt_func(model.parameters(), lr,weight_decay=WEIGHT_DECAY)
    sched = torch.optim.lr_scheduler.OneCycleLR(optimizer, lr, epochs=epochs, 
                                                steps_per_epoch=len(train_data_loader))
    for epoch in range(epochs):
        # Training Phase 
        model.train()
        train_losses = []

        for batch in train_data_loader:
            
            loss = model.training_step(batch)
            train_losses.append(loss)
            loss.backward()

            # Gradient clipping
            if grad_clip: 
                nn.utils.clip_grad_value_(model.parameters(), grad_clip)

            optimizer.step()
            optimizer.zero_grad()

            # Record & update learning rate
            sched.step()
            
        # Validation Phase
        result = evaluate(model, val_loader)
        result['train_loss'] = torch.stack(train_losses).mean().item()
        model.epoch_end(epoch, result)
        history.append(result)
    return history, result

@torch.no_grad()
def evaluate(model, val_loader):
    model.eval()
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)



def predict_image(img, model, device, num_classes):
    # Convert to a batch of 1
    ximg = to_device(img.unsqueeze(0), device)
    yimg = model(ximg)
    ## Picking the image with highest probability
    prob, preds  = torch.max(yimg, dim=1)
    # Getting the class label
    num_classes = ['buildings', 'forest', 'glacier', 'mountain', 'sea', 'street']
    return num_classes[preds[0].item()]