import time
import boto3
from zip_util import *

try:
    import paramiko
except:
    print("PARAMIKO FAILED TO IMPORT")


def OpenCredentials(cred_path: str):
    """
    Opens and parses an AWS credentials file.

    :param cred_path: Path to the file containing the credentials
    :return: A dict containing the credentials
    """
    with open(cred_path) as file:
        keys, values = map(lambda s: s.strip().split(','), file)
    credentials = dict(zip(keys, values))
    return credentials


def OpenSession(cred_path: str, region: str = 'us-east-2'):
    cred = OpenCredentials(cred_path)
    return boto3.session.Session(
        aws_access_key_id=cred['Access key ID'],
        aws_secret_access_key=cred['Secret access key'],
        region_name=region
    )


def OpenEC2Client(cred_path: str, region: str = 'us-east-2'):
    """
    Open a boto3 EC2 resource using the specified credentials in the specified region

    :param cred_path: Path to the credentials file
    :param region: region to open the client in
    :return:
    """
    session = OpenSession(cred_path, region)
    ec2_client = session.client('ec2', region_name=region)
    return ec2_client


def OpenEC2Resource(cred_path: str, region: str = 'us-east-2'):
    """
    Open a boto3 EC2 resource using the specified credentials in the specified region

    :param cred_path: Path to the credentials file
    :param region: region to open the client in
    :return:
    """
    session = OpenSession(cred_path, region)
    ec2_resource = session.resource('ec2', region_name=region)
    return ec2_resource


def OpenLambdaClient(cred_path: str, region: str = 'us-east-2'):
    """
    Open a boto3 Lambda client using the specified credentials in the specified region

    :param cred_path: Path to the credentials file
    :param region: region to open the client in
    :return:
    """
    session = OpenSession(cred_path, region)
    lambda_client = session.client('lambda', region_name=region)
    return lambda_client


def OpenLambdaResource(cred_path: str, region: str = 'us-east-2'):
    """
    Open a boto3 Lambda resource using the specified credentials in the specified region

    :param cred_path: Path to the credentials file
    :param region: region to open the resource in
    :return:
    """
    session = OpenSession(cred_path, region)
    lambda_resource = session.resource('lambda', region_name=region)
    return lambda_resource


def OpenS3Client(cred_path: str, region: str = 'us-east-2'):
    """
    Open a boto3 S3 client using the specified credentials in the specified region

    :param cred_path: Path to the credentials file
    :param region: region to open the client in
    :return: The opened s3 client
    """
    session = OpenSession(cred_path, region)
    s3_client = session.client('s3', region_name=region)
    return s3_client


class EC2_Client:
    def __init__(self, cred_path: str, region: str = 'us-east-2'):
        """
        Open a boto3 EC2 client using the specified credentials in the specified region

        :param cred_path: Path to the credentials file
        :param region: region to open the client in
        :return:
        """
        self.client = OpenEC2Client(cred_path, region)

    def GetDNS(self, instance_id: str):
        """
        Retrieves the public dns of an ec2-instance

        :param instance_id: Id of the instance to get the dns
        :return: A string containing the dns
        """
        response = self.client.describe_instances(InstanceIds=[instance_id])
        instance = response["Reservations"][0]["Instances"][0]
        dns = instance["PublicDnsName"]
        return dns

    def SSH(self, instance_id: str, key_file: str, user_name: str = "ec2-user"):
        """
        Connects to an ec2-instance through a Paramiko ssh client.

        :param instance_id: Id of the instance to connect to
        :param key_file: File path leading to the file containing the key pair used to connect to the instance
        :param user_name: User lambda_name used to connect to the instance
        :return: The Paramiko ssh client
        """
        dns = self.GetDNS(instance_id)
        ssh = paramiko.SSHClient()
        # Allow the ssh client to accept untrusted hosts
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Convert the private key file to something that paramiko understands
        key = paramiko.RSAKey.from_private_key_file(key_file)
        # Use our ssh client to start a jupyter lab
        ssh.connect(
            hostname=dns,
            username=user_name,
            pkey=key
        )
        return ssh

    def GetStatus(self, instance_id: str):
        """
        Gets the status of an EC2 instance

        :param instance_id: Id of the instance to check
        :return: The status code of the EC2 instance
        """

        instance = self.client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
        return instance['State']['Code']

    def IsRunning(self, instance_id: str):
        """
        Checks if an EC2 instance is running

        :param instance_id: Id of the instance to check
        :return: True if the instance is running
        """
        return self.GetStatus(instance_id) == 16

    def WaitTillRunning(self, instance_id: str, timeout: int = 300):
        """
        Halts code execution until an EC2 instance is running.

        Raises a TimeoutError() if time exceeds the timeout

        :param instance_id: Id of the instance to wait for
        :param timeout: Maximum length of time to wait (in secs)
        :return:
        """
        start = time.time()
        while not self.IsRunning(instance_id):
            if time.time() - start > timeout:
                raise TimeoutError()
            time.sleep(1)

    def GetTags(self, instance_id: str):
        """
        Retrieves the tags from an EC2 instance and returns them in dict form:
            {
                tag_key: tag_value,
            }

        :param instance_id: The id of the instance to get the tags from
        :return: Thr tags of the instance in dict form
        """
        response = self.client.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        tag_list = instance['Tags']
        tag_dict = dict((map(lambda d: (d['Key'], d["Value"]), tag_list)))
        return tag_dict


class Lambda_Client:
    def __init__(self, cred_path: str, bucket_name: str, region: str = 'us-east-2'):
        """
        Open a boto3 EC2 client using the specified credentials in the specified region

        :param cred_path: Path to the credentials file
        :param bucket_name: Name of the s3 bucket where the lambda function will be stored
        :param region: region to open the client in
        :return:
        """
        self.client = OpenLambdaClient(cred_path, region)
        self.s3 = OpenS3Client(cred_path, region)
        self.bucket_name = bucket_name

    def UpdateLambda(self, lambda_name: str, zip_path: str):
        """
        Updates a AWS Lambda function using the given zip file

        :param lambda_name: Name of the Lambda function to be updated
        :param zip_path: Path to the zip file to be uploaded to the function
        :return: The response from Lambda
        """
        key = '{}/{}'.format(lambda_name, os.path.basename(zip_path))
        print("Uploading to s3... ", end='')
        with open(zip_path, 'rb') as zip_file:
            self.s3.put_object(
                Body=zip_file,
                Bucket=self.bucket_name,
                Key=key
            )
        print("Uploaded!")
        print("Updating Lambda... ", end='')
        response = self.client.update_function_code(
            FunctionName=lambda_name,
            S3Bucket=self.bucket_name,
            S3Key=key,
        )
        print('Updated!')
        return response

    def UpdateLambdaFromFolder(self, lambda_name: str, folder_path: str):
        """
        Updates a AWS Lambda function using the given folder

        Does so by zipping the folder first

        :param lambda_name: Name of the Lambda function to be updated
        :param folder_path: Path to the folder to be uploaded to the function
        :return: The response from Lambda
        """
        print("Zipping folder... ", end='')
        zip_file_path = ZipFolder(folder_path)
        print("Zipped!")
        response = self.UpdateLambda(lambda_name, zip_file_path)
        return response
