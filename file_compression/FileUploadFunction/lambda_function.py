import json
import base64
import boto3
from PIL import Image
import io


def is_image(file_content):
    try:
        # Attempt to open the file as an image
        Image.open(io.BytesIO(file_content))
        return True
    except Exception:
        # If an exception occurs, it's not an image
        return False
    
def change_extension(file_name, new_extension):
    # Find the index of the last dot in the file name
    last_dot_index = file_name.rfind('.')
    
    # Extract the part of the file name before the last dot
    name_without_extension = file_name[:last_dot_index] if last_dot_index != -1 else file_name
    
    # Concatenate the new name with the new extension
    new_file_name = name_without_extension + '.' + new_extension
    
    return new_file_name



def lambda_handler(event, context):    
    print("run func")
    try :
        row_body = event['body']
        print(row_body)
        # parse body in json format
        body = json.loads(row_body)
        file_name = body['file_name']
        file_content_base64 = body['file_content_base64']
  

        try:
            # decode base64 file content
            file_content = base64.b64decode(file_content_base64)
            
            try :
                s3 = boto3.client('s3')
                # s3.put_object(Body=file_content, Bucket="my-bucket", Key=file_name)
                if (is_image(file_content)):
                    # If the file is an image, réencode it in webp format
                    try:
                        image = Image.open(io.BytesIO(file_content))
                        buffer = io.BytesIO()
                        image.save(buffer, format="WEBP")
                        buffer.seek(0)
                        file_content = buffer.read()
                        file_name = change_extension(file_name, 'webp')
                        s3.put_object(Body=file_content, Bucket="my-store-files", Key=file_name, ACL='public-read')
                    except Exception as e:
                        print(e)
                        return {
                            "statusCode": 400,
                            "body": json.dumps({
                                "message": "error in converting image to webp"
                            }),
                        }
                else:
                    # If the file is not an image, import it to the bucket as is
                    print("not an image")
                    try:
                        s3.put_object(Body=file_content, Bucket="my-store-files", Key=file_name, ACL='public-read')
                    except Exception as e:
                        print(e)
                        return {
                            "statusCode": 400,
                            "body": json.dumps({
                                "message": "error in uploading file to s3"
                            }),
                        }
                    

                
                # get url of uploaded file
                url =   s3.generate_presigned_url('get_object', Params = {'Bucket': "my-store-files", 'Key': file_name})
                url = url.split("?")[0]
                
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "file upload success for file : " + file_name,
                        "url": url
                    })
                }
            except Exception:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "error in uploading file to s3"
                    })
                }
        except Exception as error:
            print(error)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "error in decoding base64 file content"
                })
            }
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "error in parsing request body"
            })
        }
    
    
    
    



