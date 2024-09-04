from uploader import write_df
from prefect import flow,task


@task
def uploader_pipeline():
    write_df()


@flow(log_prints=True)
def push_to_sheet():
    print("Pipeline is running")
    uploader_pipeline()


if __name__ == "__main__":
    push_to_sheet()