#!/usr/bin/env python3
"""
Miss Gracy Baby Batch Content Processor
Handles batch processing of multiple video scripts and content ideas.
"""

import json
import os
import sys
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse
from pathlib import Path
import concurrent.futures
from dataclasses import dataclass
from generate_video_script import VideoScriptGenerator
from content_idea_generator import ContentIdeaGenerator

@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    input_file: str
    output_dir: str
    max_workers: int = 4
    continue_on_error: bool = True
    skip_existing: bool = True
    template: str = "default"

class BatchProcessor:
    def __init__(self, config_path: str = "gemini-config.json"):
        """Initialize the batch processor."""
        self.config = self._load_config(config_path)
        self.script_generator = VideoScriptGenerator(config_path)
        self.idea_generator = ContentIdeaGenerator()
        self.results = []
        
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
    
    def load_batch_config(self, config_file: str) -> Dict:
        """Load batch configuration from file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Batch configuration file not found: {config_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing batch configuration file: {e}")
            sys.exit(1)
    
    def process_single_script(self, item: Dict, index: int) -> Dict:
        """Process a single script generation item."""
        try:
            print(f"Processing item {index + 1}/{len(self.batch_config['items'])}: {item.get('title', 'Untitled')}")
            
            # Generate script
            script = self.script_generator.generate_script(
                pillar=item["pillar"],
                category=item["category"],
                subcategory=item["subcategory"],
                baby_age=item.get("baby_age", "8 months"),
                custom_params=item.get("custom_params", {})
            )
            
            # Save script
            filename = item.get("filename", None)
            if filename:
                # Ensure filename has .json extension
                if not filename.endswith('.json'):
                    filename += '.json'
                filepath = os.path.join(self.batch_config["output_dir"], filename)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"script_{index + 1}_{timestamp}.json"
                filepath = os.path.join(self.batch_config["output_dir"], filename)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(script, f, indent=2)
            
            result = {
                "status": "success",
                "item": item,
                "filename": filename,
                "filepath": filepath,
                "timestamp": datetime.now().isoformat(),
                "message": f"Script generated successfully"
            }
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "item": item,
                "filename": None,
                "filepath": None,
                "timestamp": datetime.now().isoformat(),
                "message": f"Error processing item: {str(e)}"
            }
            return error_result
    
    def process_single_idea(self, item: Dict, index: int) -> Dict:
        """Process a single content idea generation item."""
        try:
            print(f"Generating idea {index + 1}/{len(self.batch_config['items'])}: {item.get('title', 'Untitled')}")
            
            # Generate content idea
            idea = self.idea_generator.generate_content_idea(
                pillar=item.get("pillar"),
                category=item.get("category"),
                subcategory=item.get("subcategory"),
                theme_based=item.get("theme_based", False)
            )
            
            # Save idea
            filename = item.get("filename", None)
            if filename:
                # Ensure filename has .json extension
                if not filename.endswith('.json'):
                    filename += '.json'
                filepath = os.path.join(self.batch_config["output_dir"], filename)
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"idea_{index + 1}_{timestamp}.json"
                filepath = os.path.join(self.batch_config["output_dir"], filename)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(idea, f, indent=2)
            
            result = {
                "status": "success",
                "item": item,
                "filename": filename,
                "filepath": filepath,
                "timestamp": datetime.now().isoformat(),
                "message": f"Idea generated successfully"
            }
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "item": item,
                "filename": None,
                "filepath": None,
                "timestamp": datetime.now().isoformat(),
                "message": f"Error generating idea: {str(e)}"
            }
            return error_result
    
    def process_batch(self, batch_config: Dict) -> List[Dict]:
        """Process batch of items."""
        self.batch_config = batch_config
        self.results = []
        
        # Validate batch configuration
        if "items" not in batch_config:
            raise ValueError("Batch configuration must contain 'items' key")
        
        if not batch_config["items"]:
            raise ValueError("Batch configuration must contain at least one item")
        
        # Determine processing type
        process_type = batch_config.get("type", "scripts")
        
        if process_type == "scripts":
            processor_func = self.process_single_script
        elif process_type == "ideas":
            processor_func = self.process_single_idea
        else:
            raise ValueError(f"Unknown process type: {process_type}")
        
        # Process items in parallel
        max_workers = batch_config.get("max_workers", 4)
        continue_on_error = batch_config.get("continue_on_error", True)
        
        print(f"Starting batch processing with {max_workers} workers...")
        print(f"Processing {len(batch_config['items'])} items...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_index = {
                executor.submit(processor_func, item, index): index 
                for index, item in enumerate(batch_config["items"])
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    
                    if result["status"] == "success":
                        print(f"✓ Completed item {index + 1}")
                    else:
                        print(f"✗ Failed item {index + 1}: {result['message']}")
                        
                        if not continue_on_error:
                            # Cancel remaining tasks
                            for f in future_to_index:
                                f.cancel()
                            break
                            
                except Exception as e:
                    error_result = {
                        "status": "error",
                        "item": batch_config["items"][index],
                        "filename": None,
                        "filepath": None,
                        "timestamp": datetime.now().isoformat(),
                        "message": f"Unexpected error: {str(e)}"
                    }
                    self.results.append(error_result)
                    print(f"✗ Unexpected error on item {index + 1}: {str(e)}")
                    
                    if not continue_on_error:
                        # Cancel remaining tasks
                        for f in future_to_index:
                            f.cancel()
                        break
        
        return self.results
    
    def generate_batch_report(self, results: List[Dict]) -> Dict:
        """Generate a comprehensive batch processing report."""
        total_items = len(results)
        successful_items = len([r for r in results if r["status"] == "success"])
        failed_items = total_items - successful_items
        
        # Group results by status
        successful_results = [r for r in results if r["status"] == "success"]
        failed_results = [r for r in results if r["status"] == "error"]
        
        # Generate summary statistics
        report = {
            "batch_summary": {
                "total_items": total_items,
                "successful_items": successful_items,
                "failed_items": failed_items,
                "success_rate": (successful_items / total_items) * 100 if total_items > 0 else 0,
                "processing_time": datetime.now().isoformat()
            },
            "successful_results": successful_results,
            "failed_results": failed_results,
            "file_list": [r["filename"] for r in successful_results if r["filename"]],
            "error_summary": {
                "error_count": len(failed_results),
                "error_messages": list(set([r["message"] for r in failed_results]))
            }
        }
        
        return report
    
    def save_batch_report(self, report: Dict, output_dir: str) -> str:
        """Save batch processing report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_report_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        os.makedirs(output_dir, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Batch report saved to: {filepath}")
        return filepath
    
    def create_default_batch_config(self, config_type: str = "scripts", count: int = 5) -> Dict:
        """Create a default batch configuration for testing."""
        if config_type == "scripts":
            items = []
            for i in range(count):
                items.append({
                    "pillar": f"pillar_{(i % 5) + 1}",
                    "category": "learning_activities" if i % 2 == 0 else "milestone_celebrations",
                    "subcategory": "sensory_play_sessions" if i % 3 == 0 else "first_steps_series",
                    "baby_age": "8 months",
                    "custom_params": {
                        "tone": "warm and engaging",
                        "activity_description": f"Test activity {i + 1}"
                    }
                })
        else:  # ideas
            items = []
            for i in range(count):
                items.append({
                    "pillar": f"pillar_{(i % 5) + 1}",
                    "category": None,
                    "subcategory": None,
                    "theme_based": i % 2 == 0
                })
        
        return {
            "type": config_type,
            "description": f"Default {config_type} batch configuration for testing",
            "output_dir": f"generated-{config_type}",
            "max_workers": 4,
            "continue_on_error": True,
            "skip_existing": True,
            "items": items
        }

def main():
    parser = argparse.ArgumentParser(description="Batch process Miss Gracy Baby content")
    parser.add_argument("--config", required=True, help="Batch configuration file")
    parser.add_argument("--output", help="Output directory (overrides config)")
    parser.add_argument("--type", choices=["scripts", "ideas"], help="Processing type (overrides config)")
    parser.add_argument("--workers", type=int, help="Number of workers (overrides config)")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue processing even if some items fail")
    parser.add_argument("--generate-default", choices=["scripts", "ideas"], help="Generate default configuration")
    parser.add_argument("--default-count", type=int, default=5, help="Number of items for default configuration")
    parser.add_argument("--report", action="store_true", help="Generate batch processing report")
    
    args = parser.parse_args()
    
    processor = BatchProcessor()
    
    if args.generate_default:
        # Generate default configuration
        config = processor.create_default_batch_config(args.generate_default, args.default_count)
        config_file = f"default_batch_{args.generate_default}.json"
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Default batch configuration saved to: {config_file}")
        print(f"Configuration contains {len(config['items'])} items")
        return
    
    # Load batch configuration
    batch_config = processor.load_batch_config(args.config)
    
    # Override configuration with command line arguments
    if args.output:
        batch_config["output_dir"] = args.output
    if args.type:
        batch_config["type"] = args.type
    if args.workers:
        batch_config["max_workers"] = args.workers
    if args.continue_on_error:
        batch_config["continue_on_error"] = True
    
    # Process batch
    try:
        results = processor.process_batch(batch_config)
        
        # Generate and save report if requested
        if args.report:
            report = processor.generate_batch_report(results)
            report_file = processor.save_batch_report(report, batch_config["output_dir"])
            print(f"\nBatch Processing Report:")
            print(f"Total Items: {report['batch_summary']['total_items']}")
            print(f"Successful: {report['batch_summary']['successful_items']}")
            print(f"Failed: {report['batch_summary']['failed_items']}")
            print(f"Success Rate: {report['batch_summary']['success_rate']:.1f}%")
        
        print(f"\nBatch processing completed!")
        print(f"Results: {len([r for r in results if r['status'] == 'success'])} successful, {len([r for r in results if r['status'] == 'error'])} failed")
        
    except Exception as e:
        print(f"Error during batch processing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()