# hexmove_demo
hexmove_SLAM_demo

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
