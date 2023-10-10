import oss2

class AliyunOSSClient:
    def __init__(self):
        self.access_key_id = 'your_access_key_id'
        self.access_key_secret = 'your_access_key_secret'
        self.bucket_name = 'your_bucket_name'
        self.endpoint = 'http://your-endpoint'

        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)


    def upload_file(self, local_file_path, remote_file_path):
        try:
            self.bucket.put_object_from_file(remote_file_path, local_file_path)
            print(f"Uploaded {local_file_path} to {remote_file_path} successfully.")
        except oss2.exceptions.OssError as e:
            print(f"Error uploading {local_file_path}: {str(e)}")

    def download_file(self, remote_file_path, local_file_path):
        try:
            self.bucket.get_object_to_file(remote_file_path, local_file_path)
            print(f"Downloaded {remote_file_path} to {local_file_path} successfully.")
        except oss2.exceptions.OssError as e:
            print(f"Error downloading {remote_file_path}: {str(e)}")

    def delete_file(self, remote_file_path):
        try:
            self.bucket.delete_object(remote_file_path)
            print(f"Deleted {remote_file_path} successfully.")
        except oss2.exceptions.OssError as e:
            print(f"Error deleting {remote_file_path}: {str(e)}")

if __name__ == '__main__':

    oss_client = AliyunOSSClient()
    # Upload a file
    oss_client.upload_file('local_file.txt', 'remote_folder/remote_file.txt')

    # Download a file
    oss_client.download_file('remote_folder/remote_file.txt', 'local_file_downloaded.txt')

    # Delete a file
    oss_client.delete_file('remote_folder/remote_file.txt')
