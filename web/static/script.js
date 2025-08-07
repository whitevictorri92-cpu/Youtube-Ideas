document.addEventListener('DOMContentLoaded', () => {
    const generateIdeaBtn = document.getElementById('generate-idea');
    const generateScriptBtn = document.getElementById('generate-script');
    const runWorkflowBtn = document.getElementById('run-workflow');
    const generateVideoBtn = document.getElementById('generate-video');
    const outputContent = document.getElementById('output-content');
    const downloadLink = document.getElementById('download-link');

    generateIdeaBtn.addEventListener('click', () => {
        fetch('/generate_idea', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                outputContent.textContent = JSON.stringify(data, null, 2);
            });
    });

    generateScriptBtn.addEventListener('click', () => {
        fetch('/generate_script', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                outputContent.textContent = JSON.stringify(data, null, 2);
            });
    });

    runWorkflowBtn.addEventListener('click', () => {
        fetch('/run_workflow', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                outputContent.textContent = JSON.stringify(data, null, 2);
            });
    });

    generateVideoBtn.addEventListener('click', () => {
        outputContent.textContent = 'Generating video... This may take a moment.';
        downloadLink.style.display = 'none';

        fetch('/generate_video', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                outputContent.textContent = `Video generated successfully!`;
                downloadLink.href = data.video_url;
                downloadLink.style.display = 'block';
            });
    });
});