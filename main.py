from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from extract import *
from checks import WebPage
import os



SECRET = os.getenv("SECRET")

#
app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    html = """
    <html>
        <head>
                <title>Validate URL</title>
        </head>
        <body>
            <form method="post" action="/process">
                <label for="url"> Type a URL: </label><br>
                <textarea id="url" name="url" rows="40" cols="200"></textarea><br><br>
                <input type="submit" values="Send"> 
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

@app.post("/process")
async def process_url(request: Request):
    data = await request.form()
    urls = data["url"]
    print(urls)

    html = """
            <html>
                <head>
                        <title>Validate URL</title>
                </head>
                <body>
                <h1>Results:</h1>
        """

    for url in urls.split("\n"):
        test = WebPage(url)
        test.make_tests()
        html += f"<p>The url {url} is {'valid' if test.valid else f'NOT VALID because '+'; '.join(test.reason)}</p>"

    html += """
            <br>
            <a href="/">RETURN TO MAIN PAGE</a>
            </body>
        </html>
        """

    return HTMLResponse(content=html, status_code=200)



'''
async def root():    
    return {"message": "Hello World. Welcome to FastAPI!"}
'''

@app.get("/homepage")
async def demo_get():
    driver=createDriver()

    homepage = getGoogleHomepage(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}
    


