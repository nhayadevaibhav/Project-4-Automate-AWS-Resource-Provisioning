import boto3

# =========================================================
# AWS CLIENTS
# =========================================================

iam = boto3.client('iam')

s3 = boto3.client('s3')

ec2 = boto3.resource('ec2')


# =========================================================
# VARIABLES
# =========================================================

IAM_USERNAME = "vedang-dev-user"

BUCKET_NAME = "vedang-demo-bucket-2026-001"

REGION = "ap-south-1"

INSTANCE_TYPE = "t3.micro"     # Free Tier Eligible

AMI_ID = "ami-0f58b397bc5c1f2e8"


# =========================================================
# TRACK CREATED RESOURCES
# =========================================================

created_user = False
created_bucket = False
created_instance_id = None


# =========================================================
# CREATE IAM USER
# =========================================================

def create_iam_user():

    global created_user

    try:

        iam.create_user(
            UserName=IAM_USERNAME
        )

        created_user = True

        print(f"[SUCCESS] IAM User '{IAM_USERNAME}' created successfully")

    except Exception as e:

        print("[IAM ERROR]")
        print(e)

        raise


# =========================================================
# CREATE S3 BUCKET
# =========================================================

def create_s3_bucket():

    global created_bucket

    try:

        s3.create_bucket(

            Bucket=BUCKET_NAME,

            CreateBucketConfiguration={
                'LocationConstraint': REGION
            }
        )

        created_bucket = True

        print(f"[SUCCESS] S3 Bucket '{BUCKET_NAME}' created successfully")

    except Exception as e:

        print("[S3 ERROR]")
        print(e)

        raise


# =========================================================
# CREATE EC2 INSTANCE
# =========================================================

def create_ec2_instance():

    global created_instance_id

    try:

        instances = ec2.create_instances(

            ImageId=AMI_ID,

            MinCount=1,
            MaxCount=1,

            InstanceType=INSTANCE_TYPE,

            TagSpecifications=[
                {
                    'ResourceType': 'instance',

                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Boto3-FreeTier-Server'
                        }
                    ]
                }
            ]
        )

        created_instance_id = instances[0].id

        print("[SUCCESS] EC2 Instance Created")
        print("Instance ID:", created_instance_id)

    except Exception as e:

        print("[EC2 ERROR]")
        print(e)

        raise


# =========================================================
# DELETE EC2 INSTANCE
# =========================================================

def delete_ec2_instance():

    global created_instance_id

    try:

        if created_instance_id:

            instance = ec2.Instance(created_instance_id)

            instance.terminate()

            print(f"[ROLLBACK] EC2 Instance '{created_instance_id}' deleted")

    except Exception as e:

        print("[DELETE EC2 ERROR]")
        print(e)


# =========================================================
# DELETE S3 BUCKET
# =========================================================

def delete_s3_bucket():

    global created_bucket

    try:

        if created_bucket:

            s3.delete_bucket(
                Bucket=BUCKET_NAME
            )

            print(f"[ROLLBACK] S3 Bucket '{BUCKET_NAME}' deleted")

    except Exception as e:

        print("[DELETE S3 ERROR]")
        print(e)


# =========================================================
# DELETE IAM USER
# =========================================================

def delete_iam_user():

    global created_user

    try:

        if created_user:

            iam.delete_user(
                UserName=IAM_USERNAME
            )

            print(f"[ROLLBACK] IAM User '{IAM_USERNAME}' deleted")

    except Exception as e:

        print("[DELETE IAM ERROR]")
        print(e)


# =========================================================
# MAIN EXECUTION
# =========================================================

print("\n===================================")
print(" AWS AUTOMATION PROJECT STARTED ")
print("===================================\n")


try:

    # STEP 1
    create_iam_user()

    # STEP 2
    create_s3_bucket()

    # STEP 3
    create_ec2_instance()

    print("\n===================================")
    print(" AWS RESOURCE PROVISION COMPLETED ")
    print("===================================\n")


except Exception as main_error:

    print("\n[PROJECT FAILED]")
    print(main_error)

    print("\nStarting Rollback Process...\n")

    # DELETE CREATED RESOURCES
    delete_ec2_instance()

    delete_s3_bucket()

    delete_iam_user()

    print("\n[ROLLBACK COMPLETED]")