#!/usr/bin/env python3
"""
Miss Gracy Baby Content Idea Generator
Generates varied yet consistent content ideas based on content pillars and themes.
"""

import json
import os
import sys
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import argparse
from pathlib import Path

class ContentIdeaGenerator:
    def __init__(self):
        """Initialize the content idea generator."""
        self.content_blueprint = self._load_content_blueprint()
        self.pillar_templates = self._load_pillar_templates()
        self.weekly_distribution = self._setup_weekly_distribution()
        self.monthly_themes = self._setup_monthly_themes()
        
    def _load_content_blueprint(self) -> Dict:
        """Load content blueprint for reference."""
        try:
            with open("Youtube Ideas/Miss Gracy Baby Content Blueprint.md", 'r') as f:
                # Parse the markdown to extract key information
                return self._parse_blueprint(f.read())
        except FileNotFoundError:
            print("Error: Content blueprint not found")
            sys.exit(1)
    
    def _parse_blueprint(self, content: str) -> Dict:
        """Parse markdown content blueprint into structured data."""
        blueprint = {
            "content_pillars": {},
            "weekly_distribution": {},
            "monthly_themes": {},
            "content_categories": {}
        }
        
        # Extract content pillars
        lines = content.split('\n')
        current_pillar = None
        
        for line in lines:
            if line.startswith("### Pillar"):
                current_pillar = line.replace("### Pillar ", "").split(":")[0].strip()
                blueprint["content_pillars"][current_pillar] = {
                    "focus": "",
                    "target_audience": "",
                    "content_mix": ""
                }
            elif current_pillar and line.startswith("**Focus:**"):
                blueprint["content_pillars"][current_pillar]["focus"] = line.replace("**Focus:**", "").strip()
            elif current_pillar and line.startswith("**Target Audience:**"):
                blueprint["content_pillars"][current_pillar]["target_audience"] = line.replace("**Target Audience:**", "").strip()
            elif current_pillar and line.startswith("**Content Mix:**"):
                blueprint["content_pillars"][current_pillar]["content_mix"] = line.replace("**Content Mix:**", "").strip()
        
        return blueprint
    
    def _load_pillar_templates(self) -> Dict:
        """Load content pillar templates."""
        try:
            with open("prompt-templates/content-pillar-templates.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: Content pillar templates not found")
            sys.exit(1)
    
    def _setup_weekly_distribution(self) -> Dict:
        """Setup weekly content distribution."""
        return {
            "monday": {
                "pillar": "Developmental Milestones & Learning",
                "content_type": "Learning Activity",
                "video_length": "5-7 min",
                "secondary_focus": "Parenting Tip"
            },
            "tuesday": {
                "pillar": "Daily Adventures & Exploration", 
                "content_type": "First Experience",
                "video_length": "4-6 min",
                "secondary_focus": "Family Bonding"
            },
            "wednesday": {
                "pillar": "Parenting Hacks & Tips",
                "content_type": "Product Review",
                "video_length": "6-8 min",
                "secondary_focus": "Practical Solution"
            },
            "thursday": {
                "pillar": "Family Bonding & Traditions",
                "content_type": "Tradition/Activity",
                "video_length": "5-7 min",
                "secondary_focus": "Daily Adventure"
            },
            "friday": {
                "pillar": "Fun & Entertainment",
                "content_type": "Challenge/Reaction",
                "video_length": "4-6 min",
                "secondary_focus": "Developmental"
            },
            "saturday": {
                "pillar": "Mixed Content",
                "content_type": "Compilation/Update",
                "video_length": "7-10 min",
                "secondary_focus": "Multiple Pillars"
            },
            "sunday": {
                "pillar": "Relaxation",
                "content_type": "Wind-down Activity",
                "video_length": "3-5 min",
                "secondary_focus": "Family Bonding"
            }
        }
    
    def _setup_monthly_themes(self) -> Dict:
        """Setup monthly content themes."""
        return {
            "january": {
                "primary_theme": "New Beginnings",
                "secondary_theme": "Developmental Goals",
                "special_focus": "Setting intentions"
            },
            "february": {
                "primary_theme": "Love & Connection",
                "secondary_theme": "Family Traditions",
                "special_focus": "Valentine's Day"
            },
            "march": {
                "primary_theme": "Exploration",
                "secondary_theme": "Outdoor Adventures",
                "special_focus": "Spring activities"
            },
            "april": {
                "primary_theme": "Growth & Learning",
                "secondary_theme": "Educational Content",
                "special_focus": "Earth Day awareness"
            },
            "may": {
                "primary_theme": "Family Fun",
                "secondary_theme": "Outdoor Activities",
                "special_focus": "Mother's Day"
            },
            "june": {
                "primary_theme": "Summer Adventures",
                "secondary_theme": "Water Play",
                "special_focus": "Father's Day"
            },
            "july": {
                "primary_theme": "Creativity",
                "secondary_theme": "Arts & Crafts",
                "special_focus": "Independence Day"
            },
            "august": {
                "primary_theme": "Back to Basics",
                "secondary_theme": "Routines",
                "special_focus": "School preparation"
            },
            "september": {
                "primary_theme": "Learning Focus",
                "secondary_theme": "Educational Toys",
                "special_focus": "Fall activities"
            },
            "october": {
                "primary_theme": "Halloween Fun",
                "secondary_theme": "Costumes & Decorations",
                "special_focus": "Seasonal traditions"
            },
            "november": {
                "primary_theme": "Gratitude",
                "secondary_theme": "Family Traditions",
                "special_focus": "Thanksgiving"
            },
            "december": {
                "primary_theme": "Holiday Magic",
                "secondary_theme": "Gift Guides",
                "special_focus": "Year in review"
            }
        }
    
    def get_current_weekday(self) -> str:
        """Get current weekday for content planning."""
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day = datetime.now().weekday()
        return days[current_day]
    
    def get_current_month(self) -> str:
        """Get current month for theme-based content."""
        months = ["january", "february", "march", "april", "may", "june", 
                 "july", "august", "september", "october", "november", "december"]
        current_month = datetime.now().month - 1  # Convert to 0-based index
        return months[current_month]
    
    def generate_content_idea(self, pillar: str = None, category: str = None, 
                            subcategory: str = None, theme_based: bool = False) -> Dict:
        """Generate a single content idea."""
        
        if theme_based:
            return self._generate_theme_based_idea()
        elif pillar:
            return self._generate_pillar_based_idea(pillar, category, subcategory)
        else:
            return self._generate_random_idea()
    
    def _generate_theme_based_idea(self) -> Dict:
        """Generate content idea based on current month's theme."""
        current_month = self.get_current_month()
        month_theme = self.monthly_themes[current_month]
        
        # Select pillar based on theme
        theme_pillar_map = {
            "New Beginnings": "Developmental Milestones & Learning",
            "Love & Connection": "Family Bonding & Traditions",
            "Exploration": "Daily Adventures & Exploration",
            "Growth & Learning": "Developmental Milestones & Learning",
            "Family Fun": "Family Bonding & Traditions",
            "Summer Adventures": "Daily Adventures & Exploration",
            "Creativity": "Fun Challenges & Entertainment",
            "Back to Basics": "Parenting Hacks & Tips",
            "Learning Focus": "Developmental Milestones & Learning",
            "Halloween Fun": "Fun Challenges & Entertainment",
            "Gratitude": "Family Bonding & Traditions",
            "Holiday Magic": "Family Bonding & Traditions"
        }
        
        pillar_name = theme_pillar_map.get(month_theme["primary_theme"], "Daily Adventures & Exploration")
        
        # Find pillar key
        pillar_key = None
        for key, value in self.pillar_templates.items():
            if value["name"] == pillar_name:
                pillar_key = key
                break
        
        if pillar_key is None:
            pillar_key = "pillar_2_daily_adventures"
        
        # Generate idea based on pillar
        idea = self._generate_pillar_based_idea(pillar_key, None, None)
        idea["theme"] = {
            "month": current_month,
            "primary_theme": month_theme["primary_theme"],
            "secondary_theme": month_theme["secondary_theme"],
            "special_focus": month_theme["special_focus"]
        }
        
        return idea
    
    def _generate_pillar_based_idea(self, pillar: str, category: str, subcategory: str) -> Dict:
        """Generate content idea based on specific pillar."""
        
        if pillar not in self.pillar_templates:
            raise ValueError(f"Invalid pillar: {pillar}")
        
        pillar_data = self.pillar_templates[pillar]
        
        # Select category if not specified
        if not category:
            category = random.choice(list(pillar_data["categories"].keys()))
        
        category_data = pillar_data["categories"][category]
        
        # Select subcategory if not specified
        if not subcategory:
            subcategory = random.choice(category_data["subcategories"])
        
        # Generate idea details
        idea = {
            "pillar": pillar_data["name"],
            "pillar_key": pillar,
            "category": category,
            "subcategory": subcategory,
            "key_elements": category_data["key_elements"],
            "target_audience": pillar_data["target_audience"],
            "content_mix_percentage": pillar_data["content_mix_percentage"],
            "suggested_title": self._generate_title(pillar_data["name"], category, subcategory),
            "description": self._generate_description(pillar_data["name"], category, subcategory),
            "video_length": self._suggest_video_length(pillar_data["name"], category),
            "engagement_focus": self._suggest_engagement_focus(pillar_data["name"], category),
            "hashtags": self._generate_hashtags(pillar_data["name"], category, subcategory),
            "filming_tips": self._generate_filming_tips(pillar_data["name"], category),
            "editing_suggestions": self._generate_editing_suggestions(pillar_data["name"], category)
        }
        
        return idea
    
    def _generate_random_idea(self) -> Dict:
        """Generate completely random content idea."""
        pillar_key = random.choice(list(self.pillar_templates.keys()))
        return self._generate_pillar_based_idea(pillar_key, None, None)
    
    def _generate_title(self, pillar_name: str, category: str, subcategory: str) -> str:
        """Generate engaging title for content idea."""
        
        title_templates = {
            "Developmental Milestones & Learning": [
                f"Gracy's Amazing {subcategory.replace('_', ' ').title()} Journey",
                f"Watch Gracy Master {subcategory.replace('_', ' ').title()}!",
                f"Developmental Milestone: Gracy's {subcategory.replace('_', ' ').title()} Adventure",
                f"Learning Through Play: Gracy's {subcategory.replace('_', ' ').title()} Experience"
            ],
            "Daily Adventures & Exploration": [
                f"Gracy's First {subcategory.replace('_', ' ').title()} Adventure!",
                f"Exploring the World: Gracy's {subcategory.replace('_', ' ').title()} Journey",
                f"Baby's Discovery: Gracy's {subcategory.replace('_', ' ').title()} Experience",
                f"Everyday Magic: Gracy's {subcategory.replace('_', ' ').title()} Moments"
            ],
            "Parenting Hacks & Tips": [
                f"Game-Changing {subcategory.replace('_', ' ').title()} Hack for Parents!",
                f"The Ultimate {subcategory.replace('_', ' ').title()} Guide for Parents",
                f"Parenting Pro Tips: Gracy's {subcategory.replace('_', ' ').title()} Edition",
                f"Life-Saving {subcategory.replace('_', ' ').title()} Tips for New Parents"
            ],
            "Family Bonding & Traditions": [
                f"Our Family {subcategory.replace('_', ' ').title()} Tradition",
                f"Heartwarming {subcategory.replace('_', ' ').title()} Family Moments",
                f"Building Family Bonds: Gracy's {subcategory.replace('_', ' ').title()} Story",
                f"Family Traditions: Gracy's {subcategory.replace('_', ' ').title()} Adventure"
            ],
            "Fun Challenges & Entertainment": [
                f"Gracy's {subcategory.replace('_', ' ').title()} Challenge!",
                f"Baby Entertainment: Gracy's {subcategory.replace('_', ' ').title()} Adventure",
                f"Fun Times: Gracy's {subcategory.replace('_', ' ').title()} Challenge",
                f"Watch Gracy Take On the {subcategory.replace('_', ' ').title()} Challenge!"
            ]
        }
        
        templates = title_templates.get(pillar_name, ["Gracy's Amazing Adventure!"])
        return random.choice(templates)
    
    def _generate_description(self, pillar_name: str, category: str, subcategory: str) -> str:
        """Generate description for content idea."""
        
        base_descriptions = {
            "Developmental Milestones & Learning": f"Join us as we celebrate Gracy's latest developmental milestone in {subcategory.replace('_', ' ')}. Watch her learn, grow, and discover new skills in this heartwarming journey that parents and caregivers will love!",
            "Daily Adventures & Exploration": f"Come along on Gracy's latest adventure as she explores {subcategory.replace('_', ' ')}! Watch her curiosity and wonder as she discovers new things in everyday moments that make childhood so special.",
            "Parenting Hacks & Tips": f"Discover the ultimate {subcategory.replace('_', ' ')} hack that every parent needs to know! In this video, we share practical tips and strategies that have made our parenting journey easier and more enjoyable.",
            "Family Bonding & Traditions": f"Experience the magic of family bonding through our {subcategory.replace('_', ' ')} tradition. Watch how these special moments strengthen our family bonds and create lasting memories for Gracy and the whole family.",
            "Fun Challenges & Entertainment": f"Get ready for fun and entertainment with Gracy's {subcategory.replace('_', ' ')} challenge! Watch her adorable reactions and playful moments as she takes on this exciting adventure that's perfect for the whole family."
        }
        
        return base_descriptions.get(pillar_name, "Join us for another amazing adventure with Gracy!")
    
    def _suggest_video_length(self, pillar_name: str, category: str) -> str:
        """Suggest optimal video length."""
        
        length_suggestions = {
            "Developmental Milestones & Learning": "5-7 minutes",
            "Daily Adventures & Exploration": "4-6 minutes",
            "Parenting Hacks & Tips": "6-8 minutes",
            "Family Bonding & Traditions": "5-7 minutes",
            "Fun Challenges & Entertainment": "4-6 minutes"
        }
        
        return length_suggestions.get(pillar_name, "5 minutes")
    
    def _suggest_engagement_focus(self, pillar_name: str, category: str) -> str:
        """Suggest engagement focus for the content."""
        
        engagement_suggestions = {
            "Developmental Milestones & Learning": "High retention through educational value",
            "Daily Adventures & Exploration": "High engagement through authentic moments",
            "Parenting Hacks & Tips": "High shareability through practical value",
            "Family Bonding & Traditions": "High retention through emotional storytelling",
            "Fun Challenges & Entertainment": "High engagement through entertainment value"
        }
        
        return engagement_suggestions.get(pillar_name, "Balanced engagement")
    
    def _generate_hashtags(self, pillar_name: str, category: str, subcategory: str) -> List[str]:
        """Generate relevant hashtags."""
        
        base_hashtags = [
            "#MissGracyBaby", "#BabyContent", "#Parenting", "#BabyMilestones",
            "#BabyDevelopment", "#FamilyFun", "#BabyAdventures", "#ParentingHacks"
        ]
        
        pillar_hashtags = {
            "Developmental Milestones & Learning": [
                "#BabyLearning", "#EarlyChildhood", "#DevelopmentalMilestones",
                "#BabySkills", "#LearningThroughPlay", "#BabyDevelopment"
            ],
            "Daily Adventures & Exploration": [
                "#BabyExploration", "#BabyAdventures", "#EverydayMagic",
                "#BabyDiscovery", "#OutdoorFun", "#BabyLife"
            ],
            "Parenting Hacks & Tips": [
                "#ParentingTips", "#MomLife", "#DadLife", "#BabyCare",
                "#ParentingHacks", "#NewParent", "#BabyEssentials"
            ],
            "Family Bonding & Traditions": [
                "#FamilyBonding", "#FamilyTraditions", "#FamilyTime",
                "#ParentingJourney", "#FamilyMoments", "#LoveAndFamily"
            ],
            "Fun Challenges & Entertainment": [
                "#BabyFun", "#Entertainment", "#BabyChallenge",
                "#CuteBaby", "#BabyReactions", "#FamilyFun"
            ]
        }
        
        specific_hashtags = [
            f"#{subcategory.replace('_', '').title()}",
            f"#{category.replace('_', '').title()}",
            f"#{pillar_name.replace(' & ', '').replace(' ', '').replace('Milestones', 'Milestone').replace('Entertainment', 'Fun')}"
        ]
        
        all_hashtags = base_hashtags + pillar_hashtags.get(pillar_name, []) + specific_hashtags
        return list(set(all_hashtags))  # Remove duplicates
    
    def _generate_filming_tips(self, pillar_name: str, category: str) -> List[str]:
        """Generate filming tips for the content type."""
        
        filming_tips = {
            "Developmental Milestones & Learning": [
                "Use multiple camera angles to capture different perspectives",
                "Focus on baby's facial expressions and hand movements",
                "Include text overlays for key learning points",
                "Ensure good lighting for clear visibility of developmental activities"
            ],
            "Daily Adventures & Exploration": [
                "Capture authentic, unscripted moments",
                "Use a mix of wide shots and close-ups",
                "Follow the action naturally without being intrusive",
                "Capture genuine reactions and emotions"
            ],
            "Parenting Hacks & Tips": [
                "Show clear before and after comparisons",
                "Use screen recording for digital tips",
                "Demonstrate the hack in real-time",
                "Include safety warnings where applicable"
            ],
            "Family Bonding & Traditions": [
                "Capture natural interactions between family members",
                "Use soft, warm lighting for emotional moments",
                "Include multiple family members when possible",
                "Focus on authentic emotions and connections"
            ],
            "Fun Challenges & Entertainment": [
                "Capture high-energy moments with dynamic camera work",
                "Use slow motion for funny or adorable moments",
                "Include multiple angles of the challenge",
                "Capture genuine reactions and emotions"
            ]
        }
        
        return filming_tips.get(pillar_name, ["Capture authentic moments and have fun!"])
    
    def _generate_editing_suggestions(self, pillar_name: str, category: str) -> List[str]:
        """Generate editing suggestions for the content type."""
        
        editing_suggestions = {
            "Developmental Milestones & Learning": [
                "Use calm, background music that doesn't distract from learning",
                "Add text overlays for key educational points",
                "Use smooth transitions between activities",
                "Include timestamps for different learning segments"
            ],
            "Daily Adventures & Exploration": [
                "Use upbeat, trending music for energy",
                "Quick cuts to maintain engagement during exploration",
                "Add text overlays for location or activity descriptions",
                "Include natural sound when appropriate"
            ],
            "Parenting Hacks & Tips": [
                "Use clear chapter markers for different tips",
                "Add text overlays for key points and takeaways",
                "Include before/after comparisons side by side",
                "Use arrows or highlights to draw attention to important details"
            ],
            "Family Bonding & Traditions": [
                "Use warm color grading for emotional appeal",
                "Include slow motion for special moments",
                "Add text overlays for family quotes or messages",
                "Use gentle transitions between family moments"
            ],
            "Fun Challenges & Entertainment": [
                "Use fast-paced editing with quick cuts",
                "Add trending audio and sound effects",
                "Include text overlays for funny moments or reactions",
                "Use slow motion for highlight moments"
            ]
        }
        
        return editing_suggestions.get(pillar_name, ["Keep editing clean and engaging!"])
    
    def generate_weekly_content_plan(self, start_date: str = None) -> Dict:
        """Generate a complete weekly content plan."""
        
        if start_date is None:
            start_date = datetime.now()
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        weekly_plan = {
            "week_start": start_date.strftime("%Y-%m-%d"),
            "week_end": (start_date + timedelta(days=6)).strftime("%Y-%m-%d"),
            "content_schedule": {},
            "monthly_theme": self.monthly_themes[self.get_current_month()],
            "pillar_distribution": {}
        }
        
        # Generate content for each day
        for day_key, day_config in self.weekly_distribution.items():
            day_date = start_date + timedelta(days=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day_key))
            
            # Determine pillar for this day
            if day_config["pillar"] == "Mixed Content":
                # For mixed content, distribute across multiple pillars
                pillars = ["pillar_1_developmental_milestones", "pillar_2_daily_adventures", 
                          "pillar_3_parenting_hacks", "pillar_4_family_bonding", "pillar_5_fun_challenges"]
                pillar_key = random.choice(pillars)
            else:
                # Map pillar name to key
                pillar_name_to_key = {
                    "Developmental Milestones & Learning": "pillar_1_developmental_milestones",
                    "Daily Adventures & Exploration": "pillar_2_daily_adventures",
                    "Parenting Hacks & Tips": "pillar_3_parenting_hacks",
                    "Family Bonding & Traditions": "pillar_4_family_bonding",
                    "Fun & Entertainment": "pillar_5_fun_challenges",
                    "Relaxation": "pillar_4_family_bonding"
                }
                pillar_key = pillar_name_to_key.get(day_config["pillar"], "pillar_2_daily_adventures")
            
            # Generate content idea
            idea = self._generate_pillar_based_idea(pillar_key, None, None)
            
            # Add day-specific configuration
            content_item = {
                **idea,
                "day": day_key,
                "date": day_date.strftime("%Y-%m-%d"),
                "content_type": day_config["content_type"],
                "video_length": day_config["video_length"],
                "secondary_focus": day_config["secondary_focus"],
                "publishing_time": self._suggest_publishing_time(day_key)
            }
            
            weekly_plan["content_schedule"][day_key] = content_item
            
            # Track pillar distribution
            pillar_name = idea["pillar"]
            if pillar_name not in weekly_plan["pillar_distribution"]:
                weekly_plan["pillar_distribution"][pillar_name] = 0
            weekly_plan["pillar_distribution"][pillar_name] += 1
        
        return weekly_plan
    
    def _suggest_publishing_time(self, day: str) -> str:
        """Suggest optimal publishing time for each day."""
        
        publishing_times = {
            "monday": "9:00 AM",
            "tuesday": "10:00 AM", 
            "wednesday": "2:00 PM",
            "thursday": "11:00 AM",
            "friday": "3:00 PM",
            "saturday": "10:00 AM",
            "sunday": "4:00 PM"
        }
        
        return publishing_times.get(day, "2:00 PM")
    
    def save_content_idea(self, idea: Dict, filename: str = None) -> str:
        """Save content idea to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_idea_{timestamp}.json"
        
        filepath = f"content-ideas/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(idea, f, indent=2)
        
        print(f"Content idea saved to: {filepath}")
        return filepath
    
    def save_weekly_plan(self, weekly_plan: Dict, filename: str = None) -> str:
        """Save weekly content plan to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weekly_content_plan_{timestamp}.json"
        
        filepath = f"content-plans/{filename}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(weekly_plan, f, indent=2)
        
        print(f"Weekly content plan saved to: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description="Generate Miss Gracy Baby content ideas")
    parser.add_argument("--pillar", help="Content pillar to focus on")
    parser.add_argument("--category", help="Category within pillar")
    parser.add_argument("--subcategory", help="Specific subcategory")
    parser.add_argument("--theme-based", action="store_true", help="Generate idea based on current month's theme")
    parser.add_argument("--weekly-plan", action="store_true", help="Generate weekly content plan")
    parser.add_argument("--start-date", help="Start date for weekly plan (YYYY-MM-DD)")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--batch", type=int, help="Generate multiple ideas")
    
    args = parser.parse_args()
    
    generator = ContentIdeaGenerator()
    
    if args.weekly_plan:
        # Generate weekly content plan
        weekly_plan = generator.generate_weekly_content_plan(args.start_date)
        filepath = generator.save_weekly_plan(weekly_plan, args.output)
        print(f"Weekly content plan generated: {filepath}")
        
        # Display summary
        print("\nWeekly Content Plan Summary:")
        print(f"Week: {weekly_plan['week_start']} to {weekly_plan['week_end']}")
        print(f"Monthly Theme: {weekly_plan['monthly_theme']['primary_theme']}")
        print("\nContent Schedule:")
        for day, content in weekly_plan['content_schedule'].items():
            print(f"  {day.title()}: {content['suggested_title']} ({content['video_length']})")
        
    elif args.batch:
        # Generate multiple ideas
        generated_files = []
        for i in range(args.batch):
            try:
                idea = generator.generate_content_idea(
                    pillar=args.pillar,
                    category=args.category,
                    subcategory=args.subcategory,
                    theme_based=args.theme_based
                )
                filepath = generator.save_content_idea(idea, args.output)
                generated_files.append(filepath)
            except Exception as e:
                print(f"Error generating idea {i+1}: {e}")
                continue
        
        print(f"Generated {len(generated_files)} content ideas:")
        for file in generated_files:
            print(f"  - {file}")
    
    else:
        # Generate single idea
        try:
            idea = generator.generate_content_idea(
                pillar=args.pillar,
                category=args.category,
                subcategory=args.subcategory,
                theme_based=args.theme_based
            )
            
            filepath = generator.save_content_idea(idea, args.output)
            print(f"Content idea generated: {filepath}")
            
            # Display idea summary
            print("\nContent Idea Summary:")
            print(f"Pillar: {idea['pillar']}")
            print(f"Category: {idea['category']}")
            print(f"Subcategory: {idea['subcategory']}")
            print(f"Suggested Title: {idea['suggested_title']}")
            print(f"Video Length: {idea['video_length']}")
            print(f"Target Audience: {idea['target_audience']}")
            print(f"Hashtags: {', '.join(idea['hashtags'][:5])}...")
            
        except Exception as e:
            print(f"Error generating content idea: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
