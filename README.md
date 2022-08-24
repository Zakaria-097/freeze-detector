## Video Freeze Detector

A simple video file scanner, that can determine if there's any freezes anywhere in a given video, as well as the exact time of the freeze.

### Prerequisites

* You need Python3. Install it here. [Python3](https://www.python.org/downloads/windows/)
* You need PIP. It should come with Python3. Verify you have it with;

```bash
pip -V
```

### Install the dependencies by running the following;

```bash
python3 -m pip install ImageHash && \
python3 -m pip install art && \
python3 -m pip install opencv_python  && \
python3 -m pip install numpy && \
python3 -m pip install Pillow

```

### Run the program
```bash
python3 freeze_detector.py

```