# Airport Route Map

A web application that visualizes flight routes from various airports to Niagara Falls International Airport using a Challenger 350 private jet and Bell 429 helicopter routes from The Scotsman Hotel.

## Features

- Interactive map showing flight routes
- Displays origin airports with markers
- Shows the 3,300 nautical mile range of the Challenger 350
- Shows the 385 nautical mile range of the Bell 429 helicopter
- Elegant UI with The Scotsman Hotel branding

## Technologies Used

- Python
- Flask
- Folium (for map visualization)
- HTML/CSS
- Bootstrap

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/tysongreenan/airport_route_map.git
   cd airport_route_map
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Customizing the Logo

To replace the default logo with your custom logo:

1. Create your SVG or PNG logo file
2. Name it `scotsman-logo.svg` (or update the filename in the HTML)
3. Place it in the `static/` directory
4. The logo will automatically appear in the header

## Deploying to Vercel

This application is configured for easy deployment to Vercel:

1. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Login to Vercel:
   ```
   vercel login
   ```

3. Deploy the application:
   ```
   vercel
   ```

4. For production deployment:
   ```
   vercel --prod
   ```

5. Your application will be available at the URL provided by Vercel

## Setting Up Vercel Edge Config for Branding

To use Vercel Edge Config for storing your branding information:

1. Create an Edge Config in your Vercel dashboard:
   - Go to your Vercel project
   - Navigate to Storage → Edge Config
   - Create a new Edge Config

2. Add the following items to your Edge Config:
   - `hotel_name`: Your hotel name
   - `tagline`: Your tagline
   - `primary_color`: Your primary brand color (hex code)
   - `secondary_color`: Your secondary brand color (hex code)

3. Set up environment variables in your Vercel project:
   - `EDGE_CONFIG_TOKEN`: Your Edge Config token
   - `EDGE_CONFIG_ITEM_KEY`: Your Edge Config ID

4. For local development, create a `.env` file with these variables:
   ```
   EDGE_CONFIG_TOKEN=your_edge_config_token
   EDGE_CONFIG_ITEM_KEY=your_edge_config_item_key
   ```

5. The application will automatically use your Edge Config values when deployed

## License

This project is for demonstration purposes only. 