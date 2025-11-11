#!/usr/bin/env python3
"""
Fix image paths in markdown files by renaming files with %20 to use underscores
and updating all markdown references.
"""

import os
import re
from pathlib import Path
import urllib.parse

def fix_image_paths():
    """Rename image files and update markdown references."""
    images_dir = Path('images')
    guides_dir = Path('guides')
    
    # Find all markdown files
    md_files = list(guides_dir.glob('*.md'))
    
    # Find all image files with %20
    image_files = list(images_dir.glob('*%20*'))
    
    print(f"Found {len(image_files)} image files with %20 encoding")
    print(f"Found {len(md_files)} markdown files to update\n")
    
    # Track renames
    renames = {}
    
    # Rename image files
    for img_file in image_files:
        old_name = img_file.name
        # Decode URL encoding and replace spaces with underscores
        decoded = urllib.parse.unquote(old_name)
        new_name = decoded.replace(' ', '_')
        
        if new_name != old_name:
            new_path = img_file.parent / new_name
            # Handle collisions
            counter = 1
            while new_path.exists() and new_path != img_file:
                name_parts = new_name.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_name = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                else:
                    new_name = f"{new_name}_{counter}"
                new_path = img_file.parent / new_name
                counter += 1
            
            renames[old_name] = new_name
            print(f"Will rename: {old_name} -> {new_name}")
            img_file.rename(new_path)
            print(f"  ✓ Renamed")
    
    # Update markdown files
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all image references
        for old_name, new_name in renames.items():
            # Replace in markdown image syntax: ![](../images/old_name)
            # Handle both URL-encoded and various formats
            patterns = [
                (rf'!\[([^\]]*)\]\(\.\./images/{re.escape(old_name)}\)', 
                 rf'![\1](../images/{new_name})'),
                (rf'!\[([^\]]*)\]\(\.\./images/{re.escape(urllib.parse.quote(old_name))}\)',
                 rf'![\1](../images/{new_name})'),
            ]
            
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Updated {md_file.name}")
    
    print(f"\nDone! Renamed {len(renames)} files and updated markdown references.")

if __name__ == '__main__':
    fix_image_paths()

