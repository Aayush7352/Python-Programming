"""
Fine-tuning LLMs demonstration.

Requires: pip install torch transformers datasets accelerate
"""
import sys


def main():
    try:
        import torch
        from transformers import (
            AutoTokenizer, AutoModelForSequenceClassification,
            TrainingArguments, Trainer, pipeline
        )
        from datasets import Dataset
        import numpy as np
    except ImportError:
        print("Required packages not installed.")
        print("pip install torch transformers datasets accelerate")
        sys.exit(1)

    print("=== Fine-tuning LLMs ===\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using: {device}")

    # Load a small pre-trained model for demonstration
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"

    print(f"  Loading tokenizer and model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Freeze base layers (only fine-tune classifier head)
    for param in model.distilbert.parameters():
        param.requires_grad = False

    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Trainable params: {trainable_params:,} / {total_params:,}")

    # Create synthetic training data
    print("\n=== Creating Training Data ===")
    texts = [
        "This movie was fantastic!",
        "I really enjoyed this product",
        "Terrible experience, would not recommend",
        "Absolutely amazing!",
        "Not worth the money",
        "Great service and quality",
        "Disappointing and poor quality",
        "Best purchase I've made",
        "Horrible customer support",
        "Very satisfied with my purchase",
    ]
    labels = [1, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # 1=positive, 0=negative

    dataset = Dataset.from_dict({"text": texts, "label": labels})

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    tokenized_dataset = dataset.map(tokenize_function, batched=True)
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="/tmp/llm_finetune",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=10,
        weight_decay=0.01,
        logging_dir="/tmp/logs",
        logging_steps=5,
        evaluation_strategy="epoch",
        save_strategy="no",
        report_to="none",
        disable_tqdm=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
    )

    print("\n=== Training ===")
    trainer.train()

    print("\n=== Evaluation ===")
    eval_results = trainer.evaluate()
    print(f"  Evaluation results: {eval_results}")

    # Inference with fine-tuned model
    print("\n=== Inference ===")
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1,
    )

    test_texts = [
        "This is absolutely wonderful!",
        "I hate this so much",
        "Pretty good overall",
        "Not my favorite",
    ]

    for text in test_texts:
        result = classifier(text)[0]
        print(f"  '{text}' -> {result['label']} ({result['score']:.4f})")

    print("\n=== Fine-tuning Approaches ===")
    print("  1. Full fine-tuning: update all parameters")
    print("  2. Feature extraction: freeze base, train head")
    print("  3. LoRA: low-rank adaptation")
    print("  4. Prefix tuning: learn virtual tokens")
    print("  5. Prompt tuning: optimize input prompts")

    print("\n=== Best Practices ===")
    print("  1. Start with a good pre-trained model")
    print("  2. Use appropriate learning rate (2e-5 to 5e-5)")
    print("  3. Use gradient accumulation for large models")
    print("  4. Monitor for overfitting")
    print("  5. Use mixed precision training")
    print("  6. Evaluate on validation set regularly")
    print("  7. Save checkpoints for recovery")


if __name__ == "__main__":
    main()
