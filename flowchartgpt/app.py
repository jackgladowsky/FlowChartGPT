import os
import openai
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

systemPrompt = """
You are an AI assistant that is tasked with generating Mermaid.js 
flowchart code based on user input. 
When given a prompt describing a flowchart, 
respond with the appropriate Mermaid.js code for the flowchart.
It has to be ONLY the mermaid.js code, no saying here is the code, 
or exaplaining what it does, do not say mermaid either, 
start with graph TD and end with the last node connection.
"""

def generate_reply(prompt, model='gpt-3.5-turbo'):
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": f"Create a Mermaid.js flowchart for the following prompt: {prompt}"}
        ]
    )
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = generate_reply(prompt)
        if response['choices'][0]['message']['content'][0:3] == 'gra':
            flowchart_content = response['choices'][0]['message']['content']
            return render_template('flowchart.html', flowchart_content=flowchart_content)
        else:
            return render_template('home.html', error="Invalid Mermaid.js code generated. Please try again.")
    return render_template('home.html', error=None)

@app.route('/flowchart', methods=['GET', 'POST'])
def flowchart():
    if request.method == 'POST':
        prompt = request.form['prompt']
        return redirect(url_for('flowchart', prompt=prompt))
    else:
        prompt = request.args.get('prompt', '')
        if not prompt:
            return redirect(url_for('home'))

        response = generate_reply(prompt)
        if response['choices'][0]['message']['content'][0:3] == 'gra':
            flowchart_content = response['choices'][0]['message']['content']
            return render_template('flowchart.html', flowchart_content=flowchart_content)
        else:
            return render_template('home.html', error="Invalid Mermaid.js code generated. Please try again.")


if __name__ == '__main__':
    app.run(debug=True)
