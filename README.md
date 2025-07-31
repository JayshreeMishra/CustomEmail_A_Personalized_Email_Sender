# **CustomEmail – A Personalized Email Sender**  

**CustomEmail** is a production-ready web app that automates and personalizes email campaigns for outreach at scale. It reduces human error, avoids spam filters, and improves response rates by integrating ML-driven spelling correction and spam detection.

---

## 🔧 Features

### ✉️ Smart Email Personalization
- Dynamically replaces the recipient's name and company in the message body
- Send up to **50 custom emails per batch**
- File attachments supported

### 🤖 Machine Learning Enhancements

#### 1. Spam Detection
- Uses `TfidfVectorizer + MultinomialNB` to detect spammy content
- Alerts sender before sending risky messages
- Trained on [Email Spam Classification Dataset](https://www.kaggle.com/datasets/balaka18/email-spam-classification-dataset-csv?source=post_page-----aa44e7ff9b21--------------------------------)
- Accuracy: 97%

#### 2. Spelling Corrector
- Powered by **SymSpell**
- Flags and auto-corrects misspelled words before sending
- (Formerly used `language-tool-python`; removed for lightweight deployment)

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JS
- **Backend**: Flask, Python
- **ML Libraries**: scikit-learn, nltk, SymSpell
- **Deployment**: Render (web), Railway domain (web)

---

### 📁 Project Structure

```

├── app/                               # Web application logic
│   ├── static/                        # Images and CSS
│   ├── templates/                     # HTML forms
│   ├── email_sender.py                # email sending logic
│   └── utils.py
│
│
├── ml/                                # All machine learning logic
│   ├── components/                    # Modular components for each ML feature
│   │   ├── spam_detection/            # Spam classification pipeline
│   │   │   ├── data_ingestion.py
│   │   │   ├── data_transformation.py
│   │   │   └── model_trainer.py
│   │   └── spelling_corrector/        # Spelling correction pipeline
│   │       ├── data_ingestion.py
│   │       ├── data_transformation.py
│   │       └── model_trainer.py
│   │
│   ├── data/
│   |
│   ├── pipeline/                      # Inference pipelines
│   │   ├── predict_pipeline_spam_detection.py
│   │   ├── predict_pipeline_spelling_corrector.py
│   │   └── utils.py
│   │
│   └── notebook_experiment/          # Jupyter notebooks for prototyping
│
├── main.py                            # Entry point to run the Flask app
├── template.py                        
├── requirements.txt                   # Project dependencies
├── setup.py                           # Setup configuration 
├── README.md
├── LICENSE
└── .gitignore

```
---

## 🧠 Why This Matters
Cold email outreach is noisy and easily flagged as spam. **CustomEmail** solves:
- Poor personalization → automated, template-driven fields
- High spam risk → ML-powered content inspection
- Typos → real-time correction for professional delivery

---

## 🚀 Future Additions
- Tone analysis (friendly, formal, urgent)
- Sent Email dashboard (send volume, response rate trends)
- Enhanced grammar correction via lightweight transformer

---

## 👩‍💻 Built By
A Data scientist solving outreach friction with applied ML. See my other work at [GitHub](https://github.com/JayshreeMishra).
