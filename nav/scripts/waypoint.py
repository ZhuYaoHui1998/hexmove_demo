#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PointStamped, PoseStamped
from actionlib_msgs.msg import GoalStatusArray

# 全局变量，用于存储点击的点和机器人当前的状态
waypoints = []
current_goal_reached = True  # 初始状态设为True，表示可以发送第一个目标点

def clicked_point_callback(msg):
    global waypoints
    point = msg.point
    rospy.loginfo("New point received: x: {}, y: {}, z: {}".format(point.x, point.y, point.z))
    waypoints.append(point)

def status_callback(msg):
    global current_goal_reached
    # 检查最新的状态是否存在，并且判断是否达到了目标点
    if msg.status_list:
        latest_status = msg.status_list[-1].status
        if latest_status == 3:  # 如果状态等于3，表示到达目标点
            rospy.loginfo("Goal reached.")
            current_goal_reached = True
        else:
            current_goal_reached = False

def publish_waypoints():
    global waypoints, current_goal_reached

    # 初始化节点
    rospy.init_node('waypoint_collector', anonymous=True)

    # 订阅/clicked_point主题
    rospy.Subscriber("/clicked_point", PointStamped, clicked_point_callback)

    # 订阅/move_base/status主题
    rospy.Subscriber("/move_base/status", GoalStatusArray, status_callback)

    # 发布到/move_base_simple/goal
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    rate = rospy.Rate(1)  # 设置发布频率为1Hz
    waypoint_index = 0  # 当前巡航到的点的索引
    while not rospy.is_shutdown():
        # 如果有新的目标点且机器人到达了前一个目标点
        if waypoint_index < len(waypoints) and current_goal_reached:
            # 创建并发布PoseStamped消息
            goal = PoseStamped()
            goal.header.frame_id = "map"  # 确保帧ID与RViz中使用的一致
            goal.header.stamp = rospy.Time.now()
            goal.pose.position.x = waypoints[waypoint_index].x
            goal.pose.position.y = waypoints[waypoint_index].y
            goal.pose.position.z = waypoints[waypoint_index].z
            goal.pose.orientation.w = 1.0  # 设定一个默认的方向

            rospy.loginfo("Publishing waypoint {}: x: {}, y: {}, z: {}".format(
                waypoint_index, waypoints[waypoint_index].x, waypoints[waypoint_index].y, waypoints[waypoint_index].z))
            goal_pub.publish(goal)

            # 更新状态，等待到达目标点
            current_goal_reached = False
            waypoint_index += 1

        rate.sleep()

if __name__ == '__main__':
    try:
        publish_waypoints()
    except rospy.ROSInterruptException:
        pass
