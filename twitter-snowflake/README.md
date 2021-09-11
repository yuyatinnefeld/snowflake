# Twitter Data into Snowflake

## Pipeline and Architecture
1. Python Application in a Docker container extracts tweets by using the Twitter REST API
2. AWS S3 is stores these tweets
3. Snowpipe ingests the data into a user configured table in snowflake
4. Snowflake queries and transforms the JSON data

Twitter Developer: https://developer.twitter.com/en
Github Repo: https://github.com/Snowflake-Labs/sfguide-twitter-auto-ingest

## Setup

1. Download the repo
```bash
git clone https://github.com/Snowflake-Labs/demo-twitter-auto-ingest
cd demo-twitter-auto-ingest
```

2. Edit the Dockerfile

```bash
#get your AWS Access keys: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html
ENV AWS_Access_Key_ID="********************"\
AWS_Secret_Access_Key="****************************************"\
#get your Twitter API Key and Secret https://developer.twitter.com/en/apply-for-access
consumer_key="*************************"\
consumer_secret="**************************************************"\
# get your Twitter Access Token and Secret https://developer.twitter.com/en/apply-for-access
access_token="**************************************************"\
access_token_secret="*********************************************"\
```

```bash
#AWS bucket name
bucket="my-twitter-bucket-ytinnefeld"\

# specify your own default twitter keyword here.
keyword="covid19"

```

3. Setup the stage (Snowflake)
```sql
/*********************************************************************************
Create external S3 stage pointing to the S3 buckets storing the tweets
*********************************************************************************/

use role accountadmin
use warehouse compute_wh
create or replace database twitter_db
create or replace STAGE twitter_db.public.tweets
URL = 's3://my-twitter-bucket-ytinnefeld/'
CREDENTIALS = (AWS_KEY_ID = 'xxxxxxxxxxxxxxxxxxxx'
AWS_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
file_format=(type='JSON')
COMMENT = 'Tweets stored in S3';

```

4. Build the Image
```bash
docker build . -t snowflake-twitter
```
This command builds the Dockerfile and tags the built image as snowflake-twitter. If successful, you'll get an output whose last two lines take the following form:

```bash
writing image <YOUR_IMAGE_ID>
naming to docker.io/library/snowflake-twitter
```

5. run the image
```bash
docker run --name <YOUR_CONTAINER_NAME> snowflake-twitter:latest <YOUR_TWITTER_KEYWORD>
```
<YOUR_TWITTER_KEYWORD>: Tweets will be pulled only if they contain this hashtag. That keyword overrides the default keyword specified in your Dockerfile.
```bash
# example contaienr name = twitter-success, keyword = bitcoin
docker run --name twitter-success snowflake-twitter:latest bitcoin
```

6. Configure Snowpipe in Snowflake

6.1. Login into the Snowflake account
6.2. Query 0_setup_twitter_snowpipe.sql script
6.3. Make sure to configure event notifications in AWS S3 as described here.

7. stop the docker container

```bash
docker stop <YOUR_CONTAINER_NAME>
```

Note: the container has a "safety" timeout of 15 minutes.
