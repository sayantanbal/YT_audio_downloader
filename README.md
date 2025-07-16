# 🎵 YouTube Audio Downloader

A modern, responsive web application for downloading audio from YouTube videos. This application consists of a React frontend and Flask backend, designed for deployment on separate EC2 instances.

![YouTube Audio Downloader](https://via.placeholder.com/800x400/667eea/ffffff?text=YouTube+Audio+Downloader)

## ✨ Features

- 🚀 **Fast Processing** - Quick audio extraction and conversion
- 🎵 **High Quality** - Best available audio quality
- 🔒 **Private & Safe** - No data stored on servers
- 📱 **Mobile Friendly** - Responsive design that works on all devices
- 🎨 **Modern UI** - Beautiful, gradient-based design with smooth animations
- ⚡ **Real-time Validation** - Instant URL validation and feedback
- 📊 **Progress Tracking** - Visual progress indicators for downloads

## 🔗 Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/shorts/VIDEO_ID`

## � Project Structure

```
├── frontend/          # React frontend application
├── backend/           # Flask backend API
├── deployment/        # Deployment scripts and configurations
└── README.md         # This file
```

## 🚀 Getting Started

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

### Backend (Flask + Python)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## 🛠️ Technology Stack

- **Frontend Framework**: React 19
- **Build Tool**: Vite 7
- **Styling**: Pure CSS with modern features
- **HTTP Client**: Axios (for API requests)
- **Development**: ESLint for code quality

## 📖 How to Use

1. **Copy YouTube URL**: Go to YouTube and copy the URL of the video you want to download audio from
2. **Paste URL**: Paste the URL into the input field on the application
3. **Validation**: The app will automatically validate the URL format
4. **Download**: Click the "Download Audio" button
5. **Processing**: Wait for the app to process the video and extract audio
6. **Save**: The audio file will be automatically downloaded to your device

## ⚖️ Legal Considerations

This tool is designed for educational and personal use only. Users are responsible for:

- Ensuring they have permission to download the content
- Complying with YouTube's Terms of Service
- Respecting copyright laws in their jurisdiction
- Using downloaded content appropriately

## 🔧 Development Notes

### Current Implementation

The current version includes:
- Frontend-only implementation using YouTube's oEmbed API for video information
- Demo download functionality (creates instruction files)
- Complete UI/UX for a production-ready application

### Production Implementation

For a full production deployment, you would need:

1. **Backend Service**: A server-side service to handle actual YouTube downloads
2. **YouTube API**: Proper API keys and integration
3. **Audio Processing**: Server-side audio extraction and conversion
4. **File Storage**: Temporary storage for processed files

### Recommended Backend Technologies

- **Node.js** with `youtube-dl-exec` or `ytdl-core`
- **Python** with `yt-dlp` or `youtube-dl`
- **Docker** for containerized deployment
- **Cloud Storage** for temporary file handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Disclaimer

This application is provided for educational purposes. The developers are not responsible for any misuse of this tool. Users must ensure they comply with all applicable laws and terms of service when using this application.

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include browser information and steps to reproduce any problems

## 🎯 Future Enhancements

- [ ] Playlist support
- [ ] Multiple format options (MP3, WAV, FLAC)
- [ ] Quality selection
- [ ] Batch downloads
- [ ] Browser extension
- [ ] Desktop application version

---

Made with ❤️ for the community+ Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
