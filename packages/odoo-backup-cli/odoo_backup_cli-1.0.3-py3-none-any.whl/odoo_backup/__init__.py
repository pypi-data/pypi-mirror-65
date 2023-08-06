from datetime import datetime

import click
from minio import Minio
from requests import post


@click.command()
@click.option('--odoo_url', help='Odoo URL')
@click.option('--master_password', help='Odoo DB master password')
@click.option('--db', help='Database')
@click.option('--s3_url', help='S3 Bucket URL')
@click.option('--s3_bucket', help='S3 bucket')
@click.option('--s3_access_token_id', help='S3 Access token ID')
@click.option('--s3_secret_token', help='S3 Secret token')
def tool(odoo_url, master_password, db, s3_url, s3_bucket, s3_access_token_id,
         s3_secret_token):
    make_backup(db, master_password, odoo_url, s3_access_token_id, s3_bucket,
                s3_secret_token, s3_url)


def make_backup(db, master_password, odoo_url, s3_access_token_id, s3_bucket,
                s3_secret_token, s3_url):
    url = f'{odoo_url}/web/database/backup'
    print(url)

    params = {
        'master_pwd': master_password,
        'name': db,
        'backup_format': 'zip'
    }
    response = post(url, data=params)
    print('Response code: ', response.status_code)
    if response.status_code == 200:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{db}{now}.zip'

        with open(filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

        minio_client = Minio(
            s3_url,
            access_key=s3_access_token_id,
            secret_key=s3_secret_token,
            secure=False
        )
        upload_url = odoo_url.replace('https://', '')
        minio_client.fput_object(s3_bucket, f'{upload_url}/{filename}',
                                 filename)
    else:
        print(response.text)
