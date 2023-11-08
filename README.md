# ABC - Toolkit
Docker containers for XNAT integration.

## Building an image
Commands need to be formatted as a JSON list and written into the associated Dockerfile. To do this:
1. Write the commands into a file (`command.json`). See [here](https://github.com/NrgXnat/docker-images/tree/master) for examples.
2. Prepare the Dockerfile.
3. Run `./command2label.py PATH-TO-COMMAND.JSON >> PATH-TO-DOCKERFILE`

Then build the image as normal:

```
$ docker build -t dmcsweeney/IMAGE-NAME:VERSION -f PATH-TO-DOCKERFILE .
```
And push to DockerHub - so that XNAT can see it:
```
$ docker push IMAGE-NAME:VERSION
```
## Todo
- `src` should be cloned from source directory (this needs to be set up).
- `requirements.txt` was copied from `sanity-viewer/master`, needs trimming.

