import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib
import random

matplotlib.rcParams['font.family'] = 'Malgun Gothic'

class TrafficLight:
    def __init__(self, intersection_id):
        self.intersection_id = intersection_id
        self.state = 'RED'
        self.timer = 30

    def update(self, traffic_density):
        if traffic_density > 7 and self.state != 'GREEN':
            self.state = 'GREEN'
            self.timer = 30
        elif traffic_density <= 7 and self.state != 'RED':
            self.state = 'RED'
            self.timer = 30

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            self.state = 'RED' if self.state == 'GREEN' else 'GREEN'
            self.timer = 30

    def __str__(self):
        return f"교차로 {self.intersection_id} 신호등: {self.state}, 타이머: {self.timer}"

class TrafficSign:
    def __init__(self, location):
        self.location = location
        self.message = '정상'
        self.color = 'blue'

    def update(self, traffic_density):
        if traffic_density > 7:
            self.message = '혼잡'
            self.color = 'red'
        elif traffic_density > 3:
            self.message = '보통'
            self.color = 'green'
        else:
            self.message = '쾌적'
            self.color = 'blue'

    def __str__(self):
        return f"교차로 {self.location} 표지판: {self.message}"

def draw_traffic_system(ax, intersections, signs, t):
    ax.clear()
    for i, intersection in enumerate(intersections):
        color = 'green' if intersection.state == 'GREEN' else 'red'
        ax.scatter(i, 2, color=color, s=500)
        ax.text(i, 2.3, f'ID: {intersection.intersection_id}', 
                horizontalalignment='center', fontsize=10, weight='bold')
        ax.text(i, 2.15, f'상태: {intersection.state}', 
                horizontalalignment='center', fontsize=9)
        ax.text(i, 2.0, f'타이머: {intersection.timer}s', 
                horizontalalignment='center', fontsize=9)

    for i, sign in enumerate(signs):
        ax.scatter(i, 0, color='gray', s=500)
        ax.text(i, 0.3, f'위치: {sign.location}', 
                horizontalalignment='center', fontsize=10, weight='bold')
        ax.text(i, 0.15, f'교통 상태: {sign.message}', 
                horizontalalignment='center', fontsize=9, color=sign.color)

    ax.set_xlim(-1, len(intersections))
    ax.set_ylim(-1, 3)
    ax.set_title(f"시간: {t}s", fontsize=16)
    ax.axis('off')

class TrafficSimulationGUI:
    def __init__(self, duration):
        self.duration = duration
        self.current_time = 0
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.intersections = [TrafficLight(i) for i in range(5)]
        self.signs = [TrafficSign(f"교차로 {i}") for i in range(5)]

        self.button_ax_backward = self.fig.add_axes([0.1, 0.05, 0.15, 0.075])
        self.button_ax_forward = self.fig.add_axes([0.3, 0.05, 0.15, 0.075])
        self.button_backward = Button(self.button_ax_backward, '이전')
        self.button_forward = Button(self.button_ax_forward, '다음')
        self.button_backward.on_clicked(self.previous_view)
        self.button_forward.on_clicked(self.next_view)

        self.update_plot()

    def next_view(self, event):
        if self.current_time < self.duration - 1:
            self.current_time += 1
            self.update_plot()

    def previous_view(self, event):
        if self.current_time > 0:
            self.current_time -= 1
            self.update_plot()

    def update_plot(self):
        traffic_densities = [random.randint(0, 10) for _ in range(5)]

        for i, intersection in enumerate(self.intersections):
            traffic_density = traffic_densities[i]
            intersection.update(traffic_density)
            print(intersection)

        for i, sign in enumerate(self.signs):
            traffic_density = traffic_densities[i]
            sign.update(traffic_density)
            print(sign)

        for intersection in self.intersections:
            intersection.tick()

        draw_traffic_system(self.ax, self.intersections, self.signs, self.current_time)
        plt.draw()

if __name__ == "__main__":
    gui = TrafficSimulationGUI(duration=100)
    plt.show()
