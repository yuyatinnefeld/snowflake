# Cloud Storage
Info: https://cloud.google.com/storage/docs/moving-buckets

## About
Cloud Storage allows world-wide storage and retrieval of any amount of data at any time. You can use Cloud Storage for a range of scenarios including serving website content, storing data for archival and disaster recovery, or distributing large data objects to users via direct download.

## Storage Type
- Standard Storage: hot data : used everyday - $.02 per GB per month 	
- Nearline Storage: warm data: used once a month - $.01 per GB per month 	
- Coldline Storage: cold data: used once a quartal - $.004 per GB per month 	
- Archive Storage: backup data: used once a year - $.0012 per GB per month

## Benefits
- Low latency
- High durability (99.999999999% annual durability)
- Strong consistency
- Flexible processing
- Strong access control
- Good solution for data like

### define ENV variables
```bash
REGION=xxxxx
ZONE=xxxxx
PROJECT_ID=xxxxx
STORAGE_CLASS=xxxx
BUCKET_NAME=xxxx
```

## create a bucket
```bash
gsutil mb -p $DEVSHELL_PROJECT_ID -c ${STORAGE_CLASS} -l ${REGION} -b on gs://${BUCKET_NAME}
```
## check buckets
```bash
gsutil ls
```

## copy a gs bucket
```bash
gsutil cp -r gs://${SOURCE_BUCKET}/* gs://${DESTINATION_BUCKET}
```

## upload local file into the gs bucket
```bash
gsutil cp ${LOCAL_FILE_PATH}/* gs://${DESTINATION_BUCKET}
```

## download the file from gs
```bash
gsutil cp gs://{BUCKET_NAME}/{FILE_NAME} {LOCAL_FILE_PATH}
```

## remove bucket / file
```bash
gsutil rm -r gs://{BUCKET_NAME}
```
