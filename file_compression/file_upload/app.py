import json
import base64
import boto3
import PIL
import io

# Replace these values with your MinIO information

def is_image(file_content):
    try:
        # Attempt to open the file as an image
        PIL.Image.open(io.BytesIO(file_content))
        return True
    except Exception:
        # If an exception occurs, it's not an image
        return False


def file_upload(event):    
    
    
    try :
        row_body = event['body']
        # parse body in json format
        body = json.loads(row_body)
        file_name = body['file_name']
        file_content_base64 = body['file_content_base64']
        try:
            # decode base64 file content
            file_content = base64.b64decode(file_content_base64)
            
            try :
            
                s3 = boto3.client('s3')
                s3.put_object(Body=file_content, Bucket="my-store-files", Key=file_name)
                
                if (is_image(file_content)):
                    # If the file is an image, réencode it in webp format
                    try:
                        image = PIL.Image.open(io.BytesIO(file_content))
                        buffer = io.BytesIO()
                        image.save(buffer, format="WEBP")
                        buffer.seek(0)
                        file_content = buffer.read()
                        file_name = file_name + ".webp"
                        s3.put_object(Body=file_content, Bucket="my-store-files", Key=file_name)
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
                    s3.put_object(Body=file_content, Bucket="my-store-files", Key=file_name)
                    

                
                # get url of uploaded file
                url =   s3.generate_presigned_url('get_object', Params = {'Bucket': "my-store-files", 'Key': file_name})
                
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "file upload success for file: " + file_name,
                        "url": url
                    }),
                }
            except Exception as e:
                print(e)
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "error in uploading file to s3"
                    }),
                }
        except Exception as e:
            print(e)
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "error in decoding base64 file content"
                }),
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "error in parsing request body"
            }),
        }
    
    
    
    



