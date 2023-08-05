import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from kornia.utils.metrics import *
from typing import Optional, Callable
import cv2

# np.set_printoptions(precision=3)

def mean_iou(
        input: torch.Tensor,
        target: torch.Tensor,
        num_classes: int,
        eps: Optional[float] = 1e-6) -> torch.Tensor:
    r"""Calculate mean Intersection-Over-Union (mIOU).

    The function internally computes the confusion matrix.

    Args:
        input (torch.Tensor) : tensor with estimated targets returned by a
          classifier. The shape can be :math:`(B, *)` and must contain integer
          values between 0 and K-1.
        target (torch.Tensor) : tensor with ground truth (correct) target
          values. The shape can be :math:`(B, *)` and must contain integer
          values between 0 and K-1, whete targets are assumed to be provided as
          one-hot vectors.
        num_classes (int): total possible number of classes in target.

    Returns:
        torch.Tensor: a tensor representing the mean intersection-over union
        with shape :math:`(B, K)` where K is the number of classes.
    """
    np.set_printoptions(precision=3)

    input = torch.argmax(input, axis=1 )
    if not torch.is_tensor(input) and input.dtype is not torch.int64:
        raise TypeError("Input input type is not a torch.Tensor with "
                        "torch.int64 dtype. Got {}".format(type(input)))
    if not torch.is_tensor(target) and target.dtype is not torch.int64:
        raise TypeError("Input target type is not a torch.Tensor with "
                        "torch.int64 dtype. Got {}".format(type(target)))
    if not input.shape == target.shape:
        raise ValueError("Inputs input and target must have the same shape. "
                         "Got: {} and {}".format(input.shape, target.shape))
    if not input.device == target.device:
        raise ValueError("Inputs must be in the same device. "
                         "Got: {} - {}".format(input.device, target.device))
    if not isinstance(num_classes, int) or num_classes < 2:
        raise ValueError("The number of classes must be an intenger bigger "
                         "than two. Got: {}".format(num_classes))
    # we first compute the confusion matrix
    conf_mat: torch.Tensor = confusion_matrix(input, target, num_classes)

    # compute the actual intersection over union
    sum_over_row = torch.sum(conf_mat, dim=1)
    sum_over_col = torch.sum(conf_mat, dim=2)
    conf_mat_diag = torch.diagonal(conf_mat, dim1=-2, dim2=-1)
    denominator = sum_over_row + sum_over_col - conf_mat_diag

    # NOTE: we add epsilon so that samples that are neither in the
    # prediction or ground truth are taken into account.
    ious = (conf_mat_diag + eps) / (denominator + eps)

    return np.array(ious.cpu())

def center_crop(path):
    im = Image.open(str(path))

    max_val = min(im.shape)

    new_width, new_height = max_val, max_val
    width, height = im.size   # Get dimensions

    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    return np.array(im)

def plot_result_comparison(standard_path,
                            learn: torch.nn.Module,
                            resize: tuple=None,
                            crop_center: bool=False,
                            label_fcn: Callable=None):
    '''
    Plots comparison of results using `learner` that is defined globally.

        :stanndard_path: Path-object

    '''

    # grab images
    display_img = np.array(Image.open(standard_path))
    mask = plt.imread(label_fcn(standard_path))

    # get results
    res = learn.predict(display_img)

    # resize if necessary
    if crop_center:
        display_img = center_crop(standard_path)
        mask = center_crop(label_fcn(standard_path))
    elif resize:
        display_img = cv2.resize(display_img, dsize=(resize[0], resize[1]), interpolation=cv2.INTER_LINEAR)
        mask = cv2.resize(mask, dsize=(resize[0], resize[1]), interpolation=cv2.INTER_LINEAR)

    plt.subplots(131, figsize=(24,8))
    plt.subplot(131)
    plt.title('Original')
    plt.imshow(display_img)
    plt.subplot(132)
    plt.title('Target')
    plt.imshow(mask)
    plt.subplot(133)
    plt.title('Prediction')
    plt.imshow(res[0])
    plt.show()

