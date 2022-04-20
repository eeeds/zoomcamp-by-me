## 1. First create a Dockerfile with this command in this directory


```docker build -t test:pandas .```

## 2. You can now run the container with this command (Use "winpty" if you are using bash on Windows)

```winpty docker run -it test:pandas```

## 3. Create pipeline.py and copy the original to the container

```winpty docker build -t test:pandas .```