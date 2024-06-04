from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Replace with your Genesys Cloud API headers
headers = {
    'Authorization': 'Bearer du5lDtNgvO0RHNeJ5I4V_mPMNRffrS1ShvH1wWyPEmn26g2DAcYYPEmNfYXzbx9TdgkY2o8eBTkV3NK_1QmjMw',
    'Content-Type': 'application/json'
}

@app.route('/')
def index():
    return render_template('index.html')

def fetch_all_queues():
    all_queues = []
    page = 1
    page_size = 100
    while True:
        response = requests.get(f'https://api.mypurecloud.com.au/api/v2/routing/queues?pageSize={page_size}&pageNumber={page}', headers=headers)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        all_queues.extend(data['entities'])
        if not data.get('nextUri'):
            break
        page += 1
    return all_queues

@app.route('/get_queues', methods=['GET'])
def get_queues():
    try:
        queues = fetch_all_queues()
        return jsonify({'entities': queues})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching queues: {e}")
        return jsonify({"error": "Failed to fetch queues"}), 500

@app.route('/get_queue_members', methods=['POST'])
def get_queue_members():
    queue_id = request.form['queue_id']
    try:
        response = requests.get(f'https://api.mypurecloud.com.au/api/v2/routing/queues/{queue_id}/members?pageSize=100&joined=true&expand=skills', headers=headers)
        response.raise_for_status()  # Check if the request was successful
        members = response.json()
        print(json.dumps(members, indent=2))  # Print the response for debugging
        return jsonify(members)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching queue members: {e}")
        return jsonify({"error": f"Failed to fetch members for queue {queue_id}"}), 500

@app.route('/update_skills', methods=['POST'])
def update_skills():
    data = request.json
    try:
        if 'updates' in data:
            updates = data['updates']
            for update in updates:
                user_id = update['userId']
                for skill in update['skills']:
                    skill_payload = {
                        "proficiency": skill['proficiency']
                    }
                    skill_id = skill['id']
                    response = requests.put(f'https://api.mypurecloud.com.au/api/v2/users/{user_id}/routingskills/{skill_id}', headers=headers, data=json.dumps(skill_payload))
                    response.raise_for_status()
        else:
            user_id = data['userId']
            skills = data['skills']
            for skill in skills:
                skill_payload = {
                    "proficiency": skill['proficiency']
                }
                skill_id = skill['id']
                response = requests.put(f'https://api.mypurecloud.com.au/api/v2/users/{user_id}/routingskills/{skill_id}', headers=headers, data=json.dumps(skill_payload))
                response.raise_for_status()
        return jsonify({"success": True})
    except requests.exceptions.RequestException as e:
        print(f"Error updating skills: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/add_agent', methods=['POST'])
def add_agent():
    data = request.json
    user_id = data['userId']
    queue_id = data['queueId']
    try:
        response = requests.post(f'https://api.mypurecloud.com.au/api/v2/routing/queues/{queue_id}/members', headers=headers, data=json.dumps({"userId": user_id}))
        response.raise_for_status()
        return jsonify({"success": True})
    except requests.exceptions.RequestException as e:
        print(f"Error adding agent to queue: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
