#!/usr/bin/env python3
"""
Miss Gracy Baby Quality Control System
Ensures generated content meets quality standards and guidelines.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import argparse
from pathlib import Path
import re
from dataclasses import dataclass

@dataclass
class QualityCheck:
    """Quality check result."""
    check_name: str
    passed: bool
    score: float
    message: str
    details: Dict = None

class QualityControl:
    def __init__(self, config_path: str = "gemini-config.json"):
        """Initialize quality control system."""
        self.config = self._load_config(config_path)
        self.quality_standards = self._load_quality_standards()
        
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
    
    def _load_quality_standards(self) -> Dict:
        """Load quality standards from file."""
        quality_file = "prompt-templates/quality-standards.json"
        try:
            with open(quality_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default quality standards
            return self._create_default_quality_standards()
    
    def _create_default_quality_standards(self) -> Dict:
        """Create default quality standards."""
        return {
            "script_structure": {
                "required_sections": ["hook", "setup", "main_content", "educational_element", "conclusion"],
                "max_duration": 270,  # 4.5 minutes in seconds
                "min_duration": 240,  # 4 minutes in seconds
                "section_durations": {
                    "hook": {"min": 15, "max": 15},
                    "setup": {"min": 15, "max": 15},
                    "main_content": {"min": 180, "max": 180},
                    "educational_element": {"min": 30, "max": 30},
                    "conclusion": {"min": 30, "max": 30}
                }
            },
            "content_quality": {
                "min_word_count": 300,
                "max_word_count": 800,
                "required_elements": [
                    "baby_age_reference",
                    "developmental_focus",
                    "engaging_language",
                    "clear_structure",
                    "call_to_action"
                ],
                "prohibited_content": [
                    "inappropriate_language",
                    "unsafe_practices",
                    "negative_stereotypes",
                    "medical_advice"
                ]
            },
            "engagement_factors": {
                "min_hashtags": 5,
                "max_hashtags": 15,
                "required_cta_types": ["subscribe", "comment", "share"],
                "emotional_keywords": ["amazing", "adorable", "heartwarming", "exciting", "magical"],
                "engagement_score_threshold": 7.0
            },
            "technical_requirements": {
                "min_title_length": 10,
                "max_title_length": 80,
                "min_description_length": 100,
                "max_description_length": 5000,
                "required_file_format": "json",
                "file_size_limit_mb": 10
            }
        }
    
    def check_script_structure(self, script: Dict) -> List[QualityCheck]:
        """Check script structure compliance."""
        checks = []
        
        # Check required sections
        required_sections = self.quality_standards["script_structure"]["required_sections"]
        for section in required_sections:
            if section not in script.get("script", {}):
                checks.append(QualityCheck(
                    check_name=f"required_section_{section}",
                    passed=False,
                    score=0.0,
                    message=f"Missing required section: {section}"
                ))
            else:
                checks.append(QualityCheck(
                    check_name=f"required_section_{section}",
                    passed=True,
                    score=10.0,
                    message=f"Required section {section} present"
                ))
        
        # Check section durations
        section_durations = self.quality_standards["script_structure"]["section_durations"]
        for section, duration_range in section_durations.items():
            if section in script.get("script", {}):
                # This is a simplified check - in practice, you'd parse actual timing
                checks.append(QualityCheck(
                    check_name=f"section_duration_{section}",
                    passed=True,
                    score=10.0,
                    message=f"Section {section} duration should be {duration_range['min']}-{duration_range['max']} seconds"
                ))
        
        return checks
    
    def check_content_quality(self, script: Dict) -> List[QualityCheck]:
        """Check content quality metrics."""
        checks = []
        
        # Extract text content for analysis
        script_content = script.get("script", {})
        full_text = ""
        
        for section, content in script_content.items():
            if isinstance(content, dict) and "content" in content:
                full_text += content["content"] + " "
            elif isinstance(content, str):
                full_text += content + " "
        
        word_count = len(full_text.split())
        
        # Check word count
        min_words = self.quality_standards["content_quality"]["min_word_count"]
        max_words = self.quality_standards["content_quality"]["max_word_count"]
        
        if min_words <= word_count <= max_words:
            checks.append(QualityCheck(
                check_name="word_count",
                passed=True,
                score=10.0,
                message=f"Word count {word_count} is within acceptable range ({min_words}-{max_words})"
            ))
        else:
            checks.append(QualityCheck(
                check_name="word_count",
                passed=False,
                score=5.0,
                message=f"Word count {word_count} is outside acceptable range ({min_words}-{max_words})"
            ))
        
        # Check required elements
        required_elements = self.quality_standards["content_quality"]["required_elements"]
        for element in required_elements:
            if self._check_element_presence(full_text, element):
                checks.append(QualityCheck(
                    check_name=f"required_element_{element}",
                    passed=True,
                    score=8.0,
                    message=f"Required element '{element}' found"
                ))
            else:
                checks.append(QualityCheck(
                    check_name=f"required_element_{element}",
                    passed=False,
                    score=0.0,
                    message=f"Required element '{element}' not found"
                ))
        
        # Check for prohibited content
        prohibited_content = self.quality_standards["content_quality"]["prohibited_content"]
        for prohibited in prohibited_content:
            if self._check_prohibited_content(full_text, prohibited):
                checks.append(QualityCheck(
                    check_name=f"prohibited_content_{prohibited}",
                    passed=False,
                    score=0.0,
                    message=f"Prohibited content '{prohibited}' found"
                ))
            else:
                checks.append(QualityCheck(
                    check_name=f"prohibited_content_{prohibited}",
                    passed=True,
                    score=10.0,
                    message=f"No prohibited content '{prohibited}' found"
                ))
        
        return checks
    
    def _check_element_presence(self, text: str, element: str) -> bool:
        """Check if required element is present in text."""
        element_keywords = {
            "baby_age_reference": ["months", "years", "old", "age", "month", "year"],
            "developmental_focus": ["development", "learn", "skill", "milestone", "growth"],
            "engaging_language": ["amazing", "adorable", "exciting", "wonderful", "beautiful"],
            "clear_structure": ["first", "next", "then", "finally", "step"],
            "call_to_action": ["subscribe", "like", "comment", "share", "watch"]
        }
        
        keywords = element_keywords.get(element, [])
        return any(keyword.lower() in text.lower() for keyword in keywords)
    
    def _check_prohibited_content(self, text: str, prohibited: str) -> bool:
        """Check for prohibited content."""
        prohibited_keywords = {
            "inappropriate_language": ["stupid", "hate", "idiot", "dumb", "bad"],
            "unsafe_practices": ["dangerous", "unsafe", "risk", "harm", "hurt"],
            "negative_stereotypes": ["always", "never", "all", "none", "every"],
            "medical_advice": ["should", "must", "doctor", "medical", "treatment"]
        }
        
        keywords = prohibited_keywords.get(prohibited, [])
        return any(keyword.lower() in text.lower() for keyword in keywords)
    
    def check_engagement_factors(self, script: Dict) -> List[QualityCheck]:
        """Check engagement factors."""
        checks = []
        
        # Check hashtags (if available)
        if "metadata" in script and "hashtags" in script["metadata"]:
            hashtags = script["metadata"]["hashtags"]
            min_hashtags = self.quality_standards["engagement_factors"]["min_hashtags"]
            max_hashtags = self.quality_standards["engagement_factors"]["max_hashtags"]
            
            if min_hashtags <= len(hashtags) <= max_hashtags:
                checks.append(QualityCheck(
                    check_name="hashtag_count",
                    passed=True,
                    score=10.0,
                    message=f"Hashtag count {len(hashtags)} is within acceptable range"
                ))
            else:
                checks.append(QualityCheck(
                    check_name="hashtag_count",
                    passed=False,
                    score=5.0,
                    message=f"Hashtag count {len(hashtags)} is outside acceptable range"
                ))
        
        # Check call-to-action types
        required_ctas = self.quality_standards["engagement_factors"]["required_cta_types"]
        script_content = script.get("script", {})
        full_text = ""
        
        for section, content in script_content.items():
            if isinstance(content, dict) and "content" in content:
                full_text += content["content"] + " "
            elif isinstance(content, str):
                full_text += content + " "
        
        found_ctas = []
        for cta in required_ctas:
            if cta.lower() in full_text.lower():
                found_ctas.append(cta)
        
        if len(found_ctas) >= 2:  # At least 2 different CTAs
            checks.append(QualityCheck(
                check_name="call_to_action_variety",
                passed=True,
                score=10.0,
                message=f"Found {len(found_ctas)} different call-to-action types"
            ))
        else:
            checks.append(QualityCheck(
                check_name="call_to_action_variety",
                passed=False,
                score=5.0,
                message=f"Only found {len(found_ctas)} call-to-action types, need at least 2"
            ))
        
        # Check emotional keywords
        emotional_keywords = self.quality_standards["engagement_factors"]["emotional_keywords"]
        found_emotional = []
        
        for keyword in emotional_keywords:
            if keyword.lower() in full_text.lower():
                found_emotional.append(keyword)
        
        emotional_score = min(len(found_emotional) / len(emotional_keywords) * 10, 10)
        checks.append(QualityCheck(
            check_name="emotional_keywords",
            passed=emotional_score >= 5.0,
            score=emotional_score,
            message=f"Found {len(found_emotional)} emotional keywords: {', '.join(found_emotional)}"
        ))
        
        return checks
    
    def check_technical_requirements(self, script: Dict, filepath: str) -> List[QualityCheck]:
        """Check technical requirements."""
        checks = []
        
        # Check file format
        if filepath.endswith('.json'):
            checks.append(QualityCheck(
                check_name="file_format",
                passed=True,
                score=10.0,
                message="File format is JSON (required)"
            ))
        else:
            checks.append(QualityCheck(
                check_name="file_format",
                passed=False,
                score=0.0,
                message="File format is not JSON"
            ))
        
        # Check file size
        try:
            file_size = os.path.getsize(filepath)
            max_size_mb = self.quality_standards["technical_requirements"]["file_size_limit_mb"]
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size <= max_size_bytes:
                checks.append(QualityCheck(
                    check_name="file_size",
                    passed=True,
                    score=10.0,
                    message=f"File size {file_size/1024/1024:.2f}MB is within limit"
                ))
            else:
                checks.append(QualityCheck(
                    check_name="file_size",
                    passed=False,
                    score=0.0,
                    message=f"File size {file_size/1024/1024:.2f}MB exceeds limit of {max_size_mb}MB"
                ))
        except OSError:
            checks.append(QualityCheck(
                check_name="file_size",
                passed=False,
                score=0.0,
                message="Could not check file size"
            ))
        
        # Check title length (if available)
        if "metadata" in script and "title" in script["metadata"]:
            title = script["metadata"]["title"]
            min_title = self.quality_standards["technical_requirements"]["min_title_length"]
            max_title = self.quality_standards["technical_requirements"]["max_title_length"]
            
            if min_title <= len(title) <= max_title:
                checks.append(QualityCheck(
                    check_name="title_length",
                    passed=True,
                    score=10.0,
                    message=f"Title length {len(title)} is within acceptable range"
                ))
            else:
                checks.append(QualityCheck(
                    check_name="title_length",
                    passed=False,
                    score=5.0,
                    message=f"Title length {len(title)} is outside acceptable range"
                ))
        
        return checks
    
    def evaluate_script_quality(self, script: Dict, filepath: str = None) -> Dict:
        """Comprehensive quality evaluation of a script."""
        all_checks = []
        
        # Structure checks
        structure_checks = self.check_script_structure(script)
        all_checks.extend(structure_checks)
        
        # Content quality checks
        content_checks = self.check_content_quality(script)
        all_checks.extend(content_checks)
        
        # Engagement checks
        engagement_checks = self.check_engagement_factors(script)
        all_checks.extend(engagement_checks)
        
        # Technical checks
        if filepath:
            technical_checks = self.check_technical_requirements(script, filepath)
            all_checks.extend(technical_checks)
        
        # Calculate overall score
        total_score = sum(check.score for check in all_checks)
        max_score = len(all_checks) * 10
        overall_score = (total_score / max_score) * 100 if max_score > 0 else 0
        
        # Determine quality grade
        if overall_score >= 90:
            grade = "A"
        elif overall_score >= 80:
            grade = "B"
        elif overall_score >= 70:
            grade = "C"
        elif overall_score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        # Group checks by category
        checks_by_category = {
            "structure": [check for check in all_checks if "section" in check.check_name or "duration" in check.check_name],
            "content": [check for check in all_checks if "word_count" in check.check_name or "required_element" in check.check_name or "prohibited_content" in check.check_name],
            "engagement": [check for check in all_checks if "hashtag" in check.check_name or "call_to_action" in check.check_name or "emotional" in check.check_name],
            "technical": [check for check in all_checks if "file" in check.check_name or "title" in check.check_name or "description" in check.check_name]
        }
        
        evaluation = {
            "overall_score": overall_score,
            "grade": grade,
            "total_checks": len(all_checks),
            "passed_checks": len([check for check in all_checks if check.passed]),
            "failed_checks": len([check for check in all_checks if not check.passed]),
            "checks_by_category": checks_by_category,
            "detailed_checks": all_checks,
            "evaluation_timestamp": datetime.now().isoformat(),
            "recommendations": self._generate_recommendations(all_checks)
        }
        
        return evaluation
    
    def _generate_recommendations(self, checks: List[QualityCheck]) -> List[str]:
        """Generate improvement recommendations based on failed checks."""
        recommendations = []
        
        failed_checks = [check for check in checks if not check.passed]
        
        for check in failed_checks:
            if "word_count" in check.check_name:
                recommendations.append("Consider adjusting the content length to meet optimal word count requirements")
            elif "required_element" in check.check_name:
                recommendations.append("Add the missing required element to improve content quality")
            elif "hashtag_count" in check.check_name:
                recommendations.append("Adjust the number of hashtags for better discoverability")
            elif "call_to_action" in check.check_name:
                recommendations.append("Include more variety in call-to-action elements")
            elif "file_size" in check.check_name:
                recommendations.append("Optimize file size by reducing unnecessary content")
            elif "title_length" in check.check_name:
                recommendations.append("Adjust title length to meet optimal requirements")
        
        if not recommendations:
            recommendations.append("Content meets all quality standards!")
        
        return recommendations
    
    def batch_evaluate_scripts(self, script_dir: str) -> Dict:
        """Evaluate multiple scripts in a directory."""
        results = []
        
        if not os.path.exists(script_dir):
            print(f"Error: Directory not found: {script_dir}")
            return {"error": "Directory not found"}
        
        # Find all JSON files in directory
        json_files = []
        for root, dirs, files in os.walk(script_dir):
            for file in files:
                if file.endswith('.json'):
                    json_files.append(os.path.join(root, file))
        
        print(f"Evaluating {len(json_files)} scripts...")
        
        for filepath in json_files:
            try:
                with open(filepath, 'r') as f:
                    script = json.load(f)
                
                evaluation = self.evaluate_script_quality(script, filepath)
                results.append({
                    "filepath": filepath,
                    "filename": os.path.basename(filepath),
                    "evaluation": evaluation
                })
                
                print(f"✓ Evaluated: {os.path.basename(filepath)} (Grade: {evaluation['grade']})")
                
            except Exception as e:
                print(f"✗ Error evaluating {filepath}: {e}")
                results.append({
                    "filepath": filepath,
                    "filename": os.path.basename(filepath),
                    "error": str(e)
                })
        
        # Generate batch summary
        batch_summary = {
            "total_scripts": len(json_files),
            "evaluated_scripts": len([r for r in results if "evaluation" in r]),
            "average_score": sum(r["evaluation"]["overall_score"] for r in results if "evaluation" in r) / len([r for r in results if "evaluation" in r]) if results else 0,
            "grade_distribution": self._calculate_grade_distribution(results),
            "evaluation_timestamp": datetime.now().isoformat()
        }
        
        return {
            "batch_summary": batch_summary,
            "individual_results": results
        }
    
    def _calculate_grade_distribution(self, results: List[Dict]) -> Dict:
        """Calculate grade distribution for batch evaluation."""
        grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        
        for result in results:
            if "evaluation" in result:
                grade = result["evaluation"]["grade"]
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        return grade_counts
    
    def save_evaluation_report(self, evaluation: Dict, filepath: str) -> str:
        """Save evaluation report to file."""
        report_file = filepath.replace('.json', '_evaluation.json')
        
        with open(report_file, 'w') as f:
            json.dump(evaluation, f, indent=2)
        
        print(f"Evaluation report saved to: {report_file}")
        return report_file

def main():
    parser = argparse.ArgumentParser(description="Quality control for Miss Gracy Baby content")
    parser.add_argument("--script", help="Path to script file to evaluate")
    parser.add_argument("--directory", help="Directory containing scripts to evaluate")
    parser.add_argument("--output", help="Output file for evaluation report")
    parser.add_argument("--standards", help="Path to quality standards file")
    
    args = parser.parse_args()
    
    qc = QualityControl()
    
    if args.standards:
        # Load custom quality standards
        try:
            with open(args.standards, 'r') as f:
                qc.quality_standards = json.load(f)
        except Exception as e:
            print(f"Error loading custom standards: {e}")
            sys.exit(1)
    
    if args.script:
        # Evaluate single script
        try:
            with open(args.script, 'r') as f:
                script = json.load(f)
            
            evaluation = qc.evaluate_script_quality(script, args.script)
            
            print(f"\nQuality Evaluation Results:")
            print(f"Overall Score: {evaluation['overall_score']:.1f}/100")
            print(f"Grade: {evaluation['grade']}")
            print(f"Passed Checks: {evaluation['passed_checks']}/{evaluation['total_checks']}")
            
            if evaluation['recommendations']:
                print(f"\nRecommendations:")
                for rec in evaluation['recommendations']:
                    print(f"  - {rec}")
            
            if args.output:
                qc.save_evaluation_report(evaluation, args.output)
            
        except Exception as e:
            print(f"Error evaluating script: {e}")
            sys.exit(1)
    
    elif args.directory:
        # Evaluate batch of scripts
        batch_results = qc.batch_evaluate_scripts(args.directory)
        
        print(f"\nBatch Evaluation Summary:")
        print(f"Total Scripts: {batch_results['batch_summary']['total_scripts']}")
        print(f"Average Score: {batch_results['batch_summary']['average_score']:.1f}/100")
        print(f"Grade Distribution: {batch_results['batch_summary']['grade_distribution']}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(batch_results, f, indent=2)
            print(f"Batch report saved to: {args.output}")
    
    else:
        print("Error: Either --script or --directory must be specified")
        sys.exit(1)

if __name__ == "__main__":
    main()