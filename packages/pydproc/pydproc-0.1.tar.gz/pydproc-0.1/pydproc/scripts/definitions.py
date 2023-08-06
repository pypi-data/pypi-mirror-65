# This file contains paths to important dirs

from pathlib import Path
import os

# Get directory paths
package_dir = Path(os.path.abspath(__file__.rsplit('/', 1)[0] + '/..'))
docker_base_path = package_dir / "docker_base"
saved_images_path = package_dir / "saved_images"
saved_data_path = package_dir / "saved_data"

# Initialize directories
for p in [saved_images_path, saved_data_path]:
    if not p.exists():
        os.mkdir(p)
