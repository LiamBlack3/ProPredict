"""Streamlit Community Cloud entrypoint.

Cloud looks for this file at the repository root. Keep it here so deploys
cannot pick an unrelated pages/*.py from another project.
"""

from src.app import main

main()
