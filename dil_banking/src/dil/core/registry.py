from __future__ import annotations

import importlib.resources
from pathlib import Path
from typing import Dict, List, Optional

from dil.core.loader import LoadedPack, PackLoader


class DomainRegistry:
    """Discovers, loads, and filters DIL domain packs across versions and jurisdictions."""

    def __init__(self, custom_packs_dir: Optional[Path | str] = None):
        self._packs: Dict[str, Dict[str, LoadedPack]] = {}  # {domain: {version: LoadedPack}}
        self._custom_packs_dir = Path(custom_packs_dir) if custom_packs_dir else None
        self._load_builtin_packs()

        if self._custom_packs_dir and self._custom_packs_dir.exists():
            self._scan_custom_directory(self._custom_packs_dir)

    def _load_builtin_packs(self) -> None:
        """Loads bundled packs inside dil.domains."""
        # Locate domains package directory
        try:
            base_ref = importlib.resources.files("dil").joinpath("domains")
            # For Python 3.9+ editable or installed
            domains_dir = Path(str(base_ref))
            if domains_dir.is_dir():
                for domain_dir in domains_dir.iterdir():
                    if domain_dir.is_dir() and not domain_dir.name.startswith((".", "_")):
                        domain_name = domain_dir.name
                        for version_dir in domain_dir.iterdir():
                            if version_dir.is_dir() and (version_dir / "manifest.json").exists():
                                pack = PackLoader.load_pack(version_dir)
                                self.register_pack(pack)
        except Exception:
            # Fallback relative to this file
            fallback_dir = Path(__file__).resolve().parent.parent / "domains"
            if fallback_dir.is_dir():
                for domain_dir in fallback_dir.iterdir():
                    if domain_dir.is_dir() and not domain_dir.name.startswith((".", "_")):
                        for version_dir in domain_dir.iterdir():
                            if version_dir.is_dir() and (version_dir / "manifest.json").exists():
                                pack = PackLoader.load_pack(version_dir)
                                self.register_pack(pack)

    def _scan_custom_directory(self, base_dir: Path) -> None:
        for manifest_path in base_dir.rglob("manifest.json"):
            pack_dir = manifest_path.parent
            pack = PackLoader.load_pack(pack_dir)
            self.register_pack(pack)

    def register_pack(self, pack: LoadedPack) -> None:
        domain = pack.manifest.domain.lower()
        version = pack.manifest.version
        if domain not in self._packs:
            self._packs[domain] = {}
        self._packs[domain][version] = pack

    def get_pack(self, domain: str = "banking", version: Optional[str] = None) -> LoadedPack:
        domain = domain.lower()
        if domain not in self._packs:
            raise KeyError(f"Domain '{domain}' is not registered. Available domains: {list(self._packs.keys())}")

        available_versions = self._packs[domain]
        if not available_versions:
            raise KeyError(f"No versions found for domain '{domain}'")

        if version:
            if version not in available_versions:
                raise KeyError(f"Version '{version}' not found for domain '{domain}'. Available: {list(available_versions.keys())}")
            return available_versions[version]

        # Default to latest version (alphanumerically or SemVer)
        latest_version = sorted(available_versions.keys())[-1]
        return available_versions[latest_version]

    def list_domains(self) -> List[str]:
        return list(self._packs.keys())

    def list_versions(self, domain: str) -> List[str]:
        return list(self._packs.get(domain.lower(), {}).keys())

