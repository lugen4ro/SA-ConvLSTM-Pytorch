import os

from torch import nn
from torch.optim import Adam

from convlstm.seq2seq import Seq2Seq
from pipelines.evaluator import Evaluator
from pipelines.moving_mnist_pipeline.data_loader import MovingMNISTDataLoaders
from pipelines.trainer import Trainer
from pipelines.utils.early_stopping import EarlyStopping


def main():
    ###
    # Parameters
    ###
    train_epochs = 1
    train_batch_size = 1

    num_channels = 1
    kernel_size = 3
    num_kernels = 1
    padding = "same"
    activation = "relu"
    frame_size = (64, 64)
    num_layers = 1
    input_seq_length = 10
    weights_initializer = "he"
    return_sequences = True
    out_channels = 1

    ###
    # DatLoaders
    ###
    print("Loading dataset ...")
    data_loaders = MovingMNISTDataLoaders(
        train_batch_size, input_frames=input_seq_length
    )

    ###
    # Setup training
    ###
    loss_criterion = nn.MSELoss()
    acc_criterion = nn.L1Loss()
    model = Seq2Seq(
        num_channels=num_channels,
        kernel_size=kernel_size,
        num_kernels=num_kernels,
        padding=padding,
        activation=activation,
        frame_size=frame_size,
        num_layers=num_layers,
        input_seq_length=input_seq_length,
        out_channels=out_channels,
        weights_initializer=weights_initializer,
        return_sequences=return_sequences,
    )
    optimizer = Adam(model.parameters(), lr=0.0005)
    early_stopping = EarlyStopping(
        patience=30,
        verbose=True,
        delta=0.0001,
    )

    ###
    # Training
    ###
    print("Training ConvLSTM...")
    os.makedirs("./tmp", exist_ok=True)
    trainer = Trainer(
        save_model_path="./tmp",
        model=model,
        train_epochs=train_epochs,
        train_dataloader=data_loaders.train_dataloader,
        valid_dataloader=data_loaders.valid_dataloader,
        loss_criterion=loss_criterion,
        accuracy_criterion=acc_criterion,
        optimizer=optimizer,
        early_stopping=early_stopping,
        save_metrics_path="./tmp/metrics.csv",
    )
    trainer.run()

    ###
    # Evaluation
    ###
    print("Evaluating ...")
    evaluator = Evaluator(
        model=model,
        test_dataloader=data_loaders.test_dataloader,
        save_dir_path="./tmp/evaluate",
    )
    evaluator.run()


if __name__ == "__main__":
    main()