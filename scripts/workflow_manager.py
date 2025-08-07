#!/usr/bin/env python3
"""
Miss Gracy Baby Workflow Manager
Integrates all components of the content generation workflow with the content blueprint.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import argparse
from pathlib import Path
import subprocess
import logging
from dataclasses import dataclass
from enum import Enum

# Import all components
from generate_video_script import VideoScriptGenerator
from content_idea_generator import ContentIdeaGenerator
from batch_processor import BatchProcessor
from quality_control import QualityControl
from metadata_generator import MetadataGenerator

class WorkflowStep(Enum):
    """Workflow execution steps."""
    GENERATE_IDEAS = "generate_ideas"
    GENERATE_SCRIPTS = "generate_scripts"
    QUALITY_CHECK = "quality_check"
    GENERATE_METADATA = "generate_metadata"
    BATCH_PROCESS = "batch_process"
    CREATE_SCHEDULE = "create_schedule"

@dataclass
class WorkflowConfig:
    """Workflow configuration."""
    steps: List[WorkflowStep]
    input_params: Dict
    output_dir: str
    continue_on_error: bool
    log_level: str
    dry_run: bool

class WorkflowManager:
    def __init__(self, config_path: str = "gemini-config.json"):
        """Initialize workflow manager."""
        self.config = self._load_config(config_path)
        self.setup_logging()
        
        # Initialize all components
        self.script_generator = VideoScriptGenerator(config_path)
        self.idea_generator = ContentIdeaGenerator()
        self.batch_processor = BatchProcessor(config_path)
        self.quality_control = QualityControl(config_path)
        self.metadata_generator = MetadataGenerator(config_path)
        
        # Workflow state
        self.workflow_state = {
            "start_time": None,
            "end_time": None,
            "completed_steps": [],
            "failed_steps": [],
            "generated_files": [],
            "quality_results": {},
            "metadata_results": {}
        }
    
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
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('workflow.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_workflow_config(self, args: argparse.Namespace) -> WorkflowConfig:
        """Create workflow configuration from command line arguments."""
        steps = []
        
        if args.generate_ideas:
            steps.append(WorkflowStep.GENERATE_IDEAS)
        if args.generate_scripts:
            steps.append(WorkflowStep.GENERATE_SCRIPTS)
        if args.quality_check:
            steps.append(WorkflowStep.QUALITY_CHECK)
        if args.generate_metadata:
            steps.append(WorkflowStep.GENERATE_METADATA)
        if args.batch_process:
            steps.append(WorkflowStep.BATCH_PROCESS)
        if args.create_schedule:
            steps.append(WorkflowStep.CREATE_SCHEDULE)
        
        if not steps:
            # Default workflow
            steps = [
                WorkflowStep.GENERATE_IDEAS,
                WorkflowStep.GENERATE_SCRIPTS,
                WorkflowStep.QUALITY_CHECK,
                WorkflowStep.GENERATE_METADATA
            ]
        
        return WorkflowConfig(
            steps=steps,
            input_vars=vars(args),
            output_dir=args.output_dir or "generated-content",
            continue_on_error=args.continue_on_error,
            log_level=args.log_level,
            dry_run=args.dry_run
        )
    
    def execute_workflow(self, workflow_config: WorkflowConfig) -> Dict:
        """Execute the complete workflow."""
        self.workflow_state["start_time"] = datetime.now()
        
        self.logger.info(f"Starting workflow with {len(workflow_config.steps)} steps")
        self.logger.info(f"Steps: {[step.value for step in workflow_config.steps]}")
        
        try:
            for step in workflow_config.steps:
                self.logger.info(f"Executing step: {step.value}")
                
                try:
                    if step == WorkflowStep.GENERATE_IDEAS:
                        result = self.execute_generate_ideas(workflow_config)
                    elif step == WorkflowStep.GENERATE_SCRIPTS:
                        result = self.execute_generate_scripts(workflow_config)
                    elif step == WorkflowStep.QUALITY_CHECK:
                        result = self.execute_quality_check(workflow_config)
                    elif step == WorkflowStep.GENERATE_METADATA:
                        result = self.execute_generate_metadata(workflow_config)
                    elif step == WorkflowStep.BATCH_PROCESS:
                        result = self.execute_batch_process(workflow_config)
                    elif step == WorkflowStep.CREATE_SCHEDULE:
                        result = self.execute_create_schedule(workflow_config)
                    else:
                        raise ValueError(f"Unknown workflow step: {step}")
                    
                    self.workflow_state["completed_steps"].append(step.value)
                    self.logger.info(f"Completed step: {step.value}")
                    
                except Exception as e:
                    self.logger.error(f"Failed step: {step.value} - {str(e)}")
                    self.workflow_state["failed_steps"].append({
                        "step": step.value,
                        "error": str(e)
                    })
                    
                    if not workflow_config.continue_on_error:
                        raise
                    else:
                        continue
                
                # Store results
                if result:
                    self.workflow_state[f"{step.value}_results"] = result
            
            self.workflow_state["end_time"] = datetime.now()
            self.logger.info("Workflow completed successfully")
            
            return self.workflow_state
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            self.workflow_state["end_time"] = datetime.now()
            raise
    
    def execute_generate_ideas(self, config: WorkflowConfig) -> Dict:
        """Execute generate ideas step."""
        self.logger.info("Generating content ideas...")
        
        if config.input_vars.get("weekly_plan"):
            # Generate weekly content plan
            weekly_plan = self.idea_generator.generate_weekly_content_plan(
                config.input_vars.get("start_date")
            )
            
            # Save weekly plan
            plan_file = os.path.join(config.output_dir, "weekly_content_plan.json")
            os.makedirs(os.path.dirname(plan_file), exist_ok=True)
            with open(plan_file, 'w') as f:
                json.dump(weekly_plan, f, indent=2)
            
            self.workflow_state["generated_files"].append(plan_file)
            
            return {
                "type": "weekly_plan",
                "file": plan_file,
                "ideas_count": len(weekly_plan["content_schedule"])
            }
        
        else:
            # Generate individual content ideas
            ideas = []
            count = config.input_vars.get("idea_count", 5)
            
            for i in range(count):
                idea = self.idea_generator.generate_content_idea(
                    pillar=config.input_vars.get("pillar"),
                    category=config.input_vars.get("category"),
                    subcategory=config.input_vars.get("subcategory"),
                    theme_based=config.input_vars.get("theme_based", False)
                )
                
                # Save idea
                idea_file = os.path.join(config.output_dir, f"content_idea_{i+1}.json")
                os.makedirs(os.path.dirname(idea_file), exist_ok=True)
                with open(idea_file, 'w') as f:
                    json.dump(idea, f, indent=2)
                
                ideas.append(idea)
                self.workflow_state["generated_files"].append(idea_file)
            
            return {
                "type": "individual_ideas",
                "count": len(ideas),
                "ideas": ideas
            }
    
    def execute_generate_scripts(self, config: WorkflowConfig) -> Dict:
        """Execute generate scripts step."""
        self.logger.info("Generating video scripts...")
        
        scripts = []
        
        if config.input_vars.get("batch_file"):
            # Process from batch configuration
            batch_config = self.batch_processor.load_batch_config(config.input_vars["batch_file"])
            results = self.batch_processor.process_batch(batch_config)
            
            for result in results:
                if result["status"] == "success":
                    scripts.append(result)
                    self.workflow_state["generated_files"].append(result["filepath"])
        
        else:
            # Generate individual scripts
            count = config.input_vars.get("script_count", 3)
            
            for i in range(count):
                script = self.script_generator.generate_script(
                    pillar=config.input_vars.get("pillar", "pillar_2_daily_adventures"),
                    category=config.input_vars.get("category", "everyday_discoveries"),
                    subcategory=config.input_vars.get("subcategory", "morning_routine_magic"),
                    baby_age=config.input_vars.get("baby_age", "8 months"),
                    custom_params=config.input_vars.get("custom_params", {})
                )
                
                # Save script
                script_file = os.path.join(config.output_dir, f"video_script_{i+1}.json")
                os.makedirs(os.path.dirname(script_file), exist_ok=True)
                with open(script_file, 'w') as f:
                    json.dump(script, f, indent=2)
                
                scripts.append(script)
                self.workflow_state["generated_files"].append(script_file)
        
        return {
            "type": "scripts",
            "count": len(scripts),
            "scripts": scripts
        }
    
    def execute_quality_check(self, config: WorkflowConfig) -> Dict:
        """Execute quality check step."""
        self.logger.info("Performing quality checks...")
        
        script_dir = config.input_vars.get("script_dir", config.output_dir)
        quality_results = self.quality_control.batch_evaluate_scripts(script_dir)
        
        # Save quality report
        quality_file = os.path.join(config.output_dir, "quality_report.json")
        os.makedirs(os.path.dirname(quality_file), exist_ok=True)
        with open(quality_file, 'w') as f:
            json.dump(quality_results, f, indent=2)
        
        self.workflow_state["generated_files"].append(quality_file)
        self.workflow_state["quality_results"] = quality_results
        
        return quality_results
    
    def execute_generate_metadata(self, config: WorkflowConfig) -> Dict:
        """Execute generate metadata step."""
        self.logger.info("Generating metadata...")
        
        script_dir = config.input_vars.get("script_dir", config.output_dir)
        metadata_files = self.metadata_generator.batch_generate_metadata(script_dir)
        
        # Collect metadata results
        metadata_results = []
        for metadata_file in metadata_files:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            metadata_results.append(metadata)
        
        self.workflow_state["metadata_results"] = metadata_results
        self.workflow_state["generated_files"].extend(metadata_files)
        
        return {
            "type": "metadata",
            "count": len(metadata_files),
            "files": metadata_files
        }
    
    def execute_batch_process(self, config: WorkflowConfig) -> Dict:
        """Execute batch processing step."""
        self.logger.info("Running batch processing...")
        
        batch_config = self.batch_processor.load_batch_config(config.input_vars["batch_file"])
        results = self.batch_processor.process_batch(batch_config)
        
        # Generate batch report
        report = self.batch_processor.generate_batch_report(results)
        report_file = os.path.join(config.output_dir, "batch_processing_report.json")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.workflow_state["generated_files"].append(report_file)
        
        return {
            "type": "batch_processing",
            "results": results,
            "report": report
        }
    
    def execute_create_schedule(self, config: WorkflowConfig) -> Dict:
        """Execute create schedule step."""
        self.logger.info("Creating content schedule...")
        
        # Generate weekly content plan
        weekly_plan = self.idea_generator.generate_weekly_content_plan(
            config.input_vars.get("start_date")
        )
        
        # Create publishing schedule
        schedule = self.create_publishing_schedule(weekly_plan)
        
        # Save schedule
        schedule_file = os.path.join(config.output_dir, "content_schedule.json")
        os.makedirs(os.path.dirname(schedule_file), exist_ok=True)
        with open(schedule_file, 'w') as f:
            json.dump(schedule, f, indent=2)
        
        self.workflow_state["generated_files"].append(schedule_file)
        
        return {
            "type": "schedule",
            "schedule": schedule,
            "file": schedule_file
        }
    
    def create_publishing_schedule(self, weekly_plan: Dict) -> Dict:
        """Create detailed publishing schedule."""
        schedule = {
            "week_start": weekly_plan["week_start"],
            "week_end": weekly_plan["week_end"],
            "publishing_schedule": {},
            "content_calendar": {},
            "reminders": []
        }
        
        # Define optimal publishing times
        publish_times = {
            "monday": "09:00",
            "tuesday": "10:00",
            "wednesday": "14:00",
            "thursday": "11:00",
            "friday": "15:00",
            "saturday": "10:00",
            "sunday": "16:00"
        }
        
        for day, content in weekly_plan["content_schedule"].items():
            publish_time = publish_times.get(day, "14:00")
            publish_date = content["date"]
            
            schedule["publishing_schedule"][day] = {
                "date": publish_date,
                "time": publish_time,
                "title": content["suggested_title"],
                "pillar": content["pillar"],
                "content_type": content["content_type"],
                "video_length": content["video_length"],
                "status": "scheduled"
            }
            
            # Add to content calendar
            schedule["content_calendar"][publish_date] = {
                "day": day,
                "time": publish_time,
                "title": content["suggested_title"],
                "pillar": content["pillar"],
                "content_type": content["content_type"],
                "video_length": content["video_length"]
            }
            
            # Add reminders (3 days before, 1 day before, day of)
            reminder_dates = [
                (datetime.strptime(publish_date, "%Y-%m-%d") - timedelta(days=3)).strftime("%Y-%m-%d"),
                (datetime.strptime(publish_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d"),
                publish_date
            ]
            
            for reminder_date in reminder_dates:
                schedule["reminders"].append({
                    "date": reminder_date,
                    "type": "publishing_reminder",
                    "content": content["suggested_title"],
                    "days_until": (datetime.strptime(publish_date, "%Y-%m-%d") - datetime.strptime(reminder_date, "%Y-%m-%d")).days
                })
        
        return schedule
    
    def generate_workflow_report(self, workflow_state: Dict) -> Dict:
        """Generate comprehensive workflow report."""
        duration = None
        if workflow_state["start_time"] and workflow_state["end_time"]:
            duration = (workflow_state["end_time"] - workflow_state["start_time"]).total_seconds()
        
        report = {
            "workflow_summary": {
                "start_time": workflow_state["start_time"].isoformat() if workflow_state["start_time"] else None,
                "end_time": workflow_state["end_time"].isoformat() if workflow_state["end_time"] else None,
                "duration_seconds": duration,
                "completed_steps": len(workflow_state["completed_steps"]),
                "failed_steps": len(workflow_state["failed_steps"]),
                "total_generated_files": len(workflow_state["generated_files"])
            },
            "step_results": {},
            "file_list": workflow_state["generated_files"],
            "quality_summary": workflow_state.get("quality_results", {}).get("batch_summary", {}),
            "metadata_summary": {
                "total_metadata_files": len(workflow_state.get("metadata_results", []))
            },
            "success": len(workflow_state["failed_steps"]) == 0
        }
        
        # Add step results
        for step_name, results in workflow_state.items():
            if step_name.endswith("_results") and isinstance(results, dict):
                report["step_results"][step_name] = results
        
        return report
    
    def save_workflow_report(self, report: Dict, output_dir: str) -> str:
        """Save workflow report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"workflow_report_{timestamp}.json")
        
        os.makedirs(output_dir, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Workflow report saved to: {report_file}")
        return report_file

def main():
    parser = argparse.ArgumentParser(description="Miss Gracy Baby Workflow Manager")
    
    # Workflow steps
    parser.add_argument("--generate-ideas", action="store_true", help="Generate content ideas")
    parser.add_argument("--generate-scripts", action="store_true", help="Generate video scripts")
    parser.add_argument("--quality-check", action="store_true", help="Perform quality checks")
    parser.add_argument("--generate-metadata", action="store_true", help="Generate metadata")
    parser.add_argument("--batch-process", action="store_true", help="Run batch processing")
    parser.add_argument("--create-schedule", action="store_true", help="Create content schedule")
    
    # Input parameters
    parser.add_argument("--pillar", help="Content pillar")
    parser.add_argument("--category", help="Content category")
    parser.add_argument("--subcategory", help="Content subcategory")
    parser.add_argument("--baby-age", default="8 months", help="Baby's age")
    parser.add_argument("--theme-based", action="store_true", help="Generate theme-based ideas")
    parser.add_argument("--weekly-plan", action="store_true", help="Generate weekly content plan")
    parser.add_argument("--start-date", help="Start date for weekly plan")
    parser.add_argument("--idea-count", type=int, default=5, help="Number of ideas to generate")
    parser.add_argument("--script-count", type=int, default=3, help="Number of scripts to generate")
    parser.add_argument("--batch-file", help="Batch configuration file")
    parser.add_argument("--script-dir", help="Directory containing scripts")
    
    # Output and configuration
    parser.add_argument("--output-dir", default="generated-content", help="Output directory")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue workflow even if some steps fail")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Logging level")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--report", action="store_true", help="Generate workflow report")
    
    args = parser.parse_args()
    
    # Initialize workflow manager
    workflow_manager = WorkflowManager()
    
    # Create workflow configuration
    workflow_config = workflow_manager.create_workflow_config(args)
    
    # Execute workflow
    try:
        workflow_state = workflow_manager.execute_workflow(workflow_config)
        
        # Generate and save report if requested
        if args.report:
            report = workflow_manager.generate_workflow_report(workflow_state)
            workflow_manager.save_workflow_report(report, workflow_config.output_dir)
            
            print(f"\nWorkflow Summary:")
            print(f"Completed Steps: {len(workflow_state['completed_steps'])}")
            print(f"Failed Steps: {len(workflow_state['failed_steps'])}")
            print(f"Generated Files: {len(workflow_state['generated_files'])}")
            
            if workflow_state["quality_results"]:
                quality_summary = workflow_state["quality_results"].get("batch_summary", {})
                print(f"Quality Results: {quality_summary.get('success_rate', 0):.1f}% success rate")
            
            if workflow_state["failed_steps"]:
                print(f"\nFailed Steps:")
                for failed in workflow_state["failed_steps"]:
                    print(f"  - {failed['step']}: {failed['error']}")
        
        print(f"\nWorkflow completed successfully!")
        print(f"Generated {len(workflow_state['generated_files'])} files in {workflow_config.output_dir}")
        
    except Exception as e:
        print(f"Workflow failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()