# From  a POST request to a Hyper file published to Amazon S3

Once this project deployed to Heroku, you can send a POST request to create a Hyper file to your Amazon S3 bucket. For this sample, we are creating an extract with meal prep data. 

### Create a Heroku Account 
Create a Heroku Account [here](https://signup.heroku.com/)

### Create an Amazon account and create a S3 bucket  
[Amazon S3](https://aws.amazon.com/s3/) or Amazon Simple Storage Service is a service offered by Amazon Web Services that provides object storage through a web service interface.

All files in S3 are stored in buckets. Buckets act as a top-level container, much like a directory. All files sent to S3 belong to a bucket, and a bucket’s name must be unique across all of S3.

#### Credentials

Access to the S3 API is governed by an Access Key ID and a Secret Access Key. The access key identifies your S3 user account, and the secret key is a password-like credential that should be stored securely.

Enabling an application to use S3 requires that the application have access to the AWS credentials as well as the name of the bucket to store files.

Your S3 credentials can be found on the [Security Credentials section](https://console.aws.amazon.com/iam/home?#security_credential) of the [AWS “My Account/Console” menu](https://aws.amazon.com/)

You will need your Access Key ID (AWS_ACCESS_KEY_ID) and Secret Access Key (AWS_SECRET_ACCESS_KEY) to configure this app. 

#### Bucket

A single bucket typically stores the files, assets, and uploads for an application. To create a bucket, access the [S3 section of the AWS Management Console and create a new bucket](https://console.aws.amazon.com/s3/home?#) in the US Standard region.

Although you have a lot of freedom in choosing a bucket name, take care in choosing a name to ensure maximum interoperability.


### Deploy on Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Sending your first POST Request

You can [download Postman](https://www.postman.com/downloads/) for free to quickly get started. 

Your endpoint is: https://NameOfHerokyApp.herokuapp.com/create

The body of you request:
```json
{
    "data": [{
        "breakfast": "eggs",
        "lunch": "salad",
        "dinner": "chicken"
    },
    {
        "breakfast": "croissant",
        "lunch": "pasta",
        "dinner": "pizza"
    }]
}
```