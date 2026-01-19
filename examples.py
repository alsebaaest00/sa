"""Example scripts demonstrating SA platform usage"""

import os

from sa.generators import AudioGenerator, ImageGenerator, VideoGenerator
from sa.utils import SuggestionEngine, config


def example_image_generation():
    """Example: Generate an image from text"""
    print("🖼️ Example 1: Image Generation")
    print("-" * 50)

    # Initialize generator
    generator = ImageGenerator(config.replicate_api_key)

    # Generate image
    prompt = "A beautiful sunset over mountains, hyperrealistic, 4k"
    images = generator.generate(prompt, width=1024, height=1024)

    if images:
        print(f"✅ Generated {len(images)} images")
        # Download first image
        save_path = f"{config.output_dir}/example_sunset.png"
        generator.download_image(images[0], save_path)
        print(f"Saved to: {save_path}")
    else:
        print("❌ Failed to generate image")


def example_slideshow_creation():
    """Example: Create a video slideshow from images"""
    print("\n🎬 Example 2: Video Slideshow")
    print("-" * 50)

    # Assume we have some images in the outputs directory
    image_paths = [
        f"{config.output_dir}/image1.png",
        f"{config.output_dir}/image2.png",
        f"{config.output_dir}/image3.png",
    ]

    # Check if images exist (for demo purposes)
    existing_images = [p for p in image_paths if os.path.exists(p)]

    if not existing_images:
        print("⚠️ No images found. Generate some images first!")
        return

    # Create slideshow
    generator = VideoGenerator()
    output_path = f"{config.output_dir}/example_slideshow.mp4"

    video = generator.create_slideshow(
        existing_images, duration_per_image=3, output_path=output_path
    )

    if video:
        print(f"✅ Slideshow created: {video}")
    else:
        print("❌ Failed to create slideshow")


def example_text_to_speech():
    """Example: Convert text to speech"""
    print("\n🎤 Example 3: Text-to-Speech")
    print("-" * 50)

    # Initialize generator
    generator = AudioGenerator(config.elevenlabs_api_key)

    # Text to convert
    text = """
    Welcome to the SA platform. This is an example of text-to-speech conversion
    using AI-powered voices. The platform supports multiple languages and voices.
    """

    # Generate speech
    output_path = f"{config.output_dir}/example_speech.mp3"
    audio = generator.generate_speech(text, voice_name="Adam", output_path=output_path)

    if audio:
        print(f"✅ Speech generated: {audio}")
    else:
        print("❌ Failed to generate speech")


def example_prompt_improvement():
    """Example: Use AI to improve prompts"""
    print("\n✨ Example 4: Prompt Improvement")
    print("-" * 50)

    if not config.openai_api_key:
        print("⚠️ OpenAI API key required for this example")
        return

    # Initialize suggestion engine
    engine = SuggestionEngine(config.openai_api_key)

    # Original prompt
    original = "a dog in a park"
    print(f"Original: {original}")

    # Improve it
    improved = engine.improve_prompt(original, "image")
    print(f"\nImproved: {improved}")


def example_generate_variations():
    """Example: Generate prompt variations"""
    print("\n💡 Example 5: Prompt Variations")
    print("-" * 50)

    if not config.openai_api_key:
        print("⚠️ OpenAI API key required for this example")
        return

    engine = SuggestionEngine(config.openai_api_key)

    prompt = "a futuristic city"
    variations = engine.generate_variations(prompt, count=3)

    print(f"Original: {prompt}\n")
    print("Variations:")
    for i, var in enumerate(variations, 1):
        print(f"{i}. {var}")


def example_script_generation():
    """Example: Generate a video script from an idea"""
    print("\n📝 Example 6: Script Generation")
    print("-" * 50)

    if not config.openai_api_key:
        print("⚠️ OpenAI API key required for this example")
        return

    engine = SuggestionEngine(config.openai_api_key)

    idea = "A documentary about the beauty of nature in different seasons"
    script = engine.generate_script_from_idea(idea, num_scenes=3)

    print(f"Idea: {idea}\n")
    print("Generated Script:")
    for i, scene in enumerate(script, 1):
        print(f"\nScene {i}:")
        print(f"  Visual: {scene['visual']}")
        print(f"  Narration: {scene['narration']}")


def example_complete_workflow():
    """Example: Complete workflow - from idea to video"""
    print("\n🎯 Example 7: Complete Workflow")
    print("-" * 50)

    # Step 1: Generate script
    if config.openai_api_key:
        print("Step 1: Generating script...")
        engine = SuggestionEngine(config.openai_api_key)
        script = engine.generate_script_from_idea(
            "A short story about a robot discovering nature", num_scenes=2
        )
        print("✅ Script generated")
    else:
        print("⚠️ Using manual script (OpenAI key not found)")
        script = [
            {
                "visual": "A robot walking in a green forest",
                "narration": "Once upon a time, a robot discovered nature",
            },
            {
                "visual": "The robot looking at a beautiful flower",
                "narration": "It was amazed by the beauty of flowers",
            },
        ]

    # Step 2: Generate images for each scene
    print("\nStep 2: Generating images...")
    if config.replicate_api_key:
        img_gen = ImageGenerator(config.replicate_api_key)
        scene_images = []

        for i, scene in enumerate(script):
            images = img_gen.generate(scene["visual"], num_outputs=1)
            if images:
                save_path = f"{config.output_dir}/scene_{i}.png"
                img_gen.download_image(images[0], save_path)
                scene_images.append(save_path)
                print(f"  ✅ Scene {i+1} image generated")

        print(f"✅ {len(scene_images)} images generated")
    else:
        print("⚠️ Replicate API key not found")
        return

    # Step 3: Generate narration audio
    print("\nStep 3: Generating narration...")
    # Always try to generate audio - AudioGenerator has gTTS fallback
    audio_gen = AudioGenerator(config.elevenlabs_api_key)
    narration_texts = [scene["narration"] for scene in script]
    audio_path = f"{config.output_dir}/narration.mp3"

    audio = audio_gen.generate_narration_from_script(narration_texts, audio_path)
    if audio:
        print("✅ Narration generated")
    else:
        audio_path = None
        print("⚠️ Audio generation failed")

    # Step 4: Create video
    print("\nStep 4: Creating final video...")
    video_gen = VideoGenerator()
    final_video = f"{config.output_dir}/final_story.mp4"

    # Create slideshow
    video = video_gen.create_slideshow(scene_images, duration_per_image=3, output_path=final_video)

    # Add audio if available
    if video and audio_path and os.path.exists(audio_path):
        video_with_audio = video_gen.add_audio(video, audio_path)
        if video_with_audio:
            print(f"✅ Complete video created: {video_with_audio}")
    elif video:
        print(f"✅ Video created (no audio): {video}")
    else:
        print("❌ Failed to create video")


def main():
    """Run all examples"""
    print("=" * 50)
    print("SA PLATFORM - EXAMPLES")
    print("=" * 50)

    # Validate configuration
    validation = config.validate()
    print("\n📊 Configuration Status:")
    print(f"  OpenAI: {'✅' if validation['openai'] else '❌'}")
    print(f"  Replicate: {'✅' if validation['replicate'] else '❌'}")
    print(f"  ElevenLabs: {'✅' if validation['elevenlabs'] else '❌'}")

    print("\n" + "=" * 50)
    print("Choose an example to run:")
    print("1. Image Generation")
    print("2. Video Slideshow")
    print("3. Text-to-Speech")
    print("4. Prompt Improvement")
    print("5. Prompt Variations")
    print("6. Script Generation")
    print("7. Complete Workflow")
    print("0. Run all examples")
    print("=" * 50)

    choice = input("\nEnter your choice (0-7): ").strip()

    examples = {
        "1": example_image_generation,
        "2": example_slideshow_creation,
        "3": example_text_to_speech,
        "4": example_prompt_improvement,
        "5": example_generate_variations,
        "6": example_script_generation,
        "7": example_complete_workflow,
    }

    if choice == "0":
        for func in examples.values():
            func()
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
