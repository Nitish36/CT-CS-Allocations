from uploader import write_df
from ctallocation import ct_alloc
from prefect import flow,task


@task
def uploader_pipeline():
    write_df()
    ct_alloc()


@flow(log_prints=True)
def push_to_sheet():
    print("Pipeline is running")
    uploader_pipeline()


if __name__ == "__main__":
    push_to_sheet()