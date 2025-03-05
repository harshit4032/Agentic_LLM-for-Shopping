import jsonlines
import pandas as pd
import logging



def load_webshop_dataset():
    """
    Loads a sample Webshop dataset for evaluation.
    Replace this with real dataset loading if available.
    """
    return [
        {"question": "Find a floral skirt under $40 in size S. Is it in stock, and can I apply the discount code 'SAVE10'?"},
        {"question": "I need white sneakers (size 8) for under $70 that can arrive by Friday."},
        {"question": "I found a 'casual denim jacket' at $80 on SiteA. Any better deals?"},
        {"question": "I want to buy a cocktail dress from SiteB, but only if returns are hassle-free. Do they accept returns?"},
        {"question": "Find a laptop with 16GB RAM, under $1000, with fast shipping."}
    ]


def load_products(file_path):
    """
    Loads product data from the Webshop products.jsonl file.
    """
    products = []
    try:
        with jsonlines.open(file_path) as reader:
            for obj in reader:
                products.append(obj)
        logging.info(f"Loaded {len(products)} products.")
    except Exception as e:
        logging.error(f"Failed to load products: {e}")
    return pd.DataFrame(products)


def load_tasks(file_path):
    """
    Loads goal-oriented tasks from the Webshop tasks.jsonl file.
    """
    tasks = []
    try:
        with jsonlines.open(file_path) as reader:
            for obj in reader:
                tasks.append(obj)
        logging.info(f"Loaded {len(tasks)} tasks.")
    except Exception as e:
        logging.error(f"Failed to load tasks: {e}")
    return pd.DataFrame(tasks)


def get_sample_task_and_products(tasks_df, products_df, task_index=0, num_products=5):
    """
    Retrieves a sample task and a random selection of product pages.
    """
    task = tasks_df.iloc[task_index]
    sample_products = products_df.sample(n=num_products, random_state=42)
    return task, sample_products