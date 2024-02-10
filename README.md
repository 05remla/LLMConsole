# LLMConsole

*Intuitive framework to combine the utility of the console/terminal with the power of large language models*

# ![Pre-Release 0.0.1](https://github.com/05remla/LLMConsole/releases/tag/PR-0.0.1)



LLMConsole utilizes-
* xonsh
* pyautogen
* selenium
* duckduckgo_search
* openai  

HERE, WE FIRE UP XONSH, WHICH FIRES UP LLMCONSOLE (defined in .xonshrc):

Hotkey listing

![alt text](https://github.com/05remla/repo_images/blob/main/getting_started.png)



CONVENIENT HOTKEY FOR QUICK CHAT:

Just press [ctrl]+[z]... then chat 

![alt text](https://github.com/05remla/repo_images/blob/main/hot%20keys%20and%20chat%201.png)

TAB COMPLETION:

![alt text](https://github.com/05remla/repo_images/blob/main/tab%20completion.png)


EASY CODE INSERTION:

If LLM returns code, you can insert that code as your input with [ctrl]+[x]

![alt text](https://github.com/05remla/repo_images/blob/main/hot%20keys%20(cody%20insert).png)



TEACHING:

Here we see the LLM is not familiar with the topic. We make a simple query to get links, ask the LLM "what two links are the most relavent", then scrape those sites. We then ask the LLM to compress (summerize) that info down to X characters.

![alt text](https://github.com/05remla/repo_images/blob/main/teaching3.png)

![alt text](https://github.com/05remla/repo_images/blob/main/teaching4.png)

Voila! It learned something.



# GETTING STARTED

Edit the config.json file. 
* In the case of OpenAI and their GPTs, add your API key
* If you're using an LLM elsewhere, add the URL (and API if you need it)
* If you're using LLMConsole: keep the DOCKER variable 0
* Tweak other params to your heart's desire
  
![alt text](https://github.com/05remla/repo_images/blob/main/config.png)

If you're using LLMConsole with your python installation open a terminal and run:
* python -m pip install -r requirements.txt
* Then put llmConsole.py in your python/system path

If you're using the release:
* Double-click LLMConsole.exe

