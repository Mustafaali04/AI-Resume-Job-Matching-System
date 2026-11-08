SKILLS = [
    # Programming languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "sql",
    "html", "css", "r", "kotlin", "scala", "ruby", "php", "rust", "matlab",
    "bash", "shell scripting", "powershell", "perl", "dart", "golang", "vba",

    # Web development
    "react.js", "angular", "vue.js", "next.js", "node.js", "express.js",
    "bootstrap", "tailwind css", "jquery", "rest api", "graphql", "asp.net",
    ".net", "django", "flask", "fastapi", "spring boot", "hibernate", "json",
    "ajax", "web development", "responsive design", "wordpress",

    # Data and ML libraries
    "pandas", "numpy", "scipy", "scikit-learn", "matplotlib", "seaborn",
    "plotly", "tensorflow", "keras", "pytorch", "opencv", "nltk", "spacy",
    "xgboost", "lightgbm", "catboost", "statsmodels", "streamlit", "gradio",
    "hugging face", "transformers", "langchain", "openai api",
    "beautifulsoup", "selenium", "scrapy", "web scraping", "mlflow", "onnx",
    "dask",

    # AI and ML topics
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "data science", "data engineering", "data analysis",
    "data analytics", "data visualization", "data cleaning",
    "data preprocessing", "data mining", "data wrangling",
    "feature engineering", "feature selection",
    "exploratory data analysis", "statistics", "statistical analysis",
    "hypothesis testing", "probability", "linear algebra", "a/b testing",
    "time series", "forecasting", "predictive modeling",
    "recommendation systems", "anomaly detection", "clustering",
    "regression", "classification", "dimensionality reduction", "pca",
    "random forest", "decision trees", "svm", "knn", "naive bayes",
    "gradient boosting", "linear regression", "logistic regression",
    "k-means", "neural networks", "cnn", "rnn", "lstm", "bert",
    "reinforcement learning", "transfer learning", "object detection",
    "image classification", "image processing", "speech recognition",
    "text classification", "sentiment analysis", "named entity recognition",
    "model evaluation", "model deployment", "hyperparameter tuning",
    "cross validation", "generative ai", "llm", "prompt engineering",
    "retrieval augmented generation", "mlops", "big data",

    # Databases and data tools
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "sql server",
    "redis", "cassandra", "firebase", "dynamodb", "elasticsearch", "nosql",
    "dbms", "database design", "stored procedures", "excel", "power bi",
    "tableau", "google sheets", "looker", "power query", "etl",
    "data warehouse", "snowflake", "bigquery", "hadoop", "apache spark",
    "pyspark", "kafka", "airflow", "dashboards",

    # Tools and version control
    "git", "github", "gitlab", "bitbucket", "docker", "kubernetes", "linux",
    "unix", "vs code", "jupyter", "google colab", "pycharm", "eclipse",
    "intellij", "postman", "jira", "confluence", "figma", "trello",
    "ms office",

    # Cloud and DevOps
    "aws", "azure", "google cloud", "gcp", "cloud computing", "ec2",
    "heroku", "vercel", "netlify", "ci/cd", "jenkins", "github actions",
    "terraform", "ansible", "devops", "nginx",

    # Hardware and IoT
    "iot", "arduino", "raspberry pi", "esp32", "embedded systems", "sensors",
    "microcontrollers", "robotics",

    # Mobile development
    "android", "android studio", "xml", "flutter", "react native", "ios",

    # Computer science fundamentals
    "data structures", "algorithms", "oops", "oop",
    "object oriented programming", "object-oriented programming",
    "design patterns", "operating systems", "computer networks",
    "system design", "multithreading", "version control", "unit testing",
    "debugging", "software development life cycle", "sdlc", "microservices",
    "api development",

    # Security
    "cybersecurity", "network security", "cryptography", "ethical hacking",
    "penetration testing",

    # Methods
    "agile", "scrum", "kanban",

    # Soft skills
    "communication", "teamwork", "problem solving", "leadership",
    "critical thinking", "time management", "presentation skills",
    "analytical skills", "collaboration", "adaptability", "creativity",
    "decision making", "project management", "public speaking", "mentoring",
    "attention to detail", "team player",
]

# Remove any accidental duplicates, keeping the original order
SKILLS = list(dict.fromkeys(SKILLS))