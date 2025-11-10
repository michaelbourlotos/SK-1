#!/usr/bin/env python3
"""
Convert an HTML page to Markdown with images saved locally.

Usage:
    python3 html_to_markdown.py <url> [output_file.md]

Example:
    python3 html_to_markdown.py https://example.com/article output.md
"""

import sys
import os
import re
import urllib.parse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import html2text

def sanitize_filename(filename):
    """Convert a string to a safe filename."""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename or 'image'

def download_image(url, base_url, output_dir):
    """Download an image and return the local filename."""
    try:
        # Handle relative URLs
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            parsed_base = urllib.parse.urlparse(base_url)
            url = f"{parsed_base.scheme}://{parsed_base.netloc}{url}"
        elif not url.startswith('http'):
            url = urllib.parse.urljoin(base_url, url)
        
        # Get the image
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Determine filename
        parsed = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename or '.' not in filename:
            # Try to get extension from content-type
            content_type = response.headers.get('content-type', '')
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            filename = f"image_{hash(url) % 10000}{ext}"
        
        filename = sanitize_filename(filename)
        filepath = output_dir / filename
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return filename
    except Exception as e:
        print(f"Warning: Could not download image {url}: {e}", file=sys.stderr)
        return None

def convert_html_to_markdown(url, output_file=None, images_dir=None):
    """Convert an HTML page to Markdown with local images."""
    # Fetch the HTML
    print(f"Fetching {url}...")
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    response.raise_for_status()
    html_content = response.text
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Determine output file (default to guides directory)
    if output_file is None:
        parsed = urllib.parse.urlparse(url)
        filename = sanitize_filename(os.path.basename(parsed.path) or 'page') + '.md'
        if filename == '.md':
            filename = 'output.md'
        output_path = Path('guides') / filename
    else:
        output_path = Path(output_file)
        # If just a filename (no directory), put it in guides
        if not output_path.parent or output_path.parent == Path('.'):
            output_path = Path('guides') / output_path.name
    
    # Ensure guides directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    # Determine images directory (use root images/ directory)
    if images_dir is None:
        images_dir = Path('images')
    else:
        images_dir = Path(images_dir)
    
    images_dir.mkdir(exist_ok=True)
    print(f"Images will be saved to: {images_dir}")
    
    # Download images and update references
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
        if not src:
            continue
        
        local_filename = download_image(src, url, images_dir)
        if local_filename:
            # Update the src to point to local file (relative to output file)
            # Calculate relative path from output file to images directory
            try:
                relative_path = Path(os.path.relpath(images_dir / local_filename, output_path.parent))
            except ValueError:
                # If paths are on different drives (Windows), use absolute path
                relative_path = Path(images_dir.name) / local_filename
            img['src'] = str(relative_path)
            print(f"Downloaded: {local_filename}")
    
    # Convert to markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    
    markdown = h.handle(str(soup))
    
    # Write markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# Converted from: {url}\n\n")
        f.write(markdown)
    
    print(f"\nMarkdown saved to: {output_path}")
    print(f"Images saved to: {images_dir}")
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_html_to_markdown(url, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

