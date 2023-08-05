import datetime
import os

from minio import Minio

exclude = {".minio.sys"}


class MiniMinio:
    def __init__(self, hostname, access_key=None, secret_key=None, secure=True):
        self.hostname = hostname
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = True

        if hostname == "local" or hostname == "remote":
            self.client = hostname
        else:
            client = Minio(hostname,
                           access_key=access_key,
                           secret_key=secret_key,
                           secure=secure)
            self.client = client

    def get_buckets(self, remote_dir):
        store = []
        if self.client == "local" or self.client == "remote":
            if self.client is "local":
                remote_dir = os.getcwd()
            for dirpath, dirs, filenames in os.walk(remote_dir, topdown=True):
                dirs[:] = set(dirs) - exclude
                for f in filenames:
                    if f[0] == ".":
                        continue
                    else:
                        path = os.path.abspath(os.path.join(dirpath, f))
                        store.append((path, datetime.datetime.strptime(time.ctime(os.path.getctime(path)),
                                                                       "%a %b %d %H:%M:%S %Y")))
        else:
            all_buckets = self.client.list_buckets()
            for bucket in all_buckets:
                store.append((bucket.name, bucket.creation_date))
        return store
