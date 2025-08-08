import os
import re
import markdown2
from datetime import datetime
import shutil
import json

# Ensure directories exist
os.makedirs('blog', exist_ok=True)
os.makedirs('dist', exist_ok=True)
os.makedirs('dist/blog', exist_ok=True)

# Copy static assets
if os.path.exists('res'):
    shutil.copytree('res', 'dist/res', dirs_exist_ok=True)
shutil.copy('styles.css', 'dist/styles.css')
shutil.copy('script.js', 'dist/script.js')
shutil.copy('programming.html', 'dist/programming.html')
shutil.copy('music.html', 'dist/music.html')

# Read the templates
with open('index.html', 'r') as f:
    main_template = f.read()
with open('blog-template.html', 'r') as f:
    blog_template = f.read()

# Process blog posts
blog_posts = []
blog_dir = 'blog'

# Read all markdown files
for file in os.listdir(blog_dir):
    if file.endswith('.md'):
        with open(os.path.join(blog_dir, file), 'r') as f:
            content = f.read()
            
        # Extract front matter
        front_matter = {}
        if content.startswith('---'):
            _, front_matter_text, content = content.split('---', 2)
            for line in front_matter_text.strip().split('\n'):
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()
        
        # Convert markdown to HTML
        html = markdown2.markdown(content)
        # Fix code block classes for Prism.js
        html = re.sub(r'<code class="(\w+)">', r'<code class="language-\1">', html)
        
        # Save the blog post
        slug = file.replace('.md', '')
        blog_posts.append({
            'title': front_matter.get('title', 'Untitled'),
            'date': front_matter.get('date', datetime.now().strftime('%Y-%m-%d')),
            'slug': slug,
            'excerpt': front_matter.get('excerpt', content[:200] + '...'),
            'content': html
        })

# Sort blog posts by date
blog_posts.sort(key=lambda x: x['date'], reverse=True)

# Create navigation between posts
for i, post in enumerate(blog_posts):
    prev_post = blog_posts[i + 1] if i < len(blog_posts) - 1 else None
    next_post = blog_posts[i - 1] if i > 0 else None
    
    # Create navigation HTML
    nav_html = '<div class="w3-container w3-padding-32 w3-center">'
    if prev_post:
        nav_html += f'<a href="/blog/{prev_post["slug"]}.html" class="w3-button w3-black w3-padding-large w3-margin-right">← {prev_post["title"]}</a>'
    if next_post:
        nav_html += f'<a href="/blog/{next_post["slug"]}.html" class="w3-button w3-black w3-padding-large w3-margin-left">{next_post["title"]} →</a>'
    nav_html += '</div>'
    
    # Create blog post HTML using the blog template
    post_html = blog_template.replace('<!-- CONTENT -->', f'''
        <div class="w3-container w3-padding-large">
            <h1><b>{post["title"]}</b></h1>
            <p class="w3-text-gray">{post["date"]}</p>
            <div class="w3-container w3-white">
                {post["content"]}
            </div>
            {nav_html}
        </div>
    ''').replace('<!-- TITLE -->', f"{post['title']} - Autumn Nippert")
    
    with open(os.path.join('dist/blog', f'{post["slug"]}.html'), 'w') as f:
        f.write(post_html)

# Generate blog index using the blog template
blog_index = blog_template.replace('<!-- CONTENT -->', f'''
    <div class="w3-container w3-padding-large">
        <h1><b>Blog Posts</b></h1>
        <div class="w3-container w3-white">
            <div class="w3-padding-16">
                <input type="text" id="searchInput" class="w3-input w3-border" placeholder="Search posts..." onkeyup="searchPosts()">
            </div>
            <div id="blogList">
                {''.join(f'''
                    <a href="/blog/{post["slug"]}.html" class="blog-post" data-title="{post["title"].lower()}" data-excerpt="{post["excerpt"].lower()}">
                        <h3>{post["title"]}</h3>
                        <p class="w3-text-gray">{post["date"]}</p>
                        <p>{post["excerpt"]}</p>
                    </a>
                ''' for post in blog_posts)}
            </div>
        </div>
    </div>
''').replace('<!-- TITLE -->', 'Blog - Autumn Nippert')

with open('dist/blog/index.html', 'w') as f:
    f.write(blog_index)

# Create search index
search_index = {
    'posts': [{
        'title': post['title'],
        'slug': post['slug'],
        'excerpt': post['excerpt'],
        'date': post['date']
    } for post in blog_posts]
}

with open('dist/blog/search-index.json', 'w') as f:
    json.dump(search_index, f)

# Update main index.html
content_parts = main_template.split('<!-- CONTENT -->')
if len(content_parts) > 1:
    main_content = content_parts[1]
    main_index = main_template.replace('<!-- CONTENT -->' + main_content, main_content).replace('<!-- TITLE -->', 'Autumn Nippert')
    with open('dist/index.html', 'w') as f:
        f.write(main_index)
else:
    print("Error: Could not find content marker in template")

print('Build complete!') 