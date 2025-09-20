import os
import pkgutil
import importlib
import sys

def import_all_models():
    """
    Dynamically import all modules in the src.models package and its subpackages.
    Ensures all SQLAlchemy models are registered with the Base metadata for Alembic.
    """
    # Get the project root (assumes this file is in server/src/database/alembic/)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
    models_path = os.path.join(project_root, 'src', 'models')
    package_name = 'src.models'

    if models_path not in sys.path:
        sys.path.append(models_path)
    if project_root not in sys.path:
        sys.path.append(project_root)

    for importer, modname, ispkg in pkgutil.walk_packages([models_path]):
        importlib.import_module(f"{package_name}.{modname}")
