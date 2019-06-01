from datetime import datetime
import hashlib
import json
import os


dirname = os.path.dirname(__file__)
repo = os.path.join(dirname, "repo")

try:
    path = os.path.join(repo, "METADATA.json")
    with open(path, "rb") as f:
        metadata = f.read()
        metadata = json.loads(metadata)
except FileNotFoundError:
    metadata = dict()

for file_name in os.listdir(repo):
    if not file_name.endswith(".json"):
        md5_hash = hashlib.md5()
        sha1_hash = hashlib.sha1()
        sha256_hash = hashlib.sha256()
        path = os.path.join(repo, file_name)
        with open(path, "rb") as f:
            buffer = f.read()
            md5_hash.update(buffer)
            sha1_hash.update(buffer)
            sha256_hash.update(buffer)
            mtime = os.path.getmtime(path)
            last_modified = datetime.fromtimestamp(mtime)
        if file_name not in metadata:
            metadata[file_name] = dict()
        metadata[file_name]["last_modified"] = last_modified.isoformat()
        metadata[file_name]["md5"] = md5_hash.hexdigest()
        metadata[file_name]["sha1"] = sha1_hash.hexdigest()
        metadata[file_name]["sha256"] = sha256_hash.hexdigest()
        if "description" not in metadata[file_name]:
            metadata[file_name]["description"] = ""

print(json.dumps(metadata, sort_keys=True, indent=4))
