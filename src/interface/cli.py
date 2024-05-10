import argparse
import os
import sys
from src.model.training import ModelTrainer
from src.model.inference import ModelInferencer

def train_model(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs):
    trainer = ModelTrainer(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs)
    trainer.train()

def infer_model(model_name, tokenizer_name, test_data_path, batch_size):
    inferencer = ModelInferencer(model_name, tokenizer_name, test_data_path, batch_size)
    inferencer.infer()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train or infer a model.')
    subparsers = parser.add_subparsers(dest='command')

    train_parser = subparsers.add_parser('train', help='Train a model.')
    train_parser.add_argument('--model_name', type=str, required=True, help='The name of the model to train.')
    train_parser.add_argument('--tokenizer_name', type=str, required=True, help='The name of the tokenizer to use.')
    train_parser.add_argument('--train_data_path', type=str, required=True, help='The path to the training data.')
    train_parser.add_argument('--val_data_path', type=str, required=True, help='The path to the validation data.')
    train_parser.add_argument('--batch_size', type=int, default=32, help='The batch size.')
    train_parser.add_argument('--learning_rate', type=float, default=1e-5, help='The learning rate.')
    train_parser.add_argument('--num_epochs', type=int, default=3, help='The number of epochs.')

    infer_parser = subparsers.add_parser('infer', help='Infer a model.')
    infer_parser.add_argument('--model_name', type=str, required=True, help='The name of the model to infer.')
    infer_parser.add_argument('--tokenizer_name', type=str, required=True, help='The name of the tokenizer to use.')
    infer_parser.add_argument('--test_data_path', type=str, required=True, help='The path to the test data.')
    infer_parser.add_argument('--batch_size', type=int, default=32, help='The batch size.')

    args = parser.parse_args()

    if args.command == 'train':
        train_model(args.model_name, args.tokenizer_name, args.train_data_path, args.val_data_path, args.batch_size, args.learning_rate, args.num_epochs)
    elif args.command == 'infer':
        infer_model(args.model_name, args.tokenizer_name, args.test_data_path, args.batch_size)
    else:
        print('Invalid command.')
        sys.exit(1)
