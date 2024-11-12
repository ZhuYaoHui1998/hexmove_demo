
# hexmove_demo
hexmove_SLAM_demo

# pull docker images in jetson
```bash
docker pull yaohui1998/seeed-hexmove:v2.0
```

# Run Docker

```bash
sudo docker run -dit --name=noetic --network host --ipc=host  --privileged -v /home/seeed:/home/seeed -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/dri/renderD128 --device=/dev/*:/dev/* -v /dev:/dev -v /dev/dri:/dev/dri --device=/dev/snd -e DISPLAY=:0  -w /home/seeed yaohui1998/seeed-hexmove:v2.0
```

# Start vehicle lidar point2laser slam  nav
```bash
roslaunch xpkg_vehicle start.launch 
```

# start gmapping 
```bash
roslaunch nav gmapping.launch 
```


# save map 
```bash
roslaunch nav map_save.launch 
```


# waypoint multy goal navigation 
```bash
python /path to nav package/scripts/waypoint.py
```
