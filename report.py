import boto3

from botocore.exceptions import NoCredentialsError
from datetime import datetime

from database.queries.report import count_order_by_status

def generate_report():
    now_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    results = count_order_by_status()
    report_data = {
        "created_at": now_time, 
        "trackingSummary": dict(results)
    }

    # s3
    bucket_name = "cron-report-remote4"
    s3 = boto3.client('s3')
    try:
        s3.put_object(Body=str(report_data), Bucket=bucket_name, Key=f"report@{now_time}")
        print("Report uploaded to S3 successfully.")
    except NoCredentialsError:
        print("AWS credentials not available.")

if __name__ == '__main__':
    generate_report()
