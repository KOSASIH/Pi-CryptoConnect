import tkinter as tk
from tkinter import filedialog

from src.model.inference import ModelInferencer
from src.model.training import ModelTrainer


class ModelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Model Interface")

        self.model_name = tk.StringVar()
        self.tokenizer_name = tk.StringVar()
        self.train_data_path = tk.StringVar()
        self.val_data_path = tk.StringVar()
        self.test_data_path = tk.StringVar()
        self.batch_size = tk.IntVar()
        self.learning_rate = tk.DoubleVar()
        self.num_epochs = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Model Name:").pack()
        tk.Entry(self.master, textvariable=self.model_name).pack()

        tk.Label(self.master, text="Tokenizer Name:").pack()
        tk.Entry(self.master, textvariable=self.tokenizer_name).pack()

        tk.Label(self.master, text="Train Data Path:").pack()
        tk.Entry(self.master, textvariable=self.train_data_path).pack()

        tk.Button(self.master, text="Browse", command=self.browse_train_data).pack()

        tk.Label(self.master, text="Val Data Path:").pack()
        tk.Entry(self.master, textvariable=self.val_data_path).pack()

        tk.Label(self.master, text="Test Data Path:").pack()
        tk.Entry(self.master, textvariable=self.test_data_path).pack()

        tk.Label(self.master, text="Batch Size:").pack()
        tk.Entry(self.master, textvariable=self.batch_size).pack()

        tk.Label(self.master, text="Learning Rate:").pack()
        tk.Entry(self.master, textvariable=self.learning_rate).pack()

        tk.Label(self.master, text="Num Epochs:").pack()
        tk.Entry(self.master, textvariable=self.num_epochs).pack()

        tk.Button(self.master, text="Train", command=self.train_model).pack()
        tk.Button(self.master, text="Infer", command=self.infer_model).pack()

    def browse_train_data(self):
        file_path = filedialog.askopenfilename()
        self.train_data_path.set(file_path)

    def train_model(self):
        model_name = self.model_name.get()
        tokenizer_name = self.tokenizer_name.get()
        train_data_path = self.train_data_path.get()
        val_data_path = self.val_data_path.get()
        batch_size = self.batch_size.get()
        learning_rate = self.learning_rate.get()
        num_epochs = self.num_epochs.get()

        trainer = ModelTrainer(
            model_name,
            tokenizer_name,
            train_data_path,
            val_data_path,
            batch_size,
            learning_rate,
            num_epochs,
        )
        trainer.train()

    def infer_model(self):
        model_name = self.model_name.get()
        tokenizer_name = self.tokenizer_name.get()
        test_data_path = self.test_data_path.get()
        batch_size = self.batch_size.get()

        inferencer = ModelInferencer(
            model_name, tokenizer_name, test_data_path, batch_size
        )
        inferencer.infer()


root = tk.Tk()
gui = ModelGUI(root)
root.mainloop()
