import json
import os

def generate_html(jsonl_path, output_path):
    if not os.path.exists(jsonl_path):
        print(f"Error: {jsonl_path} not found.")
        return

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IT Passport Exam - April 2025 (Spring)</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f4f7f6;
            }
            h1 {
                text-align: center;
                color: #2c3e50;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 10px;
            }
            .question-container {
                background: white;
                margin-bottom: 30px;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .question-header {
                display: flex;
                justify-content: space-between;
                font-weight: bold;
                color: #7f8c8d;
                font-size: 0.9em;
                margin-bottom: 15px;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }
            .question-text {
                font-size: 1.1em;
                margin-bottom: 20px;
                white-space: pre-wrap;
            }
            .media-container {
                text-align: center;
                margin: 20px 0;
            }
            .media-container img {
                max-width: 100%;
                height: auto;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            .choices {
                list-style-type: none;
                padding: 0;
            }
            .choice {
                margin: 10px 0;
                padding: 10px 15px;
                background: #f9f9f9;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                display: flex;
            }
            .choice-letter {
                font-weight: bold;
                margin-right: 10px;
                color: #3498db;
            }
            .answer-section {
                margin-top: 20px;
                padding-top: 15px;
                border-top: 2px dashed #eee;
            }
            .answer-toggle {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9em;
            }
            .answer-toggle:hover {
                background-color: #2980b9;
            }
            .answer-content {
                display: none;
                margin-top: 15px;
                padding: 15px;
                background-color: #e8f6f3;
                border-left: 5px solid #1abc9c;
            }
            .correct-label {
                font-weight: bold;
                color: #16a085;
            }
            pre {
                background: #272822;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            code {
                font-family: 'Courier New', Courier, monospace;
            }
        </style>
        <script>
            function toggleAnswer(id) {
                var x = document.getElementById("ans-" + id);
                var btn = document.getElementById("btn-" + id);
                if (x.style.display === "none" || x.style.display === "") {
                    x.style.display = "block";
                    btn.innerText = "Hide Answer";
                } else {
                    x.style.display = "none";
                    btn.innerText = "Show Answer";
                }
            }
        </script>
    </head>
    <body>
        <h1>IT Passport Examination (Spring 2025)</h1>
    """

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            q = json.loads(line)
            
            q_id = q['id']
            metadata = q['metadata']
            content = q['content']
            feedback = q['feedback']
            
            html_content += f"""
            <div class="question-container" id="q-{q_id}">
                <div class="question-header">
                    <span>{q_id} | {metadata['major_category']}</span>
                    <span>Topic: {metadata['topic']}</span>
                </div>
                <div class="question-text">{content['question_text']}</div>
            """
            
            # Add Media
            if content['has_media']:
                for media_item in content['media']:
                    if media_item['type'] == 'image':
                        html_content += f"""
                        <div class="media-container">
                            <img src="{media_item['base64']}" alt="{media_item['label']}">
                            <div style="font-size: 0.8em; color: #666; margin-top: 5px;">{media_item['label']}</div>
                        </div>
                        """
            
            # Add Choices
            html_content += '<ul class="choices">'
            for letter in ['a', 'b', 'c', 'd']:
                choice_text = content['choices'].get(letter, "N/A")
                html_content += f"""
                <li class="choice">
                    <span class="choice-letter">{letter.upper()})</span>
                    <span>{choice_text}</span>
                </li>
                """
            html_content += '</ul>'
            
            # Add Answer Section
            html_content += f"""
                <div class="answer-section">
                    <button class="answer-toggle" id="btn-{q_id}" onclick="toggleAnswer('{q_id}')">Show Answer</button>
                    <div class="answer-content" id="ans-{q_id}">
                        <p><span class="correct-label">Correct Answer:</span> {feedback['correct_answer'].upper()}</p>
                        <p><strong>Explanation:</strong> {feedback['explanation']}</p>
                    </div>
                </div>
            </div>
            """

    html_content += """
    </body>
    </html>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML exam reconstructed successfully: {output_path}")

if __name__ == "__main__":
    generate_html('2025S_IP_Questions.jsonl', '2025S_IP_Exam.html')
