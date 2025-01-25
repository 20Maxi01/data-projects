# Fine-Tuning deepset/gbert-base for German Hate Speech Classification
## Setup
There are two model setups in the training directory:
- `BERT_FC_Layer.ipynb`: This is the script with S-Score optimization, hyperparameter tuning and pruning.
- `BERT_FC_Layer_with_fixed_params.ipynb`: This is a script for training one model on specific hyperparameters. This was used to test alternative setups based on the Interpretation of the Wandb graphs. For example when a decreasing Training loss and increasing validation loss occured a model with reduced epochs could be tested. 
<br>

Since `BERT_FC_Layer.ipynb` was the main script the following chapters will focus on this script but the basic setup of the data and model is the same in both scripts.  

### Prerequisites

- The model `deepset/gbert-base` was used 
- Google Colab Pro, Python, PyTorch were used for training and testing.
- Weights & Biases (Wandb) was used for:
  - Logging training, validation, and test metrics.
  - Generating visualizations of results (e.g. Validation loss, Training loss).
- Google Drive is mounted in Colab to store datasets, models, and logs.
- Optuna is used for hyperparameter tuning with the TPE Sampler.
- MedianPruner is used to stop unpromising trials after the third epoch.

## Data

- The dataset used for training is `Dataset_anonymized_annotated_comments_same_annotation_final.csv`.
- The dataset is located in:  
  `model/data/Dataset_anonymized_annotated_comments_same_annotation_final.csv`
- The dataset consists of labeled comments for **hate speech detection**.
- For testing purposes a **balanced subset** of 500 samples per class can be used by adjusting the variable `use_full_dataset = 0`.
- Data is **split into training (70%), validation (15%), and test (15%)**.

## Model Training

### Workflow

1. **Load and preprocess training data**:
   - Tokenization with `AutoTokenizer` (`deepset/gbert-base`).
   - Stratified split into training, validation, and test sets.
   - Compute **class weights** for handling class imbalance.
2. **Define `BERT_FY_Layer` model class**:
   - BERT encoder (`deepset/gbert-base`)
   - Fully connected classification layer
3. **Define evaluation metrics**:
   - Accuracy, Precision, Recall, F1-score, F2-score, MCC, and a custom S-Score (was provided by the Research project).
4. **Hyperparameter tuning with Optuna**:
   - **Optimizer**: TPE Sampler for Bayesian optimization.
   - **Pruning strategy**: MedianPruner (stops unpromising trials after third epoch).
   - **Warmup trials**: The first **15 trials** are used for exploration before refinement.
   - **Tuned parameters**:
     - **Epochs**: 2 - 4
     - **Batch size**: 16 or 32
     - **Learning rate**: 2e-5 to 1e-4
     - **Weight decay**: 0.01 to 0.1
     - **Warmup steps**: 5-10% of total training steps
   - **Total trials**: 50 trials are conducted to find the best model configuration.
5. **Training execution**:
   - Optuna **runs multiple trials**, logging each trial's metrics in **wandb** and `logged_model_metrics.xlsx`.
   - The best model is selected based on the S-Score.
6. **Generate Confusion matrix**:
   - After training, a **confusion matrix** is plotted to visualize classification performance.
7. **Automatic cleanup and session shutdown**:
   - `wandb.finish()` is used to ensure all logs are correctly stored.
   - Google Colab runtime is terminated after training to prevent unnecessary resource usage.

### Training Script

- `BERT_FC_Layer.ipynb`: Implements **Optuna-based hyperparameter optimization**.

## Model Saving

- The **best-performing models** are saved in **Google Drive**.
- Models are stored in timestamped folders:  
  `/content/drive/MyDrive/model/best_model_CNN_<timestamp>`
- The **final model state** and **tokenizer** are saved for later use.

## Model Testing

The trained models were evaluated on these testing datasets:

1. **Research Project Dataset**:  
   - Evaluation script: `model/BERTbase_CNN/Testing/test_BERT_CNN_on_forschungsprojekt_dataset.ipynb`
2. **GuteFrage Dataset**:
   - Evaluation script: `model/BERTbase_CNN/Testing/test_BERT_CNN_on_gutefrage_dataset.ipynb`
3. **15% Split of Training Data**:  
   - Evaluation is integrated in the training notebooks.

### Testing Workflow

1. Load the trained model from **Google Drive**.
2. Load and tokenize the test dataset.
3. Run inference on the dataset.
4. Compute and log key metrics (**Accuracy, Precision, Recall, F1, F2, MCC, and S-Score**).
5. **Plot and display confusion matrices**.
6. Log all results to **wandb**.

### Results Storage

- TThe selected best models are saved to a new directory including the model class and a timestamp in the name.
- `Wandb`and `logged_model_metrics.xlsx` store all training trials and testing results .

