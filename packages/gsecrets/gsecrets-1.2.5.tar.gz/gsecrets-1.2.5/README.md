gsecrets
===

`gsecrets` is a CLI utility and Python library for storing sensitive information using Google Cloud Key Management Service and Cloud Storage.

Architecture
---

Secrets are stored using "application level encryption". That is, secrets are stored in Google Cloud Storage, encrypted by a key before they are uploaded. Encryption keys are generated and retrieved from Google Key Management Service (KMS).

Deployment and Configuration
---

Create a keyring, key, and bucket.

Add a file `keyring.json` into the bucket with the keyring details:

```
{
	"location": "us-central1",
	"keyring": "my-key-ring",
	"key": "my-crypto-key"
}
```

Library
---

```
import gsecrets
VAULT_LOCATION = "my-project/my-bucket"
secrets_client = gsecrets.Client(VAULT_LOCATION)
    
# Get a single secret
secrets_client.get("slack/token")

# Get a dictionary of gsecrets 
secrets_client.get("manifests/admiral/env.json")

# Get a single secret from a dictionary of secrets 
secrets_client.get("manifests/admiral/env.json.airflow_fernet_key")


# Create or update a secret
secrets_client.put("slack/token", "AAABBBCCC")

# Create or update a secret, uses `dictionary.update` for the update
secrets_client.put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"})

# Replace an entire dictionary of secrets
secrets_client.put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"}, replace=True)
```

CLI
---

A CLI is provided that executes `gsecrets` inside a Docker wrapper.

Installation:

	git clone git@github.com:openeemeter/gsecrets.git
	cd gsecrets
	./install.sh

The install procedure adds the `cli.sh` scripts to `/usr/local/bin`. Make sure this directory is in your `$PATH` (normally it is by default).

The CLI depends on coreutils, so make sure if you're on mac you do `brew install coreutils`.

The library commands map to CLI actions:

```
gsecrets get my-project/my-bucket/slack/token

gsecrets put my-project/my-bucket/slack/token AAABBBCCC

gsecrets put my-project/my-bucket/slack/env.json.FERNET_KEY AAABBBCCC

# etc.

# For a full list:
gsecrets --help
```

Development
---

Run the CLI inside a container

```
./cli.sh --help
```

Release
---

```
pip install twine

python setup.py upload
```

