import openai
from config import OPENAI_API_KEY, FINE_TUNING_DATASET_FILE

openai.api_key = OPENAI_API_KEY


def upload_and_start_fine_tuning():
    """
    Uploads the fine-tuning dataset and starts fine-tuning on OpenAI.
    """
    # Upload the dataset
    file_upload = openai.File.create(
        file=open(FINE_TUNING_DATASET_FILE, "rb"),
        purpose="fine-tune"
    )
    print(f"Uploaded dataset. File ID: {file_upload.id}")

    # Start fine-tuning
    fine_tune_job = openai.FineTuningJob.create(
        training_file=file_upload.id,
        model="gpt-3.5-turbo"
    )
    print(f"Fine-tuning started. Job ID: {fine_tune_job.id}")