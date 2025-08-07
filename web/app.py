from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from workflow_manager import WorkflowManager
from content_idea_generator import ContentIdeaGenerator
from generate_video_script import VideoScriptGenerator
from video_generator import VideoGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_idea', methods=['POST'])
def generate_idea():
    idea_generator = ContentIdeaGenerator()
    idea = idea_generator.generate_content_idea()
    return jsonify(idea)

@app.route('/generate_script', methods=['POST'])
def generate_script():
    script_generator = VideoScriptGenerator()
    # For simplicity, using default parameters
    script = script_generator.generate_script(
        pillar="pillar_1_developmental_milestones",
        category="milestone_celebrations",
        subcategory="first_steps_series",
        baby_age="8 months"
    )
    return jsonify(script)

@app.route('/run_workflow', methods=['POST'])
def run_workflow():
    class Args:
        def __init__(self):
            self.generate_ideas = True
            self.generate_scripts = True
            self.quality_check = True
            self.generate_metadata = True
            self.batch_process = False
            self.create_schedule = False
            self.pillar = None
            self.category = None
            self.subcategory = None
            self.baby_age = '8 months'
            self.theme_based = False
            self.weekly_plan = False
            self.start_date = None
            self.idea_count = 1
            self.script_count = 1
            self.batch_file = None
            self.script_dir = 'generated-content'
            self.output_dir = 'generated-content'
            self.continue_on_error = False
            self.log_level = 'INFO'
            self.dry_run = False
            self.report = True

    args = Args()
    workflow_manager = WorkflowManager()
    workflow_config = workflow_manager.create_workflow_config(args)
    workflow_state = workflow_manager.execute_workflow(workflow_config)
    return jsonify(workflow_state)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    script_generator = VideoScriptGenerator()
    script = script_generator.generate_script(
        pillar="pillar_1_developmental_milestones",
        category="milestone_celebrations",
        subcategory="first_steps_series",
        baby_age="8 months"
    )

    video_generator = VideoGenerator(script)
    video_path = video_generator.generate_video()

    return jsonify({'video_url': video_path})