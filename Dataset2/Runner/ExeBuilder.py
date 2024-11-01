import sys
import os
import shutil
import subprocess


class ExeBuilder:
    def __init__(self, script_path, name_exe, icon_path=None):
        self.script_path = script_path
        self.name_exe = name_exe
        self.icon_path = icon_path
        self.dist_dir = os.path.join('dist')
        self.build_dir = os.path.join(os.getcwd(), 'build')
        self.spec_file = f"{self.name_exe}.spec"
        self.exe_file = os.path.join(self.dist_dir, f"{self.name_exe}.exe")

    def build(self):
        command = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",
            "--noconsole",
            "--collect-data", "TKinterModernThemes",
            "--hidden-import", "scipy.special._cdflib",
            "--hidden-import", "sklearn",
            "--hidden-import", "sklearn.ensemble._forest",
            "--hidden-import", "numpy.core.multiarray",
            f"--name={self.name_exe}",
            f"{self.script_path}",
        ]

        if self.icon_path and os.path.exists(self.icon_path):
            command.extend([f"--icon={self.icon_path}"])

        subprocess.run(command, check=True)

        if os.path.exists(self.exe_file):
            print("L'eseguibile è stato creato con successo!")

            # Sposta l'eseguibile nella directory corrente
            shutil.move(self.exe_file, os.getcwd())
            print(f"Eseguibile spostato nella cartella: {os.getcwd()}")

            # Elimina la cartella dist
            shutil.rmtree(self.dist_dir)
            print(f"Cartella {self.dist_dir} eliminata.")

        self.cleanup()

    def cleanup(self):
        # Pulizia della directory build
        print("Pulizia dei file temporanei...")
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        # Rimuove il file .spec
        if os.path.exists(self.spec_file):
            os.remove(self.spec_file)
        print("Pulizia completata.")


if __name__ == '__main__':
    builder = ExeBuilder("Gui.py", "Perseverance", "icon.ico")
    builder.build()
