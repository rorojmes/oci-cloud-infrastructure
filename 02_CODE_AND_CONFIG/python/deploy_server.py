#!/usr/bin/env python3
import os
import shutil
import zipfile
import subprocess
import glob

# --- SERVER PATH CONFIGURATION ---
PROJECT_DIR = "/home/ubuntu"
EXTRACTION_DIR = os.path.join(PROJECT_DIR, "temp_robert_mesa")

# Production paths on web server
REMOTE_DIR_DANZA = "/var/www/danza"
REMOTE_DIR_ASIR = "/var/www/html"

def procesar_despliegue():
    # Search for any matching ZIP in /home/ubuntu
    archivos_zip = glob.glob(os.path.join(PROYECTO_DIR, "*artista*.zip")) + glob.glob(os.path.join(PROYECTO_DIR, "*robert*.zip"))
    archivos_zip = list(set(archivos_zip)) # Remove duplicates

    if not archivos_zip:
        print(f"❌ Error: No matching ZIP file found in {PROYECTO_DIR}")
        return

    # Take the first match
    zip_path = archivos_zip[0]
    zip_name = os.path.basename(zip_path).lower()
    print(f"📦 File detected in {PROYECTO_DIR}!: {zip_name}. Starting deployment...")

    # Identify destination dynamically based on file name
    if "cv" in zip_name:
        target_dir = REMOTE_DIR_ASIR
        project_type = "ASIRWEB (CV)"
    else:
        target_dir = REMOTE_DIR_DANZA
        project_type = "ARTISTA (Danza)"

    print(f"🎯 Project type detected: {project_type} -> Destination: {target_dir}")

    deploy_ok = False
    try:
        # Cleanup previous attempts
        if os.path.exists(EXTRACTION_DIR):
            shutil.rmtree(EXTRACTION_DIR)
        os.makedirs(EXTRACTION_DIR)

        print("-> Decompressing file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for _m in zip_ref.namelist():
                _dest = os.path.join(EXTRACTION_DIR, _m)
                # Security: prevent zip-slip
                if not os.path.realpath(_dest).startswith(os.path.realpath(EXTRACTION_DIR)):
                    print(f"⚠️ Skipped malicious path: {_m}")
                    continue
                zip_ref.extract(_m, EXTRACTION_DIR)

        # Remove __MACOSX (waste from macOS ZIP)
        macosx_dir = os.path.join(EXTRACTION_DIR, "__MACOSX")
        if os.path.exists(macosx_dir):
            shutil.rmtree(macosx_dir)
            print("-> __MACOSX folder removed.")

        # Locate project root (search for package.json)
        package_json = glob.glob(os.path.join(EXTRACTION_DIR, "**/package.json"), recursive=True)
        if not package_json:
            print("❌ package.json not found. Is it a Node.js project?")
            return
        project_root = os.path.dirname(package_json[0])
        print(f"-> package.json found in: {project_root}")

        # npm install
        print("-> Executing 'npm install'...")
        result = subprocess.run(
            ["npm", "install"],
            cwd=project_root,
            capture_output=True,
            text=True,
            shell=False  # Safer: no shell
        )
        if result.returncode != 0:
            print(f"❌ Error in npm install:\n{result.stderr}")
            return
        print("✓ npm install completed.")

        # npm run build
        print("-> Executing 'npm run build'...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=project_root,
            capture_output=True,
            text=True,
            shell=False
        )
        if result.returncode != 0:
            print(f"❌ Error in npm run build:\n{result.stderr}")
            return
        print("✓ Build completed successfully.")

        # Locate 'dist' folder
        dist_dir = os.path.join(project_root, "dist")
        if not os.path.exists(dist_dir):
            print("❌ 'dist' folder not found after build.")
            return

        # Copy contents of dist/ to production destination
        print(f"-> Copying files to {target_dir}...")
        for item in os.listdir(dist_dir):
            s = os.path.join(dist_dir, item)
            d = os.path.join(target_dir, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        print("✓ Files copied successfully.")

        deploy_ok = True
        print(f"🎉 Deployment of {project_type} completed!")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Cleanup temp folder and ZIP
        if os.path.exists(EXTRACTION_DIR):
            shutil.rmtree(EXTRACTION_DIR)
        if os.path.exists(zip_path):
            os.remove(zip_path)
            print("-> Temporary files cleaned.")

if __name__ == "__main__":
    procesar_despliegue()
