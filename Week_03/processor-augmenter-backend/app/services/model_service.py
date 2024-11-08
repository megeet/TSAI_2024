import torch
from typing import Dict
import io
import random
import math

class ModelService:
    def __init__(self):
        pass

    def normalize(self, vertices):
        centroid = vertices.mean(dim=0)
        vertices = vertices - centroid
        max_dist = torch.max(torch.norm(vertices, dim=1))
        vertices = vertices / max_dist
        return vertices

    def random_rotation_matrix(self, max_angle=10):
        # Convert degrees to radians
        angle = random.uniform(-max_angle, max_angle) * math.pi / 180
        
        # Create rotation matrices for each axis
        cos_t = torch.cos(torch.tensor(angle))
        sin_t = torch.sin(torch.tensor(angle))
        
        # Rotation around X axis
        rot_x = torch.tensor([
            [1, 0, 0],
            [0, cos_t, -sin_t],
            [0, sin_t, cos_t]
        ])
        
        # Rotation around Y axis
        rot_y = torch.tensor([
            [cos_t, 0, sin_t],
            [0, 1, 0],
            [-sin_t, 0, cos_t]
        ])
        
        # Rotation around Z axis
        rot_z = torch.tensor([
            [cos_t, -sin_t, 0],
            [sin_t, cos_t, 0],
            [0, 0, 1]
        ])
        
        # Combine rotations
        rotation_matrix = torch.matmul(torch.matmul(rot_x, rot_y), rot_z)
        return rotation_matrix

    def random_scale(self, vertices, scale_range=0.2):
        scale = torch.rand(3) * scale_range * 2 + (1 - scale_range)  # Random scale between 0.8 and 1.2
        return vertices * scale

    def horizontal_flip(self, vertices, probability=0.5):
        if random.random() < probability:
            vertices[:, 0] = -vertices[:, 0]  # Flip x-coordinates
        return vertices

    def load_off_file(self, file_data: bytes) -> Dict:
        try:
            # Read OFF file content
            content = io.StringIO(file_data.decode('utf-8'))
            lines = content.readlines()
            
            # Parse OFF header
            if lines[0].strip() != 'OFF':
                raise ValueError("Not a valid OFF file")
            
            # Get counts
            num_vertices, num_faces, _ = map(int, lines[1].strip().split())
            
            # Read vertices
            vertices = []
            for i in range(num_vertices):
                x, y, z = map(float, lines[i + 2].strip().split())
                vertices.append([x, y, z])
            
            # Read faces
            faces = []
            for i in range(num_faces):
                face = list(map(int, lines[i + num_vertices + 2].strip().split()))[1:]
                faces.append(face)
            
            # Convert to torch tensors
            vertices = torch.tensor(vertices, dtype=torch.float32)
            faces = torch.tensor(faces, dtype=torch.int64)
            
            # Normalize vertices
            vertices = self.normalize(vertices)
            
            return {
                'vertices': vertices.tolist(),
                'faces': faces.tolist()
            }
        except Exception as e:
            print(f"Error loading OFF file: {str(e)}")
            raise

    def process_model(self, model_data: Dict) -> Dict:
        try:
            # Convert to torch tensors
            vertices = torch.tensor(model_data['vertices'], dtype=torch.float32)
            faces = torch.tensor(model_data['faces'], dtype=torch.int64)
            
            # Normalize vertices
            vertices = self.normalize(vertices)
            
            # Simplify mesh by averaging nearby vertices
            unique_vertices, indices = torch.unique(vertices, dim=0, return_inverse=True)
            new_faces = indices[faces]
            
            return {
                'vertices': unique_vertices.tolist(),
                'faces': new_faces.tolist()
            }
        except Exception as e:
            print(f"Error processing model: {str(e)}")
            raise

    def augment_model(self, model_data: Dict) -> Dict:
        try:
            # Convert to torch tensors
            vertices = torch.tensor(model_data['vertices'], dtype=torch.float32)
            faces = torch.tensor(model_data['faces'], dtype=torch.int64)
            
            # Apply augmentations
            # 1. Random rotation
            rotation_matrix = self.random_rotation_matrix()
            vertices = torch.matmul(vertices, rotation_matrix)
            
            # 2. Random scaling
            vertices = self.random_scale(vertices)
            
            # 3. Random horizontal flip
            vertices = self.horizontal_flip(vertices)
            
            # Normalize after transformations
            vertices = self.normalize(vertices)
            
            return {
                'vertices': vertices.tolist(),
                'faces': faces.tolist()
            }
        except Exception as e:
            print(f"Error augmenting model: {str(e)}")
            raise