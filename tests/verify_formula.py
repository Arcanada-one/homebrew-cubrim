#!/usr/bin/env python3
import argparse
import hashlib
import os
import platform
import re
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMULA = ROOT / "Formula" / "cubrim.rb"
EXPECTED_ASSETS = {
    "cubrim-v0.3.2-linux-arm64.tar.gz",
    "cubrim-v0.3.2-linux-x86_64.tar.gz",
    "cubrim-v0.3.2-macos-apple-silicon.tar.gz",
    "cubrim-v0.3.2-macos-intel.tar.gz",
}


def formula_assets() -> list[tuple[str, str]]:
    text = FORMULA.read_text(encoding="utf-8")
    pairs = re.findall(r'url "([^"]+)"\s+sha256 "([0-9a-f]{64})"', text)
    if {url.rsplit("/", 1)[-1] for url, _ in pairs} != EXPECTED_ASSETS:
        raise SystemExit("formula does not declare the exact four v0.3.2 assets")
    if 'version "0.3.2"' not in text:
        raise SystemExit("formula version is not 0.3.2")
    if 'shell_output("#{bin}/cubrim --version")' not in text:
        raise SystemExit("formula test does not execute the installed binary")
    return pairs


def download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "homebrew-cubrim-ci/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        target.write_bytes(response.read())


def verify_release_assets(pairs: list[tuple[str, str]]) -> None:
    host_asset = "cubrim-v0.3.2-linux-arm64.tar.gz" if platform.machine() in {"aarch64", "arm64"} else (
        "cubrim-v0.3.2-linux-x86_64.tar.gz"
    )

    with tempfile.TemporaryDirectory(prefix="cubrim-formula-") as temp:
        temp_dir = Path(temp)
        for url, expected_digest in pairs:
            archive = temp_dir / url.rsplit("/", 1)[-1]
            download(url, archive)
            actual_digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            if actual_digest != expected_digest:
                raise SystemExit(f"checksum mismatch for {archive.name}")

            with tarfile.open(archive, "r:gz") as bundle:
                members = bundle.getmembers()
                if any(member.name.startswith("/") or ".." in Path(member.name).parts for member in members):
                    raise SystemExit(f"unsafe archive path in {archive.name}")
                if archive.name == host_asset:
                    binary = next((member for member in members if Path(member.name).name == "cubrim"), None)
                    if binary is None or not binary.isfile():
                        raise SystemExit(f"cubrim binary missing from {archive.name}")
                    bundle.extract(binary, path=temp_dir, filter="data")
                    binary_path = temp_dir / binary.name
                    binary_path.chmod(0o755)
                    result = subprocess.run(
                        [str(binary_path), "--version"],
                        check=True,
                        capture_output=True,
                        text=True,
                        timeout=15,
                    )
                    if "cubrim" not in result.stdout.lower() or "0.3.2" not in result.stdout:
                        raise SystemExit("installed binary version output does not identify Cubrim 0.3.2")

                    source = temp_dir / "roundtrip.txt"
                    archive_path = temp_dir / "roundtrip.cbr"
                    restored_dir = temp_dir / "restored"
                    test_home = temp_dir / "home"
                    test_home.mkdir()
                    test_env = {
                        **os.environ,
                        "CUBRIM_STATE_DIR": str(test_home / ".cubrim"),
                        "HOME": str(test_home),
                        "XDG_CONFIG_HOME": str(test_home / ".config"),
                    }
                    source.write_text("Cubrim formula round-trip\n", encoding="utf-8")
                    subprocess.run(
                        [str(binary_path), "--accept-license"],
                        check=True,
                        capture_output=True,
                        env=test_env,
                        text=True,
                        timeout=15,
                    )
                    try:
                        subprocess.run(
                            [str(binary_path), "a", str(archive_path), str(source)],
                            check=True,
                            capture_output=True,
                            env=test_env,
                            text=True,
                            timeout=15,
                        )
                    except subprocess.CalledProcessError as error:
                        raise SystemExit(
                            "Cubrim archive creation failed "
                            f"(exit {error.returncode}): stdout={error.stdout!r}, stderr={error.stderr!r}"
                        ) from error
                    subprocess.run(
                        [str(binary_path), "x", str(archive_path), "-o", str(restored_dir)],
                        check=True,
                        capture_output=True,
                        env=test_env,
                        text=True,
                        timeout=15,
                    )
                    restored = restored_dir / source.name
                    if restored.read_bytes() != source.read_bytes():
                        raise SystemExit("Cubrim archive round-trip changed file content")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-releases", action="store_true")
    args = parser.parse_args()

    pairs = formula_assets()
    if args.verify_releases:
        verify_release_assets(pairs)
    print(f"formula verification passed: {len(pairs)} assets")


if __name__ == "__main__":
    main()
