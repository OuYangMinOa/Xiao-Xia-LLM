# Why restful api
因為 [小俠](https://github.com/OuYangMinOa?tab=repositories) 放在樹梅派，而語言模型在其他主機上，所以需要一個方式來讓它們溝通，我選擇使用flask搭建的restful api來進行溝通。

# Run
```
python server.py
```

# file structure
~~~
.
├── LLm.py
├── None
│   └── version.txt
├── README.md
├── client.py
├── server.py
├── .env
├── static
│   └── styles.css
└── templates
    ├── chat.html  
    └── home.html
