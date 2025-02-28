# src/interface/gui.py

import tkinter as tk
from tkinter import messagebox, filedialog
from src.model.training import ModelTrainer
from src.model.inference import ModelInferencer
from src.config import Config
import logging

class ModelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Model Management Interface")

        self.config = Config()  # Load configuration settings
        self.create_widgets()

    def create_widgets(self):
        """Create and place GUI widgets."""
        # Model Name
        self.model_name_label = tk.Label(self.master, text="Model Name:")
        self.model_name_label.pack()
        self.model_name_entry = tk.Entry(self.master)
        self.model_name_entry.pack()

        # Tokenizer Name
        self.tokenizer_name_label = tk.Label(self.master, text="Tokenizer Name:")
        self.tokenizer_name_label.pack()
        self.tokenizer_name_entry = tk.Entry(self.master)
        self.tokenizer_name_entry.pack()

        # Training Data Path
        self.train_data_label = tk.Label(self.master, text="Training Data Path:")
        self.train_data_label.pack()
        self.train_data_entry = tk.Entry(self.master)
        self.train_data_entry.pack()
        self.train_data_button = tk.Button(self.master, text="Browse", command=self.browse_train_data)
        self.train_data_button.pack()

        # Validation Data Path
        self.val_data_label = tk.Label(self.master, text="Validation Data Path:")
        self.val_data_label.pack()
        self.val_data_entry = tk.Entry(self.master)
        self.val_data_entry.pack()
        self.val_data_button = tk.Button(self.master, text="Browse", command=self.browse_val_data)
        self.val_data_button.pack()

        # Batch Size
        self.batch_size_label = tk.Label(self.master, text="Batch Size:")
        self.batch_size_label.pack()
        self.batch_size_entry = tk.Entry(self.master)
        self.batch_size_entry.insert(0, str(self.config.get("batch_size")))  # Default value
        self.batch_size_entry.pack()

        # Learning Rate
        self.learning_rate_label = tk.Label(self.master, text="Learning Rate:")
        self.learning_rate_label.pack()
        self.learning_rate_entry = tk.Entry(self.master)
        self.learning_rate_entry.insert(0, str(self.config.get("learning_rate")))  # Default value
        self.learning_rate_entry.pack()

        # Number of Epochs
        self.num_epochs_label = tk.Label(self.master, text="Number of Epochs:")
        self.num_epochs_label.pack()
        self.num_epochs_entry = tk.Entry(self.master)
        self.num_epochs_entry.insert(0, str(self.config.get("num_epochs")))  # Default value
        self.num_epochs_entry.pack()

        # Train Button
        self.train_button = tk.Button(self.master, text="Train Model", command=self.train_model)
        self.train_button.pack()

        # Infer Button
        self.infer_button = tk.Button(self.master, text="Infer Model", command=self.infer_model)
        self.infer_button.pack()

    def browse_train_data(self):
        """Open a file dialog to select training data."""
        filename = filedialog.askopenfilename(title="Select Training Data File")
        self.train_data_entry.delete(0, tk.END)
        self.train_data_entry.insert(0, filename)

    def browse_val_data(self):
        """Open a file dialog to select validation data."""
        filename = filedialog.askopenfilename(title="Select Validation Data File")
        self.val_data_entry.delete(0, tk.END)
        self.val_data_entry.insert(0, filename)

    def train_model(self):
        """Train the model using the provided parameters."""
        model_name = self.model_name_entry.get()
        tokenizer_name = self.tokenizer_name_entry.get()
        train_data_path = self.train_data_entry.get()
        val_data_path = self.val_data_entry.get()
        batch_size = int(self.batch_size_entry.get())
        learning_rate = float(self.learning_rate_entry.get())
        num_epochs = int(self.num_epochs_entry.get())

        try:
            logging.info("Starting model training...")
            trainer = ModelTrainer(model_name, tokenizer_name, train_data_path, val_data_path, batch_size, learning_rate, num_epochs)
            trainer.train()
            messagebox.showinfo("Success", "Model training completed successfully.")
            logging.info("Model training completed successfully.")
        except Exception as e:
            logging.error(f"Training failed: {e}")
            messagebox.showerror("Error", f"Training failed: {e}")

    def infer_model(self):
        """Infer using the trained model."""
        model_name = self.model_name_entry.get()
        tokenizer_name = self.tokenizer_name_entry.get()
        test_data_path = self.train_data_entry.get()  # Assuming test data is selected from the same entry
        batch_size = int(self.batch_size_entry.get())

        try:
            logging.info("Starting model inference...")
            inferencer = ModelInferencer(model_name, tokenizer_name, test_data_path, batch_size)
            inferencer.infer()
            messagebox.showinfo("Success", "Model inference completed successfully.")
            logging.info("Model inference completed successfully.")
        except Exception as e:
            logging.error(f"Inference failed: {e}")
            messagebox.showerror("Error", f"Inference failed: {e}")

def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = ModelGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
