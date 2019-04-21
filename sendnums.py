import boto3
import sys


s3 = boto3.resource('s3')

#numlist = '9\n8\n12\n3\n7\n10\n5'
numlist = '6\n6\n6\n6\n6\n6\n6'

s3.Bucket('szeton-capstone').put_object(Key='tweetcounter.txt', Body=numlist)
