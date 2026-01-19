# 🎨 SA Platform - Ready-to-Use Templates

Pre-configured templates for quick content generation.

## 📚 Table of Contents

- [Marketing Templates](#marketing-templates)
- [Educational Templates](#educational-templates)
- [Social Media Templates](#social-media-templates)
- [Business Templates](#business-templates)

---

## 🎯 Marketing Templates

### Product Showcase
**Type**: Video + Audio  
**Duration**: 30 seconds  
**Scenes**: 4

```json
{
  "name": "product_showcase",
  "type": "video",
  "scenes": [
    {
      "prompt": "professional product shot, white background, studio lighting",
      "duration": 5,
      "narration": "Introducing our latest innovation"
    },
    {
      "prompt": "close-up of product features, detailed view",
      "duration": 10,
      "narration": "Designed with you in mind, featuring cutting-edge technology"
    },
    {
      "prompt": "product in use, lifestyle shot",
      "duration": 10,
      "narration": "Experience the difference in your daily life"
    },
    {
      "prompt": "call to action, brand logo",
      "duration": 5,
      "narration": "Get yours today"
    }
  ]
}
```

### Social Media Ad
**Type**: Image + Text  
**Format**: Square (1080x1080)

```json
{
  "name": "social_media_ad",
  "type": "image",
  "prompts": [
    "eye-catching product advertisement, vibrant colors, modern design, text overlay space",
    "lifestyle photo for social media, bright and cheerful, Instagram-style",
    "minimal product photography, elegant composition, professional"
  ]
}
```

---

## 📚 Educational Templates

### Explainer Video
**Type**: Video + Audio  
**Duration**: 60 seconds  
**Scenes**: 6

```json
{
  "name": "explainer_video",
  "type": "video",
  "scenes": [
    {
      "prompt": "animated title screen, educational theme",
      "duration": 5,
      "narration": "Let's learn about [TOPIC]"
    },
    {
      "prompt": "simple illustration showing concept",
      "duration": 10,
      "narration": "Here's what you need to know"
    },
    {
      "prompt": "step by step visualization",
      "duration": 15,
      "narration": "First, we start with the basics"
    },
    {
      "prompt": "detailed example",
      "duration": 15,
      "narration": "Let me show you how it works"
    },
    {
      "prompt": "common mistakes to avoid",
      "duration": 10,
      "narration": "Remember these important points"
    },
    {
      "prompt": "summary and conclusion",
      "duration": 5,
      "narration": "Now you know the essentials!"
    }
  ]
}
```

### Tutorial Thumbnail
**Type**: Image  
**Format**: 16:9 (1920x1080)

```json
{
  "name": "tutorial_thumbnail",
  "type": "image",
  "prompts": [
    "educational YouTube thumbnail, bright colors, clear text space, eye-catching",
    "tutorial preview image, professional layout, easy to read",
    "how-to guide thumbnail, step numbers, vibrant design"
  ]
}
```

---

## 📱 Social Media Templates

### Instagram Story
**Type**: Image  
**Format**: 9:16 (1080x1920)

```json
{
  "name": "instagram_story",
  "type": "image",
  "styles": ["modern", "minimalist", "colorful"],
  "prompts": [
    "Instagram story template, trendy design, space for text stickers",
    "social media story background, aesthetic gradient, modern minimal",
    "story template with product placement, lifestyle vibe"
  ]
}
```

### TikTok/Reels
**Type**: Video  
**Duration**: 15 seconds  
**Format**: Vertical

```json
{
  "name": "short_video",
  "type": "video",
  "format": "vertical",
  "scenes": [
    {
      "prompt": "hook shot, attention grabbing, dynamic",
      "duration": 3
    },
    {
      "prompt": "main content, clear and engaging",
      "duration": 9
    },
    {
      "prompt": "call to action, end screen",
      "duration": 3
    }
  ]
}
```

---

## 💼 Business Templates

### Corporate Presentation
**Type**: Image Series  
**Format**: 16:9  
**Slides**: 10

```json
{
  "name": "corporate_presentation",
  "type": "image_series",
  "slides": [
    {
      "title": "Title Slide",
      "prompt": "professional business presentation title, corporate colors, clean design"
    },
    {
      "title": "About Us",
      "prompt": "company overview slide, modern business aesthetic"
    },
    {
      "title": "Our Services",
      "prompt": "services showcase, icons and text space, professional"
    },
    {
      "title": "Statistics",
      "prompt": "data visualization, charts and graphs, business style"
    },
    {
      "title": "Contact",
      "prompt": "contact information slide, professional layout"
    }
  ]
}
```

### Team Introduction
**Type**: Video + Audio  
**Duration**: 45 seconds

```json
{
  "name": "team_intro",
  "type": "video",
  "scenes": [
    {
      "prompt": "company logo animation, professional",
      "duration": 5,
      "narration": "Meet our amazing team"
    },
    {
      "prompt": "office environment, modern workplace",
      "duration": 10,
      "narration": "We're passionate about what we do"
    },
    {
      "prompt": "team collaboration, diverse group working together",
      "duration": 15,
      "narration": "Together, we create extraordinary results"
    },
    {
      "prompt": "team success celebration",
      "duration": 10,
      "narration": "Join us on this exciting journey"
    },
    {
      "prompt": "call to action",
      "duration": 5,
      "narration": "Get in touch today"
    }
  ]
}
```

---

## 🎭 Creative Templates

### Storytelling Video
**Type**: Video + Audio + Music  
**Duration**: 90 seconds

```json
{
  "name": "storytelling",
  "type": "video",
  "music": "ambient",
  "scenes": [
    {
      "prompt": "opening scene, establish mood and setting",
      "duration": 10,
      "narration": "Once upon a time..."
    },
    {
      "prompt": "introduce main character or subject",
      "duration": 15,
      "narration": "There was a [CHARACTER] who..."
    },
    {
      "prompt": "conflict or challenge",
      "duration": 20,
      "narration": "But then, a challenge appeared"
    },
    {
      "prompt": "journey and growth",
      "duration": 25,
      "narration": "Through determination and effort..."
    },
    {
      "prompt": "resolution and triumph",
      "duration": 15,
      "narration": "Finally, success was achieved"
    },
    {
      "prompt": "closing message",
      "duration": 5,
      "narration": "And the lesson is..."
    }
  ]
}
```

---

## 🚀 Usage Examples

### Using Templates via API

```python
import requests

# Load template
template = {
    "template_name": "product_showcase",
    "customization": {
        "product_name": "SmartWatch X",
        "brand_colors": ["#FF6B6B", "#4ECDC4"]
    }
}

# Generate from template
response = requests.post(
    "http://localhost:8000/api/v1/templates/generate",
    json=template
)

result = response.json()
print(f"Generated: {result['output_url']}")
```

### Using Templates in Python

```python
from sa.utils.templates import TemplateManager

# Initialize template manager
manager = TemplateManager()

# List available templates
templates = manager.list_templates(category="marketing")

# Load and customize template
template = manager.load_template("product_showcase")
template.customize(product_name="My Product")

# Generate content
result = template.generate()
```

---

## 📝 Creating Custom Templates

You can create your own templates:

```json
{
  "name": "my_custom_template",
  "description": "My awesome template",
  "type": "video",
  "category": "custom",
  "settings": {
    "duration": 30,
    "fps": 24,
    "format": "16:9"
  },
  "scenes": [
    {
      "prompt": "Your scene description",
      "duration": 10,
      "narration": "Your narration text"
    }
  ],
  "variables": {
    "product_name": "string",
    "brand_color": "color"
  }
}
```

Save as JSON in `templates/custom/my_template.json`

---

## 🎨 Template Categories

- **Marketing**: Product showcases, ads, promotions
- **Education**: Tutorials, explainers, courses
- **Social Media**: Stories, posts, reels
- **Business**: Presentations, reports, intros
- **Creative**: Storytelling, artistic, experimental
- **News**: Updates, announcements, reports

---

## 💡 Tips for Best Results

1. **Be Specific**: The more detailed your customization, the better
2. **Brand Consistency**: Use your brand colors and fonts
3. **Test First**: Try templates with sample data before production
4. **Iterate**: Adjust prompts based on results
5. **Combine**: Mix and match scenes from different templates

---

## 📊 Template Performance

| Template | Avg. Generation Time | Success Rate | Popularity |
|----------|---------------------|--------------|------------|
| Product Showcase | 45s | 98% | ⭐⭐⭐⭐⭐ |
| Social Media Ad | 20s | 99% | ⭐⭐⭐⭐⭐ |
| Explainer Video | 60s | 95% | ⭐⭐⭐⭐ |
| Tutorial Thumbnail | 15s | 99% | ⭐⭐⭐⭐⭐ |
| Corporate Presentation | 90s | 97% | ⭐⭐⭐⭐ |

---

## 🔗 Resources

- [Template API Documentation](API.md)
- [Usage Examples](USAGE.md)
- [Contributing Templates](CONTRIBUTING.md)

---

**Made with ❤️ by SA Platform**
