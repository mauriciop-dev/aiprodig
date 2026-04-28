#!/usr/bin/env python3
"""
SEO-GEO - Comando unificado
Ejecuta todo el proceso SEO-GEO con un solo comando.
"""

import subprocess
import sys
from pathlib import Path


def run_script(script_path, description):
    """Ejecuta un script Python y maneja errores"""
    print(f"\n{'=' * 50}")
    print(f"{description}")
    print(f"{'=' * 50}")

    result = subprocess.run([sys.executable, script_path], capture_output=False)

    if result.returncode != 0:
        print(f"[ERROR] Error al ejecutar {script_path}")
        return False

    return True


def main():
    print("=" * 50)
    print("SEO-GEO - Comando unificado v1.0")
    print("=" * 50)

    base_dir = Path(__file__).parent

    scripts = [
        (base_dir / "seo_injector.py", "[1/2] Injectando meta tags..."),
        (base_dir / "seo_generator.py", "[2/2] Generando sitemap y llms..."),
    ]

    all_ok = True
    for script, desc in scripts:
        if not run_script(script, desc):
            all_ok = False

    print(f"\n{'=' * 50}")
    if all_ok:
        print("[OK] SEO-GEO completado!")
        print(" Archivos generados:")
        print("   - sitemap.xml")
        print("   - llms.txt")
    else:
        print("[ERROR] Algunos errores ocurrieron")
        sys.exit(1)


if __name__ == "__main__":
    main()
