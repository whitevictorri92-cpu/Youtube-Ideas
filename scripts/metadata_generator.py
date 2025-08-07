#!/usr/bin/env python3
"""
Miss Gracy Baby Metadata and Description Generator
Generates optimized metadata, descriptions, and SEO elements for YouTube videos.
"""

import json
import os
import sys
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import argparse
from pathlib import Path
import re
from dataclasses import dataclass
from content_idea_generator import ContentIdeaGenerator

@dataclass
class VideoMetadata:
    """Video metadata structure."""
    title: str
    description: str
    tags: List[str]
    category: str
    custom_thumbnail: str
    publish_time: str
    playlist: str
    language: str
    subtitles: bool
    comments_enabled: bool
    age_restriction: str

class MetadataGenerator:
    def __init__(self, config_path: str = "gemini-config.json"):
        """Initialize metadata generator."""
        self.config = self._load_config(config_path)
        self.idea_generator = ContentIdeaGenerator()
        self.seo_keywords = self._load_seo_keywords()
        self.youtube_categories = self._load_youtube_categories()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)
    
    def _load_seo_keywords(self) -> Dict:
        """Load SEO keywords for different content types."""
        return {
            "developmental_milestones": {
                "primary": ["baby milestones", "developmental milestones", "baby development", "infant development", "baby learning"],
                "secondary": ["first steps", "first words", "motor skills", "cognitive development", "baby growth"],
                "long_tail": ["when do babies crawl", "baby development timeline", "infant developmental stages", "baby learning activities"]
            },
            "daily_adventures": {
                "primary": ["baby adventures", "baby exploration", "baby discovery", "baby play", "baby activities"],
                "secondary": ["baby firsts", "baby experiences", "baby fun", "baby outdoor", "baby indoor"],
                "long_tail": ["baby sensory play", "baby exploration activities", "baby discovery learning", "baby play ideas"]
            },
            "parenting_hacks": {
                "primary": ["parenting hacks", "baby tips", "parenting advice", "baby care", "new parent tips"],
                "secondary": ["baby sleep", "feeding baby", "diapering", "baby products", "parenting solutions"],
                "long_tail": ["how to get baby to sleep", "baby feeding schedule", "diaper changing tips", "baby product reviews"]
            },
            "family_bonding": {
                "primary": ["family bonding", "family time", "parenting journey", "family activities", "family traditions"],
                "secondary": ["parenting life", "family moments", "parenting vlog", "family fun", "parenting family"],
                "long_tail": ["family bonding activities", "creating family traditions", "parenting journey vlog", "family time ideas"]
            },
            "fun_challenges": {
                "primary": ["baby challenge", "baby fun", "baby entertainment", "baby games", "baby activities"],
                "secondary": ["baby reaction", "baby video", "cute baby", "baby moments", "baby laughs"],
                "long_tail": ["baby sensory challenge", "baby taste test", "baby reaction video", "baby play challenge"]
            }
        }
    
    def _load_youtube_categories(self) -> Dict:
        """Load YouTube categories."""
        return {
            "1": "Film & Animation",
            "2": "Autos & Vehicles", 
            "10": "Music",
            "15": "Pets & Animals",
            "17": "Sports",
            "19": "Travel & Events",
            "20": "Gaming",
            "22": "Videoblogging",
            "23": "Comedy",
            "24": "Entertainment",
            "25": "News & Politics",
            "26": "Howto & Style",
            "27": "Education",
            "28": "Science & Technology",
            "29": "Nonprofits & Activism"
        }
    
    def generate_metadata(self, script: Dict, custom_params: Optional[Dict] = None) -> VideoMetadata:
        """Generate complete video metadata from script."""
        
        # Extract script information
        script_content = script.get("script", {})
        metadata_info = script.get("metadata", {})
        
        # Determine content type
        pillar = metadata_info.get("pillar", "Daily Adventures & Exploration")
        content_type = self._determine_content_type(pillar)
        
        # Generate title
        title = self._generate_title(script_content, metadata_info, custom_params)
        
        # Generate description
        description = self._generate_description(script_content, metadata_info, custom_params)
        
        # Generate tags
        tags = self._generate_tags(script_content, metadata_info, content_type)
        
        # Generate category
        category = self._determine_category(pillar)
        
        # Generate publish time
        publish_time = self._suggest_publish_time()
        
        # Generate playlist
        playlist = self._suggest_playlist(pillar)
        
        # Create metadata object
        metadata = VideoMetadata(
            title=title,
            description=description,
            tags=tags,
            category=category,
            custom_thumbnail=custom_params.get("thumbnail", "") if custom_params else "",
            publish_time=publish_time,
            playlist=playlist,
            language="en",
            subtitles=True,
            comments_enabled=True,
            age_restriction="none"
        )
        
        return metadata
    
    def _determine_content_type(self, pillar: str) -> str:
        """Determine content type based on pillar."""
        pillar_to_type = {
            "Developmental Milestones & Learning": "developmental_milestones",
            "Daily Adventures & Exploration": "daily_adventures",
            "Parenting Hacks & Tips": "parenting_hacks",
            "Family Bonding & Traditions": "family_bonding",
            "Fun Challenges & Entertainment": "fun_challenges"
        }
        return pillar_to_type.get(pillar, "daily_adventures")
    
    def _generate_title(self, script_content: Dict, metadata_info: Dict, custom_params: Optional[Dict]) -> str:
        """Generate optimized YouTube title."""
        
        # Extract key elements from script
        hook = script_content.get("hook", {})
        setup = script_content.get("setup", {})
        
        # Base title from hook or setup
        base_title = hook.get("content", "") or setup.get("content", "")
        
        # Clean and optimize title
        if base_title:
            # Take first sentence or truncate
            title = base_title.split('.')[0]
            title = re.sub(r'[^a-zA-Z0-9\s\!\?\.\-\:\']', '', title)
            title = title.strip()
        else:
            # Generate fallback title
            pillar = metadata_info.get("pillar", "Baby Adventure")
            title = f"Amazing {pillar.replace(' & ', ' ')} with Gracy!"
        
        # Apply title optimization rules
        title = self._optimize_title(title, custom_params)
        
        # Ensure title length is appropriate
        if len(title) > 60:
            title = title[:57] + "..."
        elif len(title) < 10:
            title = f"Gracy's {title}" if not title.startswith("Gracy's") else title
        
        return title
    
    def _optimize_title(self, title: str, custom_params: Optional[Dict]) -> str:
        """Optimize title for SEO and engagement."""
        
        # Add emotional words if not present
        emotional_words = ["Amazing", "Adorable", "Heartwarming", "Incredible", "Wonderful"]
        if not any(word in title for word in emotional_words):
            title = f"{random.choice(emotional_words)} {title}"
        
        # Add baby reference if not present
        if "baby" not in title.lower() and "gracy" not in title.lower():
            title = f"Baby {title}"
        
        # Add year for evergreen content
        if "202" not in title:
            title = f"{title} (2024)"
        
        return title
    
    def _generate_description(self, script_content: Dict, metadata_info: Dict, custom_params: Optional[Dict]) -> str:
        """Generate comprehensive YouTube description."""
        
        # Build description sections
        sections = []
        
        # Opening hook
        sections.append(self._generate_description_header(script_content, metadata_info))
        
        # Main content description
        sections.append(self._generate_main_description(script_content, metadata_info))
        
        # Key points/bullet points
        sections.append(self._generate_key_points(script_content, metadata_info))
        
        # Call to action
        sections.append(self._generate_description_cta())
        
        # Hashtags
        sections.append(self._generate_description_hashtags(script_content, metadata_info))
        
        # Combine sections
        description = "\n\n".join(sections)
        
        # Optimize description length
        if len(description) > 5000:
            description = description[:4997] + "..."
        
        return description
    
    def _generate_description_header(self, script_content: Dict, metadata_info: Dict) -> str:
        """Generate description header section."""
        hook = script_content.get("hook", {})
        setup = script_content.get("setup", {})
        
        header_content = hook.get("content", "") or setup.get("content", "")
        
        if header_content:
            # Clean up and format
            header_content = re.sub(r'[^a-zA-Z0-9\s\!\?\.\-\:\']', '', header_content)
            return header_content
        else:
            return "Join us for another amazing adventure with Gracy!"
    
    def _generate_main_description(self, script_content: Dict, metadata_info: Dict) -> str:
        """Generate main description content."""
        main_content = script_content.get("main_content", {})
        educational = script_content.get("educational_element", {})
        conclusion = script_content.get("conclusion", {})
        
        description_parts = []
        
        # Main content summary
        if main_content and "content" in main_content:
            main_text = main_content["content"]
            # Take first paragraph or summarize
            if len(main_text) > 200:
                main_summary = main_text[:200] + "..."
            else:
                main_summary = main_text
            description_parts.append(f"In this video: {main_summary}")
        
        # Educational element
        if educational and "content" in educational:
            edu_text = educational["content"]
            description_parts.append(f"Did you know? {edu_text}")
        
        # What viewers will learn
        pillar = metadata_info.get("pillar", "baby content")
        description_parts.append(f"In this {pillar.lower()} video, you'll discover:")
        description_parts.append("• Authentic baby moments and reactions")
        description_parts.append("• Developmental insights and tips")
        description_parts.append("• Engaging content for the whole family")
        
        return "\n".join(description_parts)
    
    def _generate_key_points(self, script_content: Dict, metadata_info: Dict) -> str:
        """Generate key points section."""
        key_points = []
        
        # Add key points based on content type
        pillar = metadata_info.get("pillar", "Daily Adventures & Exploration")
        
        if "Developmental" in pillar:
            key_points.extend([
                "👶 Track developmental milestones",
                "🧠 Learn about cognitive development", 
                "🎯 Age-appropriate learning activities",
                "💡 Parenting tips and insights"
            ])
        elif "Adventures" in pillar:
            key_points.extend([
                "🌟 Baby's first experiences",
                "🎬 Authentic exploration moments",
                "🎈 Fun and engaging activities",
                "📸 Capturing precious memories"
            ])
        elif "Parenting" in pillar:
            key_points.extend([
                "🔧 Practical parenting solutions",
                "⭐ Product reviews and recommendations",
                "💝 Time-saving tips and hacks",
                "🎓 Evidence-based parenting advice"
            ])
        elif "Family" in pillar:
            key_points.extend([
                "❤️ Strengthen family bonds",
                " Create lasting traditions",
                "👨‍👩‍👧‍👦 Multi-generational moments",
                "🌈 Building family connections"
            ])
        else:  # Fun & Entertainment
            key_points.extend([
                "🎉 Fun challenges and entertainment",
                "😂 Baby's adorable reactions",
                "🎵 Music and play activities",
                "🎊 Shareable family moments"
            ])
        
        return "KEY POINTS:\n" + "\n".join(key_points)
    
    def _generate_description_cta(self) -> str:
        """Generate call-to-action section."""
        return """
🔔 DON'T FORGET TO:
• LIKE if you enjoyed this video!
• SUBSCRIBE for more baby content!
• COMMENT with your thoughts and suggestions!
• SHARE with fellow parents and caregivers!

📱 CONNECT WITH US:
• Follow our journey for daily baby moments!
• Join our community of parents!
• Share your own baby experiences below!

🎬 WATCH MORE:
• Check out our latest videos!
• Explore our playlists for more content!
• Don't miss our upcoming adventures!
"""
    
    def _generate_description_hashtags(self, script_content: Dict, metadata_info: Dict) -> str:
        """Generate hashtags section."""
        pillar = metadata_info.get("pillar", "Baby Content")
        
        # Base hashtags
        base_hashtags = [
            "#MissGracyBaby", "#BabyContent", "#Parenting", "#BabyLife",
            "#ParentingJourney", "#BabyAdventures", "#FamilyFun"
        ]
        
        # Pillar-specific hashtags
        pillar_hashtags = {
            "Developmental Milestones & Learning": [
                "#BabyMilestones", "#DevelopmentalMilestones", "#BabyDevelopment",
                "#EarlyLearning", "#BabySkills", "#InfantDevelopment"
            ],
            "Daily Adventures & Exploration": [
                "#BabyExploration", "#BabyDiscovery", "#BabyPlay",
                "#BabyActivities", "#BabyFun", "#EverydayMagic"
            ],
            "Parenting Hacks & Tips": [
                "#ParentingHacks", "#BabyTips", "#NewParent",
                "#BabyCare", "#ParentingAdvice", "#MomLife"
            ],
            "Family Bonding & Traditions": [
                "#FamilyBonding", "#FamilyTime", "#FamilyTraditions",
                "#ParentingVlog", "#FamilyMoments", "#LoveAndFamily"
            ],
            "Fun Challenges & Entertainment": [
                "#BabyChallenge", "#BabyFun", "#Entertainment",
                "#BabyReactions", "#CuteBaby", "#BabyGames"
            ]
        }
        
        all_hashtags = base_hashtags + pillar_hashtags.get(pillar, [])
        unique_hashtags = list(set(all_hashtags))  # Remove duplicates
        
        return " ".join(unique_hashtags)
    
    def _generate_tags(self, script_content: Dict, metadata_info: Dict, content_type: str) -> List[str]:
        """Generate YouTube tags for SEO."""
        
        # Get SEO keywords for content type
        seo_data = self.seo_keywords.get(content_type, {})
        primary_keywords = seo_data.get("primary", [])
        secondary_keywords = seo_data.get("secondary", [])
        long_tail_keywords = seo_data.get("long_tail", [])
        
        # Extract keywords from script content
        script_text = ""
        for section, content in script_content.items():
            if isinstance(content, dict) and "content" in content:
                script_text += content["content"] + " "
            elif isinstance(content, str):
                script_text += content + " "
        
        # Extract specific keywords from text
        extracted_keywords = self._extract_keywords_from_text(script_text)
        
        # Combine all keywords
        all_keywords = primary_keywords + secondary_keywords + extracted_keywords
        
        # Add channel-specific tags
        channel_tags = [
            "Miss Gracy Baby", "baby channel", "parenting channel", "family vlog",
            "baby development", "infant activities", "toddler play"
        ]
        
        # Remove duplicates and limit to maximum 500 characters
        all_tags = list(set(all_keywords + channel_tags))
        final_tags = []
        
        current_length = 0
        for tag in all_tags:
            tag_length = len(tag) + 2  # Include comma and space
            if current_length + tag_length <= 500:
                final_tags.append(tag)
                current_length += tag_length
            else:
                break
        
        return final_tags
    
    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        # Simple keyword extraction - in production, use more sophisticated NLP
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}
        
        words = text.lower().split()
        keywords = []
        
        for word in words:
            # Clean word
            clean_word = re.sub(r'[^a-zA-Z0-9]', '', word)
            
            # Check if it's a meaningful keyword
            if (len(clean_word) > 3 and 
                clean_word not in common_words and 
                not clean_word.isdigit()):
                keywords.append(clean_word)
        
        return list(set(keywords))
    
    def _determine_category(self, pillar: str) -> str:
        """Determine YouTube category."""
        category_mapping = {
            "Developmental Milestones & Learning": "27",  # Education
            "Daily Adventures & Exploration": "24",      # Entertainment
            "Parenting Hacks & Tips": "27",             # Education
            "Family Bonding & Traditions": "22",        # Videoblogging
            "Fun Challenges & Entertainment": "24"       # Entertainment
        }
        
        category_id = category_mapping.get(pillar, "24")  # Default to Entertainment
        return self.youtube_categories.get(category_id, "24")
    
    def _suggest_publish_time(self) -> str:
        """Suggest optimal publish time."""
        current_time = datetime.now()
        
        # Suggest next day at 10 AM
        next_day = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
        if next_day <= current_time:
            next_day = next_day.replace(day=next_day.day + 1)
        
        return next_day.isoformat()
    
    def _suggest_playlist(self, pillar: str) -> str:
        """Suggest appropriate playlist."""
        playlist_mapping = {
            "Developmental Milestones & Learning": "Developmental Milestones & Learning",
            "Daily Adventures & Exploration": "Daily Adventures & Exploration",
            "Parenting Hacks & Tips": "Parenting Hacks & Tips",
            "Family Bonding & Traditions": "Family Bonding & Traditions",
            "Fun Challenges & Entertainment": "Fun Challenges & Entertainment"
        }
        
        return playlist_mapping.get(pillar, "General Content")
    
    def save_metadata(self, metadata: VideoMetadata, script_path: str) -> str:
        """Save metadata to file."""
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(script_path))[0]
        metadata_file = f"{base_name}_metadata.json"
        metadata_path = os.path.join("generated-metadata", metadata_file)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        
        # Convert metadata to dictionary
        metadata_dict = {
            "title": metadata.title,
            "description": metadata.description,
            "tags": metadata.tags,
            "category": metadata.category,
            "custom_thumbnail": metadata.custom_thumbnail,
            "publish_time": metadata.publish_time,
            "playlist": metadata.playlist,
            "language": metadata.language,
            "subtitles": metadata.subtitles,
            "comments_enabled": metadata.comments_enabled,
            "age_restriction": metadata.age_restriction,
            "generated_at": datetime.now().isoformat()
        }
        
        # Save to file
        with open(metadata_path, 'w') as f:
            json.dump(metadata_dict, f, indent=2)
        
        print(f"Metadata saved to: {metadata_path}")
        return metadata_path
    
    def batch_generate_metadata(self, script_dir: str, output_dir: str = "generated-metadata") -> List[str]:
        """Generate metadata for all scripts in a directory."""
        metadata_files = []
        
        if not os.path.exists(script_dir):
            print(f"Error: Directory not found: {script_dir}")
            return metadata_files
        
        # Find all JSON files in directory
        json_files = []
        for root, dirs, files in os.walk(script_dir):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        
        print(f"Generating metadata for {len(json_files)} scripts...")
        
        for script_path in json_files:
            try:
                # Load script
                with open(script_path, 'r') as f:
                    script = json.load(f)
                
                # Generate metadata
                metadata = self.generate_metadata(script)
                
                # Save metadata
                metadata_path = self.save_metadata(metadata, script_path)
                metadata_files.append(metadata_path)
                
                print(f"✓ Generated metadata for: {os.path.basename(script_path)}")
                
            except Exception as e:
                print(f"✗ Error generating metadata for {script_path}: {e}")
                continue
        
        return metadata_files

def main():
    parser = argparse.ArgumentParser(description="Generate metadata for Miss Gracy Baby videos")
    parser.add_argument("--script", help="Path to script file")
    parser.add_argument("--directory", help="Directory containing scripts")
    parser.add_argument("--output", help="Output directory for metadata files")
    parser.add_argument("--title", help="Custom title override")
    parser.add_argument("--thumbnail", help="Custom thumbnail path")
    
    args = parser.parse_args()
    
    generator = MetadataGenerator()
    
    if args.script:
        # Generate metadata for single script
        try:
            with open(args.script, 'r') as f:
                script = json.load(f)
            
            # Generate metadata
            metadata = generator.generate_metadata(script, {
                "title": args.title,
                "thumbnail": args.thumbnail
            })
            
            # Save metadata
            metadata_path = generator.save_metadata(metadata, args.script)
            
            print(f"\nGenerated Metadata:")
            print(f"Title: {metadata.title}")
            print(f"Description: {metadata.description[:100]}...")
            print(f"Tags: {', '.join(metadata.tags[:5])}")
            print(f"Category: {metadata.category}")
            print(f"Publish Time: {metadata.publish_time}")
            print(f"Playlist: {metadata.playlist}")
            
        except Exception as e:
            print(f"Error generating metadata: {e}")
            sys.exit(1)
    
    elif args.directory:
        # Generate metadata for batch of scripts
        metadata_files = generator.batch_generate_metadata(args.directory, args.output)
        
        print(f"\nGenerated {len(metadata_files)} metadata files:")
        for file in metadata_files:
            print(f"  - {file}")
    
    else:
        print("Error: Either --script or --directory must be specified")
        sys.exit(1)

if __name__ == "__main__":
    main()