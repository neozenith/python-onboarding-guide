# GPG Commit Signing

<!--TOC-->

- [GPG Commit Signing](#gpg-commit-signing)
- [Generate the signing key(s)](#generate-the-signing-keys)
- [Restart gpg service](#restart-gpg-service)
  - [Git conditional config](#git-conditional-config)
  - [Telling Github about the key](#telling-github-about-the-key)

<!--TOC-->

# Generate the signing key(s)

[Telling Git about your signing key - GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)

```sh
# Install required tools. Pin Entry is required to assist with unlocking password protected keys.
brew install gpg pinentry-mac
gpg-agent
echo "pinentry-program $(which pinentry-mac)" >> ~/.gnupg/gpg-agent.conf
killall gpg-agent
# Generate Key using interactive prompt
gpg --full-generate-key
# Get the Key ID
gpg --list-secret-keys --keyid-format=long
```

This long key_id needs to go into your respective `~/play/.gitconfig.play` or `~/work/.gitconfig.work`

```sh
# Make exportable key
gpg --armor --export KEY_ID_HERE
````

Example output:

```sh
-----BEGIN PGP PUBLIC KEY BLOCK-----
... base64 encoded content ...
-----END PGP PUBLIC KEY BLOCK-----
```


The output of this needs to get added into Github here:

- https://github.com/settings/keys

# Restart gpg service
gpg config --kill --all 
```

## VSCode Settings to enable commit signing

VSCode `.vscode/settings.json`


```json
{
    "git.enableCommitSigning": true,
    "git-graph.repository.commits.showSignatureStatus": true,
    "git-graph.repository.sign.tags": true,
    "git-graph.repository.sign.commits": true
}
```

## Git conditional config

Setup your `git config` to conditionally load config based on the directory you are working in.

https://git-scm.com/docs/git-config#_conditional_includes

```
[includeIf "gitdir:~/play/"]
	path = ~/play/.gitconfig.play

[includeIf "gitdir:~/work/"]
	path = ~/work/.gitconfig.work
```

`~/play/.gitconfig.play`

```
[user]
  name = Josh Peak
  email = <personal email>
  signingkey = <key of personal signing key>
```



`~/work/.gitconfig.work`

```
[user]
  name = Josh Peak
  email = <work email>
  signingkey = <key of work signing key>
```


## Telling Github about the key

- For each email address you will need to add it here to verify you own the email address.
    - https://github.com/settings/emails
- You will also need to copy the output from `gpg --armor --export $KEYID` into here:
    - https://github.com/settings/keys
