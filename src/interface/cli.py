# src/interface/cli.py

import logging
from src.model.training import ModelTrainer
from src.model.inference import ModelInferencer
from src.config import Config

def train_model(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs):
    """Train a machine learning model."""
    try:
        logging.info("Initializing model trainer...")
        trainer = ModelTrainer(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs)
        trainer.train()
        logging.info("Training completed successfully.")
    except Exception as e:
        logging.error(f"Training failed: {e}")

def infer_model(model_name, tokenizer_name, test_data_path, batch_size):
    """Infer using a trained machine learning model."""
    try:
        logging.info("Initializing model inferencer...")
        inferencer = ModelInferencer(model_name, tokenizer_name, test_data_path, batch_size)
        inferencer.infer()
        logging.info("Inference completed successfully.")
    except Exception as e:
        logging.error(f"Inference failed: {e}")

def main_cli():
    """Main CLI function to handle user commands."""
    config = Config()
    config.validate()  # Validate the configuration settings

    # Example command handling
    command = input("Enter command (train/infer): ").strip().lower()
    
    if command == "train":
        model_name = input("Enter model name: ")
        tokenizer_name = input("Enter tokenizer name: ")
        train_data_path = input("Enter training data path: ")
        val_data_path = input("Enter validation data path: ")
        batch_size = config.get("batch_size")
        learning_rate = config.get("learning_rate")
        num_epochs = config.get("num_epochs")

        train_model(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs)

    elif command == "infer":
        model_name = input("Enter model name: ")
        tokenizer_name = input("Enter tokenizer name: ")
        test_data_path = input("Enter test data path: ")
        batch_size = config.get("batch_size")

        infer_model(model_name, tokenizer_name, test_data_path, batch_size)

    else:
        logging.error("Invalid command entered.")
        print("Please enter a valid command: 'train' or 'infer'.")

if __name__ == "__main__":
    main_cli()
