#!/usr/bin/env python
"""
Start the BhashaSetu backend server
"""
import subprocess
import sys
import os

def main():
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 60)
    print("Starting BhashaSetu Backend Server")
    print("=" * 60)
    print(f"Working directory: {os.getcwd()}")
    print(f"Python: {sys.executable}")
    print()
    
    try:
        # Start uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n✓ Server stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
