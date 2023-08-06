# GoogleNews

## Install
```
pip install GoogleNews
```
or
```
pip install --upgrade GoogleNews
```
## Usage
- Initializing
```
from GoogleNews import GoogleNews
googlenews = GoogleNews()
```
- Optional choose language and period
```
googlenews = GoogleNews('en','d')
```
or
```
googlenews.setlang('en')
googlenews.setperiod('d')
```
- Search keyword
Default return first page result
```
googlenews.search('APPL')
```
- Get other page of search results
```
googlenews.getpage(2)
```
- Get result
It will return a list, `[{'title': '...', 'media': '...', 'date': '...', 'desc': "...", 'link': '...', 'img': '...'}]`
```
googlenews.result()
```
or just get a list of news titles
```
googlenews.gettext()
```
or just get a list of news links
```
googlenews.getlinks()
```
- Clear result list
Clear result list before you get another search or page
```
googlenews.clear()
```
