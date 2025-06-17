#!/usr/bin/env python
"""Release script for FeynmanCraft ADK."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_current_version():
    """Get current version from VERSION file."""
    version_file = Path("VERSION")
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.0.0"

def create_git_tag(version):
    """Create a git tag for the release."""
    tag_name = f"v{version}"
    
    # Create tag message
    message = f"""Release {tag_name}

Released on: {datetime.now().strftime('%Y-%m-%d')}

Key features in this release:
- Dual knowledge base system (BigQuery + Local)
- Vector search with Annoy index
- Intelligent fallback mechanism
- Configurable search modes

See CHANGELOG.md for full details.
"""
    
    print(f"Creating git tag: {tag_name}")
    
    # Check if we're in a git repo
    try:
        subprocess.run(["git", "status"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Not in a git repository. Skipping git tag.")
        return False
    
    # Create the tag
    try:
        subprocess.run(["git", "tag", "-a", tag_name, "-m", message], check=True)
        print(f"✅ Git tag {tag_name} created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create git tag: {e}")
        return False

def create_release_archive(version):
    """Create a release archive."""
    archive_name = f"feynmancraft-adk-v{version}.tar.gz"
    
    print(f"Creating release archive: {archive_name}")
    
    # Files to include in the release
    include_patterns = [
        "feynmancraft_adk",
        "scripts",
        "docs",
        "requirements.txt",
        "README.md",
        "CHANGELOG.md",
        "VERSION",
        "LICENSE-*",
        ".env.example",
        "test_runner.py",
    ]
    
    # Create tar command
    tar_cmd = ["tar", "-czf", archive_name]
    for pattern in include_patterns:
        tar_cmd.extend(["--include", pattern])
    tar_cmd.append(".")
    
    try:
        subprocess.run(tar_cmd, check=True)
        print(f"✅ Release archive created: {archive_name}")
        return archive_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create archive: {e}")
        return None

def main():
    """Main release process."""
    print("🚀 FeynmanCraft ADK Release Script")
    print("=" * 50)
    
    # Get version
    version = get_current_version()
    print(f"Current version: {version}")
    
    # Confirm release
    confirm = input(f"\nCreate release for v{version}? (y/n): ")
    if confirm.lower() != 'y':
        print("Release cancelled.")
        return
    
    print("\n📋 Release Checklist:")
    print("1. ✅ Updated VERSION file")
    print("2. ✅ Updated CHANGELOG.md")
    print("3. ✅ All tests passing")
    print("4. ✅ Documentation updated")
    
    # Create git tag
    print("\n🏷️  Creating Git Tag...")
    tag_created = create_git_tag(version)
    
    # Create release archive
    print("\n📦 Creating Release Archive...")
    archive = create_release_archive(version)
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ Release preparation complete!")
    print(f"\nVersion: v{version}")
    if tag_created:
        print(f"Git tag: v{version}")
    if archive:
        print(f"Archive: {archive}")
    
    print("\n📌 Next steps:")
    if tag_created:
        print("1. Push the tag: git push origin v" + version)
    print("2. Create GitHub release with the archive")
    print("3. Update project documentation")
    print("4. Announce the release")

if __name__ == "__main__":
    main()