'''
    [ ] RAG
    [ ] https://python.langchain.com/docs/use_cases/question_answering/local_retrieval_qa
    [ ] browser.obj nuke option (pid kill)
    [X] xonsh tweaking so that if llm spit out function, automatically put it in users next console input
    [X] xonsh alias/function to chat with llm
'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path as osPath
from time import localtime
from time import sleep
# import prompt_toolkit
import sys
import atexit
import json
from urllib.parse import urlparse
from duckduckgo_search import DDGS
import yagooglesearch
from openai import OpenAI
import os
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json


class ANSI():
    CODE = {}
    class FG:
        codes = {'black':30,'red':31,'green':32,
                 'yellow':33,'blue':34,'purple':35,
                 'cyan':36,'Bblack':90,'Bred':91,
                 'Bgreen':92,'Byellow':93,'Bblue':94,
                 'Bpurple':95,'Bcyan':96}

    class BG:
        codes = {'black':40,'red':41,'green':42,
                 'yellow':43,'blue':44,'purple':45,
                 'cyan':46,'Bblack':100,'Bred':101,
                 'Bgreen':102,'Byellow':103,'Bblue':104,
                 'Bpurple':105,'Bcyan':106} 
                 
    class ST:
        codes = {'reset':'0;0','bold':1,'dim':2,
                 'italic':3, 'underline':4}
 
    def init():
        for i in ANSI.FG.codes.keys():
            ANSI.CODE['FG_{}'.format(i)] = '\33[{}m'.format(ANSI.FG.codes[i])
        for i in ANSI.BG.codes.keys():
            ANSI.CODE['BG_{}'.format(i)] = '\33[{}m'.format(ANSI.BG.codes[i])
        for i in ANSI.ST.codes.keys():
            ANSI.CODE['ST_{}'.format(i)] = '\33[{}m'.format(ANSI.ST.codes[i])

    def format(phrase):
        array = phrase.split('{')
        tmp_array = []
        for i in array:
            if '}' in i:
                array2 = i.split('}')
                for j in array2:
                    tmp_array.append(j)
            else:
                tmp_array.append(i)

        array = tmp_array
        for i in range(len(array)):
            if array[i] in ANSI.CODE.keys():
                array[i] = ANSI.CODE[array[i]]
                
        return(''.join(array))    

ANSI.init()


class connect_manager:
    '''description: connection manager for information retrieval from the internet
    '''
    class Browser:
        ''''''        
        def __init__(self, browserObject = None):
            self.obj = browserObject

        def createBrowserInstance(self, *args, **kwargs):
            ''''''
            print('creating selenium browser instance...')
            import atexit
            opts = Options()
            if 'headless' in kwargs.keys():
                if kwargs['headless']:
                    opts.add_argument("-headless")                 
            browser = webdriver.Firefox(options=opts)    
            browser.implicitly_wait(10)
            self.obj = browser
            atexit.register(self.quit)
    
        def retrieve(self, url, headless=True):
            ''''''
            print('crawling {}...'.format(url))
            if self.obj == None:
                print('scraper browser not initialized')
            self.obj.get(url)
            WebDriverWait(self.obj, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
            element = self.obj.find_element(By.TAG_NAME, 'body')
            return(element.text)
                
        def nuke():
            pass
            
        def quit(self):
            self.obj.quit()
            self.onj = None
        
    def search(query, num_ret=10):
        '''add news and instant answers'''
        with DDGS() as ddgs:
            urldata = [r for r in ddgs.text(query, max_results=num_ret)]
        return(urldata)

        
class llm:
    '''
    '''
    def __init__(self):
        self.config  = self.config()
        self.agents  = self.agents()
        self.history = self.history()
        
    class config:
        client       = None
        msg_prefix   = None
        msg_suffix   = None
        temperature  = None
        max_tokens   = None
        stop_string  = None
        oai_config   = None
        agent_tmplts = None
        
        def __init__(self):
            if getattr(sys, 'frozen', False):
                abspath = os.path.dirname(sys.executable)
            else:
                abspath = os.path.dirname(os.path.realpath(__file__))

            with open(os.path.join(abspath,'config.json'), 'r') as RF:
                data = json.load(RF)
                
            self.oai_config   = data['oai_config'][0]
            self.client       = OpenAI(base_url=self.oai_config['base_url'], api_key=self.oai_config['api_key'])
            self.temperature  = float(data['llm_console_config']['temperature'])
            self.max_tokens   = int(data['llm_console_config']['max_tokens'])
            self.stop_string  = data['llm_console_config']['stop_string'].split('\n')
            self.msg_prefix   = data['llm_console_config']['msg_prefix']
            self.msg_suffix   = data['llm_console_config']['msg_suffix']
            self.agent_tmplts = data['agents']
            os.environ['AUTOGEN_USE_DOCKER'] = data['autogen_config']['DOCKER']
                        
    
    class agents:
        pool = []
        agent = None
        termination_msg = lambda w,x: True if "TERMINATE" in x.get("content") else False

        def __init__(self):
            pass
            
        def create(self, *args, **kwargs):
            if not 'autogen_agent' in kwargs:
                autogen_agent = AssistantAgent
            if not 'name' in kwargs:
                kwargs['name'] = 'primary_assistant'
                
            agent = autogen_agent(*args, **kwargs)
            self.pool.append(agent)
            self.agent = agent

            
    class contextManager:
        '''
                ** word/sentence embedding (wordToVec) **
            [ ] Once context length reaches x, truncate context by putting y num
                history in DB
            [ ] prior to user sending message to LLM a vector relevance check
                is done with context DB and based on z relevance criteria, like
                messages are temporarily added to context for current chat
        '''
        pass
        

    class history:
        ''''''
        history = []
        history_checkpoint = []
        get_code_flipper = 0

        def __init__(self):
            pass
            
        def reset(self):
            ''''''
            self.history = [self.history[0]]
            
        def show(self):
            ''''''
            h = self.history
            for i in range(len(h)):
                print('{}{}{}. {}\n{}\n'.format(ANSI.CODE['FG_green'],
                                            str(i).zfill(2),
                                            ANSI.CODE['ST_reset'],
                                            h[i]['role'], 
                                            h[i]['content']))

        def checkpoint(self, reset=False):
            ''''''
            self.history_checkpoint += self.history
            if reset:
                self.reset()
    
        def restore(self, additions=[]):
            ''''''
            if len(additions) > 0:
                try:
                    self.history_checkpoint += additions
                except:
                    print('history additions must be wrapped as list...')
                    return
            self.history = self.history_checkpoint
            self.history_checkpoint  = []
    
        def add(self, msg='', role='user'):
            ''''''
            self.history.append({"role": role, "content": msg})

        def size(self):
            ''''''
            cntxLen = 0
            for i in self.history:
                cntxLen += len(i['content'])
            return(cntxLen)

                            
    def update_agent(self):
        ''''''
        data = self.agents.agent.system_message
        try:
            self.history.history[0] = {"role": "system", "content": data}
        except:
            self.history.history = [{"role": "system", "content": data}]
            
            
    def nullFunc(*args, **kwargs):
        ''''''
        pass

        
    def chat(self, msg='', role='user', prn=True, max_tokens=600, tmp_ctx=False, store_hist=True, ret=False):
        ''''''
        if not type(msg) == str:
            return('message must be a string')
            
        if tmp_ctx: self.history.checkpoint(True)
        self.history.history.append({"role": role, "content": msg})
        completion = self.config.client.chat.completions.create(
            model=self.config.oai_config['model'],
            messages=self.history.history,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stop=self.config.stop_string,
            stream=True
        )
    
        new_message = {"role": "assistant", "content": ""}
        
        if prn:
            prn = print
        else:
            prn = self.nullFunc
            
        for chunk in completion:
            char = chunk.choices[0].delta.content
            if char:
                prn(char, end='', flush=True)
                new_message["content"] += char
        print()
    
        if tmp_ctx: self.history.restore()
        if store_hist:
            self.history.history.append(new_message)
            self.history.change_tracker = 1
        if ret:
            return(new_message['content'])
            
        
    def teach(self, subject, instructions="Read it and return a summary of {}", fetch_urls=10, 
              validated_urls_num=2, compress=200, scrape_ret_len=2500):
        '''
            PARAMS:
            subject            : [str] overall subject (used as search query)
            instructions       : [str] what you want the llm to take-away from or 
                                       do with the data (summerize, store instructional data, etc...)
                                       use "{}" to referance the [subject] (quotes not needed)
            fetch_urls         : [int] number of search-returned URLs
            validated_urls_num : [int] number of URL suggestions llm should make
            compress           : [int] number of charecters to have the llm condense data down to
            scrape_ret_len     : [int] number of charecters to keep from scrape (each site) (-1 here keeps all data)
                
            EXAMPLES:
            llm.teach('assetto corsa compitizione car setup adjustments explained', 
                      'return info regarding setup configuraion and changes \
                       (incremental adjustments, adjustments of components, what \
                       adjustments do, etc...)', compress=600, scrape_ret_len=1000)
        '''
        print('finding relavent links...')
        # TWEAK PROMPT
        urldata = connect_manager.search(subject, fetch_urls)
        titles  = [i['title'] for i in urldata]
        urls    = [i['href'] for i in urldata]

        self.history.checkpoint(True)
        msg = '''I want to scrape information for {} on the internet. in the 
following list of webpages, return the {} most relavent urls.\n'''.format(subject, validated_urls_num)
        for i in range(len(urls)):
            msg += '{}. {} ({})'.format(str(i+1).zfill(2), titles[i], urls[i])
        self.chat(msg, prn=False)

        validatedUrls = []
        for i in range(len(titles)):
            if titles[i].lower() in self.history.history[-1]['content'].lower():
                if not urls[i] in validatedUrls and len(validatedUrls) <= validated_urls_num:
                    print('LLM chose {}'.format(urls[i]))
                    validatedUrls.append(urls[i])
                
        if len(validatedUrls) == 0:
            self.history.restore()
            print('LLM returned no valid links.')
            return()
            
        data = []
        browser = connect_manager.Browser()
        browser.createBrowserInstance(headless=True)
        for url in validatedUrls:
            try:
                data.append(browser.retrieve(url)[:2500])                
            except:
                pass
        browser.quit()                 
            
        self.history.reset()
        instructions = instructions.format(subject)
        msg = '''-the following is purely informational
-It was scraped from the web
-{}
-Capture the specifics to include, but not limited to: dates, technical details, specifications, any amplifying information 
-keep your response under {} words\n\n{}'''.format(instructions, subject, compress, "\n".join(data))
   
        print('llm processing and compressing data...')
        self.chat(msg, prn=False, max_tokens=compress)
        compressed_summary = self.history.history[-1]
        compressed_summary['role'] = 'system'
        self.history.restore([compressed_summary])
        print('complete.\n')
