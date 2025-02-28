# src/main.py

import argparse
import os
import sys
import logging
from src.interface.cli import infer_model, train_model
from src.interface.gui import ModelGUI
import tkinter as tk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Train or infer a model.")
    subparsers = parser.add_subparsers(dest="command")

    # Training command
    train_parser = subparsers.add_parser("train", help="Train a model.")
    train_parser.add_argument("--model_name", type=str, required=True, help="The name of the model to train.")
    train_parser.add_argument("--tokenizer_name", type=str, required=True, help="The name of the tokenizer to use.")
    train_parser.add_argument("--train_data_path", type=str, required=True, help="The path to the training data.")
    train_parser.add_argument("--val_data_path", type=str, required=True, help="The path to the validation data.")
    train_parser.add_argument("--batch_size", type=int, default=32, help="The batch size.")
    train_parser.add_argument("--learning_rate", type=float, default=1e-5, help="The learning rate.")
    train_parser.add_argument("--num_epochs", type=int, default=3, help="The number of epochs.")

    # Inference command
    infer_parser = subparsers.add_parser("infer", help="Infer a model.")
    infer_parser.add_argument("--model_name", type=str, required=True, help="The name of the model to infer.")
    infer_parser.add_argument("--tokenizer_name", type=str, required=True, help="The name of the tokenizer to use.")
    infer_parser.add_argument("--test_data_path", type=str, required=True, help="The path to the test data.")
    infer_parser.add_argument("--batch_size", type=int, default=32, help="The batch size.")

    # GUI command
    gui_parser = subparsers.add_parser("gui", help="Launch the GUI for model management.")

    args = parser.parse_args()

    try:
        if args.command == "train":
            logging.info("Starting training...")
            train_model(
                args.model_name,
                args.tokenizer_name,
                args.train_data_path,
                args.val_data_path,
                args.batch_size,
                args.learning_rate,
                args.num_epochs,
            )
            logging.info("Training completed successfully.")
        elif args.command == "infer":
            logging.info("Starting inference...")
            infer_model(
                args.model_name,
                args.tokenizer_name,
                args.test_data_path,
                args.batch_size
            )
            logging.info("Inference completed successfully.")
        elif args.command == "gui":
            root = tk.Tk()
            gui = ModelGUI(root)
            root.mainloop()
        else:
            logging.error("Invalid command.")
            sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
