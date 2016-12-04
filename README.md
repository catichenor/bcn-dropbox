# bcn-dropbox

## baby-connect-nightmare Dropbox Bridge

### What is this?

This is a Python script, using code mostly ripped off from [this Dropbox blog post](https://blogs.dropbox.com/developers/2013/11/low-latency-notification-of-dropbox-file-changes/) which works in conjunction with my fork of [baby-connect-nightmare](https://github.com/catichenor/baby-connect-nightmare) to upload info to BabyConnect using Dropbox rather than a server.

It works by scanning a directory on a Dropbox folder for changes to a file named `babyLog.txt`, then reads each line from the file as JSON, then sends a REST API request to `baby-connect-nightmare` to upload the info to BabyConnect.

### Why not just use baby-connect-nightmare?

`bcn-dropbox` allows you to use baby-connect-nightmare without a publicly-accessible server, and bypasses the need to upload login info anywhere, since your login info is stored locally.

### How do I use it?

Download or clone this repository locally, `cd` to the extracted directory, and create a JSON file called `accessInfo.json` with these contents:

```JSON
{
    "dropboxAccessToken": "abcdef1234567",
    "bcnURL": "http://localhost:3000",
    "email": "something@something.com",
    "password": "password",
    "kidID": "kid1234567890"
}
```

* `dropboxAccessToken`: This is an access token for a Dropbox app. 
    - I plan to make this script guide the user through the process of accessing this token, but a good way to set this up for now is to set up the [Dropbox-Uploader](https://github.com/andreafabrizi/Dropbox-Uploader) shell script.
* `bcnURL`: The URL and port where baby-connect-nightmare is running
    - The example uses localhost, but this could be any server you have access to.
* See the [README for baby-connect-nightmare](https://github.com/catichenor/baby-connect-nightmare/blob/master/README.md) for info on the `"email"`, `"password"`, and `"kidId"` entries.

Start up the `baby-connect-nightmare` server.

Once the `accessInfo.json` file is created, launch the script with the `python bcn-dropbox.py` command to start scanning a folder for changes to a file named `babyLog.txt`. JSON entries pushed to this .txt file should be in this format:

`{"type":"bm", "quantity":"large"}` - This is an entry for a large poopy diaper. Note that everything is on one line, which is required for this script to work.

The script will read each line from the file (usually this will be one line) as JSON, and add an entry to BabyConnect, then it will erase the file and create a new, empty `babyLog.txt` file. The script will only add an entry when the `babyLog.txt` file is not empty.
