# 🍎 AI Calorie Estimation App

A Streamlit application that estimates calories from food photos using computer vision and machine learning. Perfect for deployment on Streamlit Cloud and GitHub!

## ✨ Features

- 📸 **Camera Integration**: Take photos directly in the app
- 🤖 **AI-Powered**: Advanced food recognition using computer vision
- 📊 **Calorie Estimation**: Accurate calorie calculations with portion size detection
- 📱 **Mobile-Friendly**: Responsive design works on all devices
- 🚀 **Cloud-Ready**: Easy deployment on Streamlit Cloud
- 🎨 **Beautiful UI**: Modern, intuitive interface

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python)
- **AI/ML**: OpenCV, scikit-learn, custom food recognition models
- **Image Processing**: PIL, numpy, computer vision algorithms
- **Deployment**: Streamlit Cloud, GitHub

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd calorie-estimation-app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser to `http://localhost:8501`**

### Streamlit Cloud Deployment

1. **Fork this repository on GitHub**
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
3. **Click "New app" and connect your GitHub account**
4. **Select your forked repository**
5. **Set the main file path to `app.py`**
6. **Click "Deploy!"**

## 📁 Project Structure

```
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── Procfile                 # Streamlit Cloud deployment config
├── setup.sh                 # System dependencies setup
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── backend/
│   ├── models/
│   │   ├── food_detector.py     # Food detection algorithms
│   │   └── calorie_estimator.py # Calorie calculation logic
│   └── utils/
│       └── image_processor.py   # Image preprocessing utilities
└── README.md
```

## 🍽️ Supported Foods

Our AI recognizes a wide variety of foods:

- **🍎 Fruits**: Apple, banana, orange, strawberry, grape, lemon
- **🥕 Vegetables**: Carrot, broccoli, tomato, lettuce, cucumber, onion
- **🥩 Proteins**: Chicken, beef, fish, egg, cheese, yogurt
- **🍞 Grains**: Bread, rice, pasta, cereal, oats
- **🍪 Snacks**: Chips, cookies, candy, nuts, chocolate
- **🥤 Beverages**: Coffee, tea, juice, soda, water, milk

## 🎯 How It Works

1. **📸 Image Capture**: User takes a photo or uploads an image
2. **🔄 Preprocessing**: Image is enhanced and optimized for analysis
3. **🤖 AI Detection**: Computer vision algorithms identify food items
4. **📊 Calorie Calculation**: Each food item's calories are estimated
5. **📱 Results Display**: Beautiful interface shows total calories and breakdown

## 🔧 Configuration

The app includes several customizable settings:

- **Portion Sizes**: Small, medium, large, extra-large
- **Confidence Threshold**: Adjust AI detection sensitivity
- **Food Database**: Easily extensible with new food items

## 🌐 Deployment Options

### Streamlit Cloud (Recommended)
- Free hosting
- Automatic deployments from GitHub
- Custom domain support
- Built-in analytics

### Heroku
- Use the included `Procfile`
- Supports custom domains
- Easy scaling options

### Docker
```bash
docker build -t calorie-app .
docker run -p 8501:8501 calorie-app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ using Streamlit
- Powered by OpenCV and scikit-learn
- Inspired by the need for accessible nutrition tracking

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-username/calorie-estimation-app/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

---

**⭐ Star this repository if you found it helpful!**

