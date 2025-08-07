import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os
import json

# Add the scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scripts')))

from content_idea_generator import ContentIdeaGenerator
from generate_video_script import VideoScriptGenerator
from workflow_manager import WorkflowManager
from video_generator import VideoGenerator

class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.insert(tk.END, string)
        self.text_space.see(tk.END)

    def flush(self):
        pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Miss Gracy Baby - Content Generation")
        self.geometry("800x600")

        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Load pillar data
        with open("prompt-templates/content-pillar-templates.json", 'r') as f:
            self.pillar_data = json.load(f)

        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Inputs", padding="10")
        input_frame.pack(fill=tk.X, pady=5)

        # Pillar
        ttk.Label(input_frame, text="Pillar:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.pillar_var = tk.StringVar()
        self.pillar_menu = ttk.Combobox(input_frame, textvariable=self.pillar_var, values=list(self.pillar_data.keys()))
        self.pillar_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.pillar_menu.bind("<<ComboboxSelected>>", self.update_categories)

        # Category
        ttk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var)
        self.category_menu.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.category_menu.bind("<<ComboboxSelected>>", self.update_subcategories)

        # Subcategory
        ttk.Label(input_frame, text="Subcategory:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.subcategory_var = tk.StringVar()
        self.subcategory_menu = ttk.Combobox(input_frame, textvariable=self.subcategory_var)
        self.subcategory_menu.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        # Baby Age
        ttk.Label(input_frame, text="Baby Age:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.baby_age_var = tk.StringVar(value="8 months")
        self.baby_age_entry = ttk.Entry(input_frame, textvariable=self.baby_age_var)
        self.baby_age_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

        input_frame.columnconfigure(1, weight=1)

        # Controls Frame
        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        controls_frame.pack(fill=tk.X, pady=5)

        self.generate_idea_btn = ttk.Button(controls_frame, text="Generate Content Idea", command=self.generate_idea)
        self.generate_idea_btn.pack(side=tk.LEFT, padx=5)

        self.generate_script_btn = ttk.Button(controls_frame, text="Generate Video Script", command=self.generate_script)
        self.generate_script_btn.pack(side=tk.LEFT, padx=5)

        self.run_workflow_btn = ttk.Button(controls_frame, text="Run Full Workflow", command=self.run_workflow)
        self.run_workflow_btn.pack(side=tk.LEFT, padx=5)

        self.generate_video_btn = ttk.Button(controls_frame, text="Generate Video", command=self.generate_video)
        self.generate_video_btn.pack(side=tk.LEFT, padx=5)

        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=100, height=30)
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Redirect stdout
        sys.stdout = StdoutRedirector(self.output_text)

        # Status Bar
        self.status_bar = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_categories(self, event=None):
        pillar = self.pillar_var.get()
        if pillar:
            categories = list(self.pillar_data[pillar]["categories"].keys())
            self.category_menu['values'] = categories
            self.category_var.set("")
            self.subcategory_var.set("")
            self.subcategory_menu['values'] = []

    def update_subcategories(self, event=None):
        pillar = self.pillar_var.get()
        category = self.category_var.get()
        if pillar and category:
            subcategories = self.pillar_data[pillar]["categories"][category]["subcategories"]
            self.subcategory_menu['values'] = subcategories
            self.subcategory_var.set("")

    def run_in_thread(self, target):
        thread = threading.Thread(target=target)
        thread.start()
        self.monitor_thread(thread)

    def monitor_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.monitor_thread(thread))
        else:
            self.status_bar.config(text="Ready")
            self.enable_buttons()

    def disable_buttons(self):
        self.generate_idea_btn.config(state=tk.DISABLED)
        self.generate_script_btn.config(state=tk.DISABLED)
        self.run_workflow_btn.config(state=tk.DISABLED)
        self.generate_video_btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.generate_idea_btn.config(state=tk.NORMAL)
        self.generate_script_btn.config(state=tk.NORMAL)
        self.run_workflow_btn.config(state=tk.NORMAL)
        self.generate_video_btn.config(state=tk.NORMAL)

    def generate_idea(self):
        if not self.pillar_var.get() or not self.category_var.get() or not self.subcategory_var.get():
            messagebox.showerror("Error", "Please select a pillar, category, and subcategory.")
            return

        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Generating idea...")
        self.disable_buttons()
        self.run_in_thread(self._generate_idea_task)

    def _generate_idea_task(self):
        try:
            idea_generator = ContentIdeaGenerator()
            idea = idea_generator.generate_content_idea(
                pillar=self.pillar_var.get(),
                category=self.category_var.get(),
                subcategory=self.subcategory_var.get()
            )
            print(idea)
            messagebox.showinfo("Success", "Content idea generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_script(self):
        if not self.pillar_var.get() or not self.category_var.get() or not self.subcategory_var.get():
            messagebox.showerror("Error", "Please select a pillar, category, and subcategory.")
            return

        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Generating script... Querying LLM, this may take a moment.")
        self.disable_buttons()
        self.run_in_thread(self._generate_script_task)

    def _generate_script_task(self):
        try:
            script_generator = VideoScriptGenerator()
            script = script_generator.generate_script(
                pillar=self.pillar_var.get(),
                category=self.category_var.get(),
                subcategory=self.subcategory_var.get(),
                baby_age=self.baby_age_var.get()
            )
            print(script)
            messagebox.showinfo("Success", "Video script generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_workflow(self):
        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Running workflow...")
        self.disable_buttons()
        self.run_in_thread(self._run_workflow_task)

    def _run_workflow_task(self):
        try:
            # This class simulates the argparse.Namespace object that the
            # WorkflowManager expects.
            class Args:
                def __init__(self, pillar, category, subcategory, baby_age):
                    self.generate_ideas = True
                    self.generate_scripts = True
                    self.quality_check = False  # Disabled due to missing dependencies
                    self.generate_metadata = False  # Disabled due to missing dependencies
                    self.idea_count = 1
                    self.script_count = 1
                    self.batch_file = None
                    self.script_dir = 'generated-content'
                    self.output_dir = 'generated-content'
                    self.continue_on_error = False
                    self.log_level = 'INFO'
                    self.dry_run = False
                    self.report = True
                    self.pillar = pillar
                    self.category = category
                    self.subcategory = subcategory
                    self.baby_age = baby_age
                    self.theme_based = False
                    self.weekly_plan = False
                    self.start_date = None

            # Ensure required fields are selected
            if not all([self.pillar_var.get(), self.category_var.get(), self.subcategory_var.get()]):
                messagebox.showerror("Error", "Please select a pillar, category, and subcategory to run the workflow.")
                return

            args = Args(self.pillar_var.get(), self.category_var.get(), self.subcategory_var.get(), self.baby_age_var.get())

            print("Initializing Workflow Manager...")
            # Assumes a valid 'gemini-config.json' exists in the root directory.
            workflow_manager = WorkflowManager("gemini-config.json")
            print("Creating workflow configuration...")
            workflow_config = workflow_manager.create_workflow_config(args)
            print("Executing workflow...")
            workflow_state = workflow_manager.execute_workflow(workflow_config)

            print("\n--- Workflow Report ---")
            report = workflow_manager.generate_workflow_report(workflow_state)
            print(json.dumps(report, indent=2))
            messagebox.showinfo("Success", "Workflow executed. Check output for details.")
        except Exception as e:
            messagebox.showerror("Workflow Error", f"An error occurred during the workflow: {str(e)}")

    def generate_video(self):
        if not self.pillar_var.get() or not self.category_var.get() or not self.subcategory_var.get():
            messagebox.showerror("Error", "Please select a pillar, category, and subcategory.")
            return

        self.output_text.delete(1.0, tk.END)
        self.status_bar.config(text="Generating video...")
        self.disable_buttons()
        self.run_in_thread(self._generate_video_task)

    def _generate_video_task(self):
        try:
            script_generator = VideoScriptGenerator()
            script = script_generator.generate_script(
                pillar=self.pillar_var.get(),
                category=self.category_var.get(),
                subcategory=self.subcategory_var.get(),
                baby_age=self.baby_age_var.get()
            )

            video_generator = VideoGenerator(script)
            video_path = video_generator.generate_video()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()