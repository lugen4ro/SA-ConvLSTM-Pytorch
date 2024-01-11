from unittest.mock import patch

from data_loaders.moving_mnist import MovingMNISTDataLoaders
from tests.utils import MockMovingMNIST


@patch("data_loaders.moving_mnist.MovingMNIST")
def test_MovingMNISTDataLoaders(mocked_MovingMNIST):
    dataset_length = 10
    train_batch_size = 2
    input_frames = 10
    mocked_MovingMNIST.return_value = MockMovingMNIST(dataset_length=dataset_length)
    dataloaders = MovingMNISTDataLoaders(
        train_batch_size=train_batch_size, input_frames=input_frames
    )
    assert len(dataloaders.train_dataloader) == 4
    assert len(dataloaders.validation_dataloader) == 2
    assert len(dataloaders.test_dataloader) == 1
    input, target = next(iter(dataloaders.train_dataloader))
    assert input.size(0) == train_batch_size
    assert input.size(2) == input_frames
    assert target.size(0) == train_batch_size
    assert target.size(2) == input_frames