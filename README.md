# URL Shortener (SaaS)

A simple **URL Shortener** built with **Flask, Python, SQL, and HTML/CSS**.

## Features
✅ Shorten long URLs  
✅ Track usage statistics  
✅ API support  
✅ Database storage   

## Installation
```sh
git clone https://github.com/KANNAN1501/URL-SHORTEN.git
cd URL-SHORTEN
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```


## Deployment (Render)
1. Push code to GitHub.
2. Create a **Web Service** on [Render](https://render.com/).
3. Set environment variables.
4. Deploy! 🚀

## API Endpoints
| Method | Endpoint       | Description          |
|--------|---------------|----------------------|
| POST   | /shorten      | Shorten a URL       |
| GET    | /<short_code> | Redirect to full URL |
| GET    | /stats/<code> | Get URL stats       |

## License
This project is licensed under the **GNU General Public License (GPL)**. See the `LICENSE` file for details.

### Need Help?
Open an issue on [GitHub](https://github.com/KANNAN1501/URL-SHORTEN). 🚀

