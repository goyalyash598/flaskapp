from pymongo import MongoClient
import json
import http.client
import re
import pypandoc

mongo_connection_string = "mongodb+srv://goyalyash598:gym12345@cluster0.xxkdyhs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
url = "rio24.azurewebsites.net"
access_token = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZDQkMtSFM1MTIiLCJraWQiOiIwMDk2NzkwNjQ1QTQ1RkJGOEY5MzU4NjI1MEY0M0NFNUI2RkY0MDQ3IiwidHlwIjoiYXQrand0IiwiY3R5IjoiSldUIn0.hpYpBIFTdKcUph-HfzRlD5ASFKTcqqOKCaWJec31xj85-6vjf_pUPLYyWX9k3Q6PPmRgHbnyYjwKYGUxOlIUrc3BhMDWSJ3K8MZEXUnwe0iM1L_2udCMq3IslPBnauvZtNNn73oJpXziv1rw66J3V1Bdy3Kd_XU1W6f_8s_SpHwB95JeulynEYp-TQFF7f-djscD5xJJIGChEwElZSmc59J8X5GltxvbBkQs1rkSUnp-6P4JKALbkp-fvYbEcP5g_uJ0Mw9yIz4RzOlfsGu2PDyHwojwVEJMy5HcFbNe3El_3EA2V9xLSGzG49h_-JAA-q3Rxf94HsNGP8NgJTu5Tg.ku6Bfx98GxeO_vlme2fz_w.TsbajnVmbXTQD9KzPKjSrlDm-YlJcRhjH0DmsANLfFgk-YqvHbXPy660zq7XsLl0F6My1JmreENvguxbKBlOolkxYAt5Znmky9GMZrq_Ip5KdoDeoHkEA9wjTuWFq96zkTt7G1_JLtdz68HDhm3sgTDvbULbhC8PhRoxZiA7NTZCvGu9pVuVl4exC3ahuCqHLZ2YXesZkHCJEBRLIuOLQNNSHCD4kqqBBpr4iAG022LlnfhbDRjShdAsFURFr0OxB8CaiUH8vtj_eoZJcWdEuGOBikzDWByqtwQ41QErQNQS5xSL4d2hG3oHYDr7fvANl8Nx6lV8dhRmP6pcDnOZkXTKnpK4tp3PRBB-9uuM2KCWm5rB6NBGAv9N9uOtuVv1g6S3i1j1rrgL_nZDjU68Ku8ZtCjOMKhkbvu6K2wnT-G6GAgSak-sVtB-CfCKQ72D1kwJZDoYE7n5r8n8XPZ0x3MBrgYHqOLWXcqGGgyxAHJ0A5_lEo3VyKlHm5BnH3GALfF-f4GL1bQiWqiulD-BybW5s6TE2TXMRlFfVmKDLZOz-OhZMNZqREB-jlkI5og40JhywKxxuJ9lfClY7i_BKYlb7ZMq2hd3I3VzYWTYtmll2m-NRkYlivygugD6M8hSfpox4HFhRya8NEwW_aONW4GVg7lATUrWjYVaQBTAVncl4_A9Nlym-Lk5l1qvUKK4vmvpnKu4Dprc6Idzbia4WBeOJMGSjoIVLtBZtAeRyRSGi5ceysn0CQ-MGZ47DZMPlTHtTExJgeZ2UthLK9pkcrfOa9tqAdjm1x8hAs8TJdCdITPeTtq850EY3BAfzNMG23o0NqMsiIcBjKjmMIYuExklKsbSY4E1wYEmjksmmmNNCZl9022cQwf6gN7G7_OklWQXCWKmjbxuK8aiAjqdJV26XSqh6X5PmHE5EuOHkotWmCvh4Ot2SAFLNI2l0ys0U8AiTttNzNmWKanRgl9dW528K2A6Iua5TAzDmtuZintDnRkw9rTBCyamV0Tcx0foKYi3drrOEcE4qhR5j4duRmoQ2b3LWSictdLx4KktiS1Kh0yInMmgzsm-faIJsT7KYQ_qfNlWGdWIKKxf9MpAV178H87gGSpyPKvBWRDZuNoPmkegPjkn7jbEbYswREuR9-HFP53Q7CwEK30nVADW-ZHFckQpxIiP-aXnm3jZfhP_a-yCQRCOZKmk08XkZGxysnbxGrKgL82fLqWMBXU4yd7LcMSvO_wuNZcmiztqkW6rQZeMt7z73ar9H8Y_V-HdkBSITNpvEHUA7OO7IrUu_AcO3hWjmuloHeV8kdzTc8YZ7mhej-Vjx4wd2zWcuLQ3HO9RqMLX178W8M_z0i2oB5y5gJvskx7tShJe-0cldfU_AM-wgIyWgto2ofCDQInkE6DsCEI-pGCEvPiUNig2oJZHVMw9uLEfIHUBN3BYqFZyWIabsPV_6P9V3HRatOwFu_AFCjsrEzHIFCHuo84UEQ.cbD3nUCGUOilsnG3ZJFKfaoDqWIlN17IIzEfU7LXdQI"  # Bearer token field left empty as requested
client = MongoClient(mongo_connection_string)
db = client.questions_db
questions_collection = db.questions5
buffer_collection = db.buffer
data_collection = db.data

def send_insomnia_request(question):
    conn = http.client.HTTPSConnection(url)
    print(question["question_type"] == 'MCQ') 
    print(type(question["question_type"]))
    if question["question_type"] == 'MCQ':
        temp = question.get("Options", [])
        payload = json.dumps({
            "Entity": {
                "QuestionText": question["Question"],
                "IsSubjective": False,  # Set this based on your actual question type
                "EQuestionType": 0,  # Adjust based on your needs
                "BloomIndex": question["Bloom's Index"],  # Adjust based on your needs
                "QuestionCommonDataId": "1",  # Adjust based on your needs
                "EDifficultyLevel": 5,  # Adjust based on your needs
                "IsActive": 1,
                # "QuestionOptions": 
                "QuestionOptions": [
                    {
                    "QuestionOptionText": temp[0].lower() ,
                    "IsCorrect": "True" if temp[0][temp[0].find(":"):].lower() in question["Answer"].lower()  else "False",
                    "SortOrder": "1",
                    "Notes": "12"
                    },
                    {
                    "QuestionOptionText": temp[1].lower() ,
                    "IsCorrect": "True" if temp[1][temp[1].find(":"):].lower()  in question["Answer"].lower()  else "False",
                    "SortOrder": "1",
                    "Notes": "12"
                    },
                    {
                    "QuestionOptionText": temp[2].lower() ,
                    "IsCorrect": "True" if temp[2][temp[2].find(":"):].lower()  in question["Answer"].lower()  else "False",
                    "SortOrder": "1",
                    "Notes": "12"
                    },
                    {
                    "QuestionOptionText": temp[3].lower() ,
                    "IsCorrect": "True" if temp[3][temp[3].find(":"):].lower()  in question["Answer"].lower()  else "False",
                    "SortOrder": "1",
                    "Notes": "12"
                    }
                    ]
 
            }
        })
    else:

        payload = json.dumps({
            "Entity": {
                "QuestionText": question["Question"],
                "IsSubjective": True,  # Set this based on your actual question type
                "EQuestionType": 0,  # Adjust based on your needs
                "BloomIndex": question["Bloom's Index"],  # Adjust based on your needs
                "QuestionCommonDataId": "1",  # Adjust based on your needs
                "EDifficultyLevel": 5,  # Adjust based on your needs
                "IsActive": 1,
                "QuestionOptions": []
            }
        })
    
    with open('payload.json', 'a') as f:
        f.write(payload)


    print(payload)
    headers = {
        'cookie': "ARRAffinity=23564d5724d5738e1473c580c4ceefbbbe719a290964305a0fb76422b865e31c; ARRAffinitySameSite=23564d5724d5738e1473c580c4ceefbbbe719a290964305a0fb76422b865e31c",
        'Content-Type': "application/json",
        'User-Agent': "insomnia/9.2.0",
        'Authorization': f"Bearer {access_token}"
    }

    conn.request("POST", "/Services/ExamSpace/Question/CreateQuestionWithOption", payload, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8"), res.status

def save_questions_to_db(questions, question_type,bloom):
    with open("save_question.txt", "w", encoding='utf-8') as f:
        f.write(questions)
    # print(type(questions))
    if(question_type=="MCQ"):
        pattern = re.compile(r'\*\*Question \d+:\*\* (.*?)\n\*\*Options:\*\*\n'
    r'a\) (.*?)\n'
    r'b\) (.*?)\n'
    r'c\) (.*?)\n'
    r'd\) (.*?)\n'
    r'\*\*Answer:\*\* (.*?)\n',re.DOTALL)
        matches = pattern.findall(questions)

        if not matches:
            pattern = re.compile(r'\*\*Question \d+:\*\* (.*?)\n\n\*\*Options:\*\*\n\n'
            r'a\) (.*?)\n'
            r'b\) (.*?)\n'
            r'c\) (.*?)\n'
            r'd\) (.*?)\n'
            r'\*\*Answer:\*\* (.*?)\n',re.DOTALL)
            matches = pattern.findall(questions)
            # print("test")
        # Check if matches is empty
        if not matches:
            print("JSON CONVERSION ERROR MCQ")
            return
        else:
            # Construct a list of dictionaries with keys "Question", "Options", and "Answer"
            qa_pairs = []
            for match in matches:
                question = match[0].strip()
                options = {
                    'a': match[1].strip(),
                    'b': match[2].strip(),
                    'c': match[3].strip(),
                    'd': match[4].strip()
                    }
                answer = match[5].strip()
                qa_pairs.append({
                        "Question": question,
                        "Options": options,
                        "Answer": answer
                    })


            # Convert the list to a JSON string
            jsonString = json.dumps(qa_pairs, indent=4)
    elif(question_type=="Descriptive"):
        pattern = re.compile(r'\*\*Question \d+:\*\* (.*?)\n\*\*Answer:\*\*\s(.*?)(?:\n\n|\n$)', re.DOTALL)
        # Find all matches in the text
        matches = pattern.findall(questions)
        # Check if matches is empty
        if not matches:
            print("JSON CONVERSION ERROR Descriptive")
            return

        # Construct a list of dictionaries with keys "Question" and "Answer"
        qa_pairs = [{"Question": match[0].strip(), "Answer": match[1].strip()} for match in matches]

        # Convert the list to a JSON string
        jsonString = json.dumps(qa_pairs, indent=4)
    else: 
        pattern = re.compile(r'\*\*Question \d+:\*\* (.*?)\n\*\*Answer:\*\*\s(.*?)(?:\n\n|\n$)', re.DOTALL)

        # Find all matches in the text
        matches = pattern.findall(questions)
        # Check if matches is empty
        if not matches:
            print("JSON CONVERSION ERROR Fill in the Blanks.")
            return

        # Construct a list of dictionaries with keys "Question" and "Answer"
        qa_pairs = [{"Question": match[0].strip(), "Answer": match[1].strip()} for match in matches]

        # Convert the list to a JSON string
        jsonString = json.dumps(qa_pairs, indent=4)
 
 
    try:
        jsonObject = json.loads(jsonString)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")

        return

    # Debugging logs
    bloom_index = {"Knowledge":0, "Comprehension":1, "Application":2,"Analysis":3,"Synthesis":4,"Evaluation":5}
    for i in jsonObject :

        i["question_type"] = question_type
        i["Bloom's Index"] = bloom_index[bloom]

    # print(len(jsonObject))
    #Call latex converter
    latexObj = json_to_latex(jsonObject,question_type)
    # print(latexObject)
    # with open("latextest.txt", "w",encoding='utf-8') as f:
    #     f.write(str(latexObj))
    print("Successfully wrote in latex file")
    questions_collection.insert_many(latexObj)
    buffer_collection.insert_many(latexObj)
    print("Questions stored in MongoDB successfully")
    for entry in latexObj:
        entry.pop('_id', None)
        entry.pop("Bloom's Index",None)
        entry.pop("key",None)
    print(latexObj)
    combined_dict = {f"{i+1}" :item for  i,item in enumerate(latexObj)}
    # with open("latex.txt",'w') as f:
    #         f.write(json.dumps(combined_dict, indent=4))
    return combined_dict



def json_to_latex(questions, question_type):
    # questions = json.loads(questions_json)
    latex_output = ""
    latexObject = []
    if question_type == "Descriptive" or question_type == "Fill in the Blanks":
        i = 1
        for question in questions:
            temp = dict()
            question_text = question["Question"]
            answer_text = question["Answer"]
            temp["Question"] = f"\\textbf{{Question}}: {question_text}\n\n"
            temp ["Answer"] = f"\\textbf{{Answer}}: {answer_text}\n\n"
            temp["question_type"] = question_type
            temp["Bloom's Index"] = question["Bloom's Index"]
            temp["Key"] = str(i)
            i+=1
            latexObject.append(temp)
    elif question_type == "MCQ":
        i = 1
        for question in questions:
            temp = dict()
            question_text = question["Question"]
            answer_text = question["Answer"]
            temp["Question"] = f"\\textbf{{Question}}: {question_text}\n\n"
            # latex_output = f"\\begin{{itemize}}\n"
            d1 = question["Options"]
            temp["Options"] = []
            # for option in d1.keys():
            #     latex_output += f"  \\item {d1[option]}\n"
            # latex_output += f"\\end{{itemize}}\n\n"
            for option in d1.keys() :
                temp["Options"].append(f"\\textbf{{Option}}: {option}) {d1[option]}\n\n")
            # temp["Options"] = latex_output
            temp["Answer"] = f"\\textbf{{Answer}}: {answer_text}\n\n"
            temp["question_type"] = question_type
            temp["Bloom's Index"] = question["Bloom's Index"]
            temp["Key"] = str(i)
            i+=1
            latexObject.append(temp)
    else:
        raise ValueError("Invalid question_type provided. It must be 'Descriptive', 'Fill in the Blanks', or 'MCQ'.")

    return latexObject


def store_in_api(match):
    responses = []
    jsonObject = get_question_for_API(match)
    print(jsonObject)
    print(type(jsonObject))
    
    try: 
        print("before iteration")
        for question in jsonObject:
            print('after iteration')
            response, status = send_insomnia_request(question)
            print(response)
            responses.append(status)
        print(f"Requests sent! Status code {status}")
    except Exception as e:
        print(f"Error in sending request: {e}")
    
    return responses
 
def get_question_for_API(match):
    temp = []
    for i in match:
        temp.append(list(buffer_collection.find({"Key":{"$eq":i}}))[0])
    return temp

def clear_data():
    buffer_collection.delete_many({})

def save_data_to_db(data):
    filter = {"text": {"$exists": True}}
    data_collection.replace_one(filter, {"text": data}, upsert=True)

def get_data():
    filter = {"text": {"$exists": True}}
    document = data_collection.find_one(filter)
    return document

def markdown_to_latex(markdown_text):

    # html_text = markdown.markdown(markdown_text)
    latex_text = pypandoc.convert_text(markdown_text, 'latex', format='md')
    return latex_text

