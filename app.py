import os
import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    App, Stack,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_s3 as s3,
)
import aws_cdk.aws_kinesisfirehose_alpha as firehose
import aws_cdk.aws_kinesisfirehose_destinations_alpha as destinations

class AWSService(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        # s3の作成
        bucket = s3.Bucket(self, "MyFirstBucket",
            bucket_name = "stream-bucket-cdk-sample12",
            block_public_access = 
                s3.BlockPublicAccess(
                    block_public_acls=True,
                    block_public_policy=True,
                    ignore_public_acls=True,
                    restrict_public_buckets=True
                )
        )

        # kinesisの作成
        firehose.DeliveryStream(self, "Delivery Stream",
            destinations=[destinations.S3Bucket(bucket,
            data_output_prefix="uuid",
            error_output_prefix="error",
            buffering_interval=cdk.Duration.seconds(60)
        )]
        )

        # dynamodbの作成
        table = dynamodb.Table(
            self, "usertable",
            table_name= 'test_table',
            partition_key=dynamodb.Attribute(name="uuid",type=dynamodb.AttributeType.NUMBER),
            sort_key=dynamodb.Attribute(name="date", type=dynamodb.AttributeType.STRING), 
        )


app = App()
AWSService(app, "test-stack")
app.synth()