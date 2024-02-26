"""
Really simple example showing how to train a ResNet18 model on CIFAR-10 using command-line arguments and torchbearer.
Supports snapshotting, resume, etc
"""
import argparse

import torch
import torchbearer
import torchvision
from torch.utils.data import Dataset
from torchbearer import Trial
from torchbearer.callbacks import MultiStepLR
from torchvision.datasets import CIFAR10
from torchvision.models import resnet18


if __name__ == '__main__':
    # Setup
    parser = argparse.ArgumentParser(description='PyTorch CIFAR10 Training')
    parser.add_argument('--dataset-path', type=str, default=".", help='Optional dataset path')
    parser.add_argument('--model', default="ResNet18", type=str, help='model type')
    parser.add_argument('--epochs', default=2, type=int, help='total epochs to run')
    parser.add_argument('--lr', default=0.1, type=float, help='learning rate')
    parser.add_argument('--batch-size', default=128, type=int, help='batch size')
    parser.add_argument('--device', default='cuda', type=str, help='Device on which to run')
    parser.add_argument('--num-workers', default=8, type=int, help='Number of dataloader workers')

    parser.add_argument('--resume', action='store_true', default=False,
                        help='Set to resume training from model path')
    parser.add_argument('--verbose', type=int, default=2, choices=[0, 1, 2])
    parser.add_argument('--seed', default=0, type=int, help='random seed')

    # Scheduling
    parser.add_argument('--schedule', type=int, nargs='+', default=[100, 150],
                        help='Decrease learning rate at these epochs.')

    parser.add_argument('--model-file', default='./cifar10_model.pt',
                        help='Path under which to save model. eg ./model.py')
    args = parser.parse_args()

    if args.seed != 0:
        torch.manual_seed(args.seed)

    # add a little data augmentation
    train_transforms = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        torchvision.transforms.RandomCrop((32, 32), padding=(4, 4)),
        torchvision.transforms.RandomHorizontalFlip(),
    ])
    train_ds = CIFAR10(".", train=True, transform=train_transforms, download=True)

    val_transforms = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    val_ds = CIFAR10(".", train=False, transform=val_transforms, download=True)

    # create data loaders
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,
                                               num_workers=args.num_workers)
    val_loader = torch.utils.data.DataLoader(val_ds, batch_size=args.batch_size, shuffle=False,
                                             num_workers=args.num_workers)

    # create model
    model = resnet18(num_classes=10)

    # define loss and optimiser
    loss = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, weight_decay=1e-4)

    trial = Trial(model, optimizer, loss, metrics=['loss', 'lr', 'acc'],
                  callbacks=[torchbearer.callbacks.MostRecent(args.model_file), MultiStepLR(milestones=args.schedule)])
    trial.with_generators(train_generator=train_loader, val_generator=val_loader).to(args.device)

    if args.resume:
        print('resuming from: ' + args.model_file)
        state = torch.load(args.model_file)
        trial.load_state_dict(state)
        trial.replay()

    trial.run(args.epochs, verbose=args.verbose)
    trial.evaluate(data_key=torchbearer.VALIDATION_DATA)
