# Name Trend Predictor

This project predicts the probability that a given name will become trendy again based on historical popularity data scraped from [beliebte-vornamen.de](https://www.beliebte-vornamen.de).

## Project Structure

- **backend/**: Flask backend serving API endpoints.
  - `app.py`: Main application.
- **frontend/**: Static files for the user interface.
  - `index.html`: Main UI page.
  - `styles.css`: Basic styling.
- **model/**: Machine learning model training and saving.
  - `model.py`: Script to train a dummy model and save it.
- **spider/**: Scrapy spider to scrape name data.
  - **spider/spiders/**: Contains the spider code (`name_spider.py`).
  - `scrapy.cfg`: Scrapy configuration.
  - `settings.py`: Scrapy settings.
- **.github/workflows/**: CI/CD deployment workflow (example for Azure).
- **requirements.txt**: Python dependencies.
- **Dockerfile**: (Optional) Container build file.

## Installation and Running

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/name-trend-predictor.git
   cd name-trend-predictor
