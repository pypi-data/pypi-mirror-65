import datetime
import os
import time


def get_minio_object(attributes, s3_object, store):
    store.append(s3_object)
    return store


def get_attributes_local(files, path, store, ext):
    for name in files:
        mtime = os.path.getmtime(path)
        if ext is None:
            store.append((os.path.join(path, name),
                          datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")))
        else:
            filename, filename_ext = os.path.splitext(name)
            if filename_ext in ext:
                store.append((os.path.join(path, name),
                              datetime.datetime.strptime(time.ctime(mtime), "%a %b %d %H:%M:%S %Y")))
    return store


def path_leaf_last(path):
    head, tail = os.path.split(path)
    head = os.path.basename(head)
    return tail or head


def get_attributes_single_local(path, store):
    store.append((path,
                  datetime.datetime.strptime(time.ctime(os.path.getmtime(path)), "%a %b %d %H:%M:%S %Y")))
    return store
