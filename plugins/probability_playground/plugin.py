import numpy as np
from scipy.ndimage import gaussian_filter
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pygame
from plugin_base import PluginBase

class GameVisualizerPlugin(PluginBase):
    def __init__(self):
        super().__init__('game_visualizer')
        
        # Generate a synthetic binary classification dataset
        self.X, self.y = make_blobs(n_samples=200, centers=2, random_state=42, cluster_std=1.5)

        # Split the dataset into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        # Initialize classifiers
        self.classifiers = {
            'Logistic Regression': LogisticRegression(),
            'Random Forest': RandomForestClassifier(),
            'SVM': SVC(probability=True)
        }

        # Default classifier
        self.current_classifier_name = 'Random Forest'
        self.model = self.classifiers[self.current_classifier_name]
        self.model.fit(self.X_train, self.y_train)

        # Pygame setup
        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Probability Concepts Visualization")

        # Colors
        self.BLUE = np.array([0, 0, 255])
        self.RED = np.array([255, 0, 0])
        self.WHITE = np.array([255, 255, 255])
        self.BLACK = np.array([0, 0, 0])
        self.GREEN = np.array([0, 255, 0])
        self.ORANGE = np.array([255, 165, 0])
        self.PURPLE = np.array([128, 0, 128])
        self.BLUE_back = np.array([0, 0, 100])
        self.RED_back = np.array([100, 0, 0])

        # Grid resolution
        self.grid_resolution = 100

        # Define range for the grid
        self.x_min, self.x_max = self.X[:, 0].min() - 1, self.X[:, 0].max() + 1
        self.y_min, self.y_max = self.X[:, 1].min() - 1, self.X[:, 1].max() + 1

        # Calculate scale factor
        self.x_scale = self.window_size / (self.x_max - self.x_min)
        self.y_scale = self.window_size / (self.y_max - self.y_min)

        # Variables for adding points
        self.new_points = []
        self.current_label = 0
        self.grid_cache = None

        # Font
        self.font = pygame.font.SysFont(None, 30)

        # Initial classification
        self.classify_grid()

    def classify_grid(self):
        x_range = np.linspace(self.x_min, self.x_max, self.grid_resolution)
        y_range = np.linspace(self.y_min, self.y_max, self.grid_resolution)
        xx, yy = np.meshgrid(x_range, y_range)
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        if hasattr(self.model, 'predict_proba'):
            predictions_proba = self.model.predict_proba(grid_points)
            predictions = (predictions_proba[:, 1] > 0.5).astype(int)
        else:
            predictions = self.model.predict(grid_points)

        colors = np.zeros((grid_points.shape[0], 3), dtype=int)
        colors[predictions == 1] = self.BLUE_back
        colors[predictions == 0] = self.RED_back
        colors_reshaped = colors.reshape((self.grid_resolution, self.grid_resolution, 3))
        self.grid_cache = gaussian_filter(colors_reshaped.astype(float), sigma=1.0)

    def grid_to_surface(self):
        array = np.clip(self.grid_cache, 0, 255).astype(np.uint8)
        surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        scaled_surface = pygame.transform.scale(surface, (self.window_size, self.window_size))
        return scaled_surface

    def calculate_statistics(self):
        combined_points = np.vstack((self.X, np.array([[p[0], p[1]] for p in self.new_points]))) if self.new_points else self.X
        mean = np.mean(combined_points, axis=0)
        median = np.median(combined_points, axis=0)
        std_dev = np.std(combined_points, axis=0)
        iqr = np.percentile(combined_points, 75, axis=0) - np.percentile(combined_points, 25, axis=0)
        min_point = np.min(combined_points, axis=0)
        max_point = np.max(combined_points, axis=0)
        return mean, median, std_dev, iqr, min_point, max_point

    def draw_statistics(self, mean, median, std_dev, iqr, min_point, max_point):
        # Drawing statistics (same logic as before)
        ...

    def update(self, events, delta_time):
        data_changed = False
        for event in events:
            if event.type == pygame.QUIT:
                self.active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_label = 0
                elif event.key == pygame.K_2:
                    self.current_label = 1
                elif event.key == pygame.K_r:
                    X_combined = np.vstack((self.X, np.array([[p[0], p[1]] for p in self.new_points])))
                    y_combined = np.hstack((self.y, np.array([p[2] for p in self.new_points]))) if self.new_points else self.y
                    self.model.fit(X_combined, y_combined)
                    self.classify_grid()
                    data_changed = False
                elif event.key == pygame.K_l:
                    self.current_classifier_name = 'Logistic Regression'
                    self.model = self.classifiers[self.current_classifier_name]
                    self.classify_grid()
                elif event.key == pygame.K_f:
                    self.current_classifier_name = 'Random Forest'
                    self.model = self.classifiers[self.current_classifier_name]
                    self.classify_grid()
                elif event.key == pygame.K_s:
                    self.current_classifier_name = 'SVM'
                    self.model = self.classifiers[self.current_classifier_name]
                    self.classify_grid()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                data_x = self.x_min + (mouse_x / self.window_size) * (self.x_max - self.x_min)
                data_y = self.y_min + (mouse_y / self.window_size) * (self.y_max - self.y_min)
                self.new_points.append((data_x, data_y, self.current_label))
                data_changed = True

    def draw(self, surface):
        surface.fill(self.WHITE)
        grid_surface = self.grid_to_surface()
        surface.blit(grid_surface, (0, 0))

        for point, label in zip(self.X, self.y):
            color = self.BLUE if label == 1 else self.RED
            screen_x = int((point[0] - self.x_min) * self.x_scale)
            screen_y = int((point[1] - self.y_min) * self.y_scale)
            pygame.draw.circle(surface, self.BLACK, (screen_x, screen_y), 6)
            pygame.draw.circle(surface, color, (screen_x, screen_y), 5)

        for point in self.new_points:
            data_x, data_y, label = point
            color = self.BLUE if label == 1 else self.RED
            screen_x = int((data_x - self.x_min) * self.x_scale)
            screen_y = int((data_y - self.y_min) * self.y_scale)
            pygame.draw.circle(surface, self.BLACK, (screen_x, screen_y), 6)
            pygame.draw.circle(surface, color, (screen_x, screen_y), 5)

        mean, median, std_dev, iqr, min_point, max_point = self.calculate_statistics()
        self.draw_statistics(mean, median, std_dev, iqr, min_point, max_point)

        status_text = f"Current Classifier: {self.current_classifier_name} | Current Label: {'Blue (1)' if self.current_label == 1 else 'Red (0)'}"
        label_surface = self.font.render(status_text, True, self.BLACK)
        surface.blit(label_surface, (10, 10))

# Required for dynamic plugin loading
plugin = GameVisualizerPlugin()
