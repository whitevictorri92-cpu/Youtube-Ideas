#!/usr/bin/env python3
"""
Miss Gracy Baby Video Script Generator
Generates engaging video scripts using Gemini AI based on content pillars and structure templates.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse
import re
from pathlib import Path

class VideoScriptGenerator:
    def __init__(self, config_path: str = "gemini-config.json"):
        """Initialize the script generator with configuration."""
        self.config = self._load_config(config_path)
        self.video_structure = self._load_video_structure()
        self.pillar_templates = self._load_pillar_templates()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load Gemini configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def _load_video_structure(self) -> Dict:
        """Load video structure template."""
        try:
            with open("prompt-templates/video-structure-template.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: Video structure template not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing video structure template: {e}")
            sys.exit(1)
    
    def _load_pillar_templates(self) -> Dict:
        """Load content pillar templates."""
        try:
            with open("prompt-templates/content-pillar-templates.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: Content pillar templates not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing content pillar templates: {e}")
            sys.exit(1)
    
    def generate_prompt(self, pillar: str, category: str, subcategory: str, 
                       baby_age: str, custom_params: Optional[Dict] = None) -> str:
        """Generate a detailed prompt for Gemini AI."""
        
        if pillar not in self.pillar_templates:
            raise ValueError(f"Invalid pillar: {pillar}")
        
        pillar_data = self.pillar_templates[pillar]
        category_data = None
        
        # Find the category
        for cat_name, cat_data in pillar_data["categories"].items():
            if subcategory in cat_data["subcategories"]:
                category_data = cat_data
                break
        
        if category_data is None:
            raise ValueError(f"Subcategory '{subcategory}' not found in pillar '{pillar}'")
        
        # Build the prompt using the template
        template = pillar_data["prompt_template"]
        
        # Replace template variables
        prompt = template.replace("{subcategory}", subcategory)
        prompt = prompt.replace("{baby_age}", baby_age)
        prompt = prompt.replace("{audience_focus}", pillar_data["target_audience"])
        prompt = prompt.replace("{activity_description}", custom_params.get("activity_description", "") if custom_params else "")
        prompt = prompt.replace("{key_elements}", ", ".join(category_data["key_elements"]))
        prompt = prompt.replace("{tone}", custom_params.get("tone", "warm and engaging") if custom_params else "warm and engaging")
        prompt = prompt.replace("{parenting_challenge}", custom_params.get("parenting_challenge", "") if custom_params else "")
        prompt = prompt.replace("{practical_elements}", custom_params.get("practical_elements", "") if custom_params else "")
        prompt = prompt.replace("{audience_need}", custom_params.get("audience_need", "") if custom_params else "")
        prompt = prompt.replace("{emotional_elements}", custom_params.get("emotional_elements", "") if custom_params else "")
        prompt = prompt.replace("{entertainment_elements}", custom_params.get("entertainment_elements", "") if custom_params else "")
        
        # Add structure requirements
        prompt += f"""
        
        VIDEO STRUCTURE REQUIREMENTS:
        - Total duration: 4 minutes 30 seconds
        - Hook (0:00-0:15): High-energy, attention-grabbing opening
        - Setup (0:15-0:30): Context establishment and what to expect
        - Main Content (0:30-3:30): Core content with engaging segments
        - Educational Element (3:30-4:00): Learning point or takeaway
        - Conclusion (4:00-4:30): Summary and call-to-action
        
        STYLE GUIDELINES:
        - Tone: {custom_params.get('tone', 'warm and engaging') if custom_params else 'warm and engaging'}
        - Pacing: Dynamic but natural
        - Visual: Multiple camera angles, authentic moments
        - Audio: Clear voiceover, appropriate background music
        
        CONTENT REQUIREMENTS:
        - Focus on {subcategory} within {pillar_data['name']}
        - Baby age: {baby_age}
        - Target audience: {pillar_data['target_audience']}
        - Include authentic baby reactions and moments
        - Provide educational value where appropriate
        - End with clear call-to-action
        """
        
        return prompt
    
    def generate_script(self, pillar: str, category: str, subcategory: str, 
                       baby_age: str, custom_params: Optional[Dict] = None) -> Dict:
        """Generate a complete video script using Gemini AI."""
        
        # This is a placeholder for actual Gemini API integration
        # In a real implementation, you would call the Gemini API here
        
        prompt = self.generate_prompt(pillar, category, subcategory, baby_age, custom_params)
        
        # Simulate AI response (replace with actual API call)
        script = self._simulate_ai_response(prompt, pillar, subcategory)
        
        return {
            "metadata": {
                "pillar": pillar,
                "category": category,
                "subcategory": subcategory,
                "baby_age": baby_age,
                "generated_at": datetime.now().isoformat(),
                "prompt": prompt
            },
            "script": script
        }
    
    def _simulate_ai_response(self, prompt: str, pillar: str, subcategory: str) -> Dict:
        """Simulate AI response (replace with actual Gemini API integration)."""
        
        # This is a simulation - replace with actual API call to Gemini
        structure = self.video_structure["sections"]
        
        # Generate script content based on structure
        script = {
            "title": f"Gracy's {subcategory.replace('_', ' ').title()} Adventure",
            "hook": {
                "content": f"Get ready for something amazing! Today we're exploring {subcategory} and Gracy's reaction is priceless!",
                "visual_description": "Close-up of Gracy's excited face with text overlay",
                "audio": "Upbeat trending music starts",
                "duration": "0:00-0:15"
            },
            "setup": {
                "content": "Hi everyone! Today we're going to [activity] and I'm so excited because [reason]. Gracy has been looking forward to this all morning!",
                "visual_description": "Wide shot of the activity setup",
                "audio": "Music continues at moderate volume",
                "duration": "0:15-0:30"
            },
            "main_content": {
                "content": self._generate_main_content(pillar, subcategory),
                "visual_description": "Multiple camera angles capturing authentic moments",
                "audio": "Background music with clear voiceover",
                "duration": "0:30-3:30"
            },
            "educational_element": {
                "content": "Did you know that [educational fact]? This is great for Gracy's [developmental area] development. Pro tip: [practical advice]",
                "visual_description": "Clean text overlay with simple graphics",
                "audio": "Reduced background music",
                "duration": "3:30-4:00"
            },
            "conclusion": {
                "content": "Thanks for joining us today for this [subcategory] adventure! If you enjoyed this video, don't forget to subscribe and hit the notification bell. What should we try next? Let me know in the comments below!",
                "visual_description": "Happy family moment with channel branding",
                "audio": "Music fades out",
                "duration": "4:00-4:30"
            }
        }
        
        return script
    
    def _generate_main_content(self, pillar: str, subcategory: str) -> str:
        """Generate main content based on pillar and subcategory."""
        
        # Content generation logic based on different pillars
        if pillar == "pillar_1_developmental_milestones":
            return f"""
            First, we set up the {subcategory} environment with [specific setup details]. 
            Gracy immediately shows interest by [baby's reaction]. 
            As we begin the activity, you can see how focused she becomes on [specific aspect]. 
            Her little hands work so hard to [specific action], and you can tell she's really concentrating. 
            It's amazing to watch her problem-solving skills develop as she [specific achievement]. 
            The way her eyes light up when she [success moment] just melts my heart! 
            We encourage her with [specific encouragement], and she responds with [baby's response]. 
            This type of activity is perfect for developing her [developmental skill] at {subcategory.replace('_', ' ')}.
            """
        
        elif pillar == "pillar_2_daily_adventures":
            return f"""
            We start by introducing Gracy to the [environment/activity] for today's adventure. 
            At first, she's a bit curious but cautious, which is completely normal. 
            As she begins to explore, her curiosity takes over and she starts [exploration behavior]. 
            Every new discovery brings a fresh reaction - from surprise to delight! 
            I love watching her little mind work as she processes each new experience. 
            The way she interacts with [specific element] shows how much she's learning every day. 
            Her laughter and excitement are contagious as she [fun moment]. 
            These everyday moments become such precious memories as she grows and explores the world around her.
            """
        
        elif pillar == "pillar_3_parenting_hacks":
            return f"""
            Let me show you the [hack/solution] that has been a game-changer for us! 
            First, we start with [initial setup], which is crucial for success. 
            The key is [important technique] - this makes all the difference. 
            As we demonstrate, you'll notice [specific detail] that makes it work so well. 
            Gracy's reaction shows how [effective/comfortable] this approach is. 
            One of the best parts is [benefit] that parents often struggle with. 
            We've found that [additional tip] helps even more for [specific situation]. 
            This method has saved us so much time and reduced [common problem] significantly. 
            The results speak for themselves - [positive outcome]!
            """
        
        elif pillar == "pillar_4_family_bonding":
            return f"""
            Today's family tradition brings us together for [specific activity]. 
            It's moments like these that strengthen our family bonds and create lasting memories. 
            You can see the joy in Gracy's eyes as she [family interaction]. 
            The way [family member] engages with her shows the beautiful connections we're building. 
            These traditions aren't just activities - they're the foundation of our family culture. 
            As we share this time together, Gracy learns about [family value] through our actions. 
            The laughter, the learning, the love - it all comes together in these precious family moments. 
            I'm so grateful to document these memories that we'll cherish for years to come.
            """
        
        elif pillar == "pillar_5_fun_challenges":
            return f"""
            Get ready for today's exciting challenge: [challenge description]! 
            Gracy is so curious about [challenge elements] and her reaction is priceless. 
            As we begin, she approaches it with [initial reaction], which is absolutely adorable. 
            The challenge unfolds as she [progress through challenge], showing her [specific skills]. 
            Every moment is filled with surprise and delight as she discovers new aspects. 
            Her little problem-solving skills kick in when she [overcomes obstacle], and I'm so proud! 
            The way she [funny/successful moment] had us all laughing and cheering. 
            This challenge not only entertains but also helps develop her [developmental benefit] in such a fun way!
            """
        
        else:
            return f"""
            Today we're exploring {subcategory} and it's such a wonderful experience! 
            Gracy approaches this with her natural curiosity and enthusiasm. 
            As we begin, you can see her focus and engagement with the activity. 
            Each moment brings new discoveries and reactions that capture the essence of childhood wonder. 
            It's amazing to watch her learn and grow through these everyday experiences. 
            The joy and excitement she shows reminds us all to appreciate the simple things in life. 
            These moments become cherished memories that we'll look back on with fondness.
            """
    
    def save_script(self, script: Dict, filename: str = None) -> str:
        """Save generated script to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"video_script_{timestamp}.json"
        
        filepath = f"generated-scripts/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(script, f, indent=2)
        
        print(f"Script saved to: {filepath}")
        return filepath
    
    def generate_batch(self, batch_config: List[Dict]) -> List[str]:
        """Generate multiple scripts from batch configuration."""
        generated_files = []
        
        for config in batch_config:
            try:
                script = self.generate_script(
                    pillar=config["pillar"],
                    category=config["category"],
                    subcategory=config["subcategory"],
                    baby_age=config.get("baby_age", "8 months"),
                    custom_params=config.get("custom_params", {})
                )
                
                filename = config.get("filename", None)
                filepath = self.save_script(script, filename)
                generated_files.append(filepath)
                
            except Exception as e:
                print(f"Error generating script for {config.get('subcategory', 'unknown')}: {e}")
                continue
        
        return generated_files

def main():
    parser = argparse.ArgumentParser(description="Generate Miss Gracy Baby video scripts")
    parser.add_argument("--pillar", required=True, help="Content pillar (pillar_1_developmental_milestones, pillar_2_daily_adventures, etc.)")
    parser.add_argument("--category", required=True, help="Category within pillar")
    parser.add_argument("--subcategory", required=True, help="Specific subcategory")
    parser.add_argument("--baby-age", default="8 months", help="Baby's age")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--batch", help="Batch configuration file")
    
    args = parser.parse_args()
    
    generator = VideoScriptGenerator()
    
    if args.batch:
        # Process batch configuration
        try:
            with open(args.batch, 'r') as f:
                batch_config = json.load(f)
            generated_files = generator.generate_batch(batch_config)
            print(f"Generated {len(generated_files)} scripts:")
            for file in generated_files:
                print(f"  - {file}")
        except Exception as e:
            print(f"Error processing batch: {e}")
            sys.exit(1)
    else:
        # Generate single script
        try:
            script = generator.generate_script(
                pillar=args.pillar,
                category=args.category,
                subcategory=args.subcategory,
                baby_age=args.baby_age
            )
            
            filepath = generator.save_script(script, args.output)
            print(f"Script generated successfully: {filepath}")
            
        except Exception as e:
            print(f"Error generating script: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()