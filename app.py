import os
import openai
from flask import Flask, request, jsonify

openai.api_key = os.environ['OPENAI_KEY']

app = Flask(__name__)

@app.route('/')
def home():
   return 'OK'

def text_completion(system_prompt:str, prompt: str) -> dict:
  '''
    Call Openai API for text completion
    Parameters:
        - prompt: user query (str)
    Returns:
        - dict
    '''
  try:
    response = openai.chat.completions.create(
      messages=[
          {
              'role': 'system',
              'content': system_prompt
          },
        {
          'role': 'user',
          'content': prompt
        }
      ],
      model='gpt-3.5-turbo',
      max_tokens=200,
    )
    return {'status': 1, 'response': response.choices[0].message.content}
  except:
    return {'status': 0, 'response': ''}

@app.route('/dialogflow/es/receiveMessage', methods=['POST'])
def esReceiveMessage():
    data = request.get_json()
    print("########################")
    print(data)
    print("########################")

    query = data['queryResult']['queryText']
    system_prompt = "You are a helpful assistant."
    query = "Given the question and the answer. You have to generate a follow up question for the answer.\n" + query + "\nJust return a question alone without any other text."

    result = text_completion(system_prompt, query)

    if result['status'] == 1:
        return jsonify(
            {
                'fulfillmentText': result['response']
            }
        )
    else:
        return jsonify(
            {
                'fulfillmentText': "Couldn't fetch response for query"
            }
        )

if __name__ =='__main__':
   app.run(
     host='0.0.0.0',
     port=5000,
     debug=True
   )